translate simplified_chinese python:
    CHSdef = "tl/simplified_chinese/DroidSansFallback.ttf"

translate simplified_chinese style l_default:
    font CHSdef
    size 16

translate simplified_chinese style l_button_text:
    selected_font CHSdef
    selected_bold True

translate simplified_chinese style l_link_text:
    font CHSdef

translate simplified_chinese style l_alternate_text:
    font CHSdef

translate simplified_chinese style l_navigation_button_text:
    font CHSdef

translate simplified_chinese style l_navigation_text:
    font CHSdef
    bold True

translate simplified_chinese style l_checkbox_text:
    selected_font CHSdef

translate simplified_chinese style l_nonbox_text:
    selected_font CHSdef

translate simplified_chinese style hyperlink_text:
    font CHSdef

translate simplified_chinese python:
    make_style_backup()
