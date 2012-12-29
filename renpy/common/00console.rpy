# console.rpy # Ren'Py debug console
# Copyright (C) 2012 Shiz, C, delta.
#
# This program is free software. It comes without any warranty, to the extent permitted by applicable law.
# You can redistribute it and/or modify it under the terms of the Do What The Fuck You Want To Public License, 
# Version 2, as published by Sam Hocevar. See http://sam.zoy.org/wtfpl/COPYING for more details.
#
# Usage:
#  With config.developer set to True, press the key assigned to config.debug_console_keybind (~, the tilde, by default) to open the console.
#  Type 'help' for in-console help. Press the same key again to close the console.
#
# The following configuration variables are offered for customization:
#  - config.debug_console_layer: the layer the debug console will draw on, will be created at init-time. default: 'debug_console'
#  - config.debug_console_history_size: the number of commands to store in history. default: 100
#  - config.debug_console_keybind: the key combination used to open the console. default: 'shift_K_BACKQUOTE', which defaults to the tilde (~) on QWERTY.
#  - config.debug_console_custom_commands: a simple name -> function dictionary for custom commands. Command functions should take a single parameter, the full command and return a tuple of (result, no_error).
#
# The following styles are offered for customization:
#  - debug_console: the debug console frame.
#
#  - debug_console_input: the input frame.
#  - debug_console_prompt: the '>' or '...' text preceding a command input.
#  - debug_console_input_text: the actual text that is being input by the user.
#
#  - debug_console_history: the history frame.
#  - debug_console_history_item: an item frame in the history.
#  - debug_console_command: a command frame in the command history.
#  - debug_console_command_text: the actual command text.
#  - debug_console_result: the result frame from a command in the command history, if applicable.
#  - debug_console_result_text: the actual result text.
#
#  - debug_console_trace: the trace box used to show expression and variable traces.
#  - debug_console_trace_var: the variable in a trace box.
#  - debug_console_trace_value: the value in a trace box.
#
# Changelog:
#  v1.3b: Fixed some rollback issues, fixed custom command invocation, updated documentation, added styles for the trace box.
#  v1.3: Added error highlighting, added ability to run init commands (image, transform definitions...), delegated Python block execution
#        to Ren'Py.
#  v1.2: Added custom keybinding to open console, allowed pressing the console key again to close it, UI revamp, 
#        added more styling options, added configuration variables, added support for variable and expression tracing, Python expressions
#        now also capture console (stdout, stderr) output, added custom commands, partially fixed rollback issue.
#  v1.1b: Added nicer handling of multi-line input.
#  v1.1: Fixed python: block support, fixed spacing issue in showing multi-line commands in command history.
#  v1.0: Initial release.
#
# Known bugs/defects:
#  - Menus can mess with flow. This is solved by adding 'return' to the end of every console-defined menu option.
#  - When writing multi-line blocks, you can't go back to a previous line to edit it.
#  - Rollback after executing a Ren'Py command in the console works, but isn't fully smooth yet: added commands will be marked as non-seen.
# Tested on Ren'Py 6.13.11, 6.14.0 and 6.14.1. Not guaranteed to work on any other version.

