# console.rpy
# Ren'Py debug console
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
python early:
    # Create configuration variables.
    locked = config.locked
    config.locked = False
    config.debug_console_layer = 'debug_console'
    config.debug_console_history_size = 100
    config.debug_console_keybind = 'shift_K_BACKQUOTE'
    config.debug_console_custom_commands = { }
    config.locked = locked
    
    # Create default styles. See above for documentation.
    style.create('debug_console', 'frame')
    style.debug_console.background = "#00000000"
    style.debug_console.xpos = 0
    style.debug_console.ypos = 0
    style.debug_console.xpadding = 0
    style.debug_console.ypadding = 0
    
    style.create('debug_console_input', 'frame')
    style.debug_console_input.background = "#00000040"
    style.debug_console_input.xpos = 0
    style.debug_console_input.ypos = 0
    style.debug_console_input.xpadding = 0
    style.debug_console_input.ypadding = 0
    style.debug_console_input.xfill = True
    
    style.create('debug_console_prompt', 'text')
    style.debug_console_prompt.color = "#ffffff"
    style.debug_console_prompt.xpos = 50
    
    style.create('debug_console_input_text', 'input')
    style.debug_console_input_text.color = "#fafafa"
    style.debug_console_input_text.xpos = 50
    
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
    style.debug_console_command_text.xpos = 60
    
    style.create('debug_console_result', 'frame')
    style.debug_console_result.background = "#00000000"
    
    style.create('debug_console_result_text', 'text')
    style.debug_console_result_text.color = "#ffffff"
    style.debug_console_result_text.xpos = 80
    
    style.create('debug_console_error_text', 'text')
    style.debug_console_error_text.color = "#ff0000"
    style.debug_console_error_text.xpos = 80
    
    style.create('debug_console_trace', 'frame')
    style.debug_console_trace.background = "#00000040"
    style.debug_console_trace.xalign = 1.0
    style.debug_console_trace.top_margin = 10
    style.debug_console_trace.right_margin = 20
    
    style.create('debug_console_trace_var', 'text')
    style.debug_console_trace_var.bold = True
    
    style.create('debug_console_trace_value', 'text')

