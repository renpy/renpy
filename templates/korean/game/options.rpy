## 이 파일은 당신의 렌파이 게임을 꾸미기 위해 변경할 수 있는
## 일부 옵션을 포함하고 있습니다. 흔히 사용되는 옵션만 포함하고 있으며
## 이 외에도 여러가지 옵션이 있습니다.
##
## 두 개의 #으로 시작하는 줄은 주석입니다. 그러므로 주석을 풀지 마세요.
## 하나의 # 마크로 시작하는 라인은 임시로 주석처리한 코드로,
## 해당 코드를 사용하고 싶다면 적절히 주석을 풀어 이용하시기 바랍니다.

init -1 python hide:

    # 기본 폰트: 나눔 고딕
    # 경로: 프로젝트폴더/tl/None/
    style.default.font = "tl/None/NanumGothic.ttf"
    style._default.font = "tl/None/NanumGothic.ttf"


    ## 개발자 도구를 활성화시킵니까? 게임이 배포되기 전에 False로 설정해서
    ## 사용자가 개발자툴을 이용하여 속임수를 쓰지 않도록 하세요.

    config.developer = True

    ## 화면 해상도를 제어합니다.

    config.screen_width = 800
    config.screen_height = 600

    ## 렌파이가 창 모드에서 실행중일 때 표시할 창 제목을 제어합니다.

    config.window_title = u"PROJECT_NAME"

    # 트레이스백 파일과 기타 디버그 기록에 적힐
    # 게임 이름과 버전을 입력합니다.
    config.name = "PROJECT_NAME"
    config.version = "0.0"

    #########################################
    # 테마

    ## 테마 기능은 게임의 겉모양을 꾸밀 때 사용됩니다.
    ## themes.roundrect은 둥근 모서리의 사각형을 사용하는 테마입니다.
    ##
    ## 테마 기능은 색상 체계를 꾸밀 수 있는 여러개의 매개변수를 취합니다.

    theme.roundrect(

        ## 일반적인 위젯의 겉모습.
        widget = "#003c78",

        ## 마우스가 올려진 위젯의 겉모습.
        widget_hover = "#0050a0",

        ## 위젯 내의 텍스트 색상.
        widget_text = "#c8ffff",

        ## 선택된 위젯 안에 있는 텍스트의 색상.
        ## (예를 들면, 환경설정의 현재값)
        widget_selected = "#ffffc8",

        ## 비활성화중인 위젯의 겉모습.
        disabled = "#404040",

        ## 비활성화중인 위젯의 텍스트 색상.
        disabled_text = "#c8c8c8",

        ## 안내 텍스트 레이블의 색상.
        label = "#ffffff",

        ## 위젯을 포함하고 있는 프레임의 색상.
        frame = "#6496c8",

        ## True면 게임 내의 창 모서리가 둥글어집니다. False면
        ## 사각형이 됩니다.
        rounded_window = False,

        ## 메인 메뉴의 배경 그림. #으로 시작하는
        ## 색상코드이거나 이미지 파일 이름이 올 수도 있습니다.
        ## 이미지 파일이라면 화면의 최대 가로, 세로 길이를 충분히 덮을 수 있어야 합니다.
        mm_root = "#dcebff",


        ## 게임 메뉴의 배경 그림. #으로 시작하는
        ## 색상코드이거나 이미지 파일 이름이 올 수도 있습니다.
        ## 이미지 파일이라면 화면의 최대 가로, 세로 길이를 충분히 덮을 수 있어야 합니다.
        gm_root = "#dcebff",

        ## 이로써 테마 설정은 모두 마쳤습니다. 테마는 다양한 스타일로
        ## 꾸밀 수 있으므로 테마를 변경하고 싶다면,
        ## 이 아래 공간에서 설정해야 합니다.

        )


    #########################################
    ## 아래의 설정들은 대사창을 이미지로 교체하여
    ## 대사나 나래이션이 표시되는 대사창을 꾸미도록 해줍니다.

    ## 대사창의 배경그림. Frame에서 두 숫자는
    ## 각각 좌우와 상하 경계의 크기를 뜻합니다.

    # style.window.background = Frame("frame.png", 12, 12)

    ## margin은 대사창의 배경 그림이 그려지지 않는
    ## 대사창 주변의 여백입니다.

    # style.window.left_margin = 6
    # style.window.right_margin = 6
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    ## padding은 대사창 내부의 배경그림이 그려지는 공간
    ## 안 쪽에 들어가는 여백입니다.

    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    ## 빈 공간과 여백을 포함한 대사창의 최소 높이를 설정합니다.

    # style.window.yminimum = 250


    #########################################
    ## 메인 메뉴의 위치를 변경하는 설정입니다.

    ## 위치를 변경하는 방식:
    ## 디스플레이어블 내에서 앵커를 찾고, 화면에서 위치(pos)점을 찾습니다.
    ## 그 후 디스플레이어블을 위치시켜
    ## 앵커와 위치점을 같은 곳에 위치시킵니다.

    ## 앵커/pos 는 정수나 부동 소수점 숫자 형태로
    ## 지정할 수 있습니다. 정수는 왼쪽 위 모서리로부터
    ## 떨어져있는 픽셀 숫자로 처리됩니다. 부동 소수점이라면
    ## 그 숫자는 디스플레이어블이나 스크린의 비율로
    ## 해석됩니다.

    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5


    #########################################
    ## 아래의 설정들을 이용하면
    ## 렌파이에서 사용되는 기본 폰트를 꾸밀 수 있습니다.

    ## 기본 폰트.

    # style.default.font = "DejaVuSans.ttf"

    ## 기본 글자 크기

    # style.default.size = 22

    ## 위의 설정은 일부 텍스트의 크기만을 변경합니다.
    ## 다른 버튼 텍스트들은 고유의 스타일로 설정되어 있습니다..

    #########################################
    ## 아래의 설정들을 이용하면 렌파이에서 사용되는 소리들을
    ## 변경할 수 있습니다.

    ## 게임에 효과음이 없다면 False로 설정하세요.
    config.has_sound = True

    ## 게임에 배경음악이 없다면 False로 설정하세요.

    config.has_music = True

    ## 게임에 음성이 있다면 True로 설정하세요.

    config.has_voice = False

    ## 버튼이나 이미지맵이 클릭될 때 재생하는 효과음.

    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    ## 게임 메뉴에 진입하거나 빠져나올 때 재생하는 효과음.

    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    ## 효과음 볼륨을 체크할 때 재생되는 샘플 효과음.

    # config.sample_sound = "click.wav"

    ## 사용자가 메인 메뉴에 있을 때 재생되는 음악.

    # config.main_menu_music = "main_menu_theme.ogg"


    #########################################
    ## 도움말

    ## 렌파이 메뉴에서 도움말 옵션을 설정할 수 있는 변수입니다.
    ## 다음과 같은 값을 입력할 수 있습니다.
    ## - 사용자에게 도움말을 표시할 때 호출되는 스크립트에 적힌 레이블.
    ## - 웹브라우저로 열리는 파일 이름. 기본 디렉토리가 기본 경로이다.
    ## - None : 도움말을 비활성화한다.
    config.help = "README.html"


    #########################################
    ## 화면 전환 효과

    ## 게임에서 게임 메뉴로 진입할 때 사용합니다.
    config.enter_transition = None

    ## 게임 메뉴에서 게임으로 돌아갈 때 사용합니다.
    config.exit_transition = None

    ## 게임 메뉴 내부의 스크린들을 표시할 때 사용합니다.
    config.intra_transition = None

    ## 메인 메뉴에서 게임 메뉴로 진입할 때 사용합니다.
    config.main_game_transition = None

    ## 게임에서 메인 매뉴로 돌아갈 때 사용합니다.
    config.game_main_transition = None

    ## 스플래시 스크린에서 메인 메뉴로 진입할 때 사용합니다.
    config.end_splash_transition = None

    ## 게임이 끝난 후 메인 메뉴로 진입할 때 사용합니다.
    config.end_game_transition = None

    ## 게임을 불러올 때 사용합니다.
    config.after_load_transition = None

    ## 대사창이 나타날 때 사용합니다.
    config.window_show_transition = None

    ## 대사창이 사라질 때 사용합니다.
    config.window_hide_transition = None

    ## ADV 모드 텍스트 다음에 NVL 모드 텍스트를 표시할 때 사용합니다.
    config.adv_nvl_transition = dissolve

    ## NVL 모드 텍스트 다음에 ADV 모드 텍스트를 표시할 때 사용합니다.
    config.nvl_adv_transition = dissolve

    ## 예/아니오 창이 나타날 때 사용합니다.
    config.enter_yesno_transition = None

    ## 예/아니오 창이 사라질 때 사용합니다.
    config.exit_yesno_transition = None

    ## 다시보기 화면에 진입할 때 사용합니다.
    config.enter_replay_transition = None

    ## 다시보기 화면에서 나갈 때 사용합니다.
    config.exit_replay_transition = None

    ## 이미지 속성이 적힌 say문으로 이미지를 변경할 때 사용합니다.
    config.say_attribute_transition = None

    #########################################
    ## 게임 데이터가 저장되는 경로의 이름입니다.
    ## (이 경로는 지속 데이터를 init 코드에서 사용할 수 있도록
    ## 다른 init 블럭의 코드가 사용되기 전에 미리 설정되어야 합니다.)
python early:
    config.save_directory = "PROJECT_NAME-UNIQUE"

init -1 python hide:
    #########################################
    ## 환경설정 기본값.

    ## 주의: 이 옵션은 게임을 실행할 때 처음 한 번만 계산하는 값들입니다.
    ## 값을 수정한 다음에 수정한 값을 다시 적용하려면
    ## game/saves/persistent 파일을 삭제하세요.

    ## 전체 화면 모드로 시작할까요?

    config.default_fullscreen = False

    ## 기본 글자 표시 속도로 초당 표시 글자 수.
    ## 0을 입력하면 글자가 한 번에 표시됩니다.

    config.default_text_cps = 0

    ## 자동 진행 시간 설정의 기본값.

    config.default_afm_time = 10

    #########################################
    ## 아래에 기타 설정값을 입력할 수 있습니다.
