# main.py
# Run with: py -3.11 main.py

import pygame
import sys

from characters import fighters
from battle_logic import (
    reset_fighter,
    reset_arena,
    choose_enemy_move,
    take_turn,
    find_heal_threshold,
    interpolated_heal_value,
    run_monte_carlo,
)
from ui import draw_battle_screen

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fantasy Battle Simulator")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 42)

BLACK = (0, 0, 0)

state = "select_player"
player = None
enemy = None
battle_messages = ["Choose your fighter to begin."]


def draw_text(text, x, y, color=BLACK, use_big=False):
    chosen_font = big_font if use_big else font
    text_surface = chosen_font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def key_to_index(key):
    keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]

    if key in keys:
        return keys.index(key)

    return None


def draw_fighter_select_screen(title, chosen_player=None):
    screen.fill((245, 245, 255))
    draw_text(title, 320, 40, use_big=True)

    for i, fighter in enumerate(fighters):
        x = 70 + (i % 2) * 450
        y = 110 + (i // 2) * 145

        pygame.draw.rect(screen, fighter["color"], (x, y, 100, 100), border_radius=18)
        pygame.draw.rect(screen, BLACK, (x, y, 100, 100), 2, border_radius=18)

        draw_text(f"{i + 1}. {fighter['name']}", x + 120, y + 8)
        draw_text(f"Type: {fighter['type']}", x + 120, y + 33)
        draw_text(f"HP: {fighter['base_max_hp']}", x + 120, y + 58)
        draw_text(f"ATK: {fighter['base_attack']}  SP: {fighter['base_special_attack']}", x + 120, y + 83)

        if chosen_player is not None and fighter["name"] == chosen_player["name"]:
            draw_text("YOUR FIGHTER", x + 120, y + 108)

    draw_text("Press 1, 2, 3, 4, 5, or 6", 350, 555)


def start_battle(chosen_enemy):
    global enemy, state, battle_messages

    if chosen_enemy["name"] == player["name"]:
        battle_messages = ["You cannot fight yourself. Choose a different opponent."]
        return

    enemy = chosen_enemy
    reset_fighter(player)
    reset_fighter(enemy)
    reset_arena()

    battle_messages = [f"{player['name']} vs {enemy['name']}!"]
    state = "battle"


def show_numerical_info():
    global battle_messages

    threshold = find_heal_threshold(player, enemy)
    heal_estimate = interpolated_heal_value(player, player["hp"])

    if threshold is None:
        threshold_text = "No heal threshold found."
    else:
        threshold_text = f"Root-finding: heal below about {threshold:.1f} HP."

    battle_messages = [
        threshold_text,
        f"Interpolation: heal value now is about {heal_estimate:.1f}.",
        "Press M for Monte Carlo matchup test.",
    ]


def show_monte_carlo_results():
    global battle_messages

    results = run_monte_carlo(player, enemy, battles=250)

    battle_messages = [
        "Monte Carlo: 250 AI battles simulated.",
        f"{player['name']} win rate: {results['player_win_rate']:.1f}%",
        f"{enemy['name']} win rate: {results['enemy_win_rate']:.1f}%",
        f"Avg turns: {results['avg_turns']:.1f}",
        f"Avg ending HP: {player['name']} {results['avg_player_hp']:.1f}, {enemy['name']} {results['avg_enemy_hp']:.1f}",
    ]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type != pygame.KEYDOWN:
            continue

        selected_index = key_to_index(event.key)

        if state == "select_player" and selected_index is not None:
            player = fighters[selected_index]
            state = "select_enemy"
            battle_messages = [f"You chose {player['name']}. Now choose your opponent."]

        elif state == "select_enemy" and selected_index is not None:
            start_battle(fighters[selected_index])

        elif state == "battle" and player["hp"] > 0 and enemy["hp"] > 0:
            if selected_index is not None and selected_index < 4:
                player_move = player["moves"][selected_index]
                enemy_move = choose_enemy_move(enemy, player)
                battle_messages = take_turn(player, enemy, player_move, enemy_move)

            elif event.key == pygame.K_n:
                show_numerical_info()

            elif event.key == pygame.K_m:
                show_monte_carlo_results()

        elif state == "battle" and event.key == pygame.K_r:
            player = None
            enemy = None
            battle_messages = ["Choose your fighter to begin."]
            state = "select_player"

    if state == "select_player":
        draw_fighter_select_screen("Choose Your Fighter")

    elif state == "select_enemy":
        draw_fighter_select_screen("Choose Your Opponent", chosen_player=player)
        if battle_messages:
            draw_text(battle_messages[0], 170, 80)

    else:
        draw_battle_screen(screen, font, big_font, player, enemy, battle_messages)
        draw_text("Press N for numerical info. Press M for Monte Carlo.", 250, 585)

        if player["hp"] <= 0 or enemy["hp"] <= 0:
            draw_text("Press R to return to fighter select", 320, 390)

    pygame.display.flip()
    clock.tick(60)
