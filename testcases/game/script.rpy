screen text_test:
    
    add renpy.display.newtext.NewText(s, xmaximum=749, **kwargs)

    # window:    
    #    has vbox
  
    #    add renpy.display.newtext.NewText(s, **kwargs)

    #    if old:
    #        add Text(s, **kwargs)

init python:
    _preferences.text_cps = 20

init python:

    TEST = ": We are not now that strength which in old days moved earth and heaven; that which we are, we are; One equal temper of heroic hearts, made weak by time and fate, but strong in will to strive, to seek, to find, and not to yield."

    def text_test(s, test=TEST, old=True, **kwargs):
        ui.saybehavior()
        renpy.call_screen("text_test", s=s + test, old=old, kwargs=kwargs)
        
label main_menu:
    return

label start:

    python:
        text_test("Justify", justify=True)        
        text_test("Justify w/ Outline", justify=True, outlines=[(2, "#00f", 0, 0)])        
        text_test("Normal")
        text_test("Aliased", antialias=False)
        text_test("Bold", bold=True)
        text_test("Color", color="#ff0")
        text_test("First Indent", first_indent=50)
        text_test("Font", font="mikachan.ttf")
        text_test("Size", size=30)
        text_test("Italic", italic=True)
        text_test("Justify", justify=True)        
        text_test("Min_width, should be right-aligned.", test="", min_width=780, text_align=1.0)
        text_test("Outlines", outlines=[ (1, "#f00"), (1, "#00f", 2, 2) ])
        text_test("Rest Indent", rest_indent=50)
        text_test("Slow CPS", slow_cps=10)
        text_test("Slow CPS Mul", slow_cps_multiplier=2.0)
        text_test("Right-align", text_align=1.0)
        text_test("Center-align", text_align=0.5)
        text_test("Underline", underline=True)
        text_test("Strikethrough", strikethrough=True)
        
        # TODO: Test language.
        # TODO: Test layout.
        # TODO: test black_color

        
        
    