.. _history:

Dialogue History
================

Ren'Py includes a dialogue history system that stores each line of dialogue
after it has been shown to the player. This stored dialogue can then be
retrieved and re-shown to the player.

The dialogue history system is controlled by two variables.
The :var:`config.history_length` variable controls the maximum number
of history entries that are stored, and must be set to enable history
at all. The :var:`_history` variable can be used to disable and re-enable
history storage.

Finally, the :var:`_history_list` variable stores the actual history, as
a list of HistoryEntry objects. HistoryEntry objects contain data in
their fields, as defined below.

.. class:: HistoryEntry

    .. attribute:: kind

        The kind of character that created this history. Ren'Py sets this
        to either "adv" or "nvl".

    .. attribute:: who

        A string giving the name of the character that is speaking, or None
        if no such string exists.

    .. attribute:: what

        A string giving the dialogue text.

    .. attribute:: who_args

        A dictionary giving the properties that were supplied to the who
        text widget when the dialogue was originally shown.

    .. attribute:: what_args

        A dictionary giving the properties that were supplied to the what
        text widget when the dialogue was originally shown.

    .. attribute:: window_args

        A dictionary giving the properties that were supplied to the
        dialogue window when the dialogue was originally shown.

    .. attribute:: show_args

        A dictionary giving the properties that were supplied to the say
        screen when the dialogue was originally shown.

    .. attribute:: image_tag

        The image tag given to the :func:`Character`, or None if no such
        tag was given.

    .. attribute:: voice

        This is the object returned from :func:`_get_voice_info`, storing
        information about the voice that is being played.

    .. attribute:: rollback_identifier

        This is an identifier that can be passed to the :func:`RollbackToIdentifier`
        action, to cause a rollback to the line of script that generated
        this history entry. The rollback only occurs if the location is still in
        the script log, otherwise the action is insensitive.


Once a HistoryEntry has been created, it is passed to each of the
callbacks in :var:`config.history_callbacks`, which allows creator-written
code to add new fields.


