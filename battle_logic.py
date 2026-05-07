
import copy
import random

from characters import (
    get_type_multiplier,
    fighters,
    final_strike,
    heal,
    monster,
    nahach,
    waters_grace,
    gaian_strength,
)

arena_damage_multiplier = 1.0
arena_damage_turns = 0
BASE_DAMAGE_SCALE = 1.18



# RESET FUNCTIONS

def reset_arena():
    global arena_damage_multiplier, arena_damage_turns
    arena_damage_multiplier = 1.0
    arena_damage_turns = 0


def reset_fighter(fighter):
    fighter["max_hp"] = fighter["base_max_hp"]
    fighter["hp"] = fighter["base_max_hp"]
    fighter["attack"] = fighter["base_attack"]
    fighter["special_attack"] = fighter["base_special_attack"]
    fighter["defense"] = fighter["base_defense"]
    fighter["speed"] = fighter["base_speed"]

    # reset status effects
    fighter["rage"] = False
    fighter["evasion_multiplier"] = 1.0
    fighter["next_accuracy_multiplier"] = 1.0
    fighter["confused_turns"] = 0
    fighter["monster_turns"] = 0
    fighter["monster_damage"] = 0
    fighter["flame_boost"] = 1.0
    fighter["earth_boost"] = 1.0
    fighter["temp_defense_turns"] = 0
    fighter["temp_defense_amount"] = 0



# BASIC BATTLE MATH

def calculate_damage(attacker, defender, move):
    global arena_damage_multiplier

    if move["category"] == "physical":
        damage = (attacker["attack"] / defender["defense"]) * (1 + move["power"])
    elif move["category"] == "special":
        damage = (attacker["special_attack"] / defender["defense"]) * (1 + move["power"])
    else:
        damage = 0

    damage *= BASE_DAMAGE_SCALE

    if move["move_type"] == "Fire":
        damage *= attacker["flame_boost"]
    if move["move_type"] == "Earth":
        damage *= attacker["earth_boost"]

    type_multiplier = get_type_multiplier(move["move_type"], defender["type"])
    damage *= type_multiplier
    damage *= arena_damage_multiplier

    if damage > 0:
        damage = max(1, int(damage))

    return damage, type_multiplier


def move_hits(attacker, defender, move):
    accuracy = move["accuracy"]
    accuracy *= attacker["next_accuracy_multiplier"]
    accuracy *= defender["evasion_multiplier"]
    accuracy = max(0, min(100, accuracy))

    attacker["next_accuracy_multiplier"] = 1.0
    return random.randint(1, 100) <= accuracy


def add_type_message(type_multiplier, messages):
    if type_multiplier == 1.15:
        messages.append("It was super effective!")
    elif type_multiplier == 0.85:
        messages.append("It was not very effective.")



# NUMERICAL METHOD 1: ROOT-FINDING

def bisection_root(function, low, high, tolerance=0.1, max_steps=50):
   
    f_low = function(low)
    f_high = function(high)

    if f_low * f_high > 0:
        return None

    for _ in range(max_steps):
        middle = (low + high) / 2
        f_middle = function(middle)

        if abs(f_middle) < tolerance:
            return middle

        if f_low * f_middle < 0:
            high = middle
            f_high = f_middle
        else:
            low = middle
            f_low = f_middle

    return (low + high) / 2


def expected_attack_value(attacker, defender):
   
    best_value = 0

    for move in attacker["moves"]:
        if move["category"] == "physical":
            base_damage = (attacker["attack"] / defender["defense"]) * (1 + move["power"])
        elif move["category"] == "special":
            base_damage = (attacker["special_attack"] / defender["defense"]) * (1 + move["power"])
        else:
            continue

        # Very high-risk attacks are not used for the heal threshold estimate.
        if move["accuracy"] < 70:
            continue

        value = base_damage * (move["accuracy"] / 100)
        best_value = max(best_value, value)

    return best_value


def heal_value_at_hp(fighter, hp):
    """Estimated value of Heal at a given HP."""
    missing_hp = fighter["max_hp"] - hp
    return missing_hp * heal["heal_missing_percent"]


