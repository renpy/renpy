# klondike.rpy - Klondike Solitaire
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
            self.waste = t.stack(LEFT + COL_SPACING, TOP, xoff=CARD_XSPACING, drag=DRAG_TOP, show=self.deal, click=True)

            # The 4 foundation stacks.
            self.foundations = [ ]
            for i in range(0, 4):
                s = t.stack(LEFT + COL_SPACING * (i + 3), TOP, xoff=0, yoff=0, drag=DRAG_TOP, drop=True)
                self.foundations.append(s)

            # The 7 tableau stacks.
            self.tableau = [ ]
            for i in range(0, 7):
                s = t.stack(LEFT + COL_SPACING * i, TOP + ROW_SPACING, xoff=0, yoff=CARD_YSPACING, drag=DRAG_ABOVE, click=True, drop=True)
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

            # Ensure that the bottom of each tableau is faceup.
            for i in range(0, 7):
                if self.tableau[i]:
                    self.table.set_faceup(self.tableau[i][-1], True)


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

                return "tableau_drag"

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

                return "tableau_drag"

            return False
                    
        def foundation_drag(self, evt):

            # We can only drag one card at a time to a foundation.
            if len(evt.drag_cards) != 1:
                return False

            suit, rank = evt.drag_cards[0]

            # If there is a card on the foundation already, then
            # check to see if we're dropping then next one in
            # sequence.
            if len(evt.drop_stack):
                dsuit, drank = evt.drop_stack[-1]
                if suit == dsuit and rank == drank + 1:
                    evt.drop_stack.append(evt.drag_cards[0])
                    return "foundation_drag"
                    
            # Otherwise, make sure we're dropping an ace.
            else:
                if rank == 1:
                    evt.drop_stack.append(evt.drag_cards[0])
                    return "foundation_drag"

            return False
                
        def tableau_doubleclick(self, evt):

            # Make sure that there's at least one card in the stack.
            if not evt.stack:
                return False

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
                return "foundation_drag"

            # Otherwise, see if there's a foundation where we can put
            # the card.
            for i in self.foundations:
                if not i:
                    continue
                
                fsuit, frank = i[-1]
                if suit == fsuit and rank == frank + 1:
                    i.append(card)
                    return "foundation_drag"

            return False
        
        def stock_click(self, evt):

            # If there are cards in the stock, dispense up to three3
            # of them.
            if self.stock:
                for i in range(0, self.deal):
                    if self.stock:
                        c = self.stock[-1]
                        self.table.set_faceup(c, True)
                        self.waste.append(c)

                return "stock_click"
                        
            # Otherwise, move the contents of the waste to the stock.
            else:
                while self.waste:
                    c = self.waste[-1]
                    self.table.set_faceup(c, False)
                    self.stock.append(c)

                return "stock_click"

                    
        def interact(self):

            evt = ui.interact()
            rv = False
            
            # Check the various events, and dispatch them to the methods
            # that handle them.
            if evt.type == "drag":
                if evt.drop_stack in self.tableau:
                    rv = self.tableau_drag(evt)
                    
                elif evt.drop_stack in self.foundations:
                    rv = self.foundation_drag(evt)
                    
            elif evt.type == "click":
                if evt.stack == self.stock:
                    rv = self.stock_click(evt)
                    
            elif evt.type == "doubleclick":
                if (evt.stack in self.tableau) or (evt.stack is self.waste):
                    rv = self.tableau_doubleclick(evt)
                    
            # Ensure that the bottom card in each tableau is faceup.
            for i in range(0, 7):
                if self.tableau[i]:
                    self.table.set_faceup(self.tableau[i][-1], True)

            # Check to see if any of the foundations has less than
            # 13 cards in it. If it does, return False. Otherwise,
            # return True.
            for i in self.foundations:
                if len(i) != 13:
                    return rv

            return "win"

        # Sets things as sensitive (or not).
        def set_sensitive(self, value):
            self.table.set_sensitive(value)
        
        # Utility functions.

        # Is it okay to drag the over card onto under, where under is
        # part of a tableau.
        def can_hint(self, under, over):
            usuit, urank = under
            osuit, orank = over

            if orank == 1:
                return False
            
            ublack = (usuit == self.SPADE) or (usuit == self.CLUB)
            oblack = (osuit == self.SPADE) or (osuit == self.CLUB)

            if (oblack != ublack) and (orank == urank - 1):
                return True

        # Returns the first faceup card in the stack.
        def first_faceup(self, s):
            for c in s:
                if self.table.get_faceup(c):
                    return c

        # This tries to find a reasonable hint, and returns it as a
        # pair of cardnames.
        def hint(self):

            for i in self.tableau:
                if not i:
                    continue

                over = self.first_faceup(i)

                for j in self.tableau:
                    if not j or i is j:
                        continue

                    under = j[-1]

                    if self.can_hint(under, over):
                        return (under, over)

            if self.waste:

                over = self.waste[-1]

                for j in self.tableau:
                    if not j:
                        continue

                    under = j[-1]

                    if self.can_hint(under, over):
                        return (under, over)
                
            return None, None
            
        def card_name(self, c):
            suit, rank = c

            return  [
                "INVALID",
                "Ace",
                "Two",
                "Three",
                "four",
                "Five",
                "Six",
                "Seven",
                "Eight",
                "Nine",
                "Ten",
                "Jack",
                "Queen",
                "King" ][rank] + " of " + [
                "Clubs",
                "Spades",
                "Hearts",
                "Diamonds" ][suit]
                     
                    