# Configuration and style initalization.
init -1500 python:

    # If true, the console is enabled despite config.developer being False.
    config.debug_console = False

    config.debug_console_layer = 'debug_console'
    config.debug_console_history_size = 100
    config.debug_console_commands = { }
    
    # Create default styles. See above for documentation.
    style.create('debug_console', '_default')
    style.debug_console.background = None
    
    style.create('debug_console_input', '_default')
    style.debug_console_input.background = "#00000040"
    style.debug_console_input.xfill = True
    
    style.create('debug_console_prompt', 'text')
    style.debug_console_prompt.color = "#ffffff"
    style.debug_console_prompt.minwidth = 25
    style.debug_console_prompt.text_align = 1.0
    
    style.create('debug_console_input_text', 'input')
    style.debug_console_input_text.color = "#fafafa"
    
    style.create('debug_console_history', 'frame')
    style.debug_console_history.background = "#00000000"
    style.debug_console_history.xpos = 0
    style.debug_console_history.ypos = 0
    style.debug_console_history.xpadding = 0
    style.debug_console_history.ypadding = 0
    style.debug_console_history.xfill = True
    style.debug_console_history.yfill = True 
    
    style.create('debug_console_history_item', 'frame')
    style.debug_console_history_item.background = "#00000040"
    style.debug_console_history_item.xpos = 0
    style.debug_console_history_item.ypos = 0
    style.debug_console_history_item.xpadding = 0
    style.debug_console_history_item.ypadding = 0
    style.debug_console_history_item.top_margin = 4
    style.debug_console_history_item.xfill = True
    
    style.create('debug_console_command', 'frame')
    style.debug_console_command.background = "#00000040"
    
    style.create('debug_console_command_text', 'text')
    style.debug_console_command_text.color = "#ffffff"
    
    style.create('debug_console_result', 'frame')
    style.debug_console_result.background = "#00000000"
    
    style.create('debug_console_result_text', 'text')
    style.debug_console_result_text.color = "#ffffff"
    
    style.create('debug_console_error_text', 'text')
    style.debug_console_error_text.color = "#ff0000"
    
    style.create('debug_console_trace', 'frame')
    style.debug_console_trace.background = "#00000040"
    style.debug_console_trace.xalign = 1.0
    style.debug_console_trace.top_margin = 10
    style.debug_console_trace.right_margin = 20
    
    style.create('debug_console_trace_var', 'text')
    style.debug_console_trace_var.bold = True
    
    style.create('debug_console_trace_value', 'text')

