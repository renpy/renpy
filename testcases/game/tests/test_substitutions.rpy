# Tests for renpy.substitutions.

# ==============
# == Fixtures ==
# ==============

init python:
    from renpy.substitutions import SubstitutionError, convert, interpolate, parse, substitute

    substitution_store_value = "from the store"

    def parse_error_info(s):
        """
        Returns the (message, pos) of the SubstitutionError raised when
        parsing `s`, or None if no error is raised.
        """

        try:
            list(parse(s))
        except SubstitutionError as e:
            return e.message, e.pos

        return None

    def interpolate_error(s, scope):
        """
        Returns the exception raised when interpolating `s`, or None.
        """

        try:
            interpolate(s, scope)
        except Exception as e:
            return e

        return None

    def convert_error(value, conv):
        """
        Returns the exception raised by convert(value, conv, {}), or None.
        """

        try:
            convert(value, conv, {})
        except Exception as e:
            return e

        return None

    def test_triple_underscore():
        local_value = "a local"
        return renpy.substitutions.___("value: [local_value]")

    # Config values to restore after each testcase, captured at init time.
    # (Test statement scopes do not survive from "before" to "after" hooks.)
    substitutions_config_backup = (
        renpy.config.interpolate_exprs,
        renpy.config.new_substitutions,
        renpy.config.say_menu_text_filter,
        renpy.config.say_menu_text_filters,
    )


label substitutions__basic:
    $ name = "World"
    $ n = 5

    "Hello [name]!"
    "Escaped [[name] bracket."
    "Sum is [n + 1]."
    "Store says [substitution_store_value]."


label substitutions__conversions:
    $ name = "wORLD"
    $ braced = "{notatag}"
    $ tmpl = "inner [name]"

    "Upper [name!u] end."
    "Lower [name!l] end."
    "Capital [name!c] end."
    "Repr [name!r] end."
    "Quoted [braced!q] end."
    "Inner [tmpl!i] end."


label substitutions__format:
    $ n = 5
    $ pi = 3.14159

    "Pad [n:03d] end."
    "Pi [pi:.2f] end."
    "Right [n:>5] end."
    "Debug [n + 1=] end."


# ==============
# === Tests ====
# ==============

