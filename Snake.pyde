import os
import random

#define global variables
BOARD_W = 600   #board width 
BOARD_H = 600   #board height
TILE_W = 30     #each image's pixel width
TILE_H = 30     #each image's pixel height
NUM_C = BOARD_W/TILE_W    #number of columns
NUM_R = BOARD_H/TILE_H    #number of rows
STARTING_R = NUM_C/2*TILE_W  #initial y position of the snake
STARTING_C = NUM_R/2*TILE_H  #initial x position of the snake
INITIAL_LENGTH = 2    #initial tail length of the snake

global score     #keep track of the score
score = 0

global newFood  #control creating the food
newFood = False

global gameOver   #check game over status
gameOver = False

global collide    #check if the snake crashes into itself
collide = False

path = os.getcwd() # get the current working directory of the folder this file is stored in

#Define the snake's head, including position and direction
class Head:
    def __init__(self,x,y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.img1 = loadImage(path + "/images/" + "head_left.png")  #load the left head  
        self.img2 = loadImage(path + "/images/" + "head_up.png")    #load the up head
        self.direction = RIGHT   #default/initial heading direction
    
    #display the head image according to the direction it's heading 
    def display(self):
        if self.direction == RIGHT:        #flip the headleft image to head right through cropping
            image(self.img1, self.x, self.y, TILE_W, TILE_H, TILE_W,0,0,TILE_H)
        if self.direction == LEFT:
            image(self.img1, self.x, self.y, TILE_W, TILE_H)
        if self.direction == UP:
            image(self.img2, self.x, self.y, TILE_W, TILE_H)
        if self.direction == DOWN:         #flip the headup image to head down through cropping
            image(self.img2, self.x, self.y, TILE_W, TILE_H, TILE_W,TILE_H,0,0)
        
#Define the tails, including position, radius and color
class Body:
    def __init__(self,x,y,r,c):
        self.x = x       #for the positionX of the tail element
        self.y = y       #for the positionY of the tail element
        self.r = r       #for the raduis of the tail element
        self.c = c       #for the color of the tail
    
    def display(self):
        fill(self.c)
        noStroke()
        circle(self.x,self.y,self.r)

#Display the head and the tails in the snake list
class Snake(list):
    def __init__(self,x,y,r):
        self.x = x        #positionX of the snake's head
        self.y = y        #positionY of the snake's head
        self.r = r        #radius of the tail
        self.vx = TILE_W  #moving speed at x axis
        self.vy = 0       #moving speed at y axis
        self.tailX = self.x + TILE_W/2  #X position where the head is drawn if the head is a circle (for copy position purpose)
        self.tailY = self.y + TILE_H/2  #Y position where the head is drawn if the head is a circle (for copy position purpose)
        
        self.append(Head(self.x,self.y, RIGHT))         #store the head in the snake list
        for n in range(INITIAL_LENGTH):                 #store the intial 2 tails in the snake list
            self.append(Body(self.tailX - TILE_W* (n+1), self.tailY, TILE_W,color(80,153,32)))
        
        self.key_handler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}   #handler to control the snake's direction, determined by keyboard input
    
    #show the snake (including head and tails)
    def show_snake(self):
        for element in self:
            element.display()
        
    # move the snake by updating each element(head and tails)'s position
    def move(self):
        
        #move according to the keyborad's input
        #avoid going in opposite direction
        if self.key_handler[RIGHT] and self[0].direction != LEFT:  
            self.vy = 0            #stop moving vertically
            self.vx = TILE_W       #start moving horizontally, by each unit 
            self[0].direction = RIGHT     #control the head image (which direction it faces)
        if self.key_handler[LEFT] and self[0].direction != RIGHT:
            self.vy = 0  
            self.vx = -TILE_W 
            self[0].direction = LEFT
        if self.key_handler[UP] and self[0].direction != DOWN: 
            self.vx = 0  
            self.vy = -TILE_H 
            self[0].direction = UP
        if self.key_handler[DOWN] and self[0].direction != UP:    
            self.vx = 0    
            self.vy = TILE_H
            self[0].direction = DOWN  
                      
        self.x = self.x + self.vx      #update the snake's head position based on velocity
        self.y = self.y + self.vy      
    
        #make the following tails follow the previous one
        for n in range(len(self)-1,0,-1):
            if n>= 2:
                self[n].x = self[n-1].x
                self[n].y = self[n-1].y
                
        #update the first tail's drawing point relative to the head's drawing point
        self[1].x = self.tailX
        self[1].y = self.tailY

        #adjust the drawing center relative to the position of the head
        self.tailX = self.x + TILE_W/2
        self.tailY = self.y + TILE_H/2

        #move the head
        self[0].x = self.x
        self[0].y = self.y
        
  
    
    #update the snake's movement
    def update(self):
        global gameOver   #introduce the global variable to check for game status
        global collide    #introduce the global variable to check if the snake collides into itself
        
        self.show_snake()   #continuously show the snake 
        
        if (collide == False):   #if the snake doesn't collide into itself
            #if the snake did not hit the edge, make it move
            if self.x + TILE_W < BOARD_W and self.x > 0 and self.y > 0 and self.y + TILE_H < BOARD_H:   
                self.move()
            
            #if the snake hits the edge but it is changing direction, make it move
            #if the snake is moving on the right edge, make it move within a certain limit
            elif self.x + TILE_W == BOARD_W and self[0].direction != RIGHT:    
                if self.y + TILE_H != BOARD_H and self.y != 0:  #if the snake hasn't reached the corner, make it move   
                    self.move()
                elif self.y + TILE_H == BOARD_H:    #if the snake has reached the right corner and is changing direction, make it move
                    if self[0].direction == UP or self[0].direction == LEFT:
                        self.move()
                    else:
                        gameOver = True      #if it collides into the corner without changing direction, game is over
                elif self.y == 0:
                    if self[0].direction == LEFT or self[0].direction == DOWN:
                        self.move()
                    else:
                        gameOver = True
                else:
                    gameOver = True
                    
            #if the snake is moving at the left edge
            elif self.x == 0 and self[0].direction != LEFT:
                if self.y + TILE_H != BOARD_H and self.y != 0:
                    self.move()
                elif self.y + TILE_H == BOARD_H:
                    if self[0].direction == UP or self[0].direction == RIGHT:
                        self.move()
                    else:
                        gameOver = True     
                elif self.y == 0:
                    if self[0].direction == RIGHT or self[0].direction == DOWN:
                        self.move()
                    else:
                        gameOver = True                                   
                else:
                    gameOver = True
                    
            #if the snake hits the top edge
            elif self.y == 0 and self[0].direction != UP:
                if self.x + TILE_W != BOARD_W and self.x != 0:
                    self.move()
                else:
                    gameOver = True
            
            # if the snake hits the bottom edge
            elif self.y + TILE_H == BOARD_H and self[0].direction != DOWN:
                if self.x + TILE_W != BOARD_W and self.x != 0:
                    self.move()
                else:
                    gameOver = True
            else:
                gameOver = True
        
        else:         #if the snake collides into itself, game is over
            gameOver = True
            
        #check if the head has hit any of the tail
        for n in range(len(self)-1):
            if self.x == self[n+1].x - TILE_W/2 and self[0].y == self[n+1].y - TILE_H/2:
                collide = True
                gameOver = True
                self.vx = 0
                self.vy = 0             

