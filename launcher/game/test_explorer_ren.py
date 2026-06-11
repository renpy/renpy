import sys
import renpy

"""renpy
default persistent.test_sorter = "order"

init python:
"""
from typing import Any, TypedDict
from dataclasses import dataclass
import json
import os
import subprocess
import re
import time

TESTING_POLL_INTERVAL = 1.0
TESTING_STALL_TIMEOUT = 5.0
test_roots = []

class ParameterizedItem(TypedDict):
    index: int
    display_name: str

class DumpItem(TypedDict):
    full_path: str
    name: str
    kind: str
    file: str
    line: int
    parent_full_path: str | None
    parameterized: list[ParameterizedItem]
    description: str

class TestNode:
    def __init__(self, raw_data: DumpItem, execution_order: int) -> None:
        self.execution_order = execution_order
        self.full_path = raw_data.get("full_path", "")
        self.name = raw_data.get("name", self.full_path)
        self.kind = raw_data.get("kind", "")
        self.file = raw_data.get("file", "")
        self.line = raw_data.get("line", 0)
        self.parent_full_path = raw_data.get("parent_full_path", None)
        self.description = raw_data.get("description", "")
        self.parameterized = raw_data.get("parameterized", [])

        # Sub-properties for hierarchy and display
        self.children: list[TestNode] = []
        self.parent: TestNode | None = None
        self.display_path = self.full_path

        # To handle parameterized variations
        self.is_param_group = False
        self.param_index = None

@dataclass(kw_only=True)
class TestResult:
    status: str = "not_run"
    duration_seconds: float | None = None
    error: str | None = None
    traceback: str | None = None

@dataclass(kw_only=True)
class BaseEvent:
    event: str
    sequence: int
    timestamp: float
    run_id: str | None = None

@dataclass(kw_only=True)
class OnRunStartEvent(BaseEvent):
    event: str = "on_run_start"

@dataclass(kw_only=True)
class OnTestInfoEvent(BaseEvent):
    event: str = "on_test_info"
    test_id: str
    name: str
    kind: str
    file: str
    line: int
    parent_test_id: str | None = None

@dataclass(kw_only=True)
class OnTestStartEvent(BaseEvent):
    event: str = "on_test_start"
    test_id: str

@dataclass(kw_only=True)
class OnTestEndEvent(BaseEvent):
    event: str = "on_test_end"
    test_id: str
    status: str
    duration_seconds: float | None = None
    error: str | None = None
    traceback: str | None = None

@dataclass(kw_only=True)
class OnHeartbeatEvent(BaseEvent):
    event: str = "on_heartbeat"

@dataclass(kw_only=True)
class OnRunEndEvent(BaseEvent):
    event: str = "on_run_end"
    final_status: str
    total: int
    passed: int
    xfailed: int
    failed: int
    xpassed: int
    skipped: int
    not_run: int


class EventDecoder(json.JSONDecoder):
    def decode(self, s: str) -> BaseEvent:
        obj: dict[str, Any] = super().decode(s)

        event_type = obj.get("event")
        if event_type == "on_run_start":
            return OnRunStartEvent(**obj)
        elif event_type == "on_test_info":
            return OnTestInfoEvent(**obj)
        elif event_type == "on_test_start":
            return OnTestStartEvent(**obj)
        elif event_type == "on_test_end":
            return OnTestEndEvent(**obj)
        elif event_type == "on_heartbeat":
            return OnHeartbeatEvent(**obj)
        elif event_type == "on_run_end":
            return OnRunEndEvent(**{
                "sequence": obj.get("sequence", 0),
                "timestamp": obj.get("timestamp", 0.0),
                "final_status": obj.get("final_status", ""),
                **obj.get("summary", {}).get("testcases", {}),
                })
        raise ValueError(f"Unknown event type: {event_type}")

