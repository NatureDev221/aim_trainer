import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Set fullscreen and get actual width and height
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Aim Trainer with Menu")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Load and scale background image
background_img = pygame.image.load("image.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)
fps_font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()
fps_history = []
max_history_len = 30

# Difficulty settings by mode
difficulty_settings = {
    'Easy': 50,
    'Medium': 30,
    'Hard': 20
}

# Menu button class
class Button:
    def __init__(self, text, x, y, width, height, color_active, color_inactive):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.hovered = False

    def draw(self, screen):
        color = self.color_active if self.hovered else self.color_inactive
        pygame.draw.rect(screen, color, self.rect)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def draw_fps():
    fps = clock.get_fps()
    fps_history.append(fps)
    if len(fps_history) > max_history_len:
        fps_history.pop(0)
    avg_fps = sum(fps_history) / len(fps_history)
    fps_text = fps_font.render(f'FPS: {int(avg_fps)}', True, WHITE)
    fps_rect = fps_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(fps_text, fps_rect)

def draw_score(score):
    text = small_font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def draw_target(pos, radius):
    pygame.draw.circle(screen, RED, pos, radius)
    pygame.draw.circle(screen, BLACK, pos, radius, 3)
    crosshair_size = 8
    x, y = pos
    pygame.draw.line(screen, BLACK, (x - crosshair_size, y), (x + crosshair_size, y), 2)
    pygame.draw.line(screen, BLACK, (x, y - crosshair_size), (x, y + crosshair_size), 2)

def show_menu():
    buttons = []
    button_width = 200
    button_height = 80
    gap = 20
    start_y = HEIGHT // 3
    labels = ['Easy', 'Medium', 'Hard']

    # Create buttons positioned vertically centered
    for i, label in enumerate(labels):
        x = (WIDTH - button_width) // 2
        y = start_y + i * (button_height + gap)
        buttons.append(Button(label, x, y, button_width, button_height, GRAY, BLACK))

    selected_mode = None

    while selected_mode is None:
        screen.blit(background_img, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        selected_mode = button.text

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return selected_mode  # returns 'Easy', 'Medium', or 'Hard'

def main_game(target_radius):
    score = 0
    target_pos = [random.randint(target_radius, WIDTH - target_radius),
                  random.randint(target_radius, HEIGHT - target_radius)]

    while True:
        clock.tick(240)
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Return to menu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                dist = math.hypot(mouse_pos[0] - target_pos[0], mouse_pos[1] - target_pos[1])
                if dist <= target_radius:
                    score += 1
                    target_pos = [random.randint(target_radius, WIDTH - target_radius),
                                  random.randint(target_radius, HEIGHT - target_radius)]

        draw_target(target_pos, target_radius)
        draw_score(score)
        draw_fps()

        pygame.display.flip()

def main():
    while True:
        mode = show_menu()
        radius = difficulty_settings.get(mode, 30)
        main_game(radius)

if __name__ == "__main__":
    main()