#Define the food, including position and type
class Food:
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.type = type
        if type == "apple":
            self.food = loadImage(path + "/images/" + "apple.png") 
        elif type == "banana":
            self.food = loadImage(path + "/images/" + "banana.png") 
    
    #check if the food has been hit/eaten by the snake
    def checkCollision(self):
        #check condition1: if the head hits the food from the x axis
        if self.y == snake[0].y and snake.vy == 0 and abs(self.x - snake[0].x) < TILE_W:  
            #check which kind of fruit the snake crashes into
            if self.type == "apple":        
                snake.append(Body(snake[len(snake)-1].x, snake[len(snake)-1].y, TILE_W, color(173,48,32)))  #append a new red tail to the snake list
            elif self.type == "banana":
                snake.append(Body(snake[len(snake)-1].x, snake[len(snake)-1].y, TILE_W, color(251,226,76)))  #append a new yellow tail to the snake list
            
            #remove the eaten food
            game.fruits.pop()
            
            #set the newFood to true so that a new one could be created 
            global newFood 
            newFood = True
            
            #keep track of the score
            global score       
            score +=1
            
        #check condition2: if the head hits the food from the y axis 
        elif self.x == snake[0].x and snake.vx == 0 and abs(self.y - snake[0].y) < TILE_H:
            if self.type == "apple":        
                snake.append(Body(snake[len(snake)-1].x, snake[len(snake)-1].y, TILE_W, color(173,48,32)))  #append a new red tail to the snake list
            elif self.type == "banana":
                snake.append(Body(snake[len(snake)-1].x, snake[len(snake)-1].y, TILE_W, color(251,226,76)))  #append a new yellow tail to the snake list
            
            #remove the eaten food
            game.fruits.pop()
            
            #set the newFood to true so that a new one could be created 
            global newFood 
            newFood = True
            
            #keep track of the score
            global score        
            score +=1
        
    #show the food's picture according to the inputs
    def display(self):
        image(self.food,self.x,self.y,TILE_W,TILE_H)
    
    #update the methods 
    def update(self):
        self.display()
        self.checkCollision()

