label textshader_jitter:

    "Default jitter: all glyphs should move together, and the effect should continue indefinitely." (what_textshader="jitter")

    "Larger jitter: all glyphs should move together by up to 10 pixels horizontally and 5 pixels vertically." (what_textshader="jitter:20, 10")

    "Individual jitter: each glyph should move independently, and the effect should continue indefinitely." (what_textshader="jitter:10, 10:u__individual=1")

    "Zero duration: the jitter should continue indefinitely." (what_textshader="jitter:10, 10:u__duration=0")

    "Negative duration: the jitter should also continue indefinitely." (what_textshader="jitter:10, 10:u__duration=-1")

    "Timed block jitter: all glyphs should move together for two seconds, then return to their normal positions." (what_textshader="jitter:10, 10:u__duration=2")

    "Timed individual jitter: each glyph should move independently for two seconds, then return to its normal position." (what_textshader="jitter:10, 10:u__duration=2:u__individual=1")

    "Only {shader=jitter:10, 10:u__duration=2:u__individual=1}these words{/shader} should jitter independently for two seconds. The rest should remain still." (what_textshader="typewriter")

    "{cps=15}Slow text: jitter should stop after two seconds, even while the remaining glyphs are still appearing.{/cps}" (what_textshader="jitter:10, 10:u__duration=2:u__individual=1")

    return
