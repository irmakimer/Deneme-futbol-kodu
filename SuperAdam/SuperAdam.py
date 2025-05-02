import pygame
import math
import sys
import random
import time
import os

pygame.init()

# Ekran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Futbol Oyunu")
clock = pygame.time.Clock()

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (0, 200, 0)

# Görseller
player_standing = pygame.image.load('run1.png')
ball_image = pygame.image.load("futboltopu.png").convert_alpha()
ball_image = pygame.transform.scale(ball_image, (50, 50))
background_image = pygame.image.load("stadyum.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

goal_image = pygame.image.load("kale.png").convert_alpha()

# Şut animasyon görselleri
shoot_anim = [
    pygame.image.load("run2.png"),
    pygame.image.load("run3.png"),
    pygame.image.load("run4.png")
]



# Karakter
width, height = 64, 64
vel = 5

animation_timer = 0
frame_delay = 5  # Her animasyon karesi 5 frame boyunca gösterilecek


# Top
ball_start = [150, HEIGHT - 50]
ball_pos = list(ball_start)
ball_radius = 25
ball_angle = 45
power = 20
ball_in_motion = False
velocity = [0, 0]
gravity = 0.5
score = 0
total_shots = 0
bounces = 0
bounce_limit = 3
bounce_damping = 0.7

# Şut animasyonu kontrol
shooting_animation = False
shooting_frame = 0

# Fontlar
font = pygame.font.SysFont(None, 28)
title_font = pygame.font.SysFont(None, 64)
score_font = pygame.font.SysFont(None, 48)

# Menü
menu = True
game_over = False
start_time = None
time_limit = 90
elapsed_time = 0

def random_hoop():
    hoop_y = random.randint(100, HEIGHT - 200)
    hoop_h = random.randint(80, 140)
    return pygame.Rect(WIDTH - 120, hoop_y, 30, hoop_h)

def load_high_score():
    if os.path.exists("highest_score.txt"):
        with open("highest_score.txt", "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open("highest_score.txt", "w") as f:
        f.write(str(score))

high_score = load_high_score()
hoop = random_hoop()

def draw_trajectory(pos, angle, power):
    points = []
    rad = math.radians(angle)
    vel_x = math.cos(rad) * power * 0.5
    vel_y = -math.sin(rad) * power * 0.5
    for t in range(50):
        dx = pos[0] + vel_x * t * 0.2
        dy = pos[1] + vel_y * t * 0.2 + 0.5 * gravity * (t * 0.2) ** 2
        if dy > HEIGHT:
            break
        points.append((int(dx), int(dy)))
    if len(points) > 1:
        pygame.draw.lines(screen, WHITE, False, points, 2)

def reset_ball():
    global ball_pos, velocity, ball_in_motion, bounces
    ball_pos = list(ball_start)
    velocity = [0, 0]
    bounces = 0
    ball_in_motion = False

def draw_menu():
    screen.blit(background_image, (0, 0))
    title = title_font.render("Futbol Oyunu", True, BLACK)
    start_text = font.render("ENTER - Başlat", True, BLACK)
    quit_text = font.render("ESC - Çıkış", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 280))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 320))
    pygame.display.flip()

def draw_game_over():
    screen.blit(background_image, (0, 0))
    game_over_text = title_font.render("Oyun Bitti!", True, RED)
    score_text = score_font.render(f"Skor: {score}", True, BLACK)
    high_score_text = score_font.render(f"En Yüksek Skor: {high_score}", True, GREEN)
    restart_text = font.render("ENTER - Yeniden Başlat", True, BLACK)
    quit_text = font.render("ESC - Çıkış", True, BLACK)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 180))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 290))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 350))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 380))
    pygame.display.flip()

# Ana Oyun Döngüsü
while True:
    if menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            menu = False
            start_time = time.time()
            score = 0
            total_shots = 0
            elapsed_time = 0
            reset_ball()
            hoop = random_hoop()
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        continue

    if game_over:
        draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_over = False
            menu = True
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        continue

    clock.tick(60)
    screen.blit(background_image, (0, 0))
    elapsed_time = int(time.time() - start_time)

    if elapsed_time >= time_limit:
        game_over = True
        if score > high_score:
            high_score = score
            save_high_score(high_score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not ball_in_motion and not shooting_animation:
        if keys[pygame.K_UP]:
            ball_angle = min(80, ball_angle + 1)
        if keys[pygame.K_DOWN]:
            ball_angle = max(10, ball_angle - 1)
        if keys[pygame.K_RIGHT]:
            power = min(50, power + 1)
        if keys[pygame.K_LEFT]:
            power = max(10, power - 1)
        if keys[pygame.K_SPACE]:
            shooting_animation = True
            shooting_frame = 0
            rad = math.radians(ball_angle)
            velocity = [math.cos(rad) * power * 0.5, -math.sin(rad) * power * 0.5]
            total_shots += 1
        if keys[pygame.K_ESCAPE]:
            menu = True
            continue

    if shooting_animation:
        if shooting_frame < len(shoot_anim):
            if animation_timer % frame_delay == 0:
                screen.blit(shoot_anim[shooting_frame], (ball_pos[0] - 150, HEIGHT - 250))  # Karakter top hizasında
                shooting_frame += 1
            else:
                screen.blit(shoot_anim[shooting_frame - 1], (ball_pos[0] - 150, HEIGHT - 250))
            animation_timer += 1
        else:
            shooting_animation = False
            shooting_frame = 0
            animation_timer = 0
            ball_in_motion = True
    else:
        screen.blit(player_standing, (WIDTH - 780, HEIGHT - 250))  # Duran pozisyonda topla aynı hizada

    if ball_in_motion:
        velocity[1] += gravity
        ball_pos[0] += velocity[0]
        ball_pos[1] += velocity[1]

        ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius, ball_radius * 2)
        if ball_rect.colliderect(hoop):
            score += 1
            hoop = random_hoop()
            reset_ball()
        elif ball_pos[1] + ball_radius >= HEIGHT:
            if bounces < bounce_limit:
                ball_pos[1] = HEIGHT - ball_radius
                velocity[1] = -velocity[1] * bounce_damping
                velocity[0] *= 0.8
                bounces += 1
            else:
                reset_ball()
        elif ball_pos[0] > WIDTH:
            reset_ball()

    screen.blit(ball_image, (int(ball_pos[0] - ball_radius), int(ball_pos[1] - ball_radius)))
    screen.blit(pygame.transform.scale(goal_image, (hoop.width, hoop.height)), (hoop.x, hoop.y))

    if not ball_in_motion and not shooting_animation:
        draw_trajectory(ball_pos, ball_angle, power)


    accuracy = round((score / total_shots) * 100, 1) if total_shots > 0 else 0
    screen.blit(font.render(f"Açı: {ball_angle}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Güç: {power}", True, WHITE), (10, 30))
    screen.blit(font.render(f"Skor: {score}", True, WHITE), (10, 50))
    screen.blit(font.render(f"Atış: {total_shots}", True, WHITE), (10, 70))
    screen.blit(font.render(f"İsabet Oranı: %{accuracy}", True, WHITE), (10, 90))
    screen.blit(font.render(f"Süre: {time_limit - elapsed_time}s", True, WHITE), (10, 110))
    screen.blit(score_font.render(f"En Yüksek Skor: {high_score}", True, WHITE), (WIDTH - 330, 10))

    pygame.display.flip()
