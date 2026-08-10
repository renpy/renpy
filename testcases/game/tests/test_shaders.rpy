# This file tests the GLSL dialects shader parts can be written in and the
# translation between them.

# ==============
# == Fixtures ==
# ==============

init python:

    def test_shaders__cache():
        return getattr(renpy.display.draw, "shader_cache", None)

    def test_shaders__compile(*parts):
        """
        Compiles a shader built from `parts` through the real shader cache.
        """

        cache = test_shaders__cache()

        if cache is None:
            return None

        try:
            cache.get(tuple(parts))
        except Exception as e:
            return str(e)

        return None

    renpy.register_shader(
        "test_shaders.modern", glsl=300,
        variables="uniform float u__amount;",
        fragment_600="renpy_FragColor.rgb *= u__amount;\n",
    )

    renpy.register_shader(
        "test_shaders.legacy", glsl=100,
        variables="uniform float u__amount;",
        fragment_600="gl_FragColor.rgb *= u__amount;\n",
    )

    # GLSL ES 3.00 features: textureSize, integer arithmetic, and a loop whose
    # bound isn't a constant expression.
    renpy.register_shader(
        "test_shaders.es3", glsl=300,
        variables="uniform sampler2D tex0;\nuniform int u__taps;",
        fragment_600="""
            ivec2 l__size = textureSize(tex0, 0);
            vec4 l__acc = vec4(0.0);
            for (int l__i = 0; l__i < u__taps; l__i += 1) {
                l__acc += renpy_FragColor;
            }
            renpy_FragColor = l__acc / float(max(u__taps * l__size.x, 1));
        """,
    )

    # Legacy syntax that doesn't declare a dialect.
    renpy.register_shader(
        "test_shaders.undeclared",
        variables="uniform float u__amount;",
        fragment_600="gl_FragColor.rgb *= u__amount;\n",
    )


transform test_shaders__both:
    shader [ "test_shaders.modern", "test_shaders.legacy" ]
    u_test_shaders_modern_amount 0.5
    u_test_shaders_legacy_amount 0.5


label test_shaders__render__label:
    show eileen happy at test_shaders__both

    return


# ==============
# === Tests ====
# ==============

testsuite shaders:
    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase builtin_parts:
        description "Ren'Py's own shader parts compile at the emitted version"

        python:
            cache = test_shaders__cache()

            if cache is not None:
                for name in sorted(renpy.gl2.gl2shadercache.shader_part):
                    if not name.startswith("renpy."):
                        continue
                    if name in ("renpy.geometry", "renpy.ftl"):
                        continue

                    error = test_shaders__compile("renpy.texture", name)
                    assert error is None, f"{name} did not compile: {error}"

    testcase mixed_dialects:
        description "Parts in both dialects combine into one shader"

        python:
            error = test_shaders__compile(
                "renpy.texture", "test_shaders.modern", "test_shaders.legacy")
            assert error is None, f"Mixed-dialect shader did not compile: {error}"

    testcase es3_features:
        description "GLSL ES 3.00 features work where the system provides them"

        python:
            cache = test_shaders__cache()
            error = test_shaders__compile("renpy.texture", "test_shaders.es3")

            if cache is None:
                pass
            elif cache.version >= 300:
                assert error is None, \
                    f"ES 3.00 features did not compile at GLSL {cache.version}: {error}"
            else:
                assert error is not None, \
                    f"ES 3.00 features unexpectedly compiled at GLSL {cache.version}"

    testcase undeclared_legacy_errors:
        description "Legacy syntax without a declared dialect is an error"

        python:
            error = test_shaders__compile("renpy.texture", "test_shaders.undeclared")

            if renpy.config.glsl_version in (300, 330):
                assert error is not None, \
                    "A part using gl_FragColor without glsl=100 should not have compiled"
                assert "glsl=100" in error, \
                    f"The error should suggest glsl=100, got: {error}"
            else:
                assert error is None, f"Legacy part did not compile: {error}"

    testcase renders:
        description "Draws with parts in both dialects"

        run Start("test_shaders__render__label")
        pause 0.3
