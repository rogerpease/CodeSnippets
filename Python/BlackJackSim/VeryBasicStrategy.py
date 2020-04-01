
from CardShoe import Card,SumCards 

#
# Very Basic Strategy-  Hit up to 16, stand on 17. 
#
# In this case we're using no context and not looking at Dealer's cards- all we do is look at our own cards. 
#

#
# Each function must be formatted as: 
#  PlayerAction(playerCards,dealerCards,context) 
#
#  Where playerCards is the list of playerCards, 
#  dealerCards is the list of dealerCards, 
#  context is a "memory" if you want to test a Card-counting algorithm. 
#
#


#
# Initialize Context. 
#
def InitializeContext():
   return ()
                          
def PlayerAction(playerCards,dealerCards,context): 
   if SumCards(playerCards)['maxNonBustTotal'] >= 17: 
     return 'stand' 
   else: 
     return 'hit' 


#
# I've never seen a dealer play based on player's hands (unless they all bust/fold) and 
#   usually there are rules about when they must hit/stand (i.e. "Dealer must hit on 16 and stand on all 17s") 
#
def DealerAction(playerCards,dealerCards,context): 
   if SumCards(dealerCards)['maxNonBustTotal'] >= 17: 
     return 'stand' 
   else: 
     return 'hit' 


#
# Test Assertions.... to make sure I'm implementing properly. 
#
#

def TestProc():
  
   #
   # In theory I should build this in CardShoe 
   # 
   soft16 = (Card('5','d'),Card('A','d'))
   hard16 = (Card('6','d'),Card('J','d'))
   soft17 = (Card('6','d'),Card('A','d'))
   hard17 = (Card('7','d'),Card('J','d'))

   context = InitializeContext() 
   assert(DealerAction(hard17, hard17,context) == 'stand') 
   assert(DealerAction(hard17, soft17,context) == 'stand') 
   assert(DealerAction(hard17, soft16,context) == 'hit') 

   assert(PlayerAction(hard16, hard17,context) == 'hit') 
   assert(PlayerAction(hard17, soft17,context) == 'stand') 
   assert(PlayerAction(soft16, soft16,context) == 'hit') 
   assert(PlayerAction(soft17, soft16,context) == 'stand') 



if __name__ == "__main__":
  TestProc()

