# cardgame.rpy - Cardgame support for Ren'Py
# Copyright (C) 2008 PyTom <pytom@bishoujo.us>
#
# This software may be distributed in modified or unmodified form,
# provided:
#
# (1) This complete license notice is retained.
#
# (2) This software and all software and data files distributed
# alongside this software and intended to be loaded in the same
# memory space may be redistributed without requirement for
# payment, notification, or other forms of compensation.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Commercial licensing for this software is available, please
# contact pytom@bishoujo.us for information.

init python:

    import pygame
    
    DRAG_NONE = 0
    DRAG_CARD = 1
    DRAG_ABOVE = 2
    DRAG_STACK = 3
    DRAG_TOP = 4

    # Returns the overlap of the area between the two
    # rectangles.
    def __rect_overlap_area(r1, r2):
        if r1 is None or r2 is None:
            return 0
        
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2

        maxleft = max(x1, x2)
        minright = min(x1 + w1, x2 + w2)
        maxtop = max(y1, y2)
        minbottom = min(y1 + h1, y2 + h2)

        if minright < maxleft:
            return 0

        if minbottom < maxtop:
            return 0

        return (minright - maxleft) * (minbottom - maxtop)

    def __default_can_drag(table, stack, card):
        return table.get_faceup(card)
    
    class Table(renpy.Displayable):

        def __init__(self, back=None, base=None, springback=0.1, rotate=0.1, can_drag=__default_can_drag, doubleclick=.33, **kwargs):

            renpy.Displayable.__init__(self, **kwargs)
            
            # A map from card value to the card object corresponding to
            # that value.
            self.cards = { }

            # A list of the stacks that have been defined.
            self.stacks = [ ]

            # The back of cards that don't have a more specific back
            # defined.
            self.back = renpy.easy.displayable_or_none(back)

            # The base of stacks that don't have a more specific base
            # defined.
            self.base = renpy.easy.displayable_or_none(base)

            # The amount of time it takes for cards to springback
            # into their rightful place.
            self.springback = springback

            # The amount of time it takes for cards to rotate into
            # their proper orientation.
            self.rotate = rotate

            # A function that is called to tell if we can drag a
            # particular card.
            self.can_drag = can_drag

            # The time between clicks for the click to be considered a
            # double-click.
            self.doubleclick = doubleclick

            # Are we sensitive to input? [doc]
            self.sensitive = True
            
            # The last click event.
            self.last_event = CardEvent()
            
            # The card that has been clicked.
            self.click_card = None

            # The stack that has been clicked.
            self.click_stack = None
            
            # The list of cards that are being dragged.
            self.drag_cards = [ ]
            
            # Are we dragging the cards?
            self.dragging = False
            
            # The position where we clicked.
            self.click_x = 0
            self.click_y = 0
            
            # The amount of time we've been shown for.
            self.st = 0

        # This shows the table on the given layer.
        def show(self, layer='master'):

            for v in self.cards.itervalues():
                v.offset = __Fixed(0, 0)

            ui.layer(layer)
            ui.add(self)
            ui.close()

        # This hides the table.
        def hide(self, layer='master'):
            ui.layer(layer)
            ui.remove(self)
            ui.close()

        # This controls sensitivity.
        def set_sensitive(self, value):
            self.sensitive = value
            
        def get_card(self, value):
            if value not in self.cards:
                raise Exception("No card has the value %r." % value)

            return self.cards[value]
            
        # This sets the faceup status of a card.
        def set_faceup(self, card, faceup=True):
            self.get_card(card).faceup = faceup
            renpy.redraw(self, 0)

        def get_faceup(self, card):
            return self.get_card(card).faceup
            
        # This sets the rotation of a card.
        def set_rotate(self, card, rotation):
            __Rotate(self.get_card(card), rotation)
            renpy.redraw(self, 0)

        def get_rotate(self, card):
            return self.get_card(card).rotate.rotate_limit()
            
        def add_marker(self, card, marker):
             self.get_card(card).markers.append(marker)
             renpy.redraw(self, 0)

        def remove_marker(self, card, marker):
            self.get_card(card).markers.remove(marker)
            renpy.redraw(self, 0)

        # Called to create a new card.
        def card(self, value, face, back=None):
            self.cards[value] = __Card(self, value, face, back)

        # Called to create a new stack.
        def stack(self, x, y, xoff=0, yoff=0, show=1024, base=None,
                  click=False, drag=DRAG_NONE, drop=False, hidden=False):

            rv = __Stack(self, x, y, xoff, yoff, show, base, click, drag, drop, hidden) 
            
            self.stacks.append(rv)
            return rv

        # Force a redraw on each interaction.
        def per_interact(self):
            renpy.redraw(self, 0)

        
        def render(self, width, height, st, at):

            self.st = st

            rv = renpy.Render(width, height)

            for s in self.stacks:

                if s.hidden:
                    s.rect = None
                    for c in s.cards:
                        c.rect = None
                    continue

                s.render_to(rv, width, height, st, at)
                
                for c in s.cards:
                    c.render_to(rv, width, height, st, at)
            
            return rv

        def event(self, ev, x, y, st):

            self.st = st

            if not self.sensitive:
                return

            grabbed = renpy.display.focus.get_grab()

            if (grabbed is not None) and (grabbed is not self):
                return
            
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:

                if self.click_stack:
                    return

                stack = None
                card = None
                
                for s in self.stacks:

                    sx, sy, sw, sh = s.rect
                    if sx <= x and sy <= y and sx + sw > x and sy + sh > y:
                        stack = s


                    for c in s.cards[-s.show:]:
                        if c.rect is None:
                            continue

                        cx, cy, cw, ch = c.rect
                        if cx <= x and cy <= y and cx + cw > x and cy + ch > y:
                            card = c
                            stack = c.stack
                            
                if stack is None:
                    return

                # Grab the display.
                renpy.display.focus.set_grab(self)
                
                # Don't let the user grab a moving card.
                if card is not None:
                    xoffset, yoffset = card.offset.offset()
                    if xoffset or yoffset:
                        return
                    
                # Move the stack containing the card to the front.
                self.stacks.remove(stack)
                self.stacks.append(stack)
                
                if stack.click or stack.drag:
                    self.click_card = card
                    self.click_stack = stack
                
                if card is None or not self.can_drag(self, card.stack, card.value):
                    self.drag_cards = [ ]
                elif card.stack.drag == DRAG_CARD:
                    self.drag_cards = [ card ]
                elif card.stack.drag == DRAG_ABOVE:
                    self.drag_cards = [ ]
                    for c in card.stack.cards:
                        if c is card or self.drag_cards:
                            self.drag_cards.append(c)
                elif card.stack.drag == DRAG_STACK:
                    self.drag_cards = list(card.stack.cards)
                elif card.stack.drag == DRAG_TOP:
                    if card.stack.cards[-1] is card:
                        self.drag_cards = [ card ]
                    else:
                        self.drag_cards = [ ]

                for c in self.drag_cards:
                    c.offset = __Fixed(0, 0)
                        
                self.click_x = x
                self.click_y = y
                self.dragging = False
                
                renpy.redraw(self, 0)
                
                raise renpy.IgnoreEvent()

            if ev.type == pygame.MOUSEMOTION or (ev.type == pygame.MOUSEBUTTONUP and ev.button == 1):

                if abs(x - self.click_x) > 7 or abs(y - self.click_y) > 7:
                    self.dragging = True

                dx = x - self.click_x
                dy = y - self.click_y

                for c in self.drag_cards:
                    xoffset, yoffset = c.offset.offset()
                    
                    cdx = dx - xoffset
                    cdy = dy - yoffset

                    c.offset = __Fixed(dx, dy)
                    
                    if c.rect:
                        cx, cy, cw, ch = c.rect
                        cx += cdx
                        cy += cdy
                        c.rect = (cx, cy, cw, ch)

                area = 0
                dststack = None 
                dstcard = None
                
                for s in self.stacks:
                    if not s.drop:
                        continue
                    
                    for c in self.drag_cards:

                        if c.stack == s:
                            continue
                        a = __rect_overlap_area(c.rect, s.rect)
                        if a >= area:
                            dststack = s
                            dstcard = None
                            area = a
                            
                        for c1 in s.cards:
                            a = __rect_overlap_area(c.rect, c1.rect)
                            if a >= area:
                                dststack = s
                                dstcard = c1
                                area = a

                if area == 0:
                    dststack = None
                    dstcard = None

                renpy.redraw(self, 0)

                if ev.type == pygame.MOUSEMOTION:
                    raise renpy.IgnoreEvent()

            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:

                # Ungrab the display.
                renpy.display.focus.set_grab(None)

                evt = None

                if self.dragging:
                    if dststack is not None and self.drag_cards:

                        evt = CardEvent()
                        evt.type = "drag"
                        evt.table = self
                        evt.stack = self.click_stack
                        evt.card = self.click_card.value
                        evt.drag_cards = [c.value for c in self.drag_cards]
                        evt.drop_stack = dststack
                        if dstcard:
                            evt.drop_card = dstcard.value
                        evt.time = st
                            
                else:

                    if self.click_stack.click:                    

                        evt = CardEvent()
                        evt.type = "click"
                        evt.table = self
                        evt.stack = self.click_stack
                        if self.click_card:
                            evt.card = self.click_card.value
                        else:
                            evt.card = None

                        evt.time = st

                        if (evt.type == self.last_event.type
                            and evt.stack == self.last_event.stack
                            and evt.card == self.last_event.card
                            and evt.time < self.last_event.time + self.doubleclick):

                            evt.type = "doubleclick"

                if evt is not None:
                    self.last_event = evt
                        
                for c in self.drag_cards:
                    c.springback()
                    
                self.click_card = None
                self.click_stack = None
                self.drag_cards = [ ]

                if evt is not None: 
                    return evt
                else:
                    raise renpy.IgnoreEvent()

                
    class CardEvent(object):

        def __init__(self):
            self.type = None
            self.stack = None
            self.card = None
            self.drag_cards = None
            self.drop_stack = None
            self.drop_card = None
            self.time = 0
            
    # Represents a stack of one or more cards, which can be placed on the
    # table.
    class __Stack(object):

        def __init__(
            self, table,
            x, y,
            xoff, yoff,
            show, base,
            click, drag, drop,
            hidden):


            # The table this stack belongs to.
            self.table = table

            # The x and y coordinates of the center of the top card of
            # this stack.
            self.x = x
            self.y = y

            # The offset in the x and y directions of each successive
            # card.
            self.xoff = xoff
            self.yoff = yoff

            # The number of cards to show from this stack. (We show the
            # last show cards if this is less than the numebr of cards
            # in the stack.)
            self.show = show

            # The image that is shown behind the stack. If None, the
            # background is taken from the table.
            self.base = base

            # Should we report click events on this stack?
            self.click = click

            # Should we allow dragging this stack? If so, how?
            self.drag = drag

            # Should we allow dropping to this stack?
            self.drop = drop

            # Is this stack hidden?
            self.hidden = hidden
            
            # The list of cards in this stack.
            self.cards = [ ]

            # The rectangle for the background of this effect.
            self.rect = None
            
        def insert(self, index, card):
            card = self.table.get_card(card)

            if card.stack:
                card.stack.cards.remove(card)

            card.stack = self
            self.cards.insert(index, card)

            self.table.stacks.remove(self)
            self.table.stacks.append(self)
            
            card.springback()
            
        def append(self, card):
            if card in self.cards:                
                self.insert(len(self.cards) - 1, card)
            else:
                self.insert(len(self.cards), card)

        def remove(self, card):
            card = self.table.get_card(card)            
            self.cards.remove(card)
            card.stack = None
            card.rect = None

        def deal(self):
            if not self.cards:
                return None
                
            card = self.cards[-1]
            self.remove(card.value)
            return card.value

        def shuffle(self):
            renpy.random.shuffle(self.cards)
            renpy.redraw(self.table, 0)
            
        def __len__(self):
            return len(self.cards)

        def __getitem__(self, idx):
            return self.cards[idx].value

        def __iter__(self):
            for i in self.cards:
                yield i.value

        def __contains__(self, item):
            return self.table.get_card(card) in self.cards
                
        def render_to(self, rv, width, height, st, at):

            base = self.base or self.table.base

            if base is None:
                return

            surf = renpy.render(base, width, height, st, at)
            cw, ch = surf.get_size()

            cx = self.x - cw / 2
            cy = self.y - ch / 2

            self.rect = (cx, cy, cw, ch)
            rv.blit(surf, (cx, cy))
            
    class __Card(object):

        def __init__(self, table, value, face, back):

            # The table this card belongs to.
            self.table = table

            # The value of this card.
            self.value = value

            # The face of this card.
            self.face = renpy.easy.displayable(face)

            # The back of this card. If None, then the back is taken from
            # the table the card belongs to.
            self.back = renpy.easy.displayable_or_none(back)

            # Is this card faceup (or face down?)
            self.faceup = True

            # Object that's called to decide how rotated this card should
            # be.
            self.rotate = None

            # A series of highlights that should be drawn over this card.
            self.highlights = [ ]

            # The stack this card is in.
            self.stack = None

            # An object that gives the offset of this card relative to
            # where it would normally be placed.
            self.offset = __Fixed(0, 0)
            
            # The rectangle where this card was last drawn to the screen
            # at.
            self.rect = None

            __Rotate(self, 0)
            
        # Returns the base x and y placement of this card.
        def place(self):
            s = self.stack
            offset = max(len(s.cards) - s.show, 0)
            index = max(s.cards.index(self) - offset, 0)

            return (s.x + s.xoff * index, s.y + s.yoff * index)

        def springback(self):
            if self.rect is None:
                self.offset = __Fixed(0, 0)
            else:
                self.offset = __Springback(self)
                        
        def render_to(self, rv, width, height, st, at):
            
            x, y = self.place()
            xoffset, yoffset = self.offset.offset()
            x += xoffset
            y += yoffset

            if self.faceup:
                d = self.face
            else:
                d = self.back or self.table.back
                
            # TODO: Figure out if we can reuse some of this.

            if self.highlights:
                d = Fixed(* ([d] + [renpy.easy.displayable(i) for i in self.highlights]))

            r = self.rotate.rotate()
            if r:
                d = RotoZoom(r, r, 0, 1, 1, 0)(d)
                
            surf = renpy.render(d, width, height, st, at)
            w, h = surf.get_size()

            x -= w / 2
            y -= h / 2

            self.rect = (x, y, w, h)

            rv.blit(surf, (x, y))
            
        def __repr__(self):
            return "<__Card %r>" % self.value
        

    class __Springback(object):

        def __init__(self, card):
            self.card = card
            self.table = table = card.table
            
            self.start = table.st

            cx, cy, cw, ch = self.card.rect
            x = cx + cw / 2
            y = cy + ch / 2

            self.startx = x
            self.starty = y

        def offset(self):

            t = (self.table.st - self.start) / self.table.springback
            t = min(t, 1.0)
            
            if t < 1.0:
                renpy.redraw(self.table, 0)

            px, py = self.card.place() 
                
            return int((self.startx - px) * (1.0 - t)), int((self.starty - py) * (1.0 - t))


    class __Fixed(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def offset(self):
            return self.x, self.y
        

    class __Rotate(object):
        def __init__(self, card, amount):

            self.table = table = card.table
            self.start = table.st
            
            if card.rotate is None:
                self.start_rotate = amount
            else:
                self.start_rotate = card.rotate.rotate()

            self.end_rotate = amount

            card.rotate = self

            
        def rotate(self):

            if self.start_rotate == self.end_rotate:
                return self.start_rotate

            t = (self.table.st - self.start) / self.table.springback
            t = min(t, 1.0)

            if t < 1.0:
                renpy.redraw(self.table, 0)

            return self.start_rotate + (self.end_rotate - self.start_rotate) * t
        
        def rotate_limit(self):
            return self.end_rotate