class TestRunner:
    """
    Smart polling loop that reads the JSONL file using append-only delta reads.

    Algorithm:
      1. stat() the file; skip read if size unchanged.
      2. Read only the appended bytes from the last offset.
      3. Split on newlines; hold trailing partial line in buffer.
      4. Parse each complete line and fire onEvent / onInfrastructureError.
      5. While process is alive, check stall timeout.
      6. After notifyProcessExited(), fire infrastructure error if on_end was not received.
    """
    def __init__(self) -> None:
        self.process = None
        self.results: dict[str, TestResult] = {}
        self.last_event_time: float = 0.0
        self.run_file = ""
        self.last_offset = 0
        self.last_stat_size = 0
        self.carry = b""
        self.param_group_children: dict[str, list[str]] = {}
        self.child_to_group: dict[str, str] = {}

        self.test_started: bool = False
        self.process_exited: bool = False
        self.process_exited_time: float = 0.0
        self.disposed: bool = False

        self.num_total: int = 0
        self.num_passed: int = 0
        self.num_failed: int = 0

    def launch(self, node: TestNode) -> None:
        # Cleanup previous
        if self.process:
            self.stop()

        self.last_event_time: float = 0.0
        self.last_offset = 0
        self.last_stat_size = 0
        self.carry = b""
        self.param_group_children.clear()
        self.child_to_group.clear()
        self.last_event_time = 0.0

        self.test_started = False
        self.process_exited = False
        self.process_exited_time = 0.0
        self.disposed = False

        self.num_passed = 0
        self.num_failed = 0

        def build_param_maps(n: TestNode) -> None:
            if n.is_param_group:
                child_paths = [c.full_path for c in n.children]
                self.param_group_children[n.full_path] = child_paths
                for cp in child_paths:
                    self.child_to_group[cp] = n.full_path
            for c in n.children:
                build_param_maps(c)

        build_param_maps(node)
        project.current.make_tmp()
        self.run_file = os.path.join(project.current.tmp, "test_results.jsonl")

        # Ensure folder exists
        os.makedirs(os.path.dirname(self.run_file), exist_ok=True)

        if os.path.exists(self.run_file):
            os.remove(self.run_file)

        target = node.display_path

        # Mirror project.launch() executable resolution so we respect pythonw preference
        executable_path = os.path.dirname(renpy.exports.fsdecode(sys.executable))
        ext = ".exe" if (renpy.windows or os.name == "nt") else ""
        executables = [os.path.join(executable_path, "python" + ext)]
        executables.append(sys.executable)
        py_exe = sys.executable
        for candidate in executables:
            if os.path.exists(candidate):
                py_exe = candidate
                break

        cmd = [
            py_exe,
            sys.argv[0],
            project.current.path,
            "test",
            target,
            "--reporter",
            "jsonl",
            "--jsonl-output",
            self.run_file,
            "--jsonl-flush-interval-ms",
            f"{TESTING_POLL_INTERVAL * 1000:.0f}",
        ]

        # Mark node and children as pending
        def mark_pending(n: TestNode) -> None:
            self.results[n.full_path] = TestResult(status="pending")
            for c in n.children:
                mark_pending(c)

        mark_pending(node)

        try:
            self.process = subprocess.Popen(cmd)
        except Exception as e:
            self.results[node.full_path] = TestResult(status="failed", error=str(e))

    def stop(self) -> None:
        self.disposed = True
        if self.process:
            self.process.terminate()
            self.process = None

        # Mark any pending as skipped
        for test_id, res in self.results.items():
            if res.status in ("pending", "running"):
                self.results[test_id].status = "skipped"

    def poll(self) -> None:
        if self.disposed:
            return

        if self.process is None or (self.process.poll() is not None and not self.process_exited):
            self.process_exited = True
            self.process_exited_time = time.time()

        poll_start_time = time.time()

        # Read any new data from the run file and update results
        if os.path.exists(self.run_file):
            stat = os.stat(self.run_file)
            if stat.st_size > self.last_stat_size:
                self.last_stat_size = stat.st_size

                with open(self.run_file, "rb") as f:
                    f.seek(self.last_offset)
                    data = f.read(stat.st_size - self.last_offset)
                    self.update_results(data)

        # Detect stalled run, and mark pending as failed if we haven't seen any events for a while
        if (
            self.test_started
            and not self.process_exited
            and time.time() - self.last_event_time > TESTING_STALL_TIMEOUT
        ):
            for test_id, res in self.results.items():
                if res.status in ("pending", "running"):
                    self.results[test_id].status = "failed"
                    self.results[test_id].error = (
                        f"Test run stalled: no events received for {time.time() - self.last_event_time:.1f} seconds. "
                        f"(timeout: {TESTING_STALL_TIMEOUT} seconds)"
                    )
            self.stop()
            return

        # Grace window: after process exits, poll one last time for buffered events
        if self.process_exited:
            if poll_start_time > self.process_exited_time:
                self.stop()
                return

    def update_results(self, data: bytes) -> None:
        "Look for complete lines of JSON, and update results based on them."

        self.last_offset += len(data)
        self.carry += data

        lines = self.carry.decode("utf-8", "replace").split("\n")
        self.carry = lines.pop().encode("utf-8")  # Keep trailing partial line

        if len(lines) > 0:
            self.test_started = True

        for line in lines:
            line = line.strip()
            if not line:
                continue

            event: BaseEvent = json.loads(line, cls=EventDecoder)
            self.last_event_time = event.timestamp

            if isinstance(event, OnTestStartEvent):
                if event.test_id not in self.results:
                    self.results[event.test_id] = TestResult(status="running")
                else:
                    self.results[event.test_id].status = "running"

                if event.test_id in self.child_to_group:
                    group_path = self.child_to_group[event.test_id]
                    if group_path in self.results:
                        self.results[group_path].status = "running"
                    else:
                        self.results[group_path] = TestResult(status="running")

            elif isinstance(event, OnTestEndEvent):
                if event.test_id not in self.results:
                    continue

                status = event.status
                if status == "xfailed":
                    self.results[event.test_id].status = "passed"

                elif status in ("failed", "xpassed"):
                    self.results[event.test_id].status = "failed"
                    self.results[event.test_id].error = event.error
                    self.results[event.test_id].traceback = event.traceback
                else:
                    self.results[event.test_id].status = status

                if event.duration_seconds is not None:
                    self.results[event.test_id].duration_seconds = event.duration_seconds

                # Calculate aggregate status for parent groups, if applicable
                if event.test_id in self.child_to_group:
                    group_path = self.child_to_group[event.test_id]
                    child_paths = self.param_group_children[group_path]
                    child_statuses = [
                        self.results[cp].status
                        for cp in child_paths
                        if cp in self.results
                    ]
                    terminal = ("passed", "failed", "skipped")
                    if (
                        len(child_statuses) == len(child_paths)
                        and all(s in terminal for s in child_statuses)
                    ):
                        if any(s == "failed" for s in child_statuses):
                            agg = "failed"
                        elif all(s == "passed" for s in child_statuses):
                            agg = "passed"
                        else:
                            agg = "skipped"
                        if group_path in self.results:
                            self.results[group_path].status = agg
                        else:
                            self.results[group_path] = TestResult(status=agg)

                if persistent.test_sorter in ("status", "duration"):
                    sort_test_nodes(test_roots)

            elif isinstance(event, OnRunEndEvent):
                self.num_passed = event.passed + event.xfailed
                self.num_failed = event.failed + event.xpassed
                self.num_total = self.num_passed + self.num_failed
                self.stop()
                return


