# This file is responsible for displaying code examples. It expects to see
# comments like #begin foo and #end foo a the start of lines. The code is
# then used to create example fragments.
#
# When we see:
#
# show screen example(['foo', 'bar'])
#
# We concatenate fragements foo and bar, highlight them, wrap them into a
# viewport, button and transform, and display them to the user.

