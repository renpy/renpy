screen text_test:
    
    window:    
       has vbox
  
       add renpy.display.newtext.NewText(s, slow=True, **kwargs)

       if old:
           add Text(s, **kwargs)

init python:
    _preferences.text_cps = 100

init python:

    TEST = ": We are not now that strength which in old days moved earth and heaven; that which we are, we are; One equal temper of heroic hearts, made weak by time and fate, but strong in will. To strive, to seek, to find, and not to yield."


    def text_test(s, test=TEST, old=True, **kwargs):
        ui.saybehavior()
        kwargs.update(text_extra)
        renpy.call_screen("text_test", s=s + test, old=old, kwargs=kwargs)
        
    style.red = Style(style.default)
    style.red.color = "#f00"
        
label main_menu:
    return

label start:

    $ text_extra = dict()
    
    $ text_test("Tags", test=": {b}Bold {plain}Plain{/plain} Bold{/b} {i}Italics{/i} {color=#f00}color{/color} {font=mikachan.ttf}Font{/font} {image=arrow.png} {s}strikeout{/s} {u}underline{/u} {=red}red style{/=red}")
    $ text_test("Size Tag", test=": {size=30}absolute{/size} {size=+10}relative bigger{/size} {size=-10}relative smaller{/size}")
    $ text_test("Spacing", test=":{space=100}horizontal{vspace=30}vertical", old=False)
    
    $ text_test("Font", font="mikachan.ttf")
    $ text_test("Justify", justify=True)        
    $ text_test("Normal")
    $ text_test("Aliased", antialias=False)
    $ text_test("Bold", bold=True)
    $ text_test("Color", color="#ff0")
    $ text_test("First Indent", first_indent=250)
    $ text_test("Size", size=30)
    $ text_test("Italic", italic=True)
    $ text_test("Justify", justify=True)        
    $ text_test("Min_width, should be right-aligned.", test="", min_width=780, text_align=1.0)
    $ text_test("Rest Indent", rest_indent=250)
    $ text_test("Slow CPS", slow_cps=10)
    $ text_test("Slow CPS Mul", slow_cps_multiplier=2.0)
    $ text_test("Right-align", text_align=1.0)
    $ text_test("Center-align", text_align=0.5)
    $ text_test("Underline", underline=True)
    $ text_test("Strikethrough", strikethrough=True)
    
    $ text_extra = dict(outlines=[ (1, "#00f", 1, 1), (1, "#f00") ])

    $ text_test("Font", font="mikachan.ttf")
    $ text_test("Justify", justify=True)        
    $ text_test("Normal")
    $ text_test("Aliased", antialias=False)
    $ text_test("Bold", bold=True)
    $ text_test("Color", color="#ff0")
    $ text_test("First Indent", first_indent=250)
    $ text_test("Size", size=30)
    $ text_test("Italic", italic=True)
    $ text_test("Justify", justify=True)        
    $ text_test("Min_width, should be right-aligned.", test="", min_width=780, text_align=1.0)
    $ text_test("Rest Indent", rest_indent=250)
    $ text_test("Slow CPS", slow_cps=10)
    $ text_test("Slow CPS Mul", slow_cps_multiplier=2.0)
    $ text_test("Right-align", text_align=1.0)
    $ text_test("Center-align", text_align=0.5)
    $ text_test("Underline", underline=True)
    $ text_test("Strikethrough", strikethrough=True)

    
    # TODO: Test language.
    # TODO: Test layout.
    # TODO: test black_color

        
        
    