init -1500 python in _debug_console:
    from store import config
    import sys
    import traceback
    
    class BoundedList(list):
        """
        A list that's bounded at a certain size.
        """
        
        def __init__(self, size):
            self.size = size

        def append(self, value):
            super(BoundedList, self).append(value)
    
            while len(self) >= self.size:
                self.data.pop(0)
        
        def clear(self):
            self[:] = [ ]

    class HistoryEntry(object):
        """
        Represents an entry in the history list.
        """
        
        def __init__(self, command, result=None, is_error=False):
            self.command = command
            self.result = result
            self.is_error = is_error
    
    class ScriptErrorHandler(object):
        """
        Handles error in Ren'Py script.
        """
        
        def __init__(self):
            self.target_depth = renpy.call_stack_depth()
            
        def __call__(self, short, full, traceback_fn):
            he = debug_console.history[-1] 
            he.result = short.split("\n")[-2]
            he.is_error = True

            while renpy.call_stack_depth() > self.target_depth:
                renpy.pop_call()
                
            renpy.jump("_debug_console")


    class DebugConsole(object):
        
        def __init__(self):
            
            self.reset()
            
            self.history = BoundedList(config.debug_console_history_size)
            self.first_time = True
            
            self.help_message = (""
                "Ren\'Py debug console\n"
                " by Shiz, C and delta.\n"
                "commands:\n"
                " <any Ren'Py command>  - execute Ren'Py command as if it were placed in a script file.\n"
                " $ <pycode>            - execute Python command.\n"
                " clear                 - clear the command history.\n"
                " crash                 - crash the game with an appropriate error message.\n"
                " reload                - reload the game.\n"
                " watch <expression>    - watch variable or expression.\n"
                " unwatch <expression>  - stop watching variable or expression.\n"
                " unwatchall            - stop watching all variables and expressions.\n"
                " help                  - show this message.\n"
                " exit/quit/~           - close the console.")

        def start(self):
            he = HistoryEntry(None)
        
            message = ""
            
            if self.first_time:      
                message += renpy.version() + " console, originally by Shiz, C, and delta.\n"
                message += "Press <esc> to exit console. Type help for help.\n"
                self.first_time = None
            
            if self.can_renpy():
                message += "Ren'Py script enabled."
            else:
                message += "Ren'Py script disabled."

            he.result = message
            self.history.append(he)

        def reset(self):
        
            # The list of lines that have been entered by the user, but not yet
            # processed.
            self.lines = [ ]

        def interact(self):

            def get_indent(s):
                """
                Computes the indentation for the line following line s.
                """
                
                rv = ""
                
                for i in s:
                    if i == " ":
                        rv += " "
                    else:
                        break

                if s.rstrip().endswith(":"):
                    rv += "    "

                if not s.rstrip():
                    rv = rv[:-4]
                    
                return rv
            
            renpy.game.context().exception_handler = None
                    
            # Prompt the user for a line of code.
            if self.lines:
                indent = get_indent(self.lines[-1])
            else:
                indent = ""
                
            default = indent
            renpy.show_screen("_debug_console", lines=self.lines, indent=indent, default=default, history=self.history, _transient=True)
            line = ui.interact()

            self.lines.append(line)

            if get_indent(line) != "":
                return

            lines = self.lines
            self.lines = [ ]
            
            self.run(lines)
            
        def can_renpy(self):
            """
            Returns true if we can run Ren'Py code.
            """
            
            return renpy.game.context().rollback
            
        def format_exception(self):
            etype, evalue, etb = sys.exc_info()
            return traceback.format_exception_only(etype, evalue)[-1]
            
        def run(self, lines):

            line_count = len(lines)
            code = "\n".join(lines)

            he = HistoryEntry(code)
            self.history.append(he)

            try:

                # If we have 1 line, try to parse it as a command.
                if line_count == 1:
                    block = [ ( "<console>", 1, code, [ ]) ]
                    l = renpy.parser.Lexer(block)
                    l.advance()
                    
                    # Command can be None, but that's okay, since the lookup will fail.
                    command = l.name()
                    
                    command_fn = config.debug_console_commands.get(command, None)

                    if command_fn is not None:
                        he.result = command_fn(l)
                        return
                    
                error = None
                    
                # Try to run it as Ren'Py.
                if self.can_renpy():
                        
                    # TODO: Can we run Ren'Py code?
                    name = renpy.load_string(code + "\nreturn")

                    if name is not None:
                        renpy.game.context().exception_handler = ScriptErrorHandler()
                        renpy.call(name)
                    else:
                        error = "\n\n".join(renpy.get_parse_errors())
                
                # Try to eval it. 
                try:
                    renpy.python.py_compile(code, 'eval')
                except:
                    pass
                else:
                    result = renpy.python.py_eval(code)
                    he.result = repr(result)
                    return
 
                # Try to exec it.
                try:
                    renpy.python.py_compile(code, "exec")
                except:
                    if error is None:
                        error = self.format_exception()
                else:
                    renpy.python.py_exec(code)
                    return
                        
                if error is not None:
                    he.result = error
                    he.is_error = True

            except renpy.game.CONTROL_EXCEPTIONS:
                raise

            except:
                he.result = self.format_exception()
                he.is_error = True


#        def enable(self):
#            if not self.enabled:
#                self.enabled = True
#                renpy.call_in_new_context('_debug_console_trampoline')
        
#        def disable(self):
#            if self.enabled:
#                ui.layer(self.layer)
#                ui.clear()
#                ui.close()
#                self.enabled = False
        
#        def draw(self, input_lines = [], current_depth = 0):
#            # Clear out any existing content and draw the base frame.
#            ui.layer(self.layer)
#            ui.clear()
#            ui.frame(style='debug_console')
#            ui.vbox()
        
#            # Draw current command input.
#            self.draw_input(input_lines, current_depth)
#            # Draw command history.
#            self.draw_history()
            
#            # Close console vbox and frame, and the console layer.
#            ui.close()
#            ui.close()
        
