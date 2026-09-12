import pygame
import sys
import random
import tkinter as tk

pygame.init()

# ================= CONSTANTS =================
WIDTH, HEIGHT = 1280, 750
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH, HEIGHT

BLOCK_SIZE = 20
SPEED = 15
PLAYER_SPEED = 6
BULLET_SPEED = 10
ALIEN_SPEED = 3
FPS = 60


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 128, 255)

# ================= GLOBALS =================
username = ""
high_scores = {}

# ================= TKINTER USERNAME =================
def get_username():
    global username

    def submit():
        global username
        username = entry.get()
        root.destroy()
        game_selection()

    root = tk.Tk()
    root.title("Enter Username")
    root.geometry("1366x768")

    tk.Label(root, text="Enter Username").pack(pady=10)
    entry = tk.Entry(root)
    entry.pack(pady=10)
    tk.Button(root, text="Start", command=submit).pack(pady=10)

    root.mainloop()


# ================= GUESSING GAME =================
def start_guessing_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)

    secret = random.randint(1, 10)
    guess = ""
    message = "Guess a number (1-10)"

    while True:
        screen.fill(BLACK)
        text = font.render(message, True, WHITE)
        screen.blit(text, (WIDTH//2 - 200, HEIGHT//2 - 50))

        input_text = font.render(f"Your input: {guess}", True, GREEN)
        screen.blit(input_text, (WIDTH//2 - 200, HEIGHT//2 + 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if guess.isdigit():
                        if int(guess) == secret:
                            message = "Correct! Press R to return"
                        else:
                            message = f"Wrong! It was {secret}. Press R"
                elif event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                elif event.key == pygame.K_r:
                    return
                else:
                    if event.unicode.isdigit():
                        guess += event.unicode

        clock.tick(30)


# ================= SNAKE GAME =================
def snake_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)

    snake = [(200, 200), (220, 200), (240, 200)]
    direction = "RIGHT"
    food = (400, 300)
    score = 0

    def spawn_food():
        return (
            random.randint(0, WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE,
            random.randint(0, HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE,
        )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        head_x, head_y = snake[-1]

        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        new_head = (head_x, head_y)

        if (
            new_head in snake
            or head_x < 0 or head_x >= WIDTH
            or head_y < 0 or head_y >= HEIGHT
        ):
            high_scores[username] = max(score, high_scores.get(username, 0))
            return

        snake.append(new_head)

        if new_head == food:
            score += 1
            food = spawn_food()
        else:
            snake.pop(0)

        screen.fill(BLACK)

        for s in snake:
            pygame.draw.rect(screen, GREEN, (*s, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(screen, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

        pygame.display.flip()
        clock.tick(SPEED)


# ================= SHOOTING GAME =================
def shooting_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = pygame.Rect(WIDTH//2, HEIGHT-100, 50, 50)
    bullets = []
    aliens = [pygame.Rect(random.randint(0, WIDTH-50), 0, 50, 50) for _ in range(5)]
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(player.centerx, player.top, 5, 10))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED

        for b in bullets[:]:
            b.y -= BULLET_SPEED
            if b.y < 0:
                bullets.remove(b)

        for a in aliens[:]:
            a.y += ALIEN_SPEED
            if a.y > HEIGHT:
                a.x = random.randint(0, WIDTH-50)
                a.y = 0

        for b in bullets[:]:
            for a in aliens[:]:
                if b.colliderect(a):
                    bullets.remove(b)
                    aliens.remove(a)
                    aliens.append(pygame.Rect(random.randint(0, WIDTH-50), 0, 50, 50))
                    score += 1
                    break

        for a in aliens:
            if player.colliderect(a):
                high_scores[username] = max(score, high_scores.get(username, 0))
                return

        screen.fill(BLACK)

        pygame.draw.rect(screen, BLUE, player)

        for b in bullets:
            pygame.draw.rect(screen, WHITE, b)

        for a in aliens:
            pygame.draw.rect(screen, RED, a)

        pygame.display.flip()
        clock.tick(FPS)


# ================= MENU =================
def game_selection():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 70)

    while True:
        screen.fill(BLACK)

        screen.blit(font.render("1. Guessing Game", True, WHITE), (400, 200))
        screen.blit(font.render("2. Snake Game", True, WHITE), (400, 300))
        screen.blit(font.render("3. Shooting Game", True, WHITE), (400, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start_guessing_game()
                elif event.key == pygame.K_2:
                    snake_game()
                elif event.key == pygame.K_3:
                    shooting_game()


# ================= START =================
get_username()
