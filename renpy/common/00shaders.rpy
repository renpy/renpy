init python:

    renpy.register_shader("renpy.geometry", variables="""
        uniform mat4 uTransform;
        attribute vec4 aPosition;
    """, vertex_100="""
        gl_Position = uTransform * aPosition;
    """)

    renpy.register_shader("renpy.texture", variables="""
        uniform sampler2D uTex0;
        attribute vec2 aTexCoord;
        varying vec2 vTexCoord;
    """, vertex_110="""
        vTexCoord = aTexCoord;
    """, fragment_110="""
        gl_FragColor = texture2D(uTex0, vTexCoord.xy);
    """)

    renpy.register_shader("renpy.solid", variables="""
        uniform vec4 uSolidColor;
    """, fragment_110="""
        gl_FragColor = uSolidColor;
    """)

    renpy.register_shader("renpy.dissolve", variables="""
        uniform sampler2D uTex0;
        uniform sampler2D uTex1;
        uniform float uDissolve;
        attribute vec2 aTexCoord;
        varying vec2 vTexCoord;
    """, vertex_110="""
        vTexCoord = aTexCoord;
    """, fragment_110="""
        vec4 color0 = texture2D(uTex0, vTexCoord.st);
        vec4 color1 = texture2D(uTex1, vTexCoord.st);

        gl_FragColor = mix(color0, color1, uDissolve);
    """)

    renpy.register_shader("renpy.imagedissolve", variables="""
        uniform sampler2D uTex0;
        uniform sampler2D uTex1;
        uniform sampler2D uTex2;
        uniform float uDissolveOffset;
        uniform float uDissolveMultiplier;
        attribute vec2 aTexCoord;
        varying vec2 vTexCoord;
    """, vertex_110="""
        vTexCoord = aTexCoord;
    """, fragment_110="""
        vec4 color0 = texture2D(uTex0, vTexCoord.st);
        vec4 color1 = texture2D(uTex1, vTexCoord.st);
        vec4 color2 = texture2D(uTex2, vTexCoord.st);

        float a = clamp((color0.a + uDissolveOffset) * uDissolveMultiplier, 0.0, 1.0);
        gl_FragColor = mix(color1, color2, a);
    """)


    renpy.register_shader("renpy.colormatrix", variables="""
        uniform mat4 uColorMatrix;
    """, fragment_120="""
        gl_FragColor = gl_FragColor * uColorMatrix;
    """)

    renpy.register_shader("renpy.alpha", variables="""
        uniform float uAlpha;
        uniform float uOver;
    """, fragment_130="""
        gl_FragColor = gl_FragColor * vec4(uAlpha, uAlpha, uAlpha, uAlpha * uOver);
    """)

    renpy.register_shader("renpy.ftl", variables="""
        attribute vec4 aPosition;
        attribute vec2 aTexCoord;
        varying vec2 vTexCoord;
        uniform sampler2D uTex0;
    """, vertex_100="""
        vTexCoord = aTexCoord;
        gl_Position = aPosition;
    """, fragment_100="""
        gl_FragColor = texture2D(uTex0, vTexCoord.xy);
    """)
