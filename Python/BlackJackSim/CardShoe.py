#!/usr/bin/python3.6 

import random

suits = ['h','s','c','d']; 
ranks = [ 'A','2','3','4','5','6','7','8','9','10','J','Q','K'];


#
# Card Class 
#
class Card:
   def __init__(self,rank,suit): 
      self.Rank = rank
      self.Suit = suit

   def RankValue(self):
     if self.Rank == 'A':
       return 1;
     if self.Rank == 'J' or self.Rank == 'Q' or self.Rank == 'K' or self.Rank == '10':
       return 10;
     return ord(self.Rank)-ord('0')

   # How to print this. 
   def __str__(self):
      return self.Rank + self.Suit


def SumCards(cards):
   result = dict()
   minTotal = 0
   aces = 0
   for card in cards: minTotal += card.RankValue() 
   for card in cards: 
     if card.Rank == 'A':
        aces += 1
   maxNonBustTotal = minTotal  
   result['aces'] = aces
   while aces > 0 and minTotal < 12:
     maxNonBustTotal += 10
     aces -= 1
   result['minTotal'] = minTotal 
   result['maxNonBustTotal'] = maxNonBustTotal
   result["Bust"] = 0
   if minTotal > 21:
     result["Bust"] = 1
   return result 

#
# Who has the better hand? 
#

def BetterHand(playerHand,dealerHand):
   playerTotal = SumCards(playerHand)
   dealerTotal = SumCards(dealerHand)
   if playerTotal["Bust"]:
     return "DealerWins"
   elif dealerTotal["Bust"]:
     return "PlayerWins"
   elif playerTotal['maxNonBustTotal'] < dealerTotal['maxNonBustTotal']:
     return "DealerWins" 
   elif playerTotal['maxNonBustTotal'] == dealerTotal['maxNonBustTotal']:
     return "Draw" 
   else:  
     return "PlayerWins" 

#
# Hold the state of the shoe. 
#
#

class CardShoe: 
   def __init__(self,numDecks):   
      self.deck  = [ Card(rank,suit) for rank in ranks for suit in suits ] * numDecks
      random.shuffle(self.deck)
 
   def count(self):
     return len(self.deck)

   def DealCard(self):
      newcard = self.deck.pop()
      return newcard
   # Here you might put other elements such as a count of Ace Cards. 


def TestProcedure(): 
   # Test the shoe. 
   myFourCardShoe = CardShoe(4)
   assert (myFourCardShoe.count() == 208) 
   mycard = myFourCardShoe.DealCard() 
   assert (myFourCardShoe.count() == 207) 

   # Test values. 
   kingOfSpades = Card('K','s')
   assert (kingOfSpades.RankValue() == 10) 
   aceOfHearts = Card('A','h')
   assert (aceOfHearts.RankValue() == 1) 

   sumOfCards = SumCards([kingOfSpades,kingOfSpades])
   assert (sumOfCards['minTotal'] == 20) 

   sumOfCards = SumCards([kingOfSpades,aceOfHearts])
   assert (sumOfCards['minTotal'] == 11) 
   assert (sumOfCards['aces'] == 1) 
   assert (sumOfCards['maxNonBustTotal'] == 21) 




TestProcedure()

# I use test procedures and call modules with their own test procedures quite often. 
#  This is similar to TestProc() unless caller in perl. 
#
# https://stackoverflow.com/questions/6523791/why-is-python-running-my-module-when-i-import-it-and-how-do-i-stop-it
#
def main():
   TestProcedure

if __name__ == "__main__":
   main()