class RunAction(renpy.ui.Action):
    def __init__(self, runner: TestRunner, node: TestNode) -> None:
        self.runner = runner
        self.node = node

    def __call__(self) -> None:
        self.runner.launch(self.node)
        renpy.exports.restart_interaction()

    def get_sensitive(self) -> bool:
        return self.runner.process is None


class StopAction(renpy.ui.Action):
    def __init__(self, runner: TestRunner) -> None:
        self.runner = runner

    def __call__(self) -> None:
        self.runner.stop()
        renpy.exports.restart_interaction()


class ShowErrorInfo(renpy.ui.Action):
    def __init__(self, node_id: str, runner: TestRunner) -> None:
        self.node_id = node_id
        self.runner = runner

    def __call__(self) -> None:
        res = self.runner.results.get(self.node_id, None)
        if res is None:
            return

        error_message = []
        if res.traceback:
            error_message.append(self.format_traceback(res.traceback))
        if res.error:
            error_message.append(res.error)

        renpy.exports.show_screen(
            "tests_error_modal",
            full_path=self.node_id,
            error_text="\n\n".join(error_message)
        )
        renpy.exports.restart_interaction()

    def format_traceback(self, error: str) -> str:
        """
        Format tracebacks to look and function like Ren'Py tracebacks,
        with clickable file/line references and colorized carets.

        Influenced by the _ExceptionPrintContext class
        """
        # Look for lines that look like Python tracebacks, and turn them into clickable links.
        location_pattern = re.compile(r'File "(.+)", line (\d+), in (.+)')
        caret_pattern = re.compile(r"^( *)(~*)(\^*)(~*)$")

        lines = []
        for line in error.splitlines():
            if match := location_pattern.match(line.strip()):
                filename, lineno, name = match.groups()

                lines.append(f'{{a=edit:{lineno}:{filename}}}File "{filename}", line {lineno}{{/a}}, in {name}')
            elif match := caret_pattern.match(line):
                spaces, tildes, carets, tildes2 = match.groups()
                prev_line = lines[-1] if lines else ""
                updated_line = ""

                offset = 0
                if spaces:
                    text = prev_line[offset : offset + len(spaces)]
                    updated_line += text
                    offset += len(spaces)
                if tildes:
                    text = prev_line[offset : offset + len(tildes)]
                    updated_line += f"{{color={_ExceptionPrintContext.RED}}}{text}{{/color}}"
                    offset += len(tildes)
                if carets:
                    text = prev_line[offset : offset + len(carets)]
                    updated_line += f"{{color={_ExceptionPrintContext.BRIGHT_RED}}}{text}{{/color}}"
                    offset += len(carets)
                if tildes2:
                    text = prev_line[offset : offset + len(tildes2)]
                    updated_line += f"{{color={_ExceptionPrintContext.RED}}}{text}{{/color}}"

                if lines:
                    lines[-1] = updated_line
                else:
                    lines.append(updated_line)
            else:
                lines.append(line)
        return "\n".join(lines)


