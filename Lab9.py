#Chandler Long

from graphics import *
from random import *



class Card:
    def __init__(self,center,tup_val):

        width = 60
        val_list = ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']
        #each unicode character is a suit shape
        suit_chr = [u'\u2663',u'\u2666',u'\u2665',u'\u2660']
        self.center, width = center,width
        self.tup_val = tup_val
        b_right = Point(center.getX() + width//2,
                         center.getY() + width * 7 // 10)
        t_left = Point(center.getX() - width//2,
                       center.getY() - width * 7 // 10)
        tl_chr = t_left.clone()
        tl_chr.move(width//10, width//8)
        br_chr = b_right.clone()
        br_chr.move(-width//10, -width//8)
        tl_sym = tl_chr.clone()
        tl_sym.move(0,width//6)
        br_sym = br_chr.clone()
        br_sym.move(0,-width//6)
       
        self.rect = Rectangle(b_right, t_left)
        self.rect.setFill('white')
        self.big_text = Text(center,str(val_list[tup_val[0]]))
        self.big_text.setSize(36)
        self.tl_text = Text(tl_chr, str(val_list[tup_val[0]]))
        self.br_text = Text(br_chr, str(val_list[tup_val[0]]))
        self.tl_sym = Text(tl_sym, suit_chr[tup_val[1]])
        self.br_sym = Text(br_sym, suit_chr[tup_val[1]])
        self.tl_sym.setSize(14)
        self.br_sym.setSize(14)
        #Make the red cards red
        if 1 <= tup_val[1] <= 2:
            color = 'red'
        else:
            color = 'black'

        self.big_text.setTextColor(color)
        self.tl_text.setTextColor(color)
        self.br_text.setTextColor(color)
        self.tl_sym.setTextColor(color)
        self.br_sym.setTextColor(color)
        

    def draw(self,win):
        '''Draws the card.'''
        self.rect.draw(win)
        self.big_text.draw(win)
        self.tl_text.draw(win)
        self.br_text.draw(win)
        self.tl_sym.draw(win)
        self.br_sym.draw(win)

    def undraw(self,win):
        '''Undraws the card.'''
        self.rect.undraw()
        self.big_text.undraw()
        self.tl_text.undraw()
        self.br_text.undraw()
        self.tl_sym.undraw()
        self.br_sym.undraw()

    def getBJvalue(self):
        '''Returns the BJ value of the card (Aces return 1)'''
        return [1,2,3,4,5,6,7,8,9,10,10,10,10][self.tup_val[0]]


def main():

    win = GraphWin('Black Jack', 400, 400)
    stayButton = Button(win, Point(110, 325), 75, 75, 'Stay', 'red')
    hitButton = Button(win, Point(290, 325), 75, 75, 'Hit\nMe', 'Green')

    
    dealerHand = Hand(win, Point(100, 100), 'Dealer')
    dealerHand.add_card()

    playerHand = Hand(win, Point(100, 200), 'Player')
    playerHand.add_card()
    playerHand.add_card()

    dealerTotal = Text(Point(50, 130), dealerHand.getBJvalue())
    dealerTotal.setSize(24)
    dealerTotal.setFill('red')

    playerTotal = Text(Point(50, 230), playerHand.getBJvalue())
    playerTotal.setSize(24)
    playerTotal.setFill('green')

    playerTotal.draw(win)
    dealerTotal.draw(win)

    while not playerHand.busted():
        if hitButton.clicked(win.getMouse()):
            playerHand.add_card()
            playerTotal.setText(playerHand.getBJvalue())

        if stayButton.clicked(win.getMouse()):
            break
            
    if not playerHand.busted():
        while not dealerHand.stay():
            dealerHand.add_card()
            dealerTotal.setText(dealerHand.getBJvalue())

        if not playerHand.busted():        
            if playerHand.getBJvalue() > dealerHand.getBJvalue() or dealerHand.busted():
                winner = Text(Point(200,15),"You WIN!!!")
                winner.draw(win)
                playAgain = Text(Point(200,25),"click anywhere to play again")
                playAgain.draw(win)
            else:
                lose = Text(Point(200,15),"You LOSE")
                lose.draw(win)
                playAgain = Text(Point(200,25),"click anywhere to play again")
                playAgain.draw(win)
    else:
        lose = Text(Point(200,15),"You LOSE")
        lose.draw(win)
        playAgain = Text(Point(200,25),"click anywhere to play again")
        playAgain.draw(win)


    click = win.getMouse()
    win.checkMouse()
    main()
        

class Hand:
    def __init__(self, win, center,name):

        self.hand = []

        self.win = win
        self.center = center
        self.name = Text(center, name)
        self.name.move(-50, 0)
        self.name.setSize(24)
        self.name.draw(win) 

    def add_card(self):       
        tupList = (randrange(13), randrange(3))
        self.center.move(60, 0)
        card = Card(self.center, tupList)
        self.hand.append(card.getBJvalue())
        card.draw(self.win)
               
    def total(self):
        total = sum(self.hand)
        return total
    
    def has_ace(self):
        '''Return True if there is an ace in the hand.'''
        for card in self.hand:
            if card == 1:
                return True
            else:
                return False
                
                
    
    def getBJvalue(self):
        
        total = sum(self.hand)

        if self.has_ace() == True:
            if sum(self.hand) <= 17:
                total += 10
                
            elif sum(self.hand) > 17 and sum(self.hand) <= 21:
                total += 0
            else:
                total += 0

        return total

            
    def stay(self):
        '''Returns True if the BJ value of the hand is 17 or greater'''
        if sum(self.hand) >= 17:
            return True
        else:
            return False
    
    def busted(self):
        '''Returns True if the value of hand is greater than 21.'''
        if sum(self.hand) > 21:
            return True
        else:
            return False
        


class Button:

    def __init__(self, win, center, width, height, label, color):

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        self.win = win
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill(color)
        self.label = Text(center, label)
        self.activate()

    def clicked(self, p):
        "Returns true if button active and p is inside"
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        "Returns the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True
        self.rect.draw(self.win)
        self.label.draw(self.win)

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('white')
        self.rect.setWidth(1)
        self.active = False        
        self.rect.undraw()
        self.label.undraw()

main()
        
        
        