testsuite substitutions:

    after testcase:
        $ renpy.config.interpolate_exprs = substitutions_config_backup[0]
        $ renpy.config.new_substitutions = substitutions_config_backup[1]
        $ renpy.config.say_menu_text_filter = substitutions_config_backup[2]
        $ renpy.config.say_menu_text_filters = substitutions_config_backup[3]

        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase parse_literals:
        description "parse() yields literal text, unescaping [[ to [."

        assert eval list(parse("")) == []
        assert eval list(parse("hello")) == [("literal", "hello")]
        assert eval list(parse("a]b ]]c")) == [("literal", "a]b ]]c")]
        assert eval list(parse("[[")) == [("literal", "[")]
        assert eval list(parse("[[x]")) == [("literal", "[x]")]
        assert eval list(parse("a[[b]]c")) == [("literal", "a[b]]c")]

    testcase parse_fields:
        description "parse() splits substitutions into expr, conv and fmt."

        assert eval list(parse("[x]")) == [("expr", "x"), ("literal", "")]
        assert eval list(parse("a[x]b")) == [("literal", "a"), ("expr", "x"), ("literal", "b")]
        assert eval list(parse("[a][b]")) == [("expr", "a"), ("literal", ""), ("expr", "b"), ("literal", "")]

        # Whitespace inside the expression is stripped.
        assert eval list(parse("[ x ]")) == [("expr", "x"), ("literal", "")]

        # Nested brackets are part of the expression.
        assert eval list(parse("[a[0]]")) == [("expr", "a[0]"), ("literal", "")]

        # Conversion and format specifiers.
        assert eval list(parse("[x!r]")) == [("expr", "x"), ("conv", "r"), ("literal", "")]
        assert eval list(parse("[x:>10]")) == [("expr", "x"), ("fmt", ">10"), ("literal", "")]
        assert eval list(parse("[x!r:>10]")) == [("expr", "x"), ("conv", "r"), ("fmt", ">10"), ("literal", "")]

        # A trailing "!flags" in the format spec is taken as a conversion,
        # unless a conversion was already given.
        assert eval list(parse("[x:>10!i]")) == [("expr", "x"), ("conv", "i"), ("fmt", ">10"), ("literal", "")]
        assert eval list(parse("[x!r:>10!i]")) == [("expr", "x"), ("conv", "r"), ("fmt", ">10!i"), ("literal", "")]

        # Format specs may contain nested fields.
        assert eval list(parse("[x:>{width}]")) == [("expr", "x"), ("fmt", ">{width}"), ("literal", "")]

        # Self-documenting expressions.
        assert eval list(parse("[x=]")) == [("expr", "x="), ("literal", "")]
        assert eval list(parse("[x=!r]")) == [("expr", "x="), ("conv", "r"), ("literal", "")]

    testcase parse_errors:
        description "parse() reports malformed substitutions with positions."

        assert eval parse_error_info("[]") == ("expected expression", 0)
        assert eval parse_error_info("[!]") == ("expected expression", 0)
        assert eval parse_error_info("[:]") == ("expected expression", 0)

        assert eval parse_error_info("[foo") == ("'[' was never closed", 0)
        assert eval parse_error_info("[foo:") == ("'[' was never closed", 0)

        assert eval parse_error_info("[foo!]") == ("conversion specifier cannot be empty", 5)
        assert eval parse_error_info("[foo!!]") == ("invalid conversion character '!'", 5)
        assert eval parse_error_info("[foo!x]") == ("invalid conversion character 'x'", 5)

    testcase interpolate_basic:
        description "interpolate() evaluates expressions in the given scope."

        $ _scope = {"name": "World", "n": 5, "items": [10, 20, 30]}

        assert eval interpolate("hello", _scope) == "hello"
        assert eval interpolate("Hello [name]!", _scope) == "Hello World!"
        assert eval interpolate("[name][n]", _scope) == "World5"
        assert eval interpolate("[[name]", _scope) == "[name]"

        # Expressions are evaluated with the scope as locals.
        assert eval interpolate("[n + 1]", _scope) == "6"
        assert eval interpolate("[items[1]]", _scope) == "20"

        # Unknown names raise.
        assert eval isinstance(interpolate_error("[missing]", _scope), NameError)

    testcase interpolate_conversions:
        description "interpolate() applies conversion flags."

        $ _scope = {"name": "wORLD", "n": 5, "braced": "{a}", "tmpl": "Hi [name]!"}

        assert eval interpolate("[name!u]", _scope) == "WORLD"
        assert eval interpolate("[name!l]", _scope) == "world"
        assert eval interpolate("[name!c]", _scope) == "WORLD"
        assert eval interpolate("[name!r]", _scope) == "'wORLD'"
        assert eval interpolate("[n!s]", _scope) == "5"

        # Multiple flags are applied in a fixed order.
        assert eval interpolate("[name!ul]", _scope) == "world"

        # "q" doubles text tag braces.
        assert eval interpolate("[braced!q]", _scope) == "{{a}"

        # "i" interpolates the result again.
        assert eval interpolate("[tmpl!i]", _scope) == "Hi wORLD!"

    testcase interpolate_format_specs:
        description "interpolate() applies format specs."

        $ _scope = {"n": 5, "pi": 3.14159, "width": 3}

        assert eval interpolate("[n:03d]", _scope) == "005"
        assert eval interpolate("[pi:.2f]", _scope) == "3.14"
        assert eval interpolate("[n:>5]", _scope) == "    5"

        # Format specs are used verbatim; nested fields are not supported.
        assert eval isinstance(interpolate_error("[n:0>{width}]", _scope), ValueError)

    testcase interpolate_self_documenting:
        description "interpolate() supports f-string-like [expr=]."

        $ _scope = {"name": "World", "n": 5}

        assert eval interpolate("[name=]", _scope) == "name='World'"
        assert eval interpolate("[name=!s]", _scope) == "name=World"
        assert eval interpolate("[n + 1=]", _scope) == "n + 1=6"

    testcase interpolate_exprs_config:
        description "config.interpolate_exprs switches expression evaluation off or to fallback."

        $ _scope = {"d": {"k": "v"}, "items": [10, 20], "n": 5}

        # Old-style field access, without expression evaluation.
        $ renpy.config.interpolate_exprs = False
        assert eval interpolate("[d[k]]", _scope) == "v"
        assert eval interpolate("[items[1]]", _scope) == "20"
        assert eval isinstance(interpolate_error("[n + 1]", _scope), KeyError)

        # Fallback to field access when expression evaluation fails.
        $ renpy.config.interpolate_exprs = "fallback"
        assert eval interpolate("[n + 1]", _scope) == "6"
        assert eval interpolate("[d[k]]", _scope) == "v"

    testcase convert:
        description "convert() applies and validates conversion flags."

        assert eval convert("abc", "r", {}) == "'abc'"
        assert eval convert("abc", "s", {}) == "abc"
        assert eval convert("{a}", "q", {}) == "{{a}"
        assert eval convert("aBc", "u", {}) == "ABC"
        assert eval convert("aBc", "l", {}) == "abc"
        assert eval convert("hello world", "c", {}) == "Hello world"

        # "t" translates; untranslated strings are returned as-is.
        assert eval convert("abc", "t", {}) == "abc"

        # "f" applies config.say_menu_text_filter(s).
        $ renpy.config.say_menu_text_filter = lambda s: s + "!"
        $ renpy.config.say_menu_text_filters = [lambda s: s.upper()]
        assert eval convert("ab", "f", {}) == "AB!"

        # Empty and invalid conversions are rejected.
        assert eval isinstance(convert_error("abc", ""), ValueError)
        assert eval isinstance(convert_error("abc", "x"), ValueError)

    testcase substitute:
        description "substitute() translates and formats, reporting if it changed the string."

        assert eval substitute("plain") == ("plain", False)
        assert eval substitute(123) == ("123", False)
        assert eval substitute("Hello [name]!", {"name": "World"}) == ("Hello World!", True)
        assert eval substitute("a [n] b", {"n": 42}) == ("a 42 b", True)

        # The store is used as a fallback scope.
        assert eval substitute("[substitution_store_value]") == ("from the store", True)

        # Strings without substitutions are returned unchanged.
        assert eval substitute("no brackets", {"n": 42}) == ("no brackets", False)

        # Substitution can be disabled, and forced back on.
        $ renpy.config.new_substitutions = False
        assert eval substitute("a [n] b", {"n": 42}) == ("a [n] b", False)
        assert eval substitute("a [n] b", {"n": 42}, force=True) == ("a 42 b", True)

    testcase triple_underscore:
        description "___() substitutes using the caller's local variables."

        assert eval test_triple_underscore() == "value: a local"

    testcase say_interpolation:
        description "Say dialogue interpolates variables, expressions and escaped brackets."

        run Start("substitutions__basic")
        assert "Hello World!" timeout 1.0
        assert "Hello [name]!" raw
        advance

        assert "Escaped [name] bracket." timeout 1.0
        advance

        assert "Sum is 6." timeout 1.0
        advance

        assert "Store says from the store." timeout 1.0
        advance until screen "main_menu"

    testcase say_conversions:
        description "Say dialogue applies conversion flags."

        run Start("substitutions__conversions")
        assert "Upper WORLD end." timeout 1.0
        advance

        assert "Lower world end." timeout 1.0
        advance

        assert "Capital WORLD end." timeout 1.0
        advance

        assert "Repr 'wORLD' end." timeout 1.0
        advance

        # The !q flag doubles "{" in the substituted (searched) text; the
        # screen renders it back to a single "{", but the selector searches
        # the pre-tag-parse text.
        assert "Quoted {{notatag} end." timeout 1.0
        advance

        assert "Inner inner wORLD end." timeout 1.0
        advance until screen "main_menu"

    testcase say_format_specs:
        description "Say dialogue applies format specs and self-documenting expressions."

        run Start("substitutions__format")
        assert "Pad 005 end." timeout 1.0
        advance

        assert "Pi 3.14 end." timeout 1.0
        advance

        assert "Right     5 end." timeout 1.0
        advance

        assert "Debug n + 1=6 end." timeout 1.0
        advance until screen "main_menu"