class PollAction(renpy.ui.Action):
    def __init__(self, runner: TestRunner) -> None:
        self.runner = runner

    def __call__(self) -> None:
        if self.runner.process is not None:
            self.runner.poll()
            renpy.exports.restart_interaction()


def build_test_tree(raw_items: list[DumpItem]) -> list[TestNode]:
    # Maps an item's original full_path to a list of placement contexts.
    # Each context is a tuple of (children_list, parent_full_path, parent_display_path)
    # that a child node should be inserted into.
    #
    # When a node is parameterized, it produces one context per parameter instance.
    # Every child item is duplicated once per parent instance.
    placement_contexts_by_item_path: dict[str, list[tuple[list[TestNode], str, str]]] = {}
    root_nodes: list[TestNode] = []
    execution_order: int = 0

    for item_data in raw_items:
        item_path = item_data.get("full_path", item_data.get("id", ""))
        parent_path = item_data.get("parent_full_path", None)
        item_name = item_data.get("name", item_path)
        param_sets: list[ParameterizedItem] = item_data.get("parameterized", [])
        param_count: int = len(param_sets)

        # Resolve where to insert this item's node(s).
        # Root items go directly into root_nodes; children are inserted under
        # each instantiated copy of their parent.
        if parent_path is None:
            parent_placement_contexts = [(root_nodes, "", "")]
        else:
            parent_placement_contexts = placement_contexts_by_item_path.get(parent_path) or [(root_nodes, "", "")]

        # The portion of this item's path that comes after its parent's path (e.g. ".foo")
        if parent_path is not None:
            path_fragment = item_path[len(parent_path):]
        else:
            path_fragment = item_path

        # Placement contexts for this item's children, populated below.
        child_placement_contexts = []

        for siblings_list, parent_full_path, parent_display_path in parent_placement_contexts:
            full_path = parent_full_path + path_fragment

            if param_count <= 1:
                # Non-parameterized (or single-instance): one node per parent context.
                node = TestNode(item_data, execution_order)
                execution_order += 1
                node.full_path = full_path
                node.display_path = parent_display_path + path_fragment
                if param_count == 1 and "display_name" in param_sets[0]:
                    node.name = param_sets[0]["display_name"]
                siblings_list.append(node)
                child_placement_contexts.append((node.children, full_path, node.display_path))
            else:
                # Multi-param: create a group node that owns one child node per parameter set.
                param_group_node = TestNode(item_data, execution_order)
                execution_order += 1
                param_group_node.full_path = full_path
                param_group_node.is_param_group = True
                siblings_list.append(param_group_node)

                for param_data in param_sets:
                    param_display_name = param_data.get("display_name", item_name)
                    param_instance_node = TestNode(item_data, execution_order)
                    execution_order += 1
                    param_instance_node.name = param_display_name
                    param_instance_node.parameterized = []
                    param_instance_display_path = f"{parent_display_path}.{param_display_name}"
                    param_instance_node.full_path = param_instance_display_path
                    param_instance_node.display_path = param_instance_display_path
                    param_instance_node.parent = param_group_node
                    param_group_node.children.append(param_instance_node)
                    # Children of this param instance inherit its paths.
                    child_placement_contexts.append(
                        (
                            param_instance_node.children,
                            param_instance_display_path,
                            param_instance_display_path
                        ))

        placement_contexts_by_item_path[item_path] = child_placement_contexts

    # Finally, sort each level alphabetically by name.
    for root_node in root_nodes:
        sort_test_nodes(root_node.children)

    return root_nodes

