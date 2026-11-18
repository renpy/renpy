## This file tests rollback identifiers.

# ==============
# == Fixtures ==
# ==============

default rollback_identifier_menu_count = 0
default menu_rollback_identifier = None

label rollback_identifier_menu:
    "Before the menu."

    $ rollback_identifier_menu_count += 1

    menu:
        "Which way?"

        "Done":
            pass

    "After the menu."
    return

init python:
    def capture_menu_rollback_identifier(statement):
        if statement.startswith("menu"):
            store.menu_rollback_identifier = renpy.get_rollback_identifier()

# ==============
# === Tests ====
# ==============

testsuite rollback_identifier:
    description "Tests `renpy.get_rollback_identifier` with `RollbackToIdentifier`."

    setup:
        $ config.statement_callbacks.append(capture_menu_rollback_identifier)

    teardown:
        $ config.statement_callbacks.remove(capture_menu_rollback_identifier)

    testcase menu:
        description "Rolls back to a menu identifier captured by a statement callback."

        $ menu_rollback_identifier = None
        run Start("rollback_identifier_menu")
        advance until screen "choice"

        assert eval (menu_rollback_identifier is not None)
        assert eval (rollback_identifier_menu_count == 1)

        click "Done"
        advance until "After the menu."
        assert eval (renpy.get_identifier_checkpoints(menu_rollback_identifier) is not None)

        run RollbackToIdentifier(menu_rollback_identifier)
        pause until screen "choice"

        assert eval (rollback_identifier_menu_count == 1)

        click "Done"
        advance until "After the menu."
