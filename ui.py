# ui.py
# Draws the game screens.

import pygame
from characters import fighters

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 60, 60)


# Try to load Emmanuel's sprite. If it is missing, the game still runs.
def load_emmanuel_sprite():
    try:
        image = pygame.image.load("sprites/emmanuel.png")
        image = pygame.transform.scale(image, (150, 150))
        image.set_colorkey((255, 255, 255))
        return image
    except Exception:
        return None


emmanuel_img = load_emmanuel_sprite()


def draw_text(screen, font, big_font, text, x, y, color=BLACK, use_big=False):
    chosen_font = big_font if use_big else font
    text_surface = chosen_font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_hp_bar(screen, x, y, width, height, current_hp, max_hp):
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)

    fill_width = int(width * (current_hp / max_hp))
    fill_width = max(0, fill_width)

    if current_hp > max_hp * 0.35:
        color = GREEN
    else:
        color = RED

    pygame.draw.rect(screen, color, (x, y, fill_width, height))


def draw_fighter_box(screen, fighter, x, y):
    if fighter["name"] == "Emmanuel" and emmanuel_img is not None:
        screen.blit(emmanuel_img, (x, y))
    else:
        pygame.draw.rect(screen, fighter["color"], (x, y, 150, 150), border_radius=20)


def draw_battle_screen(screen, font, big_font, player, enemy, battle_messages):
    screen.fill((235, 245, 255))

    # ground circles
    pygame.draw.ellipse(screen, (180, 210, 180), (90, 250, 220, 70))
    pygame.draw.ellipse(screen, (180, 210, 180), (650, 120, 220, 70))

    draw_fighter_box(screen, player, 140, 160)
    draw_fighter_box(screen, enemy, 700, 60)

    draw_text(screen, font, big_font, f"{player['name']} ({player['type']})", 70, 30, use_big=True)
    draw_text(screen, font, big_font, f"{enemy['name']} ({enemy['type']})", 620, 20, use_big=True)

    draw_hp_bar(screen, 70, 70, 280, 25, player["hp"], player["max_hp"])
    draw_hp_bar(screen, 650, 60, 280, 25, enemy["hp"], enemy["max_hp"])

    draw_text(screen, font, big_font, f"HP: {player['hp']} / {player['max_hp']}", 70, 100)
    draw_text(screen, font, big_font, f"HP: {enemy['hp']} / {enemy['max_hp']}", 650, 90)

    # move box
    pygame.draw.rect(screen, WHITE, (40, 420, 920, 150))
    pygame.draw.rect(screen, BLACK, (40, 420, 920, 150), 3)

    for i, move in enumerate(player["moves"]):
        x = 80 + (i % 2) * 420
        y = 455 + (i // 2) * 45
        draw_text(screen, font, big_font, f"{i + 1}. {move['name']} ({move['move_type']})", x, y)

    # battle messages
    y = 210
    for line in battle_messages[-6:]:
        draw_text(screen, font, big_font, line, 390, y)
        y += 30

    if player["hp"] <= 0:
        draw_text(screen, font, big_font, f"{enemy['name']} wins!", 390, 380, use_big=True)
    elif enemy["hp"] <= 0:
        draw_text(screen, font, big_font, f"{player['name']} wins!", 390, 380, use_big=True)


def draw_select_screen(screen, font, big_font):
    screen.fill((245, 245, 255))
    draw_text(screen, font, big_font, "Choose Your Fighter", 350, 40, use_big=True)

    for i, fighter in enumerate(fighters):
        x = 70 + (i % 2) * 450
        y = 110 + (i // 2) * 145

        pygame.draw.rect(screen, fighter["color"], (x, y, 100, 100), border_radius=18)
        pygame.draw.rect(screen, BLACK, (x, y, 100, 100), 2, border_radius=18)

        draw_text(screen, font, big_font, f"{i + 1}. {fighter['name']}", x + 120, y + 8)
        draw_text(screen, font, big_font, f"Type: {fighter['type']}", x + 120, y + 33)
        draw_text(screen, font, big_font, f"HP: {fighter['base_max_hp']}", x + 120, y + 58)
        draw_text(screen, font, big_font, f"ATK: {fighter['base_attack']}  SP: {fighter['base_special_attack']}", x + 120, y + 83)

    draw_text(screen, font, big_font, "Press 1-6 to choose", 350, 555)