def _sort_key_duration(n: TestNode) -> float:
    res = test_runner.results.get(n.full_path, None)
    if res and res.duration_seconds is not None:
        return -res.duration_seconds
    else:
        return -float("inf")

def _sort_key_name(n: TestNode) -> str:
    return n.name.lower()

def _sort_key_order(n: TestNode) -> int:
    return n.execution_order

def _sort_key_status(n: TestNode) -> tuple[int, int, str]:
    res = test_runner.results.get(n.full_path, TestResult())
    status_order = {
        "running": 0,
        "pending": 1,
        "failed": 2,
        "passed": 3,
        "skipped": 4,
        "not_run": 5,
    }
    return (
        status_order.get(res.status, 99),
        n.execution_order,
        n.name.lower(),
    )

def sort_test_nodes(nodes: list[TestNode], key=None) -> None:
    if key is None:
        if "duration" in persistent.test_sorter:
            key = _sort_key_duration
        elif "name" in persistent.test_sorter:
            key = _sort_key_name
        elif "status" in persistent.test_sorter:
            key = _sort_key_status
        else:
            key = _sort_key_order

    nodes.sort(key=key)
    for node in nodes:
        sort_test_nodes(node.children, key=key)


def flatten_tree(
        nodes: list[TestNode],
        expanded_items: set[str],
        level: int = 0
    ) -> list[tuple[int, TestNode]]:

    result = []
    for node in nodes:
        result.append((level, node))
        if node.full_path in expanded_items and node.children:
            result.extend(flatten_tree(node.children, expanded_items, level + 1))
    return result


def refresh_tests(generate: bool = True) -> None:
    global test_roots
    if generate:
        project.current.update_dump(force=True)

    items = project.current.dump.get("test", {}).get("items", [])
    test_roots = build_test_tree(items)

test_runner = TestRunner()

