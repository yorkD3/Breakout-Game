# Nell Schafer and Darryl York
# January 26, 2020
# CS 111 Lab 2

"""This program (once you have finished it) implements the Breakout game."""

from pgl import GWindow, GOval, GRect, GTimer, GLabel
import random
from dataclasses import dataclass

# Constants

GWINDOW_WIDTH = 360               # Width of the graphics window
GWINDOW_HEIGHT = 600              # Height of the graphics window
N_ROWS = 5                        # Number of brick rows
N_COLS = 10                       # Number of brick columns
BRICK_ASPECT_RATIO = 4 / 1        # Width to height ratio of a brick
BRICK_TO_BALL_RATIO = 3 / 2       # Ratio of brick width to ball size
BRICK_TO_PADDLE_RATIO = 2 / 3     # Ratio of brick to paddle width
BRICK_SEP = 4                     # Separation between bricks
TOP_FRACTION = 0.2                # Fraction of window above bricks
BOTTOM_FRACTION = 0.05            # Fraction of window below paddle
N_BALLS = 3                       # Number of balls in a game
TIME_STEP = 10                    # Time step in milliseconds
INITIAL_Y_VELOCITY = 3.0          # Starting y velocity downward
MIN_X_VELOCITY = 1.0              # Minimum random x velocity
MAX_X_VELOCITY = 3.0              # Maximum random x velocity
BRICK_COLORS = ["Red", "Orange",  # List of the colors for rows of bricks from
                "Green", "Cyan",  # top to bottom
                "Blue"]
NUM_BRICKS = 50                   # Number of initial bricks

# Derived constants

BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO
PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO
PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO
PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT
BALL_SIZE = BRICK_WIDTH / BRICK_TO_BALL_RATIO

@dataclass()
class GameState:
    num_bricks: int = 0
    balls_left: int = 0
    ball_x_vel: float = 0
    ball_y_vel: float = 0
    update_timer: GTimer = None

def start_round(gw, game_state, update_fn):
    """initialize the round to start called update_fn once the user clicks the mouse"""
    if game_state.update_timer:
        game_state.update_timer.stop()
    def onclick(e):
        game_state.update_timer = gw.setInterval(update_fn, TIME_STEP)
        gw.eventManager.clickListeners.pop()
    gw.addEventListener("click", onclick)

def end_game(game_state):
    if game_state.update_timer:
        game_state.update_timer.stop()