def find_heal_threshold(healer, defender):
    """Find the HP where healing and attacking are about equal."""
    attack_value = expected_attack_value(healer, defender)

    def heal_minus_attack(hp):
        return heal_value_at_hp(healer, hp) - attack_value

    return bisection_root(heal_minus_attack, 0, healer["max_hp"])



# NUMERICAL METHOD 2: INTERPOLATION

def linear_interpolation(x0, y0, x1, y1, x):
    
    if x1 == x0:
        return y0

    slope = (y1 - y0) / (x1 - x0)
    return y0 + slope * (x - x0)


def interpolated_heal_value(fighter, hp):
    
    step = 20
    low_hp = int(hp // step) * step
    high_hp = low_hp + step

    low_hp = max(0, low_hp)
    high_hp = min(fighter["max_hp"], high_hp)

    low_value = heal_value_at_hp(fighter, low_hp)
    high_value = heal_value_at_hp(fighter, high_hp)

    return linear_interpolation(low_hp, low_value, high_hp, high_value, hp)



# AI MOVE CHOICE

def choose_enemy_move(enemy, opponent):
    if enemy["name"] == "Ryuzo" and enemy["rage"]:
        return final_strike

    if enemy["name"] == "Emmanuel" and enemy["hp"] < enemy["max_hp"]:
        threshold = find_heal_threshold(enemy, opponent)
        heal_estimate = interpolated_heal_value(enemy, enemy["hp"])
        attack_estimate = expected_attack_value(enemy, opponent)

        # Root-finding gives the threshold. Interpolation estimates the heal value.
        if threshold is not None and enemy["hp"] <= threshold and heal_estimate >= attack_estimate:
            return heal

    if enemy["name"] == "Shi-Noia" and enemy["monster_turns"] == 0:
        return monster

    if enemy["name"] == "King Zarus" and enemy["flame_boost"] == 1.0:
        return nahach

    if enemy["name"] == "Jasmine" and enemy["hp"] < enemy["max_hp"] * 0.45:
        return waters_grace

    if enemy["name"] == "Alexander" and enemy["earth_boost"] == 1.0:
        return gaian_strength

    return random.choice(enemy["moves"])


# STATUS HELPERS

def apply_monster_damage(owner, target, messages):
    if owner["monster_turns"] > 0 and target["hp"] > 0:
        target["hp"] -= owner["monster_damage"]
        target["hp"] = max(0, target["hp"])
        owner["monster_turns"] -= 1
        messages.append(f"{owner['name']}'s monsters dealt {owner['monster_damage']} damage!")


def end_round_status(fighter, messages):
    if fighter["temp_defense_turns"] <= 0:
        return

    fighter["temp_defense_turns"] -= 1

    if fighter["temp_defense_turns"] == 0 and fighter["temp_defense_amount"] > 0:
        fighter["defense"] -= fighter["temp_defense_amount"]
        fighter["temp_defense_amount"] = 0
        messages.append(f"{fighter['name']}'s defense boost wore off!")



# MOVE EFFECTS

def normal_damage_move(attacker, defender, move, messages):
    damage, type_multiplier = calculate_damage(attacker, defender, move)
    defender["hp"] -= damage
    defender["hp"] = max(0, defender["hp"])

    messages.append(f"It hit for {damage} damage!")
    add_type_message(type_multiplier, messages)

    if move["move_type"] == "Earth" and attacker["earth_boost"] > 1.0:
        attacker["earth_boost"] = 1.0
        messages.append(f"{attacker['name']}'s Earth boost was used up!")


def use_move(attacker, defender, move, messages):
    global arena_damage_multiplier, arena_damage_turns

    messages.append(f"{attacker['name']} used {move['name']}!")

    if attacker["confused_turns"] > 0:
        messages.append(f"{attacker['name']} is confused!")
        attacker["confused_turns"] -= 1

        if random.random() < 0.40:
            attacker["hp"] = max(0, attacker["hp"] - 20)
            messages.append(f"{attacker['name']} hurt themselves for 20 damage!")
            return

        messages.append(f"{attacker['name']} fought through it!")

    if not move_hits(attacker, defender, move):
        messages.append("But it missed!")

        if move["name"] == "Judgement":
            recoil = int(attacker["hp"] * move["recoil_on_miss_percent"])
            attacker["hp"] = max(0, attacker["hp"] - recoil)
            messages.append(f"{attacker['name']} lost {recoil} HP from recoil!")
        return

    name = move["name"]

    if name == "Heal":
        old_hp = attacker["hp"]
        heal_amount = int((attacker["max_hp"] - attacker["hp"]) * move["heal_missing_percent"])
        attacker["hp"] = min(attacker["max_hp"], attacker["hp"] + heal_amount)
        attacker["special_attack"] = int(attacker["special_attack"] * (1 + move["special_attack_boost_percent"]))
        messages.append(f"{attacker['name']} healed {attacker['hp'] - old_hp} HP!")
        messages.append(f"{attacker['name']}'s special attack rose!")
        return

    if name == "Family":
        attacker["max_hp"] += move["max_hp_boost"]
        attacker["hp"] = min(attacker["max_hp"], attacker["hp"] + move["heal_amount"])
        attacker["rage"] = random.random() < move["rage_chance"]
        messages.append(f"{attacker['name']}'s max HP increased!")
        messages.append(f"{attacker['name']} healed {move['heal_amount']} HP!")
        messages.append("Rage activated!" if attacker["rage"] else "Rage did not activate.")
        return

    if name == "The Ghost":
        attacker["evasion_multiplier"] *= (1 - move["evasiveness_boost_percent"])
        messages.append(f"{attacker['name']} became harder to hit!")
        return

    if name == "Blinding Light":
        normal_damage_move(attacker, defender, move, messages)
        defender["next_accuracy_multiplier"] *= move["next_accuracy_multiplier"]
        defender["speed"] = int(defender["speed"] * (1 - move["speed_drop_percent"]))
        messages.append(f"{defender['name']}'s next move accuracy was cut in half!")
        return

    if name == "Berserking Strike":
        total_damage = 0
        hit_count = 0
        last_type_multiplier = 1.0

        for chance in [1.0] + move["extra_hit_chances"]:
            if defender["hp"] <= 0 or random.random() > chance:
                break

            damage, type_multiplier = calculate_damage(attacker, defender, move)
            defender["hp"] -= damage
            total_damage += damage
            hit_count += 1
            last_type_multiplier = type_multiplier

        defender["hp"] = max(0, defender["hp"])
        messages.append(f"It hit {hit_count} time(s) for {total_damage} total damage!")
        add_type_message(last_type_multiplier, messages)
        return

    if name == "Final Strike" and attacker["rage"]:
        defender["hp"] = 1
        attacker["rage"] = False
        messages.append("Rage empowered Final Strike!")
        messages.append(f"{defender['name']} was brought down to 1 HP!")
        return

    if name == "Dream":
        defender["confused_turns"] = move["confuse_turns"]
        messages.append(f"{defender['name']} became confused!")
        return

    if name == "Monster":
        attacker["monster_turns"] = move["duration"]
        attacker["monster_damage"] = move["dot_damage"]
        messages.append(f"{attacker['name']} summoned monsters for {move['duration']} rounds!")
        return

    if name == "Fury":
        attacker["speed"] += move["speed_boost"]
        attacker["defense"] += move["defense_boost"]
        messages.append(f"{attacker['name']}'s speed rose!")
        messages.append(f"{attacker['name']}'s defense rose!")
        return

    if name == "Nahach":
        attacker["flame_boost"] = move["flame_boost_multiplier"]
        messages.append(f"{attacker['name']} engulfed the field in flames!")
        messages.append("Flame attacks are now stronger!")
        return

    if name == "Water's Grace":
        heal_percent = random.choice([0.25, 0.50, 0.75, 1.00])
        old_hp = attacker["hp"]
        attacker["hp"] = min(attacker["max_hp"], attacker["hp"] + int(attacker["max_hp"] * heal_percent))
        messages.append(f"{attacker['name']} healed {attacker['hp'] - old_hp} HP!")
        return

    if name == "Bulk Up":
        attacker["defense"] += move["defense_boost"]
        attacker["temp_defense_turns"] = move["duration"]
        attacker["temp_defense_amount"] = move["defense_boost"]
        messages.append(f"{attacker['name']}'s defense rose by {move['defense_boost']}!")
        messages.append(f"The boost will last {move['duration']} turns.")
        return

    if name == "Gaian Strength":
        attacker["earth_boost"] = move["earth_boost_multiplier"]
        attacker["defense"] += move["defense_boost"]
        messages.append(f"{attacker['name']}'s next Earth move was empowered!")
        messages.append(f"{attacker['name']}'s defense rose by {move['defense_boost']}!")
        return

    if name == "Unstoppable":
        arena_damage_multiplier = move["damage_reduction_multiplier"]
        arena_damage_turns = move["duration"]
        messages.append("The arena was reshaped!")
        messages.append("All damage is reduced for 2 turns!")
        return

    normal_damage_move(attacker, defender, move, messages)


# 
# TURN ORDER
# 
def take_turn(player1, player2, move1, move2):
    global arena_damage_multiplier, arena_damage_turns

    messages = []

    if player1["speed"] > player2["speed"]:
        first, first_move = player1, move1
        second, second_move = player2, move2
    elif player2["speed"] > player1["speed"]:
        first, first_move = player2, move2
        second, second_move = player1, move1
    else:
        first, first_move, second, second_move = random.choice([
            (player1, move1, player2, move2),
            (player2, move2, player1, move1),
        ])

    use_move(first, second, first_move, messages)

    if second["hp"] > 0:
        use_move(second, first, second_move, messages)

    if player1["hp"] > 0 and player2["hp"] > 0:
        apply_monster_damage(player1, player2, messages)
        if player2["hp"] > 0:
            apply_monster_damage(player2, player1, messages)

    end_round_status(player1, messages)
    end_round_status(player2, messages)

    if arena_damage_turns > 0:
        arena_damage_turns -= 1
        if arena_damage_turns == 0:
            arena_damage_multiplier = 1.0
            messages.append("The arena returned to normal.")

    return messages


# 
# NUMERICAL METHOD 3: MONTE CARLO
# 
def simulate_one_battle(player_template, enemy_template, max_turns=80):
    player = copy.deepcopy(player_template)
    enemy = copy.deepcopy(enemy_template)

    reset_fighter(player)
    reset_fighter(enemy)
    reset_arena()

    turns = 0

    while player["hp"] > 0 and enemy["hp"] > 0 and turns < max_turns:
        player_move = choose_enemy_move(player, enemy)
        enemy_move = choose_enemy_move(enemy, player)
        take_turn(player, enemy, player_move, enemy_move)
        turns += 1

    if player["hp"] > enemy["hp"]:
        winner = player["name"]
    elif enemy["hp"] > player["hp"]:
        winner = enemy["name"]
    else:
        winner = "Tie"

    return {
        "winner": winner,
        "turns": turns,
        "player_hp": player["hp"],
        "enemy_hp": enemy["hp"],
    }


def run_monte_carlo(player, enemy, battles=250):
    """Repeat many battles to estimate win rate and average ending HP."""
    global arena_damage_multiplier, arena_damage_turns

    old_multiplier = arena_damage_multiplier
    old_turns = arena_damage_turns

    player_wins = 0
    enemy_wins = 0
    total_player_hp = 0
    total_enemy_hp = 0
    total_turns = 0

    for _ in range(battles):
        result = simulate_one_battle(player, enemy)

        if result["winner"] == player["name"]:
            player_wins += 1
        elif result["winner"] == enemy["name"]:
            enemy_wins += 1

        total_player_hp += result["player_hp"]
        total_enemy_hp += result["enemy_hp"]
        total_turns += result["turns"]

    arena_damage_multiplier = old_multiplier
    arena_damage_turns = old_turns

    return {
        "battles": battles,
        "player_win_rate": 100 * player_wins / battles,
        "enemy_win_rate": 100 * enemy_wins / battles,
        "avg_player_hp": total_player_hp / battles,
        "avg_enemy_hp": total_enemy_hp / battles,
        "avg_turns": total_turns / battles,
    }


def choose_enemy(player):
    choices = [fighter for fighter in fighters if fighter["name"] != player["name"]]
    return random.choice(choices)