#        def draw_input(self, input_lines = [], current_depth = 0):
#            # Draw the input frame.
#            ui.frame(style='debug_console_input')
#            ui.vbox()
            
#            # Draw prompt.
#            ui.hbox()
#            ui.text('> ', id='debug_console_prompt_0', style='debug_console_prompt')
            
#            # Draw any previous input lines.
#            line_count = 0
#            for line, depth in input_lines:
#                # Draw input line content and close its hbox.
#                ui.text(line, id='debug_console_line_' + str(line_count), style='debug_console_input_text')
#                ui.close()
                
#                # Figure out next line depth and print its appropriate prompt.
#                line_count += 1
#                if len(input_lines) > line_count:
#                    next_line, next_depth = input_lines[line_count]
#                else:
#                    next_depth = current_depth
#                ui.hbox()
#                ui.text('    ' + '....' * next_depth + ' ', id='debug_console_prompt_' + str(line_count), style='debug_console_prompt')
            
#            # Draw input widget and close its hbox. Add a keymap to allow the same button that opened the console to instantly close it, 
#            # along with trapping the escape key, and disabling the right mouse click.
#            ui.input('', id='debug_console_input', style='debug_console_input_text')
#            ui.keymap(**{ config.debug_console_keybind: lambda: 'quit' })
#            ui.keymap(K_ESCAPE=lambda: 'quit')
#            ui.keymap(mouseup_3=None)
#            ui.close()
            
#            # Close input vbox and frame.
#            ui.close()
        
#        def draw_history(self):
#            # Draw command history, in reverse order.
#            commands = range(self.history_size)
#            commands.reverse()
            
#            # Draw the history frame, and make it scrollable.
#            ui.frame(style='debug_console_history')
#            ui.viewport(mousewheel=True)
            
#            ui.vbox(xpos=0, xfill=True)
#            for i in commands:
#                command, result, is_error = self.history.get(i)
#                if command is None:
#                    continue
                
#                # Draw command if not none, and draw result if applicable.
#                ui.frame(style='debug_console_history_item')
#                ui.vbox(xpadding=0, ypadding=0)
                
#                ui.frame(xfill=True, style='debug_console_command')
#                ui.text(self.sanitize(command), id='debug_console_command_' + str(i), style='debug_console_command_text')
                
#                if result is not None:
#                    ui.frame(xfill=True, style='debug_console_result')
#                    if is_error:
#                        ui.text(self.sanitize(result), id='debug_console_response_' + str(i), style='debug_console_error_text')
#                    else:
#                        ui.text(self.sanitize(result), id='debug_console_response_' + str(i), style='debug_console_result_text')
                    
                
#                # Close command vbox.
#                ui.close()
#            # Close history frame.
#            ui.close()

        # Accept a command, allowing for recursive blocks.
        def take_command(self):
            command = ""
            depth = 0
            lines = []
            
            while True:
                # Draw console.
                self.draw(lines, depth)
                # Get input.
                mean = ui.interact()
                
                if mean == '' or mean == 'end':
                    depth -= 1
                else:
                    lines.append((mean, depth))
                    command += "\n" + "    " * depth + mean
                    # Command enters in :, meaning a new block. Increase nesting.
                    if mean.endswith(':'):
                         depth += 1
                
                # Draw another prompt if we are at a sublevel.
                if depth < 1:
                    break
            
            # Clear all input lines now that we're done.
            return command.strip("\n")
        
#        def interact(self, **kwargs):
#            # Trick Ren'Py into thinking this context is rollback-able.
#            renpy.game.context().rollback = True
#            # Set script re-entry points and node list 'tail' for AST injection.
#            self.parent_context = renpy.game.context(-2)
#            self.parent_node = renpy.game.script.lookup(self.parent_context.current)
#            self.tail_node = self.parent_node
#            self.script_reentry_point = self.parent_node.next
            
#            # Enter read-eval-print loop.
#            while self.enabled:
#                command = self.take_command()
                
