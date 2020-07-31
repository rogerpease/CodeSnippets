#!/usr/bin/python3.6 
#
# Python program to try out KNN classification algorithm 
#
# You'll need to do:  
#
#    sudo pip3 install -U scikit-learn scipy matplotlib
#
#  Often you're better off with virtualenv's or Docker environments at that point. 
#

from sklearn.neighbors import KNeighborsClassifier 
import numpy as np 
import math
from sklearn.model_selection import train_test_split 


#
# Amplitude of a circle. 
#

def amplitude(pos):
   return math.sqrt((pos[0])**2+(pos[1])**2)
  
def inCircle(pos): 
  if (amplitude(pos) <= 1): 
    return 1
  return 0


#
# Basically we're training the algorithm to identify if a point is in a circle 
#    We give it points bounded by the square between (-1,-1) and (1,1). 
#    Everything outside the unit circle is 0.  
#    Everything inside is 1. 
# 
#
X = []
y = []
for xpos in range(-100,100,1):
  for ypos in range(-100,100,1):
    point = [xpos/100,ypos/100]
    X.append(point)
    y.append(inCircle(point))

X2 = np.array(X).reshape(-1,2)
y2 = np.array(y)
print (X2)
print (y2)


#
# Factor out a bunch of points and pick a percentage (test_size) to be test. The rest are train. 
# 
#

X_train, X_test, y_train, y_test = train_test_split( X2, y2, test_size=0.33, random_state=42)
  
kn = KNeighborsClassifier(n_neighbors=1) 
kn.fit(X_train, y_train) 

#
# How well did we do? 
#
print("Test score: {:.2f}".format(kn.score(X_test, y_test))) 

#
# When I ran this I found that 99% of the time I guessed right that 
#
#
  
verywrong = []
print ("Mispredictions: ")
for xpos in X_test: 
  prediction = kn.predict([xpos])
  if (inCircle(xpos) != prediction): 
    if (abs(1-amplitude(xpos)) > 0.01): 
      verywrong.append([xpos,amplitude(xpos)]) 

print (verywrong)

