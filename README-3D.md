# Burnout 3 PC port - stereo 3D build: how to get it and use it

[한국어는 아래에](#한국어)

This is the Burnout 3: Takedown PC port
([danielgomesvieira2000/burnout3-pc](https://github.com/danielgomesvieira2000/burnout3-pc))
with stereo 3D added: **side by side** (3D TVs, VR viewers, side-by-side
glasses) and **SR DISPLAY**, woven for Acer SpatialLabs and other Leia SR
glasses-free 3D panels. It is not the port author's release and has nothing
to do with Electronic Arts or Criterion Games. **No game content is included:
everyone needs their own copy of the game.**

It is built on the port's **[0.8.0-alpha release](https://github.com/danielgomesvieira2000/burnout3-pc/releases/tag/v0.8.0-alpha)**. The 3D zip is the
whole port with 3D added - you don't need to install the original first.

## 1. Getting the download

These repositories are private, so the release can't be seen by people who
haven't been invited. There are two ways to give someone the game:

- **Send them the zip.** Download
  `Burnout3-PC-3D-<version>-windows-x64.zip` from
  [Releases](../../releases) and give them the file. It holds only the port's
  program, `ps2sr.dll` and text files - no game data. This is the simplest
  way, and gives them nothing else.
- **Invite them on GitHub.** In this repository: **Settings → Collaborators →
  Add people**, enter their GitHub user name or e-mail. They accept the
  invitation (e-mail, or github.com/notifications) and can then open
  **Releases** and download the zip themselves, including later versions. Be
  aware that a collaborator on a personal account's repository can also
  change it (push); invite only people you trust with that, or send the zip.

To build it from source they also need to be invited to the engine
repository, `nautymac/ps2-port-engine-3d` (see section 7).

## 2. What you need

- Windows 10 or 11, 64-bit.
- A graphics card with Direct3D 11 or Vulkan 1.1 drivers. A processor with
  AVX2 runs `burnout3.exe`; an older one gets `burnout3-sse4.exe`, which
  `burnout3.exe` starts by itself.
- **Your own disc image** of Burnout 3: Takedown for the PS2, North American
  version (NTSC-U, **SLUS-21050**), as an `.iso` file.
- For **SR DISPLAY**: an Acer SpatialLabs or other Leia SR panel with its SR
  software (the SR runtime) installed - the software that came with the
  panel. Without it the game shows side by side.

## 3. Installing and the first start

1. Unzip into a folder you can write to - for example `D:\Games\Burnout3-3D`,
   not inside `Program Files`.
2. Run `burnout3.exe`.
3. The first time, choose your disc image. The choice is kept in
   `pc_settings.ini` beside the program.

### Already have the PC port installed?

(The original port's download is
[Burnout3-PC-0.8.0-alpha-windows-x64.zip](https://github.com/danielgomesvieira2000/burnout3-pc/releases/tag/v0.8.0-alpha).)
Copy the files from **inside** the zip's folder (`Burnout3-PC-3D-<version>\`)
into your PC port folder and let them replace what is there - unzipping it
"here" only makes a subfolder. `burnout3.exe`, `burnout3-sse4.exe` and the
READMEs are replaced, `ps2sr.dll` and `README-3D-ko.txt` are added; your
`pc_settings.ini`, `memcard\` (saves), `custom_songs\` and `texture pack\` stay
as they are. 3D starts off - turn it on in PC SETTINGS > VIDEO. This build is
the port's 0.8.0 with 3D, so an older install becomes 0.8.0 too. To be able to
go back, rename your original `burnout3.exe` first (e.g.
`burnout3-original.exe`).

## 4. Turning on 3D

In the main menu: **PC SETTINGS > VIDEO** - 3D and 3D DEPTH are its first two rows.

| Setting | Choose |
|---|---|
| 3D | **SIDE BY SIDE** for a 3D TV, VR viewer or side-by-side glasses; **SR DISPLAY** for an SR panel |
| RENDERER | **DIRECT3D 11** for an SR panel (applies from the next start); VULKAN works too |
| FULLSCREEN | ON for an SR panel |
| 3D DEPTH | LOW, MEDIUM, HIGH, MOST |

Keys while playing:

- **Ctrl+F5 / Ctrl+F6** - less / more depth
- **Ctrl+F7 / Ctrl+F8** - convergence (what sits on the screen's plane) nearer / further

Both are saved. In 3D the game draws 120 pictures a second, one for each eye
(FRAME RATE does not apply). Movies are flat; a short loading screen between
two 3D scenes keeps the last 3D picture on screen.

## 5. A texture pack (optional)

A PCSX2 texture pack for Burnout 3 (SLUS-21050) works in 3D too. None is
included or linked here - get one yourself. Put its files (PCSX2 keeps them
in `textures/SLUS-21050/replacements/`) in a folder named **`texture pack`**
beside `burnout3.exe`; folders inside it are fine, for example
`texture pack\SLUS-21050\replacements\...`. Start the game; **Tab** turns the
pack off and on while you play.

## 6. Updating to a new version

Unzip the new version into a new folder, then copy these from the old folder
into it:

- `pc_settings.ini` - your settings and where your disc image is
- `memcard\` - your saves
- `custom_songs\` and `texture pack\`, if you use them

Or copy the new zip's files over the old folder (the same files are
replaced, your settings and saves stay).

## 7. Building it from source

With access to both repositories:

```sh
git clone --recursive https://github.com/nautymac/burnout3-pc-3d
```

then follow **Building it** in [README.md](README.md) (your own disc image,
Visual Studio 2022, Python, LLVM). The 3D is in the default branch,
`stereo-3d`. `ps2sr.dll`, the SR weaver's bridge, is built apart against the
Leia SR SDK, which is not in either repository:
`cmake -S engine/gpu/sr_bridge -B <dir> -G Ninja -DSR_SDK=<the SDK's folder>`.

## 8. If something goes wrong

Send `burnout3.log`, from beside `burnout3.exe`, with a few words about what
happened and where. Known: the side-by-side split-screen MOD and stereo 3D
have not been tried together.

---

## 한국어

원작 PC 포트(danielgomesvieira2000/burnout3-pc)에 입체 3D를 더한 빌드입니다.
3D TV·VR 뷰어·사이드바이사이드 안경용 **좌우 나란히(SIDE BY SIDE)**, Acer
SpatialLabs 같은 Leia SR 무안경 3D 패널용 **SR DISPLAY**(위빙)를 지원합니다.
원작 포트 작성자, Electronic Arts, Criterion Games와 관계없는 비공식
빌드이며, **게임 데이터는 들어 있지 않습니다. 각자 게임을 갖고 있어야
합니다.**

원작 포트의 **[0.8.0-alpha 릴리스](https://github.com/danielgomesvieira2000/burnout3-pc/releases/tag/v0.8.0-alpha)**를 바탕으로 했습니다. 3D zip은 원작
포트 전체에 3D를 더한 것이라 원작을 먼저 설치할 필요는 없습니다.

### 1. 받는 방법

이 저장소는 비공개라서 초대받지 않은 사람에게는 릴리스가 보이지 않습니다.
다른 사람에게 주는 방법은 두 가지입니다.

- **zip 파일을 직접 보내기.** [Releases](../../releases)에서
  `Burnout3-PC-3D-<버전>-windows-x64.zip`을 받아 그 파일을 전달합니다.
  포트 프로그램, `ps2sr.dll`, 안내 문서만 들어 있고 게임 데이터는 없습니다.
  가장 간단하고, 저장소 권한을 줄 필요가 없습니다.
- **GitHub에서 초대하기.** 이 저장소의 **Settings → Collaborators → Add
  people**에서 상대의 GitHub 아이디나 이메일을 넣습니다. 상대가 초대를
  수락하면(메일 또는 github.com/notifications) **Releases**에서 직접 받을 수
  있고, 새 버전도 계속 받을 수 있습니다. 단, 개인 계정 저장소의
  협업자(collaborator)는 저장소를 수정(push)할 수도 있으니 믿을 수 있는
  사람만 초대하고, 아니면 zip을 보내 주세요.

소스에서 직접 빌드하려면 엔진 저장소 `nautymac/ps2-port-engine-3d`에도
초대가 필요합니다(7번).

### 2. 준비물

- Windows 10/11 64비트
- Direct3D 11 또는 Vulkan 1.1 드라이버가 있는 그래픽카드. AVX2가 없는 CPU는
  `burnout3.exe`가 알아서 `burnout3-sse4.exe`를 실행합니다.
- **본인 소유의 Burnout 3: Takedown PS2 북미판 디스크 이미지**(NTSC-U,
  **SLUS-21050**, `.iso`)
- **SR DISPLAY**를 쓰려면: Acer SpatialLabs 등 Leia SR 패널과 패널에 딸린 SR
  소프트웨어(SR 런타임) 설치. 없으면 좌우 나란히로 나옵니다.

### 3. 설치와 첫 실행

1. 쓰기 가능한 폴더에 압축을 풉니다(예: `D:\Games\Burnout3-3D`).
   `Program Files` 안은 피하세요.
2. `burnout3.exe`를 실행합니다.
3. 처음 한 번 디스크 이미지를 고릅니다. 위치는 옆의 `pc_settings.ini`에
   저장됩니다.

#### PC 포트를 이미 설치해 두었다면

(원작 포트 다운로드: [Burnout3-PC-0.8.0-alpha-windows-x64.zip](https://github.com/danielgomesvieira2000/burnout3-pc/releases/tag/v0.8.0-alpha))
zip 안의 폴더(`Burnout3-PC-3D-<버전>\`) **안에 있는 파일들**을 기존 PC 포트
폴더에 복사해 덮어쓰면 됩니다(zip을 그 자리에 풀면 하위 폴더만 생깁니다).
`burnout3.exe`, `burnout3-sse4.exe`, README가 바뀌고 `ps2sr.dll`,
`README-3D-ko.txt`가 추가되며, `pc_settings.ini`, `memcard\`(세이브),
`custom_songs\`, `texture pack\`은 그대로 남습니다. 3D는 꺼진 상태로
시작하니 PC SETTINGS > VIDEO에서 켜세요. 이 빌드는 원작 포트 0.8.0에 3D를
더한 것이라 이전 버전을 쓰고 있었다면 0.8.0으로 함께 올라갑니다. 되돌릴 수
있게 하려면 먼저 원래 `burnout3.exe`의 이름을 바꿔 두세요(예:
`burnout3-original.exe`).

### 4. 3D 켜기

메인 메뉴 **PC SETTINGS > VIDEO**의 맨 위 두 줄(3D, 3D DEPTH)에서:

| 항목 | 선택 |
|---|---|
| 3D | 3D TV·VR 뷰어·SBS 안경은 **SIDE BY SIDE**, SR 패널은 **SR DISPLAY** |
| RENDERER | SR 패널은 **DIRECT3D 11** 권장(다음 실행부터 적용), VULKAN도 동작 |
| FULLSCREEN | SR 패널은 ON |
| 3D DEPTH | LOW, MEDIUM, HIGH, MOST |

게임 중 키:

- **Ctrl+F5 / Ctrl+F6** - 깊이 줄이기 / 늘리기
- **Ctrl+F7 / Ctrl+F8** - 수렴(화면 면에 놓이는 거리) 가깝게 / 멀게

둘 다 저장됩니다. 3D에서는 눈마다 한 장씩 초당 120장을 그립니다(FRAME
RATE 설정은 적용되지 않음). 동영상은 평면이고, 3D 장면 사이의 짧은 로딩
화면 동안에는 마지막 3D 화면이 유지됩니다.

### 5. 텍스처 팩 (선택)

Burnout 3(SLUS-21050)용 PCSX2 텍스처 팩도 3D에서 그대로 쓸 수 있습니다.
여기에는 들어 있지도, 링크하지도 않으니 직접 구하세요. 팩의 파일(PCSX2의
`textures/SLUS-21050/replacements/` 안의 것)을 `burnout3.exe` 옆의
**`texture pack`** 폴더에 넣습니다. 하위 폴더는 괜찮습니다(예:
`texture pack\SLUS-21050\replacements\...`). 게임을 시작하면 적용되고,
**Tab** 키로 켜고 끕니다.

### 6. 새 버전으로 업데이트

새 버전을 새 폴더에 풀고, 이전 폴더에서 다음을 복사해 옵니다.

- `pc_settings.ini` - 설정과 디스크 이미지 위치
- `memcard\` - 세이브
- 쓰고 있다면 `custom_songs\`, `texture pack\`

또는 새 zip의 파일을 이전 폴더에 덮어써도 됩니다(같은 이름의 파일만
바뀌고 설정과 세이브는 남습니다).

### 7. 소스에서 빌드하기

두 저장소 권한이 있으면:

```sh
git clone --recursive https://github.com/nautymac/burnout3-pc-3d
```

그다음 [README.md](README.md)의 **Building it**을 따릅니다(본인 디스크
이미지, Visual Studio 2022, Python, LLVM). 3D는 기본 브랜치 `stereo-3d`에
있습니다. SR 위버 연결용 `ps2sr.dll`은 Leia SR SDK로 따로 빌드하며, SDK는
어느 저장소에도 들어 있지 않습니다:
`cmake -S engine/gpu/sr_bridge -B <폴더> -G Ninja -DSR_SDK=<SDK 폴더>`.

### 8. 문제가 생기면

`burnout3.exe` 옆의 `burnout3.log`를 어떤 상황이었는지와 함께 보내 주세요.
알려진 점: 좌우 분할 화면 MOD와 입체 3D를 함께 쓰는 경우는 시험하지
않았습니다.
