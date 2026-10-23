/*
 * Stereo 3D, side by side (PC SETTINGS > VIDEO > 3D). The engine draws two
 * pictures a step (ps2host/high_fps.h: the left eye's, then the right's) and
 * the display pairs them; here each is drawn from its eye: RenderWare's
 * camera moved along its right, its view window offset against the move -
 * so what is CONVERGENCE away stays on the screen's plane, and what is far
 * is DEPTH of the picture's width apart.
 *
 * 0x001E1410(camera) makes a perspective camera's view matrix (+0x20) from
 * its frame's LTM (the frame at +0x4, its LTM at +0x50: right, up, at, pos),
 * its recipViewWindow (+0x70) and viewOffset (+0x78). Across the picture
 * (0 to 1):
 *
 *     x = 0.5 + 0.5 / window.x * (offset.x - right.(p - pos) / at.(p - pos))
 *
 * An eye moved d along right, with offset o: the left d = +D, o = -D/C, the
 * right d = -D, o = +D/C put a thing z away (C: the convergence) at
 *
 *     x_right - x_left = D / window.x * (1/C - 1/z)
 *
 * apart: nothing at C, D / (C window.x) far away - DEPTH, so D = DEPTH * C
 * * window.x. Nearer than C, the right eye's further left: in front of the
 * screen. The HUD, drawn in 2D, is on the screen's plane.
 *
 * The cameras moved are the views the game draws its pictures from
 * (0x00227360, through RwCameraBeginUpdate 0x001E1FB0 - its only caller),
 * not the others (reflections, shadows). Their view matrix is made again
 * there, from the eye, whether or not the camera moved since: the right
 * eye's picture is drawn with no step of the game's between, a camera the
 * draw does not move (the garage's) keeps the left eye's matrix else.
 *
 * Ctrl+F5 / Ctrl+F6: less or more DEPTH; Ctrl+F7 / Ctrl+F8: CONVERGENCE
 * nearer or further - saved as they change ("stereo_depth", a percentage of
 * the picture's width; "stereo_convergence", in the game's units).
 */

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#include <windows.h>
#endif

#include "ps2host/high_fps.h"
#include "ps2host/host.h"
#include "ps2host/run.h"
#include "ps2host/settings.h"

// RenderWare: a perspective camera's view matrix; RwCameraBeginUpdate.
void F_001E1410(lifted::Context& c);
void F_001E1FB0(lifted::Context& c);

