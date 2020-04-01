#!/usr/bin/python3.6

import CardShoe as CardShoe
import importlib 
import sys
import os

def usage(): 
   usage("")

def usage(text): 
   print (text) 
   print ("USAGE:  ./PlayHands.py StrategyName ") 
   print ("")
   print ("     Example:  ./PlayHands.py VeryBasicStrategy") 
   sys.exit(1) 


#
# You could add things like 
#
def PlayShoe(strategyName,shoeSizeDecks = 4): 

   cardshoe = CardShoe.CardShoe(shoeSizeDecks) 
   Results = dict() 
    

   # Help gotten from https://dev.to/0xcrypto/dynamic-importing-stuff-in-python--1805
   try: 
     Strategy = importlib.import_module(name=strategyName) 

   except ImportError:
      print ("Could not import " + Strategy + " from file " +strategyName) 
      sys.exit(0)

   # While there are at least 15 cards, deal a new hand. 
   while cardshoe.count() > 15:
      playerCards = [ cardshoe.DealCard()]
      playerCards.append(cardshoe.DealCard()) 
      dealerCards = [ cardshoe.DealCard()] 
      dealerCards.append(cardshoe.DealCard())
      action = "hit" 
      context = Strategy.InitializeContext() 
      while action != "stand":
         action = Strategy.PlayerAction(playerCards,dealerCards,context)
         if action == "hit":
           playerCards.append(cardshoe.DealCard()) 
  
      action = "hit"
      while action != "stand":
         action = Strategy.DealerAction(playerCards,dealerCards,context)
         if action == "hit":
           dealerCards.append(cardshoe.DealCard()) 
  
      result = CardShoe.BetterHand(playerCards,dealerCards)
      Results[result] = Results.get(result,0) + 1
 
   return Results 

#
# Main Routine: 
# 
#


if len(sys.argv) < 2:
   usage("No Strategy Module supplied")

if sys.argv[1] == "":
   usage()
   sys.exit(0)


  
moduleName = sys.argv[1]
if not os.path.exists(moduleName+".py"): 
   usage("Module " + moduleName + " not found ")

ShoeResults = PlayShoe(sys.argv[1])
print (ShoeResults) 