#Define the grids (not shown on screen)
class Grid:
    #initialize grids attribute: position and value
    def __init__(self,r,c):
        self.r = r
        self.c = c
        self.v = r*NUM_C + c
        
    #displaying the grids without visibility
    def display(self):
        noFill()
        rect(self.c*TILE_W, self.r*TILE_H, TILE_W, TILE_H)
    
class Game(list):
    #initialize the board's attributes: rows and columns
    def __init__(self,r,c):
        self.r = r
        self.c = c 
        self.fruits = []      #create a list to store foods (control food display)
        self.randPosX = random.randint(0,NUM_C-1)      #create a random position X and Y
        self.randPosY = random.randint(0,NUM_R-1)
        
        #create a food when the game starts
        if self.randPosX % 2 == 0 and self.randPosY & 2 == 0:     #add some randomness to the food displayed
            self.fruits.append(Food(self.randPosX * TILE_W, self.randPosY * TILE_H, "apple"))
        else:
            self.fruits.append(Food(self.randPosX * TILE_W, self.randPosY * TILE_H, "banana"))
        
        #create the grids in the game based on input rows and cols
        for r in range(self.r):
            for c in range(self.c):
                self.append(Grid(r,c))
    
    #display the board with invisible grids (make it visible during programming for easier check)
    def display(self):
        #show the grids
        for grid in self:
            grid.display()
        
        #show the score at the upper right corner
        textSize(TILE_W/2)
        fill(0,0,0)
        text("Score:" + str(score), BOARD_W - TILE_W*2, TILE_H/2)
    
        #create a food when the existing food has been eaten
        global newFood
        if (newFood == True):
            self.randPosX = random.randint(0,NUM_C-1)      #create a random position X and Y
            self.randPosY = random.randint(0,NUM_R-1)
            
            #avoid generating the position that overlaps with the snake's head and tails
            for n in range(len(snake)-1):
                if n==0:     #check if the food doesn't collide with the head
                    while snake[n].x == self.randPosX and snake[n].y == self.randPosY:  #if the snake's position overlaps with the randomly generated position
                        self.randPosX = random.randint(0,NUM_C-1)      #create the new random position until it's different than the snake's
                        self.randPosY = random.randint(0,NUM_R-1)   
                else:     #for the tails
                    while snake[n].x - TILE_W/2 == self.randPosX and snake[n].y + TILE_H/2 == self.randPosY:
                        self.randPosX = random.randint(0,NUM_C-1)      #create the randomly position
                        self.randPosY = random.randint(0,NUM_R-1)  
                        
            #display the new food in randomness          
            if self.randPosX % 2 == 0 or self.randPosY & 2 == 0:    
                self.fruits.append(Food(self.randPosX * TILE_W, self.randPosY * TILE_H, "apple"))
            else:
                self.fruits.append(Food(self.randPosX * TILE_W, self.randPosY * TILE_H, "banana"))
                
            newFood = False  #set the boolean to false so that it only creates food once
        
        #display the food 
        for fruit in self.fruits:
            fruit.update()
        
        #show the snake 
        snake.update()
        
        #check for win situation
        global gameOver
        if len(snake) == NUM_R*NUM_C:             #if the snake fill the whole screen, then game is over
            gameOver = True
        
        #if game over condition has been met, display the text
        if (gameOver == True):
            textSize(TILE_W)
            fill(200, 48, 32)
            text("Game Over! Click to play again!", TILE_W*2.5, BOARD_H-TILE_H)
        
