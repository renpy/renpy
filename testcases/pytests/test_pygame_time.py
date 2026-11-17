# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

"""
Tests for renpy.pygame.time timers, and for suspending the events they post.

Timers are suspended while a mobile app is in the background. The tests suspend them directly, since SDL only
reports the app entering the background on mobile platforms.
"""

from collections.abc import Iterator

import pytest

from renpy import pygame

# How long a repeating timer waits between events, and how long a one-shot timer waits, in milliseconds.
TIMER_INTERVAL: int = 5

# How long to wait for timer events, in milliseconds. This is many intervals, so a running timer posts events
# even on a loaded machine.
SETTLE_TIME: int = 150


@pytest.fixture(scope="module")
def timer_event() -> Iterator[int]:
    """
    Starts the event system, and yields an event type for the timers in this module to post.
    """

    pygame.event.init()

    yield pygame.event.register("TEST_PYGAME_TIME")


@pytest.fixture(autouse=True)
def reset_timers(timer_event: int) -> Iterator[None]:
    """
    Removes the timer, lets timers post again, and discards the timer's events after each test.
    """

    yield

    pygame.time.set_timer(timer_event, 0)
    pygame.time._suspend_timers(False)
    pygame.time.wait(TIMER_INTERVAL * 2)
    pygame.event.clear(timer_event)


def count_events(timer_event: int) -> int:
    """
    Waits for the timer to run, then returns how many of its events were posted since the queue was last read.
    """

    pygame.time.wait(SETTLE_TIME)

    return len(pygame.event.get(timer_event))


def test_repeating_timer_posts_only_while_not_suspended(timer_event: int):
    """
    A repeating timer posts no events while timers are suspended, and posts them again afterwards without
    being set again.
    """

    pygame.time.set_timer(timer_event, TIMER_INTERVAL)
    assert count_events(timer_event) > 0

    pygame.time._suspend_timers(True)

    # Discard the events posted before the suspension, including by a callback that was already running.
    count_events(timer_event)
    assert count_events(timer_event) == 0

    pygame.time._suspend_timers(False)
    assert count_events(timer_event) > 0


def test_one_shot_timer_is_lost_while_suspended(timer_event: int):
    """
    A one-shot timer that expires while timers are suspended does not post its event later.
    """

    pygame.time._suspend_timers(True)
    pygame.time.set_timer(timer_event, TIMER_INTERVAL, once=True)
    assert count_events(timer_event) == 0

    pygame.time._suspend_timers(False)
    assert count_events(timer_event) == 0


def test_one_shot_timer_posts_once(timer_event: int):
    """
    A one-shot timer posts a single event when timers are not suspended.
    """

    pygame.time.set_timer(timer_event, TIMER_INTERVAL, once=True)
    assert count_events(timer_event) == 1
