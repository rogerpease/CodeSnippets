
from CardShoe import Card,SumCards 

#
# Basic Strategy- Based on 
#   https://www.reddit.com/r/blackjack/comments/b0hict/basic_strategy_table_with_common_deviations_advice/
#  
# We don't increase bets based on state of the shoe. 
#


#
# Initialize Context. 
#
def InitializeContext():
   return ()

playerWithPair = : 
   
                          
def PlayerAction(playerCards,dealerCards,context): 
   dealerShows = dealerCards[0]
   if (IsPair(playerCards)):
      



#
#
#
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

