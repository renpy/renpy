# The Ren'Py/DSE event dispatcher. This file contains the code that
# actually supports the running of events. Specifically, it contains
# code that determines which events are available, which events can
# run, and to actually run the events that should be run during a
# given period.

# This isn't really intended to be user-changable.

init -100 python:

    # A list of all of the events that the system knowns about,
    # it's filtered to determine which events should run when.
    all_events = [ ]

    # The base class for events. When constructed, an event
    # automatically adds itself to all_events.
    #
    # The first parameter for this is a unique name for the event,
    # which is also used as the label that is called when the
    # event executes.
    #
    # All other parameters are expressions. These expressions can
    # be either strings, or objects having an eval method. Many
    # interesting objects are given below.
    #
    # Keyword arguments are also kept on the object. Currently,
    # there is one useful keyword argument, priority. This
    # controls the order in which events are in the event list.
    # (Events with lower priority number are evaluated first. If a
    # priority is not specified, it's 100.)
    class event(object):

        def __repr__(self):
            return '<event ' + self.name + '>'

        def __init__(self, name, *args, **kwargs):

            self.name = name

            exprs = [ ]

            for i in args:
                if isinstance(i, basestring):
                    exprs.append(event.evaluate(i))
                else:
                    exprs.append(i)

            self.exprs = exprs

            self.priority = kwargs.get('priority', 100)

            all_events.append(self)

        # Checks to see if this event is valid. It's called with
        # a list of events that have already checked out to be
        # True, and returns True if this event checks out.
        def check(self, valid):

            for i in self.exprs:
                if not i.eval(self.name, valid):
                    return False

            return True

        def properties(self):

            rv = { }

            for i in self.exprs:
                rv.update(i.properties())

            return rv


        # The base class for all of the event checks given below.
        class event_check(object):

            def properties(self):
                return { }

            def __invert__(self):
                return event.false(self)

            def __and__(self, other):
                return event.and_op(self, other)

            def __or__(self, other):
                return event.or_op(self, other)


        # This evaluates the expression given as an argument, and the
        # returns true if it evaluates to true.
        class evaluate(event_check):

            def __init__(self, expr):
                self.expr = expr

            def eval(self, name, valid):
                return eval(self.expr)

        # If present as a condition to an event, an object of this
        # type ensures that the event will only execute once.
        class once(event_check):
            def eval(self, name, valid):
                return name not in events_executed

        # Returns True if no event of higher priority can execute,
        # and false otherwise. In general, solo events should be
        # the lowest priority, and are run if nothing else is.
        class solo(event_check):
            def eval(self, name, valid):

                # True if valid is empty.
                return not valid

        # Returns True if no event of higher priority can execute.
        # This also prevents other events from executing.
        class only(solo):

            def properties(self):
                return dict(only=True)


        # Returns True if the given events have happend already,
        # at any time in the game. False if at least one hasn't
        # happened yet.
        class happened(event_check):
            def __init__(self, *events):
                self.events = events

            def eval(self, name, valid):
                for i in self.events:
                    if i not in events_executed:
                        return False

                return True

        # Returns True probability of the time, where probability
        # is a number between 0 and 1.
        class random(event_check):

            def __init__(self, probability):
                self.probability = probability

            def eval(self, name, valid):
                return renpy.random.random() <= self.probability

        # Chooses only one from the group.
        class choose_one(event_check):

            def __init__(self, group, group_count=1):
                self.group = group
                self.group_count = group_count

            def eval(self, name, valid):
                return True

            def properties(self):
                return dict(group=self.group,
                            group_count=self.group_count)


        # Evaluates its argument, and returns true if it is false
        # and vice-versa.
        class false(event_check):
            def __init__(self, cond):
                self.cond = cond

            def eval(self, name, valid):
                return not self.cond.eval(name, valid)

        # Handles the and operator.
        class and_op(event_check):

            def __init__(self, *args):
                self.args = args

            def eval(self, name, valid):
                for i in self.args:
                    if not i.eval(name, valid):
                        return False
                return True

        # Handles the or operator.
        class or_op(event_check):

            def __init__(self, *args):
                self.args = args

            def eval(self, name, valid):
                for i in self.args:
                    if i.eval(name, valid):
                        return True
                return False

        # Returns True if all of the events given as arguments have
        # happened yesterday or earlier, or False otherwise.
        class depends(event_check):
            def __init__(self, *events):
                self.events = events

            def eval(self, name, valid):
                for i in self.events:
                    if i not in events_executed_yesterday:
                        return False

                return True


    # The number of periods to skip.
    skip_periods = 0

    # This returns True if the current period should be skipped,
    # or False if the current period should execute. If it returns
    # True, it decrements skip_periods.
    def check_skip_period():

        global skip_periods

        if skip_periods:
            skip_periods -= 1
            return True
        else:
            return False

    def __events_init():
        store.events_executed = { }
        store.events_executed_yesterday = { }

    config.start_callbacks.append(__events_init)
        

# This should called at the end of a (game) day, to let things
# like depends_yesterday to work.
label events_end_day:

    $ skip_periods = 0

    python hide:

        # We can't skip between days.
        skip_periods = 0

        for k in events_executed:
            events_executed_yesterday[k] = True

    return
    
# This is called once per period, to determine, and then execute, the
# events that should be run for that period. 
label events_run_period:

    $ events = [ ]

    python hide:

        eobjs = [ ]
        egroups = { }
        eingroup = { }

        for i in all_events:
            if not i.check(eobjs):
                continue
                
            eobjs.append(i)

            props = i.properties()

            if 'group' in props:
                group = props['group']
                count = props['group_count']

                egroups.setdefault(group, [ ]).extend([ i ] * count)
                eingroup[i] = group

            if 'only' in props:
                break

        echosen = { }

        for k in egroups:
            echosen[k] = renpy.random.choice(egroups[k])
            
        for i in eobjs:

            if i in eingroup and echosen[eingroup[i]] is not i:
                continue
            
            events.append(i.name)


    while not check_skip_period() and events:

        $ _event = events.pop(0)
        $ events_executed[_event] = True

        call expression _event from call_expression_event_1

    return

# If this is jumped to, it will end the current period immediately,
# and return control to the main program.
label events_end_period:

    $ skip_period = 1
    return

# If this is jumped to, it will end the current period and skip
# the next period. Use this if, say, the user goes on a date that
# takes up two time slots.
label events_skip_period:

    $ skip_period = 2
    return

        
init 100:
    python hide:
        # Sort all events on priority.
        all_events.sort(key=lambda i : i.priority)

    python hide:

        for i in all_events:
            if not renpy.has_label(i.name):
                raise Exception("'%s' is defined as an event somewhere in the game, but no label named '%s' was defined anywhere." % (i.name, i.name))
    

