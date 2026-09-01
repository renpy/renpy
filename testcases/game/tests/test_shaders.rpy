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
            cache = test_shaders__cache()

            if cache is not None:
                for name in sorted(renpy.gl2.gl2shadercache.shader_part):
                    if not name.startswith("renpy."):
                        continue
                    if name in ("renpy.geometry", "renpy.ftl"):
                        continue

                    error = test_shaders__compile("renpy.texture", name)
                    assert error is None, f"{name} did not compile: {error}"

    testcase builtin_dialect:
        description "Ren'Py's own shader parts translate down to the oldest dialect"

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

    testcase helper_function_variables:
        description "A shader-local variable used by both stages' functions is declared once"

        python:
            cache = test_shaders__cache()
            error = test_shaders__compile("renpy.texture", "test_shaders.helper")
            assert error is None, f"Helper-function shader did not compile: {error}"

            if cache is not None:
                baseline = cache.get(("renpy.texture",))
                helper = cache.get(("renpy.texture", "test_shaders.helper"))
                assert len(helper.uniform_setters) == len(baseline.uniform_setters) + 1, \
                    "A uniform shared by both stages should have one setter"

    testcase generated_fragment_output:
        description "Modern fragment output has an explicit location"

        python:
            from renpy.gl2.gl2shader import ShaderError, Variable
            import renpy.gl2.gl2shadercache as shadercache

            for gles, version in ((True, 300), (False, 330)):
                text = shadercache.source([], [], [], True, gles, version)
                assert "layout(location = 0) out vec4 fragment_color;" in text

            try:
                Variable("test_shaders.output", "layout(location = 1) out vec4 user_output;")
            except ShaderError as error:
                assert "additional fragment output" in str(error)
            else:
                assert False, "shader parts may not declare their own layout qualifiers"

    testcase invariant_varyings:
        description "Invariant varyings are emitted for each profile and stage"

        python:
            from renpy.gl2.gl2shader import ShaderError, Variable

            variable = Variable("test_shaders.invariant", "invariant out vec2 v_test;")

            assert variable.declaration(False, True, 300) == "invariant out vec2 v_test"
            assert variable.declaration(True, True, 300) == "in vec2 v_test"
            assert variable.declaration(False, False, 330) == "invariant out vec2 v_test"
            assert variable.declaration(True, False, 330) == "invariant in vec2 v_test"

            try:
                Variable("test_shaders.invariant", "invariant uniform float u_test;")
            except ShaderError as error:
                assert "only qualify a varying" in str(error)
            else:
                assert False, "invariant uniforms should produce a clear ShaderError"

    testcase interpolation_qualifiers:
        description "Interpolation is profile-aware and reports unsupported modes"

        python:
            from renpy.gl2.gl2shader import ShaderError, Variable

            old_developer = renpy.config.developer
            old_write = renpy.display.log.write
            messages = []

            def write(message, *args, messages=messages):
                messages.append(message % args if args else message)

            renpy.display.log.write = write

            try:
                renpy.config.developer = False

                flat = Variable("test_shaders.interpolation", "flat out vec2 v_flat;")
                assert flat.declaration(False, True, 300) == "flat out vec2 v_flat"
                assert flat.declaration(False, True, 100) == "varying vec2 v_flat"
                assert len(messages) == 1 and "flat interpolation" in messages[0]
                assert flat.declaration(False, True, 100) == "varying vec2 v_flat"
                assert len(messages) == 1, "unsupported interpolation should only log once"

                noperspective = Variable("test_shaders.interpolation", "noperspective out vec2 v_noperspective;")
                assert noperspective.declaration(False, False, 330) == "noperspective out vec2 v_noperspective"
                assert noperspective.declaration(False, True, 300) == "out vec2 v_noperspective"
                assert len(messages) == 2 and "noperspective interpolation" in messages[1]

                renpy.config.developer = True

                try:
                    flat.declaration(False, True, 100)
                except ShaderError as error:
                    assert "flat interpolation" in str(error)
                else:
                    assert False, "unsupported flat interpolation should fail in developer mode"

                try:
                    noperspective.declaration(False, True, 300)
                except ShaderError as error:
                    assert "noperspective interpolation" in str(error)
                else:
                    assert False, "unsupported noperspective interpolation should fail in developer mode"
            finally:
                renpy.config.developer = old_developer
                renpy.display.log.write = old_write

    testcase interpolation_minimum_dialect:
        description "Flat and noperspective interpolation require the modern dialect"

        python:
            import renpy.gl2.gl2shadercache as shadercache

            for interpolation in ("flat", "noperspective"):
                name = "test_shaders.minimum_" + interpolation
                part = shadercache.ShaderPart(
                    name,
                    glsl=100,
                    variables=f"{interpolation} varying vec2 v_test;",
                    vertex_100="v_test = vec2(0.0);",
                    fragment_100="gl_FragColor = vec4(v_test, 0.0, 1.0);",
                )

                try:
                    assert part.minimum_dialect == 300
                    assert part.minimum_feature == f"{interpolation} interpolation on v_test"
                finally:
                    del shadercache.shader_part[name]

    testcase failed_fallback_preserves_version:
        description "A failed fallback does not change the shader cache version"

        python:
            import renpy.gl2.gl2shader as shader
            import renpy.gl2.gl2shadercache as shadercache

            name = "test_shaders.fallback_failure"
            old_program = shader.Program

            class FailingProgram:
                def __init__(self, *args):
                    pass

                def load(self):
                    from renpy.gl2.gl2shader import ShaderError

                    raise ShaderError("test shader failure")

            shadercache.ShaderPart(name, glsl=100)
            shader.Program = FailingProgram

            try:
                cache = shadercache.ShaderCache("test-shaders-fallback.txt", True, 300)

                try:
                    cache.get((name,))
                except shader.ShaderError:
                    pass
                else:
                    assert False, "both shader builds should fail"

                assert cache.version == 300
            finally:
                shader.Program = old_program
                del shadercache.shader_part[name]

    testcase renders:
        description "Draws with parts in both dialects"

        run Start("test_shaders__render__label")
        pause 0.3