snake = Snake(STARTING_C, STARTING_R, TILE_W)     #initialize the snake
game = Game(NUM_R,NUM_C)       #initialize the game

def setup():
    size(BOARD_W,BOARD_H)
    
def draw():
    if frameCount%20 == 0:
        background(205)
        game.display()    #continously updating the game's status

#keyboard inputs that control the snake's moving direction
#make it lasting (not setting the handler value once) so that checking the movement status would be easier
def keyPressed():
    if keyCode == LEFT:
        snake.key_handler[LEFT] = True
        snake.key_handler[RIGHT] = False
        snake.key_handler[UP] = False
        snake.key_handler[DOWN] = False
    if keyCode == RIGHT:
        snake.key_handler[RIGHT] = True
        snake.key_handler[LEFT] = False
        snake.key_handler[UP] = False
        snake.key_handler[DOWN] = False
    if keyCode == UP:
        snake.key_handler[UP] = True
        snake.key_handler[RIGHT] = False
        snake.key_handler[LEFT] = False
        snake.key_handler[DOWN] = False
    if keyCode == DOWN:
        snake.key_handler[DOWN] = True
        snake.key_handler[RIGHT] = False
        snake.key_handler[UP] = False
        snake.key_handler[LEFT] = False

#mouse click to restart the game
def mouseClicked():
    global gameOver  #introduce the global variable to check for game status
    global score  #introduce the global variable to reset score
    global newFood #introduce the global variable to control food creation
    global collide #introduce the global variable to check if the snake crashes into itself
    
    #reset everything to initial state
    if (gameOver == True):
        gameOver = False   #set it to false so that the game could be restarted
        collide = False    #set it to false so that the snake could move and check if it collides into itself in the next round
        score = 0          #set the score back to 0
        
        #delete the current food and create a new one
        game.fruits.pop()
        newFood = True
        
        #delete everything in the snake list besides the head
        for n in range(len(snake)-1):
            snake.pop()
        snake.x = STARTING_C         #set the snake to its initial position
        snake.y = STARTING_R
        snake[0].direction = RIGHT   #set the snake to its initial direction
        snake.vx = TILE_W    #reset moving speed at x axis
        snake.vy = 0         #reset moving speed at y axis
        snake.tailX = snake.x + TILE_W/2  #reset the starting point to draw the tail
        snake.tailY = snake.y + TILE_H/2 
        snake.key_handler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}   #reset the handler to control the snake's direction
        for n in range(INITIAL_LENGTH):               #store the intial 2 tails in the snake list
            snake.append(Body(snake.tailX - TILE_W* (n+1), snake.tailY, TILE_W,color(80,153,32)))
    

            
