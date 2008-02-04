# This used to be a mirror of subprocess, which wasn't distributed with
# python 2.3. Now that we use 2.5, we can just import it.

# Annoying code since we have the same name as the module we want to import.
# :-(
subprocess = __import__('subprocess', level=0)
for i in subprocess.__all__:
    globals()[i] = getattr(subprocess, i)