#                # 'quit', 'exit', an empty string or '~' exit the console interaction.
#                if command == 'quit' or command == 'exit' or command == '~' or command == '':
#                    self.disable()
#                    return
#                # 'clear' clears the command history and thus the screen.
#                elif command == 'clear':
#                    for _ in range(self.history_size):
#                        self.history.push((None, None, None))
#                else:
#                    (result, is_error) = self.execute(command, command.startswith('init'))
#                    self.history.push((command, result, is_error))
                    
#                # Allow the UI to adapt to its consequences.
#                renpy.restart_interaction()
         
        def execute(self, command, init = False):
            # Try custom commands first.
            for c, func in self.custom_commands.items():
                if command == c:
                    try:
                        return func(command)
                    except:
                        (name, value, traceback) = sys.exc_info()
                        return (name + ': ' + str(value.message), False)
            
            # Crash the game with an appropriate error message.
            if command == 'crash':
                errors = [
                    'expected statement',
                    'Cannot start an interaction in the middle of an interaction, without creating a new context.',
                    'screen() got an unexpected keyword argument _name',
                    'indentation mismatch',
                    'Could not find user-defined statement at runtime.',
                    'Context not capable of executing Ren\'Py code.',
                    'error in Python block starting at line %d: TypeError' % renpy.random.randint(1, 25),
                    'UnicodeDecodeError: \'utf8\' codec can\'t decode byte 0xa0 in position 1329: invalid start byte'
                ];
                
                raise TypeError(renpy.random.choice(errors))
            elif command == 'reload' or command == 'R':
                renpy.call_in_new_context('_save_reload_game')
                return (None, False)
            elif command == 'help':
                return (self.help_message, False)
            # Easter egg help.
            elif command == 'halp':
                return (self.help_message.replace('e', 'a'), False)
            # Trace expression.
            elif command.startswith('trace '):
                self.traced_expressions.append(command[6:])
                return (None, False)
            # Untrace expression.
            elif command.startswith('untrace '):
                if command[8:] in self.traced_expressions:
                    self.traced_expressions.remove(command[8:])
                return (None, False)
            # Untrace all expressions.
            elif command.startswith('untraceall'):
                self.traced_expressions = []
                return (None, False)
            # Easter egg.
            elif command == '...':
                return ('...', False)
            # Python code.
            elif command.startswith('$'):
                return self.execute_python(command.lstrip('$ '))
            # Ren'Py code.
            else:
                return self.execute_renpy(command, init=init)
        
        def execute_python(self, code):
            from StringIO import StringIO
            
            # Capture console output streams as well.
            console = StringIO()
            sys.stdout = console
            sys.stderr = console
            
            is_error = False
            result = None
            try:
                # Because eval can't handle assignments, definitions and other things, we have to pass on assignments to exec if encountered.
                # No, it's not pretty.
                try:
                    result = repr(eval(code))
                except SyntaxError, e:
                    # Use renpy.store as locals, to properly store assignments.
                    exec code in globals(), vars(renpy.store)
            except:
                (name, value, traceback) = sys.exc_info()
                result = name.__name__ + ': ' + value.message
                is_error = True
            finally:
                # Restore console output streams.
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                                  
                # Get and append result and output streams.
                console_output = console.getvalue()
                console.close()
                
                # Print console output to the console.
                if console_output:
                    print console_output,
                
                result = self.safe_append(console_output, result)
                if result is not None:
                    result = result.strip()
                
                return (result, is_error)
        
        def execute_renpy(self, command, init = False):
            # Transform command into logical parser lines.
            line_number = 1
            lines = []
            for line in command.splitlines():
                if line.strip() == '':
                    continue
                lines.append(('<console command>', line_number, line))
                line_number += 1
            
            # Save a backup of the old pycode objects - we're going to restore it
            # later so we won't have this bytecode in bytecode.rpyb. This should only go
            # for init objects, but at this point we're unsure if we want init mode.
            old_pycode = renpy.game.script.all_pycode[:]
            
            # Generate logical blocks and feed them to the lexer.
            blocks = renpy.parser.group_logical_lines(lines)
            lexer = renpy.parser.Lexer(blocks)
            # Feed the lexer to the block parser, effectively parsing the command.
            nodes = renpy.parser.parse_block(lexer)
            # Assign names to our new nodes.
            renpy.game.script.assign_names(nodes, '!debug_console/%i.rpy' % (renpy.random.randint(- sys.maxint - 1, sys.maxint)))
            
            if renpy.parser.parse_errors:
                # One or more errors occurred, display them.
                errors = renpy.parser.parse_errors
                renpy.parser.parse_errors = []
                return ("\n".join(errors), True)
            else:
                # No point in execution if there are no nodes.
                if len(nodes) == 0:
                    return
                
                # Check if the parser generated an init block.
                init = init or isinstance(nodes[0], renpy.ast.Init)
                
                # Set this context to mock the init phase if the code is init code,
                # and compile any bytecode.
                if init:
                    renpy.game.context().init_phase = True
                    old_cache = renpy.game.script.bytecode_newcache.copy()
                renpy.game.script.update_bytecode()
                
                # Prepare nodes for rollback.
                renpy.game.log.begin()

                renpy.ast.chain_block(nodes, None)
                try:
                    # Keep on going until we reach our re-entry point -- we don't want to go too far.
                    node = nodes[0]
                    if init:
                        _, node = node.get_init()

                    while node and node != self.script_reentry_point:
                        # Reset next node.
                        renpy.game.context().next_node = None
                        
                        # We have to handle jump and call as special cases, since they involve context wizardry,
                        # and we're in a different (debug console) context. 
                        if isinstance(node, renpy.ast.Jump):
                            # Since we're exiting the console automatically while jumping, disable it first so we can get 
                            # back into it after the jump.
                            self.disable()
                            renpy.jump_out_of_context(node.target)
                        elif isinstance(node, renpy.ast.Call):
                            renpy.call_in_new_context(node.label)
                        else:
                            # Inject node and execute it.
                            if not init:
                                self.inject_node(node)
                            node.execute()
                            
                            # Make node available for roll-forward.
                            if not init:
                                renpy.game.script.namemap[node.name] = node
                                if self.parent_context.seen:
                                    self.parent_context.seen_session[node.name] = True
                                    self.parent_context.seen_ever[node.name] = True
                            
                            # Next node is determined by the current node executed.
                            node = renpy.game.context().next_node
                    
                    # Reset init value and bytecode cache.
                    if init:
                        renpy.game.context().init_phase = False
                        renpy.game.script.bytecode_newcache = old_cache.copy()
                        renpy.game.script.all_pycode = old_pycode[:]
                    
                    # End logging.
                    renpy.game.log.complete()
                    
                    return (None, False)
                except renpy.game.JumpOutException:
                    if init:
                        renpy.game.context().init_phase = False
                        renpy.game.script.bytecode_newcache = old_cache
                        renpy.game.script.all_pycode = old_pycode
                    # Pass JumpOutExceptions back to our outer call_in_new_context, which will then perform the proper jump.
                    self.disable()
                    raise
                except:                    
                    if init:
                        renpy.game.context().init_phase = False
                        renpy.game.script.bytecode_newcache = old_cache
                        renpy.game.script.all_pycode = old_pycode
                    (name, value, traceback) = sys.exc_info()
                    return (str(name) + ': ' + str(value.msg), True)
        
        def safe_append(self, left, right):
            # Safely append two strings, counting an empty strings as None.
            if left is None or left == '':
                if right != '':
                    return right
                return None
            elif right is None or right == '':
                return left
            else:
                return left + right
        
        # Perform actual AST injection. Don't ask.
        def inject_node(self, node):
            # Set next node of current script tail node to our newly-injected node
            self.tail_node.chain(node)
            # Set the new script tail node, and its next node to be back at our original script.
            self.tail_node = node
            self.tail_node.chain(self.script_reentry_point)
            
        # Sanitize string for Ren'Py display.
        def sanitize(self, str):
            return str.replace('[', '[[').replace('{', '{{')
    
    debug_console = None
    
    def enter():
        """
        Called to enter the debug console.
        """

        if debug_console is None:
            return

        debug_console.start()

        if renpy.game.context().rollback:
            try:
                renpy.rollback(checkpoints=0, force=True, greedy=False, label="_debug_console")
            except renpy.game.CONTROL_EXCEPTIONS:
                raise
            except:
                pass
                
        renpy.call_in_new_context("_debug_console")

