import pygame
import sys
import time
import os
from load_metrical import load_mtw
from get_metrical_embeddings import get_embeddings
from retrieve_metrical_similar import get_judge_context

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 24
TIME_LIMIT_SECONDS = 120
WIN_THRESHOLD = 50  # Example win threshold (adjust according to your scoring function)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Poetaster")
font = pygame.font.Font(None, FONT_SIZE)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 150, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)

def score_input(user_input):
    # Dummy scoring function: sum of ASCII values of input characters
    return sum(ord(c) for c in user_input)

def display_feedback(feedback, character_index):
    screen.fill(WHITE)
    feedback_to_display = feedback[:character_index]
    text_surface = font.render(feedback_to_display, True, BLACK)
    screen.blit(text_surface, (50, 50))
    pygame.display.update()

def draw_button(label, rect, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(label, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def load_screen(callback, message_text):
    """Display a load screen until the callback function returns."""
    loading = True
    while loading:
        screen.fill(WHITE)
        loading_text = font.render(message_text, True, BLACK)
        screen.blit(loading_text, (SCREEN_WIDTH // 2 - loading_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.update()

        loading = callback()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_menu():
    while True:
        screen.fill(WHITE)
        draw_button("Play", pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50)))
        draw_button("Exit", pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 25, 100, 50)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50)).collidepoint(mouse_pos):
                    main()  # Start the game if "Play" is clicked
                elif pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 25, 100, 50)).collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                pass  # Hover effect handled in the draw function

        pygame.display.update()

def create_judge_callback():
    get_judge_context()

def main():
    input_buffer = ""
    last_input_time = time.time()
    feedback = ""
    character_index = 0
    win = False



    # Main game loop
    while not win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # On Enter, score the input
                    score = score_input(input_buffer)
                    if score >= WIN_THRESHOLD:
                        win = True
                    else:
                        feedback = "Your score: {}. Keep going!".format(score)
                        input_buffer = ""  # clear input after scoring
                        character_index = 0  # reset typewriter index
                        last_input_time = time.time()  # reset timer
                elif event.key == pygame.K_BACKSPACE:
                    input_buffer = input_buffer[:-1]  # Remove last character
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:  # Add character to input buffer
                    input_buffer += event.unicode
                    last_input_time = time.time()  # reset timer

        # Check for time limit
        if time.time() - last_input_time > TIME_LIMIT_SECONDS:
            lose_screen()  # Show lose screen and return to main menu

        # Update the feedback in typewriter style
        if feedback and character_index < len(feedback):
            display_feedback(feedback, character_index)
            character_index += 1
            time.sleep(0.05)  # Speed of typewriter effect

        # Display the current user input
        screen.fill(WHITE)
        input_surface = font.render("Input: " + input_buffer, True, BLACK)
        screen.blit(input_surface, (50, 100))
        pygame.display.update()

        # Frame rate control
        pygame.time.Clock().tick(30)

    # Win condition
    screen.fill(WHITE)
    win_surface = font.render("Congratulations! You win!", True, BLACK)
    screen.blit(win_surface, (SCREEN_WIDTH // 2 - win_surface.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()
    time.sleep(3)

    main_menu()  # Return to main menu after winning

def lose_screen():
    screen.fill(WHITE)
    lose_surface = font.render("Time's up! You lost.", True, BLACK)
    screen.blit(lose_surface, (SCREEN_WIDTH // 2 - lose_surface.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()
    time.sleep(3)

    main_menu()  # Return to main menu after losing

def setup_callback():
    if not os.path.exists("metrical_embeddings.npy"):
        if not os.path.exists("metrical_poetry.jsonl"):
            load_mtw()
        get_embeddings()


    return False  # For demo purposes, it returns False immediately

if __name__ == "__main__":
    load_screen(setup_callback, "Performing initial ingestion of the canon...")  # Display load screen before the main menu
    main_menu()  # After loading, show the main menu