import random
import curses

stdscr = curses.initscr() # initialize screen
curses.curs_set(0) # make cursor invisible
height, width = stdscr.getmaxyx() # max height and width of screen
window = curses.newwin(height, width, 0, 0) # creates window of max screen size with starting location (0,0)
window.keypad(1) # make returnable values like curses.KEY_LEFT
window.timeout(100) # refresh screen every 100 milliseconds

#initializing snake and food
snk_x = width/4
snk_y = height/2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]
# display food
food = [height/2, width/2]
window.addch(food[0], food[1], curses.ACS_DIAMOND) # addch takes (y, x, cons chtype ch)

key = curses.KEY_RIGHT # set snake initial direction to be right

# print directions
window.addstr(0, 0, "Press ESC to exit or Space to pause.")

# initialize score
score = 0
window.addstr(1, 0, "Score: "+str(score))

# exit if esc pressed
while key != 27:
    # update value of key according to user input
    next_key = window.getch()
    if next_key == -1:
        key = key
    else:
        key = next_key

    # player can lose if: snake is out of the screen or intersecting itself
    if snake[0][0] in [0, height-1] or snake[0][1] in [0, width-1] or snake[0] in snake[1:]:
        break

    if key == ord(' '): # if space key pressed, pause
        continue
    
    # adding new head to snake based on given direction
    new_head = [snake[0][0], snake[0][1]] # this is the old head
    # modify old head as needed
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1
    # add new head to beginning of array
    snake.insert(0, new_head) 

    # if snake hits the food
    if snake[0] == food:
        food = None
        while food is None:
            new_food = [
                random.randint(1, height-2),
                random.randint(1, width-2)
            ]
            
            if new_food not in snake:
                food = new_food
            else:
                food = None
        window.addch(food[0], food[1], curses.ACS_DIAMOND) # now display the new food
        # update score
        score+=1
        window.addstr(1, 0, "Score: "+str(score))
    else:
        tail = snake.pop() # take off the tail to preserve length because we've added the head already
        window.addch(tail[0], tail[1], ' ') # remove tail display
    
    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

curses.endwin()
curses.curs_set(1)
quit()