init 1500 python in _debug_console:
    
    if config.developer or config.debug_console:
        debug_console = DebugConsole()


#init python 1500:
    
#    if config.developer:
        
#        # Create proper debug overlay.
#        def debug_overlay():
#            ui.keymap(**{ config.debug_console_keybind: debug_console.enable })
            
#            if len(debug_console.traced_expressions) > 0:
#                ui.frame(style='debug_console_trace')
#                ui.vbox()
#                for expression in debug_console.traced_expressions:
#                    ui.hbox()
#                    ui.text(debug_console.sanitize(expression) + ": ", style='debug_console_trace_var')
#                    ui.text(debug_console.sanitize(debug_console.execute_python(expression)), style='debug_console_trace_value')
#                    ui.close()
#                ui.close()
        
#        config.overlay_functions.append(debug_overlay)


screen _debug_console:
    # This screen takes as arguments:
    #
    # lines
    #    The current set of lines in the input buffer.
    # indent
    #    Indentation to apply to the new line.
    # history
    #    A list of command, result, is_error tuples. 
    

    zorder 1002
    modal True

    vbox:

        # Draw the current input.
        frame style "debug_console_input":
        
            has vbox
            
            for line in lines:
                hbox:
                    spacing 4
                    
                    if line[:1] != " ":
                        text "> " style "debug_console_prompt"
                    else:
                        text "... " style "debug_console_prompt"
                    
                    text "[line!q]" style "debug_console_input_text"
                    
            hbox:
                spacing 4
                
                if not indent:
                    text "> " style "debug_console_prompt"
                else:
                    text "... " style "debug_console_prompt"
                                
                input default default style "debug_console_input_text"


        # Draw historical console input.
        $ rev_history = list(history)
        $ rev_history.reverse()
        
        frame style "debug_console_history":
            
            has viewport:
                mousewheel True
                
            has vbox:
                xfill True
                
            for he in rev_history:
                
                frame style "debug_console_history_item":
                    has vbox
                        
                    if he.command is not None:
                        frame style "debug_console_command":
                            xfill True
                            text "[he.command!q]" style "debug_console_command_text"
                    
                    if he.result is not None:
                        
                        frame style "debug_console_result":
                            if he.is_error:
                                text "[he.result!q]" style "debug_console_error_text"
                            else:
                                text "[he.result!q]" style "debug_console_result_text"
    
    key "game_menu" action Jump("_debug_console_return")
    

screen _trace_screen:

    zorder 1001

    if _debug_console.traced_expressions:
    
        frame style "debug_console_trace":
            
            for expr in _debug_console.traced_expressions:
                python:
                    try:
                        value = repr(eval(expr))
                    except:
                        value = "eval failed"
                
                hbox:
                    text "[expr!q]" style "debug_console_trace_var"
                    text "[value!q]" style "debug_console_trace_value"
    

# This label is required for renpy.call_in_new_context(),
# because renpy.invoke_in_new_context() has no support for renpy.jump_out_of_context() for jumps.
label _debug_console:
    
    python in _debug_console:
        if debug_console is None:
            debug_console = DebugConsole()
    
    while True:
        python in _debug_console:
            debug_console.interact()

label _debug_console_return:
    return
