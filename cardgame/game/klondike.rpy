# klondike.rpy - Klondike Solitaire for the Ren'Py Cardgame Engine.
# Copyright (C) 2008 Tom Rothamel <pytom@bishoujo.us>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For the purposes of the GPL, the copyrighted work consists of all
# script files that run in the same engine as this file, and any other
# file loaded from those scripts, without being selected by the
# user. (This includes image, font, music, movie, and sound files.)
#
# Commercial licenses for this code are available, please contact
# pytom@bishoujo.us for information.

init python:

    class Klondike(object):

        # We represent a card as a (suit, rank) tuple. The suit is one of the
        # following four constants, while the rank is 1 for ace, 2 for 2,
        # ..., 10 for 10, 11 for jack, 12 for queen, 13 for king.        
        CLUB = 0
        SPADE = 1
        HEART = 2
        DIAMOND = 3
        
        def __init__(self, deal=3):

            # Constants that let us easily change where the game is
            # located.
            LEFT=140
            TOP=58
            COL_SPACING = 90
            ROW_SPACING = 120
            CARD_XSPACING = 20
            CARD_YSPACING = 30

            # Store the parameters.
            self.deal = deal
            
            # Create the table, stock, and waste.
            self.table = t = Table(base="card/base.png", back="card/back.png")
            self.stock = t.stack(LEFT, TOP, xoff=0, yoff=0, click=True)
            self.waste = t.stack(LEFT + COL_SPACING, TOP, xoff=CARD_XSPACING, drag=DRAG_BOTTOM, show=self.deal)

            # The 4 foundation stacks.
            self.foundations = [ ]
            for i in range(0, 4):
                s = t.stack(LEFT + COL_SPACING * (i + 3), TOP, xoff=0, yoff=0, drag=DRAG_BOTTOM, drop=True)
                self.foundations.append(s)

            # The 7 tableau stacks.
            self.tableau = [ ]
            for i in range(0, 7):
                s = t.stack(LEFT + COL_SPACING * i, TOP + ROW_SPACING, xoff=0, yoff=CARD_YSPACING, drag=DRAG_BELOW, click=True, drop=True)
                self.tableau.append(s)

            # Create the stock and shuffle it.
            for rank in range(1, 14):
                for suit in range(0, 4):
                    value = (suit, rank)
                    t.card(value, "card/%d.png" % self.card_num(suit, rank))
                    t.set_faceup(value, False)
                    self.stock.append(value)
                    
            self.stock.shuffle()
            
            # Deal out the initial tableau.
            for i in range(0, 7):
                for j in range(i, 7):
                    c = self.stock.deal()
                    self.tableau[j].append(c)                    

        # This figures out the image filename for a given suit and rank.
        def card_num(self, suit, rank):
            ranks = [ None, 1, 49, 45, 41, 37, 33, 29, 25, 21, 17, 13, 9, 5 ]
            return suit + ranks[rank]
                
        def show(self):
            self.table.show()

        def hide(self):
            self.table.hide()

        def tableau_drag(self, evt):

            card = evt.drag_cards[0]
            cards = evt.drag_cards
            stack = evt.drop_stack

            csuit, crank = card
            
            # If the stack is empty, allow a king to be dragged to it.
            if not stack:
                if crank == 13:
                    for i in cards:
                        stack.append(i)

                return

            # Otherwise, the stack has a bottom card.
            bottom = stack[-1]
            bsuit, brank = bottom

            # Figure out which of the stacks are black.
            cblack = (csuit == self.SPADE) or (csuit == self.CLUB)
            bblack = (bsuit == self.SPADE) or (bsuit == self.CLUB)

            # Can we legally place the cards?
            if (bblack != cblack) and (crank == brank - 1):

                # Place the cards:
                for i in cards:
                    stack.append(i)

        def foundation_drag(self, evt):

            # We can only drag one card at a time to a foundation.
            if len(evt.drag_cards) != 1:
                return

            suit, rank = evt.drag_cards[0]

            # If there is a card on the foundation already, then
            # check to see if we're dropping then next one in
            # sequence.
            if len(evt.drop_stack):
                dsuit, drank = evt.drop_stack[-1]
                if suit == dsuit and rank == drank + 1:
                    evt.drop_stack.append(evt.drag_cards[0])

            # Otherwise, make sure we're dropping an ace.
            else:
                if rank == 1:
                    evt.drop_stack.append(evt.drag_cards[0])
                    
        def tableau_doubleclick(self, evt):
            # Make sure that there's at least one card in the stack.
            if not evt.stack:
                return

            # The bottom card in the stack.
            card = evt.stack[-1]
            suit, rank = card

            # If the card is an ace, find an open foundation and put it
            # there.
            if rank == 1:
                for i in self.foundations:
                    if not i:
                        i.append(card)
                        break
                return

            # Otherwise, see if there's a foundation where we can put
            # the card.
            for i in self.foundations:
                if not i:
                    continue
                
                fsuit, frank = i[-1]
                if suit == fsuit and rank == frank + 1:
                    i.append(card)
                    break
        
        def stock_click(self, evt):

            # If there are cards in the stock, dispense up to three3
            # of them.
            if self.stock:
                for i in range(0, self.deal):
                    if self.stock:
                        c = self.stock[-1]
                        self.table.set_faceup(c, True)
                        self.waste.append(c)

            # Otherwise, move the contents of the waste to the stock.
            else:
                while self.waste:
                    c = self.waste[-1]
                    self.table.set_faceup(c, False)
                    self.stock.append(c)
            
        def interact(self):
 
            # Ensure that the bottom of each tableau is faceup.
            for i in range(0, 7):
                if self.tableau[i]:
                    self.table.set_faceup(self.tableau[i][-1], True)

            evt = ui.interact()

            # Check the various events, and dispatch them to the methods
            # that handle them.
            if evt.type == "drag":
                if evt.drop_stack in self.tableau:
                    self.tableau_drag(evt)

                elif evt.drop_stack in self.foundations:
                    self.foundation_drag(evt)

            elif evt.type == "click":
                if evt.stack == self.stock:
                    self.stock_click(evt)

            elif evt.type == "doubleclick":
                if evt.stack in self.tableau or evt.stack == self.waste:
                    self.tableau_doubleclick(evt)

            # Check to see if any of the foundations has less than
            # 13 cards in it. If it does, return False. Otherwise,
            # return True.
            for i in self.foundations:
                if len(i) != 13:
                    return False

            return True