def breakout():
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    game_state = GameState()
    game_state.balls_left = N_BALLS - 1
    game_state.num_bricks = NUM_BRICKS

    # CREATE THE PADDLE
    paddle = GRect(0, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT) 
    paddle.setFilled(True)
    paddle.setColor("Black")
    gw.add(paddle)

    def update_paddle(e):
        """function to update the paddle's location based on the mouse position"""
        x = e.getX()
        if x < 0 :
            paddle.setLocation(0, PADDLE_Y)
        elif x > GWINDOW_WIDTH - PADDLE_WIDTH :
            paddle.setLocation(GWINDOW_WIDTH - PADDLE_WIDTH, PADDLE_Y) #Why does this keep going off of the right edge?
        else :
            paddle.setLocation(x, PADDLE_Y)
        
    gw.addEventListener("mousemove", update_paddle) 


    # CREATE THE BALL 
    ball = GOval(GWINDOW_WIDTH / 2 - BALL_SIZE / 2, GWINDOW_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE) 
    ball.setFilled(True)
    ball.setColor("Black")
    gw.add(ball)
    # set game_state.ball_x_vel and game_state.ball_y_vel
    game_state.ball_x_vel = random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY) 
    r = random.random()
    if r < 0.5 :
       game_state.ball_x_vel = game_state.ball_x_vel
    else :
        game_state.ball_x_vel = -game_state.ball_x_vel
    
    game_state.ball_y_vel = INITIAL_Y_VELOCITY
    print("Balls Left", game_state.balls_left)

    # CREATE THE BRICKS 
    y = GWINDOW_HEIGHT * TOP_FRACTION 
    for row in range (N_ROWS) :
        color = BRICK_COLORS [row % len(BRICK_COLORS)]
        x = BRICK_SEP      
        for column in range (N_COLS) :
            brick = GRect(x, y, BRICK_WIDTH,BRICK_HEIGHT)
            brick.setFilled(True)
            brick.setColor(color)
            gw.add(brick)
            x = x + BRICK_WIDTH + BRICK_SEP
        y = y + BRICK_HEIGHT + BRICK_SEP 

    

            
        
        
        


    # FILL IN THE CODE FOR THIS FUNCTION ACCORDING TO THE STEPS OUTLINED IN THE COMMENTS (STEP 3 and 5)
    def update_ball():
        """
        function to update the ball's position and handle any collisions 
        with walls, paddle or bricks
        """
        
        # move the ball according to game_state.ball_x_vel and game_state.ball_y_vel
        # UNFINISHED
        object = ball
        x = object.getX()
        if x > (GWINDOW_WIDTH - BALL_SIZE) :
            game_state.ball_x_vel = -game_state.ball_x_vel
        elif x < 0 :
            game_state.ball_x_vel = -game_state.ball_x_vel
        y = object.getY()
        if y < 0 :
            game_state.ball_y_vel = -game_state.ball_y_vel
        elif y > (GWINDOW_HEIGHT - BALL_SIZE) :
            game_state.balls_left -= 1
            if game_state.balls_left >= 0 :
                print("Balls Left", game_state.balls_left)
            if game_state.balls_left >= 0 :
                ball.setLocation (GWINDOW_WIDTH / 2 - BALL_SIZE / 2, GWINDOW_HEIGHT / 2 - BALL_SIZE / 2)
                game_state.ball_x_vel = random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY) 
                r = random.random()
                if r < 0.5 :
                    game_state.ball_x_vel = game_state.ball_x_vel
                else :
                    game_state.ball_x_vel = -game_state.ball_x_vel
                game_state.ball_y_vel = INITIAL_Y_VELOCITY
                start_round(gw, game_state, update_ball)
            elif game_state.balls_left < 0 :
                end_game(game_state) #GAME DOESNT END AHHHHHHHHHHH
                print("Game Over")
                Reset = input("Would you like more lives? Y/N: ")
                #FIGURE THIS OUT OR DELETE:
                # if Reset == "Y" or Reset == "y" :
                #     print("Yay")
                #     gw.remove(gw)
                #     # game_state.balls_left = N_BALLS
                #     # game_state.num_bricks = NUM_BRICKS 
                #     breakout()
                #     start_round(gw, game_state, update_ball)
                # elif Reset == "N" or Reset == "n" :
                #     print("L8r Sk8r")

        object.move(game_state.ball_x_vel, game_state.ball_y_vel)
    
        # check if the ball has hit one of the side walls
        # if so, reverse the x velocity
        
        # check if the ball has hit the top (y is 0 at the top of the game window)
        # if so, reverse the y velocity

        # check if the ball has hit the bottom (y is GWINDOW_HEIGHT at the bottom of the game window)
        # if so
        #     if there are balls left
        #         decrease game_state.balls_left
        #         reset the ball to its starting location
        #         reset game_state.ball_x_vel and game_state.ball_y_vel
        #         call start_round with arguments gw, game_state, and update_ball
        #     else
        #         end the game by calling end_game(game_state)
        #         

        collider = check_collision(ball.getX(), ball.getY())
        # if collider is not None, then the ball is colliding with the paddle or bricks
        #     if collider is the paddle, reverse the y velocity
        if collider == paddle :
            game_state.ball_y_vel = -game_state.ball_y_vel
        #     otherwise, the ball has hit a brick, remove it (gw.remove(collider)) and decrease the number of bricks
        elif collider != None :
            game_state.ball_y_vel = -game_state.ball_y_vel
            gw.remove(collider)
            game_state.num_bricks = game_state.num_bricks - 1
            if game_state.num_bricks == 0 :
                end_game(game_state) 
                print("WINNER WINNER CHICKEN DINNER!")
                # FIGURE THIS OUT OR DELETE:
                # Reset = input("Play Again? Y/N: ")
                # if Reset == str(Y) or str(y) :
                #     breakout
                # elif Reset == str(N) or str(n) :
                #     print("L8r Sk8r")
        # if there are no more bricks, end_game(game_state)


    # FINISH THIS FUNCTION (STEP 5)
    def check_collision(x, y):
        """
        use gw.getElementAt to check for collisions with the ball
        return the colliding element or None if there is no collision
        x, y are the coordinates of the ball's upper left corner
        """
        # check the upper left corner
        elem = gw.getElementAt(x, y)
        if elem != None:
            return elem

        # check the upper right corner
        # YOUR CODE HERE
        elem = gw.getElementAt(x + BALL_SIZE, y)
        if elem != None:
            return elem
 
        # check the lower left corner
        # YOUR CODE HERE
        elem = gw.getElementAt(x, y + BALL_SIZE)
        if elem != None:
            return elem

        # check the lower right corner
        # YOUR CODE HERE
        elem = gw.getElementAt(x + BALL_SIZE, y + BALL_SIZE)
        if elem != None:
            return elem
    

    start_round(gw, game_state, update_ball)

if __name__ == "__main__":
    breakout()