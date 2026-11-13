번아웃 3: 테이크다운 PC 포트 - 입체 3D 빌드 (nautymac 빌드, 공식 릴리스 아님)
================================================================================

원작 PC 포트(danielgomesvieira2000/burnout3-pc) 0.8.0-alpha에 입체 3D를
더한 빌드입니다. 3D TV, VR 뷰어, 사이드바이사이드 안경에서 볼 수 있고,
Acer SpatialLabs 같은 Leia SR 무안경 3D 패널에는 위빙해서 보여 줍니다.
그 밖의 기능은 원작 포트 그대로이고, 자세한 조작·설정은 README.txt(영문)에
있습니다.

준비물
------
- Windows 10/11 64비트
- Vulkan 1.1 또는 Direct3D 11을 지원하는 그래픽 드라이버
- 본인 소유의 Burnout 3: Takedown 북미판 PS2 디스크 이미지(SLUS-21050, .iso)
  게임 데이터는 이 파일 안에 들어 있지 않고, 받을 수도 없습니다.
- SR 패널로 볼 때: SR 런타임(패널과 함께 설치된 SpatialLabs / Leia SR 소프트웨어)

처음 실행
---------
1. 압축을 쓰기 가능한 폴더에 풉니다(Program Files 안은 피하세요).
2. burnout3.exe를 실행하고, 처음 한 번 본인 디스크 이미지를 고릅니다.
3. 메인 메뉴의 PC SETTINGS > VIDEO 맨 위에서
   - 3D: SIDE BY SIDE(좌우 나란히) 또는 SR DISPLAY(SR 패널)
   - RENDERER: SR 패널이면 DIRECT3D 11 권장(다음 실행부터 적용)
   - 3D DEPTH: 입체 깊이

키
--
  Ctrl+F5 / Ctrl+F6   깊이 줄이기 / 늘리기 (저장됨)
  Ctrl+F7 / Ctrl+F8   수렴(화면 면에 놓이는 거리) 가깝게 / 멀게 (저장됨)

참고
----
- 3D에서는 한 게임 스텝에 두 장(초당 120장)을 그려 눈마다 한 장씩 씁니다.
  FRAME RATE 설정은 적용되지 않습니다. 동영상은 평면이고, 3D 장면 사이의
  짧은 로딩 화면 동안에는 마지막 3D 화면이 유지됩니다.
- SR DISPLAY에는 burnout3.exe 옆의 ps2sr.dll(이 압축 파일에 포함)과 SR
  런타임이 필요합니다. 둘 중 하나가 없으면 좌우 나란히로 나옵니다.
  ps2sr.dll은 Leia SR SDK로 빌드했고, SDK와 런타임은 포함되어 있지 않습니다.
- 설정은 burnout3.exe 옆 pc_settings.ini에 저장됩니다
  (stereo = off / sbs / sr, stereo_depth, stereo_convergence, renderer).
- 문제가 있으면 burnout3.exe 옆의 burnout3.log를 함께 알려 주세요.

텍스처 팩 (선택)
----------------
Burnout 3(SLUS-21050)용 PCSX2 텍스처 팩을 3D에서도 쓸 수 있습니다. 이
파일에는 들어 있지 않으니 직접 구하세요. 팩의 파일을 burnout3.exe 옆의
"texture pack" 폴더에 넣으면 됩니다(하위 폴더 가능, 예:
texture pack\SLUS-21050\replacements\...). 게임 중 Tab 키로 켜고 끕니다.

새 버전으로 업데이트
--------------------
새 버전을 새 폴더에 풀고, 이전 폴더의 pc_settings.ini(설정), memcard\(세이브),
custom_songs\, texture pack\ 을 복사해 옵니다.

다른 사람에게 주기
------------------
이 zip 파일을 그대로 전달하면 됩니다(게임 데이터는 들어 있지 않음). 받는
사람도 본인 소유의 디스크 이미지가 필요합니다.

원작 포트 작성자, Electronic Arts, Criterion Games와 관계없는 비공식 빌드입니다.
"Burnout"은 Electronic Arts Inc.의 상표입니다.