namespace {

constexpr float kDepthDefault = 3.0f;           // percent of the picture's width
// The game's units: the player's car, as far as the chase camera rides
// behind it (about 3.3: measured, race.args at 8 - the car 4.2% of the
// picture in front of the screen) - on the screen's plane.
constexpr float kConvergenceDefault = 3.5f;

// The views' cameras (RwCameraBeginUpdate's): the last few seen.
constexpr int kViews = 8;
u32 g_views[kViews] = {};
int g_next_view = 0;

bool AView(u32 camera) {
    for (u32 v : g_views)
        if (v == camera) return true;
    return false;
}

float Number(const char* key, float fallback) {
    const std::string s = ps2host::Setting(key, "");
    if (s.empty()) return fallback;
    char* end = nullptr;
    const float v = std::strtof(s.c_str(), &end);
    return end != s.c_str() && std::isfinite(v) ? v : fallback;
}

float Depth() { return std::clamp(Number("stereo_depth", kDepthDefault), 0.0f, 20.0f) / 100.0f; }
float Convergence() { return std::clamp(Number("stereo_convergence", kConvergenceDefault), 0.5f, 500.0f); }

float ReadF(u32 address) {
    const u32 bits = generated::ReadU32(address);
    float f;
    std::memcpy(&f, &bits, 4);
    return f;
}

void WriteF(u32 address, float f) {
    u32 bits;
    std::memcpy(&bits, &f, 4);
    generated::Write32(address, bits);
}

/* 0x001E1410(camera): the view matrix from the picture's eye, for a view's
   camera - its frame's position and its offset moved for the call, and put
   back. */
void ViewMatrix(lifted::Context& c) {
    const u32 camera = u32(c.r[4]);
    const int eye = ps2host::HighFpsEye();
    const u32 frame = eye ? u32(generated::ReadU32(camera + 0x4u)) : 0u;
    const float window = frame ? ReadF(camera + 0x68u) : 0.0f;
    if (!eye || !frame || !AView(camera) || !(std::fabs(window) > 1e-6f)) {
        F_001E1410(c);
        return;
    }
    const float sign = eye == 1 ? 1.0f : -1.0f;
    const float convergence = Convergence();
    const float d = sign * Depth() * convergence * window;
    const u32 ltm = frame + 0x50u;
    float pos[3], was_offset = ReadF(camera + 0x78u);
    for (int k = 0; k < 3; ++k) {
        pos[k] = ReadF(ltm + 0x30u + 4u * k);
        WriteF(ltm + 0x30u + 4u * k, pos[k] + d * ReadF(ltm + 4u * k));
    }
    WriteF(camera + 0x78u, was_offset - d / convergence);
    F_001E1410(c);
    for (int k = 0; k < 3; ++k) WriteF(ltm + 0x30u + 4u * k, pos[k]);
    WriteF(camera + 0x78u, was_offset);
}

/* Ctrl+F5..F8, once a press: DEPTH and CONVERGENCE. */
void Keys() {
#ifdef _WIN32
    static bool held[4] = {};
    const bool ctrl = ps2host::HostKeyDown(VK_CONTROL);
    const int keys[4] = {VK_F5, VK_F6, VK_F7, VK_F8};
    for (int k = 0; k < 4; ++k) {
        const bool down = ctrl && ps2host::WindowFocused() && ps2host::HostKeyDown(keys[k]);
        if (down && !held[k]) {
            char text[32];
            if (k < 2) {
                const float depth = std::clamp(Depth() * 100.0f + (k == 0 ? -0.5f : 0.5f), 0.0f, 20.0f);
                std::snprintf(text, sizeof text, "%.1f", depth);
                ps2host::SetSetting("stereo_depth", text);
                std::fprintf(stderr, "[stereo] depth %s%% of the picture\n", text);
            } else {
                const float convergence = std::clamp(Convergence() * (k == 2 ? 1.0f / 1.25f : 1.25f), 0.5f, 500.0f);
                std::snprintf(text, sizeof text, "%.2f", convergence);
                ps2host::SetSetting("stereo_convergence", text);
                std::fprintf(stderr, "[stereo] convergence %s\n", text);
            }
        }
        held[k] = down;
    }
#endif
}

/* 0x001E1FB0(camera): RwCameraBeginUpdate, from the view maker only - the
   camera a view's, its matrix made again from the eye first, and the eye
   into the GS's stream where the view's drawing begins: the eye its camera
   has. At the display step instead (before 2026-10-23), in real time the
   tag and the picture's last draws did not always come in the order made -
   a left eye's picture went out as a right eye's. */
void BeginUpdate(lifted::Context& c) {
    const u32 camera = u32(c.r[4]);
    if (ps2host::StereoWanted()) {
        if (!AView(camera)) {
            g_views[g_next_view] = camera;
            g_next_view = (g_next_view + 1) % kViews;
        }
        if (ps2host::HighFpsEye() && u32(generated::ReadU32(camera + 0x14u)) == 1u) {    // (perspective)
            const u64 a0 = c.r[4], ra = c.r[31];
            ViewMatrix(c);
            c.r[4] = a0;
            c.r[31] = ra;
        }
        ps2host::StereoViewBegins();
        static const bool log_views = std::getenv("PS2HOST_STEREO_LOG") != nullptr;
        if (log_views)
            std::fprintf(stderr, "[stereo] view camera %08X: eye %d (frame %llu)\n", camera, ps2host::HighFpsEye(),
                         (unsigned long long)ps2host::FrameNumber());
    }
    F_001E1FB0(c);
}

}  // namespace

/* Each picture (mods.cpp's Frame, before the draw). */
void StereoFrame() {
    if (ps2host::StereoWanted()) Keys();
}

/* After the display step (mods.cpp's Frame: 0x001F43B0 waits for the blank
   and copies the last picture to the displayed buffer): a picture of no eye
   (a movie, a menu at the game's own rate) tagged so here - one of an eye's
   is tagged where its views begin (BeginUpdate). */
void StereoDrawStart() {
    if (!ps2host::HighFpsEye()) ps2host::StereoTagPicture();
}

void RegisterStereo() {
    ps2host::Override(0x001E1410u, ViewMatrix, "a perspective camera's view matrix: from the eye (3D, PC SETTINGS)");
    ps2host::Override(0x001E1FB0u, BeginUpdate, "RwCameraBeginUpdate: a view's camera, from the picture's eye (3D)");
}
