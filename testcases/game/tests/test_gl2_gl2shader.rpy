# This file tests the GLSL dialects shader parts can be written in and the
# translation between them.

# ==============
# == Fixtures ==
# ==============

init python:

    def test_shaders__cache():
        """
        Returns the shader cache of the renderer. The testcases that use it need a GL2 renderer, so this
        fails, rather than letting them pass without checking anything, when there isn't one.
        """

        cache = getattr(renpy.display.draw, "shader_cache", None)
        assert cache is not None, "The renderer has no shader cache, so shaders can't be compiled."

        return cache

    def test_shaders__compile(*parts):
        """
        Compiles a shader built from `parts` through the real shader cache, and returns the error
        message, or None if it compiled.
        """

        try:
            test_shaders__cache().get(tuple(parts))
        except Exception as e:
            return str(e)

        return None

    renpy.register_shader(
        "test_shaders.modern", glsl=300,
        variables="uniform float u__amount;",
        fragment_600="fragment_color.rgb *= u__amount;\n",
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
                l__acc += fragment_color;
            }
            fragment_color = l__acc / float(max(u__taps * l__size.x, 1));
        """,
    )

    # Legacy syntax that doesn't declare a dialect.
    renpy.register_shader(
        "test_shaders.undeclared",
        variables="uniform float u__amount;",
        fragment_600="gl_FragColor.rgb *= u__amount;\n",
    )

    # A shader-local uniform that is only referenced inside helper functions.
    renpy.register_shader(
        "test_shaders.helper", glsl=300,
        variables="uniform float u__amount;",
        vertex_functions="""
            vec4 test_shaders_helper_scale_vertex(vec4 position) {
                return position * u__amount;
            }
        """,
        fragment_functions="""
            vec4 test_shaders_helper_scale(vec4 color) {
                return color * u__amount;
            }
        """,
        vertex_600="gl_Position = test_shaders_helper_scale_vertex(gl_Position);\n",
        fragment_600="fragment_color = test_shaders_helper_scale(fragment_color);\n",
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
            compiled = 0

            for name in sorted(renpy.gl2.gl2shadercache.shader_part):
                if not name.startswith("renpy."):
                    continue
                if name in ("renpy.geometry", "renpy.ftl"):
                    continue

                error = test_shaders__compile("renpy.texture", name)
                assert error is None, f"{name} did not compile: {error}"
                compiled += 1

            assert compiled > 10, f"Only {compiled} built-in shader parts were found."

    testcase builtin_dialect:
        description "Ren'Py's own shader parts translate down to the oldest dialect"
        # This needs no GL driver, but the renpy.* parts are registered by renpy/common/_shaders.rpym when a
        # game starts, so it can't be a pytest.

        python:
            import renpy.gl2.gl2shadercache as shadercache

            newest = shadercache.DIALECTS[-1]
            oldest = shadercache.DIALECTS[0]
            oldest_name = shadercache.dialect_name(oldest)
            version = shadercache.dialect_version(True, oldest)

            for name, part in sorted(shadercache.shader_part.items()):
                if not name.startswith(("renpy.", "live2d.", "textshader.")):
                    continue

                assert part.glsl == newest, \
                    f"{name} is not written in {shadercache.dialect_name(newest)}."
                assert part.minimum_dialect == oldest, \
                    f"{name} uses {part.minimum_feature}, so it can't run on a {oldest_name} system."

                for fragment in (False, True):
                    if fragment:
                        variables = part.fragment_variables
                        parts = part.fragment_parts
                        functions = part.fragment_functions
                    else:
                        variables = part.vertex_variables
                        parts = part.vertex_parts
                        functions = part.vertex_functions

                    text = shadercache.source(
                        variables,
                        [ (prio, nm, t, part.glsl) for prio, nm, t in parts ],
                        [ (functions, part.glsl) ],
                        fragment, True, version)

                    for _newer, pattern, marker in shadercache.newer_markers(oldest):
                        assert not pattern.search(text), \
                            f"{name} still uses {marker} when emitted as {oldest_name}."

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

            if cache.version >= 300:
                assert error is None, \
                    f"ES 3.00 features did not compile at GLSL {cache.version}: {error}"
            else:
                assert error is not None, \
                    f"ES 3.00 features unexpectedly compiled at GLSL {cache.version}"

    testcase undeclared_legacy_compiles:
        description "A part in legacy syntax that doesn't declare a dialect compiles"
        # That such a part is inferred to be GLSL ES 1.00 is checked in
        # testcases/pytests/test_gl2_gl2shadercache.py; this checks that it works with a real driver.

        python:
            error = test_shaders__compile("renpy.texture", "test_shaders.undeclared")
            assert error is None, f"Legacy part did not compile: {error}"

    testcase helper_function_variables:
        description "A shader-local variable used by both stages' functions is declared once"

        python:
            cache = test_shaders__cache()
            error = test_shaders__compile("renpy.texture", "test_shaders.helper")
            assert error is None, f"Helper-function shader did not compile: {error}"

            baseline = cache.get(("renpy.texture",))
            helper = cache.get(("renpy.texture", "test_shaders.helper"))
            assert len(helper.uniform_setters) == len(baseline.uniform_setters) + 1, \
                "A uniform shared by both stages should have one setter"

    testcase renders:
        description "Draws with parts in both dialects"

        run Start("test_shaders__render__label")
        pause 0.3