"""renpy
screen test_explorer():
    default expanded_items = set(("global",))
    default hovered_item = None

    timer TESTING_POLL_INTERVAL repeat True action PollAction(test_runner)

    frame:
        style_group "l"
        style "l_root"
        alt "Test Explorer"

        window:
            has vbox

            label _("Test Explorer")

            add HALF_SPACER

            hbox:
                xfill True

                hbox:
                    xpos 20
                    spacing 20
                    textbutton _("Refresh") action Function(renpy.invoke_in_new_context, refresh_tests)
                    textbutton _("Run All") action If(test_roots, RunAction(test_runner, test_roots[0]))
                    if test_runner.process is not None:
                        textbutton _("Stop") action StopAction(test_runner)

                hbox:
                    xalign 1.0
                    spacing 20
                    button:
                        hbox:
                            text _("Sort by: ")
                            if "duration" in persistent.test_sorter:
                                text _("Duration")
                            elif "name" in persistent.test_sorter:
                                text _("Name")
                            elif "status" in persistent.test_sorter:
                                text _("Status")
                            else:
                                text _("Execution Order")
                        action CaptureFocus("sort_dropdown")


            add SEPARATOR2
            add HALF_SPACER

            viewport:
                mousewheel True
                scrollbars "vertical"

                has vbox

                hbox:
                    spacing 2
                    null width 5
                    if test_runner.num_failed > 0:
                        add TESTING_FAIL
                    elif test_runner.num_passed > 0:
                        add TESTING_PASS
                    else:
                        null width 16
                    text f"{test_runner.num_passed}/{test_runner.num_total}" size 14

                for level, node in flatten_tree(test_roots, expanded_items):
                    button:
                        background None
                        action If(node.children, ToggleSetMembership(expanded_items, node.full_path), NullAction())
                        hovered SetScreenVariable("hovered_item", node)
                        # unhovered SetScreenVariable("hovered_item", None)
                        xfill True

                        has hbox
                        spacing 2
                        xoffset level * 20

                        # Calculate status and icon
                        $ res = test_runner.results.get(node.full_path, TestResult())

                        frame:
                            background None
                            xsize 16
                            ysize 16
                            align (0.5, 0.5)
                            if node.children:
                                add Transform(
                                    TESTING_TRIANGLE,
                                    rotate=90 if node.full_path in expanded_items else 0,
                                    align=(0.5, 0.5)
                                )

                        frame:
                            background None
                            xsize 16
                            ysize 16
                            align (0.5, 0.5)
                            if res.status == "pending":
                                add TESTING_PENDING align (0.5, 0.5) rotate 0
                            elif res.status == "running":
                                add TESTING_RUNNING align (0.5, 0.5):
                                    at transform:
                                        rotate 0 subpixel True
                                        linear 1.0 rotate 360
                                        repeat
                            elif res.status == "passed":
                                add TESTING_PASS align (0.5, 0.5) rotate 0
                            elif res.status == "failed":
                                add TESTING_FAIL align (0.5, 0.5) rotate 0
                            elif res.status == "skipped":
                                add TESTING_SKIP align (0.5, 0.5) rotate 0
                            else:
                                add TESTING_NOTRUN align (0.5, 0.5) rotate 0

                        text node.name

                        null width 10
                        frame:
                            background None
                            xsize 40
                            ysize 16
                            align (0.5, 0.5)
                            if res.duration_seconds is not None:
                                text f"{res.duration_seconds:,.3f}s" size 12 color "#888888" align (0.5, 0.5)

                        # Controls
                        # add HALF_SPACER
                        if hovered_item == node:
                            null width 10
                            hbox:
                                spacing 5
                                if test_runner.process is None:
                                    textbutton _("Run") action RunAction(test_runner, hovered_item) text_size 14 text_color "#44aaff"
                                else:
                                    textbutton _("Stop") action StopAction(test_runner) text_size 14 text_color "#ff4444"

                                textbutton _("Edit") action editor.Edit(hovered_item.file, hovered_item.line) text_size 14 text_color "#44aa44"

                                if res.status == "failed" and (res.error or res.traceback):
                                    add HALF_SPACER
                                    textbutton _("Info"):
                                        action ShowErrorInfo(hovered_item.full_path, test_runner)
                                        text_size 14
                                        text_color "#ff4444"

                                if hovered_item.description:
                                    text hovered_item.description size 14 color "#888888" xoffset 10

    textbutton _("Return") action [StopAction(test_runner), Jump("front_page")] style "l_right_button"

    if GetFocusRect("sort_dropdown"):
        dismiss action ClearFocus("sort_dropdown")

        nearrect:
            focus "sort_dropdown"

            frame:
                modal True

                has vbox

                textbutton _("Duration") size_group "sort_buttons" action [
                    SetField(persistent, "test_sorter", "duration"),
                    Function(sort_test_nodes, test_roots),
                    ClearFocus("sort_dropdown")
                    ]
                textbutton _("Execution Order") size_group "sort_buttons" action [
                    SetField(persistent, "test_sorter", "order"),
                    Function(sort_test_nodes, test_roots),
                    ClearFocus("sort_dropdown")
                    ]
                textbutton _("Name") size_group "sort_buttons" action [
                    SetField(persistent, "test_sorter", "name"),
                    Function(sort_test_nodes, test_roots),
                    ClearFocus("sort_dropdown")
                    ]
                textbutton _("Status") size_group "sort_buttons" action [
                    SetField(persistent, "test_sorter", "status"),
                    Function(sort_test_nodes, test_roots),
                    ClearFocus("sort_dropdown")
                    ]

screen tests_error_modal(full_path, error_text):
    modal True

    frame:
        style "l_root"

        frame:
            style_group "l_info"
            ypos 0

            has vbox:
                style "_vbox"

            text full_path

            viewport:
                id "viewport"
                style "_viewport"
                child_size (None, None)
                mousewheel True
                draggable True
                scrollbars "both"
                # ysize 0.85

                if error_text:
                    frame style '_trace':
                        text error_text substitute False safe True style "_text" size 14

    # label _("Test Error Output") style "l_info_label"
    textbutton _("Close") action Hide("tests_error_modal") style "l_right_button"


label run_testcases:
    python hide:
        refresh_tests(generate=False)
        renpy.call_screen("test_explorer")

    jump front_page
"""
