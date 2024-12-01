import random
import pygame
import sqlite3
pygame.init()
#sql
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("high_scores.db")
cursor = conn.cursor()

# Create a table for storing the high score
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        high_score INTEGER NOT NULL
    )
''')
# Initialize the high score if not already present
cursor.execute("SELECT COUNT(*) FROM scores")
response = cursor.fetchone()
if response[0] == 0:
    cursor.execute("INSERT INTO scores (high_score) VALUES (0)")
    high_score = 0
else: 
    cursor.execute("SELECT high_score from scores where id = 1")
    high_score = cursor.fetchone()[0]
conn.commit()
conn.close()

#icon
icon_image = pygame.image.load("icon.png")  
pygame.display.set_icon(icon_image) 


#music
pygame.mixer.init()
pygame.mixer.music.load("retro-game-music-245230.mp3")
jumpsound= pygame.mixer.Sound("jump-up-245782.mp3")
pygame.mixer.music.set_volume(0.5)
jumpsound.set_volume(0.3)
pygame.mixer.music.play(-1)

# images

frog1 = pygame.image.load("phrog nice_001.png")
frog2 = pygame.image.load("phrog nice_031.png")
swamp1 = pygame.image.load("swamp.png")
base1 = pygame.image.load("base.png")
crog1 = pygame.image.load("sprite_061.png")
end1= pygame.image.load("image.png")

# Scalng the image
frog = pygame.transform.scale(frog1, (80, 80))
frog2 = pygame.transform.scale(frog2, (80, 80))
swamp = pygame.transform.scale(swamp1, (1280, 620))
base = pygame.transform.scale(base1, (1280, 100))
crog = pygame.transform.scale(crog1, (100, 100))
end = pygame.transform.scale(end1, (1280, 720))
# constant values
white = (255, 255, 255)
black = (0, 0, 0)
greenish_blue = (13, 152, 186)
greenish_white = (235, 255, 235)
dark_green = (6, 64, 43)
croc_color1 = (115, 109, 88)
croc_color2 = (115, 120, 88)
croc_color3 = (115, 130, 94)
WIDTH = 1280
HEIGHT = 720

# Variable Values
score = 0
player_x = 0
player_y = 0
gravity = 1
altitude_change = 0
direction_change = 0
croc_pos = {1:840, 2:1580, 3:2020}
croc_speed = 5
active = False

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Phrog")
background = greenish_blue
fps = 60
font = pygame.font.Font('freesansbold.ttf', 40)
timer = pygame.time.Clock()

if __name__ == "__main__":
    running = True
    while running:
        timer.tick(fps)
        screen.blit(swamp, (0, 0))
        score_value = font.render(f'SCORE: {score}', True, white)
        screen.blit(score_value, (530, 100))
        floor = pygame.draw.rect(screen, dark_green, [0, 620, WIDTH, 100])
        screen.blit(base, (0, 620))#platform
        player = screen.blit(frog, [player_x, player_y])
        croc1 = screen.blit(crog, [croc_pos[1], 530])
        croc2 = screen.blit(crog, [croc_pos[2], 530])
        croc3 = screen.blit(crog, [croc_pos[3], 530])
        jumping = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    
            if event.type == pygame.KEYDOWN and not active:
                a = True
                if event.key == pygame.K_SPACE:
                    croc_pos = {1:840, 2:1580, 3:2020}
                    player_x = 50
                    score = 0
                    croc_speed = 5
                    active = True
                    
                    
    
            if event.type == pygame.KEYDOWN and active:
            
                if event.key == pygame.K_SPACE and altitude_change == 0:
                    altitude_change = 25
                    jumpsound.play()
                if event.key == pygame.K_a:
                    direction_change = -5
                if event.key == pygame.K_d:
                    direction_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    direction_change = 0
                if event.key == pygame.K_d:
                    direction_change = 0
    
        for i in croc_pos:
            if active:
                croc_pos[i] -= croc_speed
                if croc_pos[i] < -60:
                    new_pos = random.randint(1600, 2000)
                    croc_pos[i] = new_pos
                    score += 2
                    croc_speed += (score / 2) * 0.03
                if player.colliderect(croc1) or player.colliderect(croc2) or player.colliderect(croc3):
                    active = False
         
        if player_y < 550:
            screen.blit(frog2, [player_x, player_y])
        
    
        # conditions to make sure phrog doesnt leave the screen
        if 0 <= player_x <= 1230:
            player_x += direction_change
        if player_x < 0:
            player_x = 0
        if player_x > 1230:
            player_x = 1230
    
        if altitude_change > 0 or player_y < 550:
            player_y -= altitude_change
            altitude_change -= gravity
        if player_y > 550:
            player_y = 550
        if player_y == 550 and altitude_change < 0:
            altitude_change = 0
        if score > high_score:
            high_score = score
            conn = sqlite3.connect("high_scores.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE scores SET high_score = ? WHERE id = 1", (high_score,))
            conn.commit()
            conn.close()
        if active == False :
            screen.blit(end, (0, 0))  
            high_score_text = font.render(f'HIGH SCORE:{high_score}', True, white)
            screen.blit(high_score_text, (510, 290))
            score_value = font.render(f'SCORE:{score}', True, white)
            screen.blit(score_value, (90, 90))
        pygame.display.flip()
    pygame.quit()