=====
Tests
=====

The repository keeps tests in two groups:

``tests/unit``
    Python unit tests that run under ``unittest``.

``tests/engine``
    A Ren'Py project that runs engine-level behavior checks through the
    testcase runner.

Typical commands::

    ./.venv/bin/python -m unittest discover -s tests/unit -t .
    ./run.sh tests/engine test
