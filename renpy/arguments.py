# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file handles argument parsing. Argument parsing takes place in
# two phases. In the first phase, we only parse the arguments that are
# necessary to load the game, and run the init phase. The init phase
# can register commands and arguments. These arguments are parsed at
# the end of the init phase, before the game begins running, and can
# decide if the game runs or some other action occurs.

from __future__ import print_function

import argparse
import renpy

try:
    import site
    site._renpy_argv_emulation()  # @UndefinedVariable
except:
    pass


# A map from command name to a (function, flag) tuple. The flag is true if the
# function will parse command line arguments, and false otherwise.
commands = { }

# Commands that force compile to be set.
compile_commands = { "compile", "add_from", "merge_strings" }


class ArgumentParser(argparse.ArgumentParser):
    """
    Creates an argument parser that is capable of parsing the standard Ren'Py
    arguments, as well as arguments that are specific to a sub-command.
    """

    def __init__(self, second_pass=True, description=None, require_command=True):
        """
        Creates an argument parser.

        `second_pass`
            True if this is the second pass through argument parsing. (The pass
            that parses sub-commands.)

        `description`
            If supplied, this will be used as a description of the subcommand
            to run.
        """

        self.group = self

        argparse.ArgumentParser.__init__(self, description="The Ren'Py visual novel engine.", add_help=False)

        command_names = ", ".join(sorted(commands))

        if require_command:

            self.add_argument(
                "basedir",
                help="The base directory containing of the project to run. This defaults to the directory containing the Ren'Py executable.")

            self.add_argument(
                "command",
                help="The command to execute. Available commands are: " + command_names + ". Defaults to 'run'.")

        else:

            self.add_argument(
                "basedir",
                default='',
                nargs='?',
                help="The base directory containing of the project to run. This defaults to the directory containing the Ren'Py executable.")

            self.add_argument(
                "command",
                help="The command to execute. Available commands are: " + command_names + ". Defaults to 'run'.",
                nargs='?',
                default="run")

        self.add_argument(
            "--savedir", dest='savedir', default=None, metavar="DIRECTORY",
            help="The directory where saves and persistent data are placed.")

        self.add_argument(
            '--trace', dest='trace', action='store', default=0, type=int, metavar="LEVEL",
            help="The level of trace Ren'Py will log to trace.txt. (1=per-call, 2=per-line)")

        self.add_argument(
            "--version", action='version', version=renpy.version,
            help="Displays the version of Ren'Py in use.")

        self.add_argument(
            "--compile", action='store_true', dest='compile',
            help='Forces all .rpy scripts to be recompiled before proceeding.')

        self.add_argument(
            "--keep-orphan-rpyc", action="store_true",
            help="Prevents the compile command from deleting orphan rpyc files.")

        self.add_argument(
            "--lint", action="store_true", dest="lint",
            help=argparse.SUPPRESS)

        dump = self.add_argument_group("JSON dump arguments", description="Ren'Py can dump information about the game to a JSON file. These options let you select the file, and choose what is dumped.")
        dump.add_argument("--json-dump", action="store", metavar="FILE", help="The name of the JSON file.")
        dump.add_argument("--json-dump-private", action="store_true", default=False, help="Include private names. (Names beginning with _.)")
        dump.add_argument("--json-dump-common", action="store_true", default=False, help="Include names defined in the common directory.")

        if second_pass:
            self.add_argument("-h", "--help", action="help", help="Displays this help message, then exits.")

            command = renpy.game.args.command  # @UndefinedVariable
            self.group = self.add_argument_group("{0} command arguments".format(command), description)

    def add_argument(self, *args, **kwargs):
        if self.group is self:
            argparse.ArgumentParser.add_argument(self, *args, **kwargs)
        else:
            self.group.add_argument(*args, **kwargs)

    def parse_args(self, *args, **kwargs):
        rv = argparse.ArgumentParser.parse_args(self, *args, **kwargs)

        if rv.command in compile_commands:
            rv.compile = True

        if renpy.session.get("compile", False):
            rv.compile = True

        return rv

    def parse_known_args(self, *args, **kwargs):
        args, rest = argparse.ArgumentParser.parse_known_args(self, *args, **kwargs)

        if args.command in compile_commands:
            args.compile = True

        if renpy.session.get("compile", False):
            args.compile = True

        return args, rest


def run():
    """
    The default command, that (when called) leads to normal game startup.
    """

    ap = ArgumentParser(description="Runs the current project normally.", require_command=False)

    ap.add_argument(
        '--profile-display', dest='profile_display', action='store_true', default=False,
        help="If present, Ren'Py will report the amount of time it takes to draw the screen.")

    ap.add_argument(
        '--debug-image-cache', dest='debug_image_cache', action='store_true', default=False,
        help="If present, Ren'Py will log information regarding the contents of the image cache.")

    ap.add_argument(
        '--warp', dest='warp', default=None,
        help='This takes as an argument a filename:linenumber pair, and tries to warp to the statement before that line number.')

    args = renpy.game.args = ap.parse_args()

    if args.warp:
        renpy.warp.warp_spec = args.warp

    if args.profile_display:  # @UndefinedVariable
        renpy.config.profile = True

    if args.debug_image_cache:
        renpy.config.debug_image_cache = True

    return True


def compile():  # @ReservedAssignment
    """
    This command forces the game script to be recompiled.
    """

    takes_no_arguments("Recompiles the game script.")

    return False


def quit():  # @ReservedAssignment
    """
    This command is used to quit without doing anything.
    """

    takes_no_arguments("Recompiles the game script.")

    return False


def rmpersistent():
    """
    This command is used to delete the persistent data.
    """

    takes_no_arguments("Deletes the persistent data.")

    renpy.loadsave.location.unlink_persistent()
    renpy.persistent.should_save_persistent = False

    return False


def register_command(name, function):
    """
    Registers a command that can be invoked when Ren'Py is run on the command
    line. When the command is run, `function` is called with no arguments.

    If `function` needs to take additional command-line arguments, it should
    instantiate a renpy.arguments.ArgumentParser(), and then call parse_args
    on it. Otherwise, it should call renpy.arguments.takes_no_arguments().

    If `function` returns true, Ren'Py startup proceeds normally. Otherwise,
    Ren'Py will terminate when function() returns.
    """

    commands[name] = function


def bootstrap():
    """
    Called during bootstrap to perform an initial parse of the arguments, ignoring
    unknown arguments. Returns the parsed arguments, and a list of unknown arguments.
    """

    global rest

    ap = ArgumentParser(False, require_command=False)
    args, _rest = ap.parse_known_args()

    return args


def pre_init():
    """
    Called before init, to set up argument parsing.
    """

    global subparsers

    register_command("run", run)
    register_command("lint", renpy.lint.lint)
    register_command("compile", compile)
    register_command("rmpersistent", rmpersistent)
    register_command("quit", quit)


def post_init():
    """
    Called after init, but before the game starts. This parses a command
    and its arguments. It then runs the command function, and returns True
    if execution should continue and False otherwise.
    """

    command = renpy.game.args.command  # @UndefinedVariable

    if command == "run" and renpy.game.args.lint:  # @UndefinedVariable
        command = "lint"

    if command not in commands:
        ArgumentParser().error("Command {0} is unknown.".format(command))

    return commands[command]()


def takes_no_arguments(description=None):
    """
    Used to report that a command takes no arguments.
    """

    ArgumentParser(description=description).parse_args()
