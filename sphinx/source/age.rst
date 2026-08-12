User Age
========

To help you comply with regulations that may require you to restrict access to certain content based on the
user's age, Ren'Py exposes platform functionality that gives you a rage of ages for the user. This information
is only available on platforms that support it, and may only be available for certain jurisdictions.

.. include:: inc/age


Example
-------

::

    $ age_lower, age_upper = renpy.get_user_age()

    if age_upper < 18:
        # The user is under 18, for sure. Deny them access.
        jump under_18_screen
    elif age_lower >= 18:
        # The user is over 18, for sure. Let them in.
        jump bypass_age_check
    else:
        # Ask the user their age.
        jump age_check