init 3735929054 python:
    import sys
    
    # Simple circular buffer to hold the command history;
    # will automatically delete older commands once the limit has reached.
    class RingBuffer:
        def __init__(self, size, default_value=None):
            self.size = size
            self.default_value = default_value
            self.data = [ self.default_value for i in xrange(size)]

        def push(self, value):
            self.data.pop(0)
            self.data.append(value)
        
        def pop(self):
            self.data.append(self.default_value)
            return self.data.pop(0)

        def get(self, i):
            return self.data[i]
        
        def put(self, i, value):
            self.data[i] = value
        
    class DebugConsole:
        def __init__(self, layer='debug_console', history_size=100):
            self.enabled = False
            self.layer = layer
            
            self.history_size = history_size
            self.history = RingBuffer(self.history_size, default_value=(None, None, None))
            
            self.custom_commands = {}
            self.traced_expressions = []
            
            self.parent_context = None
            self.parent_node = None
            self.tail_node = None
            self.script_reentry_point = None
            
            self.help_message = (""
                "Ren\'Py debug console\n"
                " by Shiz, C and delta.\n"
                "commands:\n"
                " <any Ren'Py command>  - execute Ren'Py command as if it were placed in a script file.\n"
                " $ <pycode>            - execute Python command.\n"
                " clear                 - clear the command history.\n"
                " crash                 - crash the game with an appropriate error message.\n"
                " reload                - reload the game.\n"
                " trace <expression>    - trace variable or expression in overlay.\n"
                " untrace <expression>  - stop tracing variable or expression.\n"
                " untraceall            - stop tracing any variable or expression.\n"
                " help                  - show this message.\n"
                " exit/quit/~           - close the console.")
        
        def enable(self):
            if not self.enabled:
                self.enabled = True
                renpy.call_in_new_context('debug_console_trampoline')
        
        def disable(self):
            if self.enabled:
                ui.layer(self.layer)
                ui.clear()
                ui.close()
                self.enabled = False
        
        def draw(self, input_lines = [], current_depth = 0):
            # Clear out any existing content and draw the base frame.
            ui.layer(self.layer)
            ui.clear()
            ui.frame(style='debug_console')
            ui.vbox()
        
            # Draw current command input.
            self.draw_input(input_lines, current_depth)
            # Draw command history.
            self.draw_history()
            
            # Close console vbox and frame, and the console layer.
            ui.close()
            ui.close()
        
        def draw_input(self, input_lines = [], current_depth = 0):
            # Draw the input frame.
            ui.frame(style='debug_console_input')
            ui.vbox()
            
            # Draw prompt.
            ui.hbox()
            ui.text('> ', id='debug_console_prompt_0', style='debug_console_prompt')
            
            # Draw any previous input lines.
            line_count = 0
            for line, depth in input_lines:
                # Draw input line content and close its hbox.
                ui.text(line, id='debug_console_line_' + str(line_count), style='debug_console_input_text')
                ui.close()
                
                # Figure out next line depth and print its appropriate prompt.
                line_count += 1
                if len(input_lines) > line_count:
                    next_line, next_depth = input_lines[line_count]
                else:
                    next_depth = current_depth
                ui.hbox()
                ui.text('    ' + '....' * next_depth + ' ', id='debug_console_prompt_' + str(line_count), style='debug_console_prompt')
            
            # Draw input widget and close its hbox. Add a keymap to allow the same button that opened the console to instantly close it, 
            # along with trapping the escape key, and disabling the right mouse click.
            ui.input('', id='debug_console_input', style='debug_console_input_text')
            ui.keymap(**{ config.debug_console_keybind: lambda: 'quit' })
            ui.keymap(K_ESCAPE=lambda: 'quit')
            ui.keymap(mouseup_3=None)
            ui.close()
            
            # Close input vbox and frame.
            ui.close()
        
        def draw_history(self):
            # Draw command history, in reverse order.
            commands = range(self.history_size)
            commands.reverse()
            
            # Draw the history frame, and make it scrollable.
            ui.frame(style='debug_console_history')
            ui.viewport(mousewheel=True)
            
            ui.vbox(xpos=0, xfill=True)
            for i in commands:
                command, result, is_error = self.history.get(i)
                if command is None:
                    continue
                
                # Draw command if not none, and draw result if applicable.
                ui.frame(style='debug_console_history_item')
                ui.vbox(xpadding=0, ypadding=0)
                
                ui.frame(xfill=True, style='debug_console_command')
                ui.text(self.sanitize(command), id='debug_console_command_' + str(i), style='debug_console_command_text')
                
                if result is not None:
                    ui.frame(xfill=True, style='debug_console_result')
                    if is_error:
                        ui.text(self.sanitize(result), id='debug_console_response_' + str(i), style='debug_console_error_text')
                    else:
                        ui.text(self.sanitize(result), id='debug_console_response_' + str(i), style='debug_console_result_text')
                    
                
                # Close command vbox.
                ui.close()
            # Close history frame.
            ui.close()

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
        
        def interact(self, **kwargs):
            # Trick Ren'Py into thinking this context is rollback-able.
            renpy.game.context().rollback = True
            # Set script re-entry points and node list 'tail' for AST injection.
            self.parent_context = renpy.game.context(-2)
            self.parent_node = renpy.game.script.lookup(self.parent_context.current)
            self.tail_node = self.parent_node
            self.script_reentry_point = self.parent_node.next
            
            # Enter read-eval-print loop.
            while self.enabled:
                command = self.take_command()
                
                # 'quit', 'exit', an empty string or '~' exit the console interaction.
                if command == 'quit' or command == 'exit' or command == '~' or command == '':
                    self.disable()
                    return
                # 'clear' clears the command history and thus the screen.
                elif command == 'clear':
                    for _ in range(self.history_size):
                        self.history.push((None, None, None))
                else:
                    (result, is_error) = self.execute(command, command.startswith('init'))
                    self.history.push((command, result, is_error))
                    
                # Allow the UI to adapt to its consequences.
                renpy.restart_interaction()
         
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
    
    if config.developer:
        # Add the console layer.
        if not config.debug_console_layer in config.top_layers:
            config.top_layers.append(config.debug_console_layer)
        
        debug_console = DebugConsole(layer=config.debug_console_layer, history_size=config.debug_console_history_size)
        debug_console.custom_commands.update(config.debug_console_custom_commands)
        
        # Create proper debug overlay.
        def debug_overlay():
            ui.keymap(**{ config.debug_console_keybind: debug_console.enable })
            
            if len(debug_console.traced_expressions) > 0:
                ui.frame(style='debug_console_trace')
                ui.vbox()
                for expression in debug_console.traced_expressions:
                    ui.hbox()
                    ui.text(debug_console.sanitize(expression) + ": ", style='debug_console_trace_var')
                    ui.text(debug_console.sanitize(debug_console.execute_python(expression)), style='debug_console_trace_value')
                    ui.close()
                ui.close()
        
        config.overlay_functions.append(debug_overlay)

# This label is required for renpy.call_in_new_context(),
# because renpy.invoke_in_new_context() has no support for renpy.jump_out_of_context() for jumps.
label debug_console_trampoline:
    $ debug_console.interact()

