
import pygame, sys, time, random


# Window size
frame_size_x = 720
frame_size_y = 480

# Difficulty settings :
    # Basic     ->  13
    # Easy      ->  18
    # Medium    ->  25
    # Hard      ->  30
    # Pro       ->  38
difficulty_level_select = [13,18,24,30,38]
difficulty=15

score = 0

# Colours (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialise game window
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rectangle = game_over_surface.get_rect()
    game_over_rectangle.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rectangle)
    show_score(1, red, 'times', 45)
    pygame.display.flip()
    time.sleep(1.75)
    pygame.quit()
    sys.exit()


# Score
def show_score(out, colour, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, colour)
    score_rectangle = score_surface.get_rect()
    if out == 0:
        score_rectangle.midtop = (frame_size_x/10, 15)
    else:
        score_rectangle.midtop = (frame_size_x/2, frame_size_y/1.8)
    game_window.blit(score_surface, score_rectangle)


def mainGame():
    global difficulty
    global score
    # Game variables
    snake_position = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

    food_position = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    direction = 'RIGHT'
    change_dir_to = direction

    # Main logic
    while True:
        for action in pygame.event.get():
            #If user clicks on cross button or press escape, close the game
            if action.type == pygame.QUIT or (action.type == pygame.KEYDOWN and action.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif action.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if action.key == pygame.K_UP or action.key == ord('w'):
                    change_dir_to = 'UP'
                if action.key == pygame.K_DOWN or action.key == ord('s'):
                    change_dir_to = 'DOWN'
                if action.key == pygame.K_LEFT or action.key == ord('a'):
                    change_dir_to = 'LEFT'
                if action.key == pygame.K_RIGHT or action.key == ord('d'):
                    change_dir_to = 'RIGHT'

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_dir_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_dir_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_dir_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_dir_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Changing the direction of snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing mechanism and increasing slight difficulty after every 4 scores
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
            score += 1
            food_spawn = False
            if int(score%4) == 0:
                difficulty += 1
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_position = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        # Showing snake on the screen
        game_window.fill(black)
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
            # .draw.rect(play_surface, colour, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)

        # Snake food
        pygame.draw.rect(game_window, blue, pygame.Rect(food_position[0], food_position[1], 10, 10))

        # Game Over conditions :

        # Getting out of bounds
        if snake_position[0] < 0 or snake_position[0] > frame_size_x-10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > frame_size_y-10:
            game_over()
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        show_score(0, white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        
        # Refresh rate
        fps_controller.tick(difficulty)


def welcome_screen():

    global difficulty
    while True:

        welcome_font = pygame.font.SysFont('times new roman', 75)
        welcome_surface = welcome_font.render('SNAKE GAME', True, pygame.Color(229,9,20))
        welcome_rectangle = welcome_surface.get_rect()
        welcome_rectangle.midtop = (frame_size_x/2, frame_size_y/6.7)
                    
        choose_font = pygame.font.SysFont('times new roman', 40)
        choose_surface = choose_font.render('select difficulty level by typing :', True, white)
        choose_rectangle = choose_surface.get_rect()
        choose_rectangle.midtop = (frame_size_x/2, frame_size_y/2.4)

        difficulty_font = pygame.font.SysFont('times new roman', 25)
        d1_surface = difficulty_font.render('1 for BASIC', True, white)
        d1_rectangle = d1_surface.get_rect()
        d1_rectangle.midtop = (frame_size_x/2, frame_size_y/1.88)
        d2_surface = difficulty_font.render('2 for EASY', True, white)
        d2_rectangle = d2_surface.get_rect()
        d2_rectangle.midtop = (frame_size_x/2, frame_size_y/1.7)
        d3_surface = difficulty_font.render('3 for MEDIUM', True, white)
        d3_rectangle = d3_surface.get_rect()
        d3_rectangle.midtop = (frame_size_x/2, frame_size_y/1.55)
        d4_surface = difficulty_font.render('4 for HARD', True, white)
        d4_rectangle = d4_surface.get_rect()
        d4_rectangle.midtop = (frame_size_x/2, frame_size_y/1.42)
        d5_surface = difficulty_font.render('5 for PRO', True, white)
        d5_rectangle = d5_surface.get_rect()
        d5_rectangle.midtop = (frame_size_x/2, frame_size_y/1.31)

        game_window.fill(black)
        game_window.blit(welcome_surface, welcome_rectangle)
        game_window.blit(choose_surface, choose_rectangle)
        game_window.blit(d1_surface, d1_rectangle)
        game_window.blit(d2_surface, d2_rectangle)
        game_window.blit(d3_surface, d3_rectangle)
        game_window.blit(d4_surface, d4_rectangle)
        game_window.blit(d5_surface, d5_rectangle)

        for action in pygame.event.get():
            #If user clicks on cross button or press escape, close the game
            if action.type == pygame.QUIT or (action.type == pygame.KEYDOWN and action.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            # 
            elif action.type == pygame.KEYDOWN:
                # user clicks 1,2,3,4 or 5 for choosing difficulty level
                if action.key == pygame.K_1:
                    difficulty=difficulty_level_select[0]
                    time.sleep(1)
                    mainGame()
                if action.key == pygame.K_2:
                    difficulty=difficulty_level_select[1]
                    time.sleep(1)
                    mainGame()
                if action.key == pygame.K_3:
                    difficulty=difficulty_level_select[2]
                    time.sleep(1)
                    mainGame()
                if action.key == pygame.K_4:
                    difficulty=difficulty_level_select[3]
                    time.sleep(1)
                    mainGame()
                if action.key == pygame.K_5:
                    difficulty=difficulty_level_select[4]
                    time.sleep(1)
                    mainGame()
                    
        # Refresh screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)



if __name__ =="__main__":

    #initialize all pygame's modules
    pygame.init() 
    
    pygame.display.set_caption('Snake Game by Aviral')
    print("Game successfully initialised")

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()

    while True:

        welcome_screen()

