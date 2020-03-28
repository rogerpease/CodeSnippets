#!/usr/bin/python3.6 

#
#
# Roger D. Pease 28 Mar 2020 
#
#    See readme at top of this repo for ground rules. 
#

import pygame
from threading import Timer
import time 
import random
from random import shuffle
from os import listdir
from os.path import isfile, join,isdir
import sys 

debug = 0

def DebugMessage(str):
  if debug == 1:
    print(str) 


#
# Hold the state of our game. 
#    
#
class GameStateClass:
     def __init__(self,imagePath):
         # Set Variables.
         self.MasterWindowX = 800   # Width 
         self.MasterWindowY = 800   # Height 
         self.blockEvents = False
         self.done = False
         self.XSquaresInRow = 4
         self.YSquaresInCol = 4
         self.Border = 2
         self.XPicMeasInclBorder = self.MasterWindowX /self.XSquaresInRow
         self.YPicMeasInclBorder = self.MasterWindowY /self.YSquaresInCol
         self.XPicMeas = self.XPicMeasInclBorder - 2*self.Border
         self.YPicMeas = self.YPicMeasInclBorder - 2*self.Border
         self.NumSquares = self.XSquaresInRow*self.YSquaresInCol
         self.NumPairsSquares = int(self.NumSquares/2)
         self.IsEvenNumberOfSquares = (self.NumSquares == (self.NumPairsSquares*2))

         # Start Main Window. 
         self.screen = pygame.display.set_mode((self.MasterWindowX,self.MasterWindowY))
         pygame.display.set_caption("Match Game")

         # Keep an image bank in the images/ subdirectory. 
         self.imageBank = []
         if not isdir(imagePath):
             self.Valid = 0
             return
         self.imageFileNames = [
                # join is inherited from os- it turns ("/home/user", "program") to "/home/user/program". 
                # Then we use this list 
               join(imagePath,f) for f in listdir(imagePath) 
                 if isfile(join(imagePath, f))
                  ]
         self.Valid = 1  # Did we get constructed correctly?  

         NumPicsAvailable = len(self.imageFileNames)
         DebugMessage("Loaded " + str(NumPicsAvailable) + " pictures")
         if (NumPicsAvailable < self.NumPairsSquares): 
           print ("I needed " + str(self.NumPairsSquares) + " pictures in images directory but only " + str(NumPicsAvailable) +" were available")
           self.Valid = 0 
           return
         self.ImageRectBank = []
         self.imageBankIndexBySquareNumber = []

         # To select random pictures, we put numbers 0..n-1
         # where n is # of pictures into an array. 
         # then we shuffle that array, then take the first s indexes
         # of that array where s is numberof pairs of boxes. 

         self.ArrayOfPicNumbers = list(range(0,len(self.imageFileNames)))
         shuffle(self.ArrayOfPicNumbers)

         # Now pick which picture goes where. Build an array and re-sort it randomly
         for index in range (0,self.NumPairsSquares):
          self.imageBankIndexBySquareNumber.append(self.ArrayOfPicNumbers[index])
          self.imageBankIndexBySquareNumber.append(self.ArrayOfPicNumbers[index])

         # Add one more 
         if not self.IsEvenNumberOfSquares:
           self.imageBankIndexBySquareNumber.append(self.ArrayOfPicNumbers[self.NumPairsSquares])
         shuffle(self.imageBankIndexBySquareNumber)

	 # Mark all squares as covered. 
         self.IsCovered = []
         for index in range (0,self.NumSquares):
             self.IsCovered.append(True)

         # Resize all Images. 
         for imageIndex in range(0, len(self.imageFileNames)): 
           self.imageBank.append(pygame.image.load(self.imageFileNames[imageIndex]).convert())
           imageOrigX,imageOrigY = self.imageBank[imageIndex].get_size()
           imageOrigRatio = imageOrigX/imageOrigY
           displayBoxRatio = self.XPicMeas/self.YPicMeas
           # Resize Image to fit the box. 
           scaledImageX = 0
           scaledImageY = 0
           # Figure out if the display box  is wider or narrower than the image. 
           if (imageOrigRatio > displayBoxRatio):  
             scaledImageX = int(self.XPicMeas) 
             scaledImageY = int(self.YPicMeas * displayBoxRatio)
           elif (imageOrigRatio < displayBoxRatio):
             scaledImageX = int(self.XPicMeas * displayBoxRatio)
             scaledImageY = int(self.YPicMeas)
           else: 
             scaledImageX = int(self.XPicMeas)
             scaledImageY = int(self.YPicMeas)
             DebugMessage("Not Resizing image "+str(imageIndex)) 
           self.imageBank[imageIndex] = pygame.transform.scale(self.imageBank[imageIndex],(scaledImageX,scaledImageY))
           self.ImageRectBank.append(self.imageBank[imageIndex].get_rect())

         self.gameOverScreen = False
         self.blockEvents = False 
         self.redraw = False 
         self.firstClickedSquare = -1  
         self.secondClickedSquare = -1

     def GetSquareFromMousePos(self,mouseposx,mouseposy):
       colIndex = int(mouseposx/self.XPicMeasInclBorder)  
       rowIndex = int(mouseposy/self.YPicMeasInclBorder)  
       squareNumber = rowIndex*self.XSquaresInRow + colIndex
       return squareNumber


     def DrawGameScreen(self):
       self.screen.fill(WHITE)
       for colIndex in range (0,self.XSquaresInRow):
        for rowIndex in range (0,self.YSquaresInCol): 
          squareNumber = rowIndex*self.XSquaresInRow + colIndex
          imageBankIndex = self.imageBankIndexBySquareNumber[squareNumber]
          xPos = colIndex*self.XPicMeasInclBorder + self.Border
          yPos = rowIndex*self.YPicMeasInclBorder + self.Border
          self.screen.blit(self.imageBank[imageBankIndex],(xPos,yPos)) 
      #-- Draw Cover and label
          if self.IsCovered[squareNumber]:
            pygame.draw.rect(self.screen,WHITE,(xPos,yPos,self.XPicMeasInclBorder,self.YPicMeasInclBorder))
            myfont = pygame.font.SysFont("monospace", 45)
            label = myfont.render(str(squareNumber+1), 1, BLUE)
            label_width,label_height = label.get_size()
            label_x = xPos - self.Border + ((self.XPicMeasInclBorder-label_width)/2)
            label_y = yPos - self.Border + ((self.YPicMeasInclBorder-label_height)/2)
            self.screen.blit(label, (label_x,label_y))
				 
     def AllMatched(self):
      for index in range (0,self.NumSquares):
        if (self.IsCovered[index]):
          return False
      return True

     def SetAllMatched(self):
      for index in range (0,self.NumSquares):
        self.IsCovered[index] = False 
   
  
     def RecoverBothSquares(self):
      DebugMessage('Recovering Both squares')
      self.IsCovered[self.firstClickedSquare] = True 
      self.IsCovered[self.secondClickedSquare] = True 
      self.blockEvents = False
      self.redraw  = True 
      self.firstClickedSquare = -1 
      self.secondClickedSquare = -1 
		
     def RestartGame(self):
      self.done = True 


     def DrawGameOverScreen(self): 
      self.screen.fill(WHITE)
      myfont = pygame.font.SysFont("monospace", 30)
      label = myfont.render("You Won!", 1, BLUE)
      label_spacing = 6
      label_width,label_height = label.get_size()
      label_x = (self.MasterWindowX - label_width)/2
      label_y = (self.MasterWindowY - label_height)/2 
      self.screen.blit(label, (label_x,label_y))

      self.timer = Timer(2,self.RestartGame)
      self.timer.start(); 

     def ImageMatch (self):
      imageInFirstSquare = self.imageBankIndexBySquareNumber[self.firstClickedSquare]
      imageInSecondSquare = self.imageBankIndexBySquareNumber[self.secondClickedSquare]
      return (imageInFirstSquare == imageInSecondSquare)

     def ProcessEvent(self,squareClicked):
      DebugMessage ('Square Clicked'+str(squareClicked))
      # If we clicked a square, see if it was first or second. 
      # If a first, uncover it. 
      # If a second, uncover it and see if there was a match.  

      if (not squareClicked == -1):
        if (not self.IsCovered[squareClicked]):  # We already clicked this one. 
          return
        if (self.firstClickedSquare == -1):
          DebugMessage ('First Square Clicked '+ str( squareClicked))
          self.firstClickedSquare = squareClicked;
          self.IsCovered[self.firstClickedSquare] = False
        elif (self.secondClickedSquare == -1):
          DebugMessage ('Second Square Clicked ' + str( squareClicked))
          if not self.firstClickedSquare == squareClicked: 
            DebugMessage ('Second box diff from first')
            self.secondClickedSquare = squareClicked;
            self.IsCovered[self.secondClickedSquare] = False
            if (self.ImageMatch()):
              DebugMessage ('Match!')
              # We matched both squares. 
              self.firstClickedSquare = -1 
              self.secondClickedSquare = -1 
            else:
              DebugMessage ('We did not match')
           # Blank the two mismatch squares  
              self.blockEvents = True
              self.t = Timer(1.0,self.RecoverBothSquares)
              self.t.start()
          else: 
            DebugMessage ('Second Square Matched First Square Ignoring.', squareClicked)


# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)


# Loop until the user clicks the close button.
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 

def TestProcedure():
   # Verify we exit if No Pics available.  
   MyGame = GameStateClass("phonyPath");
   assert (MyGame.Valid == 0)
   return 1 



#
# Handler loop. I don't like main() to be any bigger than a screen length. 
#
#

def HandlerLoop(pygame,MyGame):
  while not MyGame.done:
    firstPass = True
    while not MyGame.done:
      eventHappened = False 
      squareClicked = -1
      # --- Main event loop
      if (MyGame.blockEvents):
        pygame.event.clear()
   
      if (pygame.event.peek):
        for event in pygame.event.get(): # User did something
          DebugMessage("Processing Event")
          if event.type == pygame.QUIT: # If user clicked close
            MyGame.done = True # Flag that we are done so we exit this loop
          elif event.type == pygame.MOUSEBUTTONDOWN: # If user clicked close
            eventHappened = True
            if event.button == 1:  # Left mouse button 
              mouseposx,mouseposy = pygame.mouse.get_pos();
              squareClicked = MyGame.GetSquareFromMousePos(mouseposx,mouseposy)
          elif event.type == pygame.KEYDOWN : # If user clicked close
            key = pygame.key.get_pressed()
            DebugMessage("Key Down")
            if event.key == pygame.K_q: 
              sys.exit(0)
            if event.key == pygame.K_e: 
             MyGame.SetAllMatched()
             
      # --- Game logic should go here
      if (eventHappened and (not squareClicked == -1)):
        MyGame.ProcessEvent(squareClicked)
    
      # --- Drawing code should go here
      if ((firstPass or eventHappened or MyGame.redraw) and 
             not MyGame.AllMatched()):
        DebugMessage ("Redrawing Screen")
        MyGame.DrawGameScreen()
        MyGame.redraw = False 
        firstPass = False
      elif (MyGame.AllMatched() and not MyGame.gameOverScreen):
        MyGame.gameOverScreen = True

      if (MyGame.gameOverScreen):
        MyGame.DrawGameOverScreen()
 
      pygame.display.flip()
      # --- Limit to 60 frames per second
      clock.tick(60)
  


# -------- Main Program Loop -----------

def main():

  result = TestProcedure()
  if not result == 1:
    print ("Failed Initial Tests")
    sys.exit(1)
  pygame.init()
  while 1: 
    print("Hit q key to make the game end prematurely") 
    print("Hit e key to make the game show end screen prematurely") 
    MyGame = GameStateClass("images")
    if (MyGame.Valid): 
      HandlerLoop(pygame,MyGame)

  del MyGame

main()
