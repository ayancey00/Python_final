# characters.py
#This file has stats and character moves only


LIGHT_BLUE = (180, 220, 255)
RED = (220, 60, 60)
PURPLE = (170, 100, 220)
ORANGE = (255, 140, 60)
WATER_BLUE = (80, 180, 255)
EARTH_BROWN = (140, 95, 50)



# TYPE EFFECTIVENESS


def get_type_multiplier(move_type, defender_type):
    if defender_type == "God Kia":
        return 1.0

    if move_type == "Fight":
        if defender_type == "Fire":
            return 0.85

    elif move_type == "Light":
        if defender_type == "Earth":
            return 0.85
        elif defender_type == "Fight":
            return 1.15

    elif move_type == "Water":
        if defender_type == "Fight":
            return 0.85

    return 1.0



# All the moves and values


judgement = {
    "name": "Judgement",
    "category": "special",
    "move_type": "Light",
    "power": 110,
    "accuracy": 50,
    "recoil_on_miss_percent": 0.25
}

heal = {
    "name": "Heal",
    "category": "support",
    "move_type": "Light",
    "accuracy": 100,
    "heal_missing_percent": 0.15,
    "special_attack_boost_percent": 0.01
}

blinding_light = {
    "name": "Blinding Light",
    "category": "special",
    "move_type": "Light",
    "power": 5,
    "accuracy": 100,
    "next_accuracy_multiplier": 0.50,
    "speed_drop_percent": 0.04
}

sword_arc = {
    "name": "Sword Arc",
    "category": "physical",
    "move_type": "Normal",
    "power": 35,
    "accuracy": 95
}

the_ghost = {
    "name": "The Ghost",
    "category": "support",
    "move_type": "Normal",
    "accuracy": 100,
    "evasiveness_boost_percent": 0.10
}

berserking_strike = {
    "name": "Berserking Strike",
    "category": "physical",
    "move_type": "Fight",
    "power": 14,
    "accuracy": 95,
    "extra_hit_chances": [0.70, 0.50, 0.30, 0.15]
}

family = {
    "name": "Family",
    "category": "support",
    "move_type": "Normal",
    "accuracy": 100,
    "max_hp_boost": 10,
    "heal_amount": 30,
    "rage_chance": 0.02
}

final_strike = {
    "name": "Final Strike",
    "category": "physical",
    "move_type": "Fight",
    "power": 45,
    "accuracy": 80,
    "rage_finisher": True
}

dream = {
    "name": "Dream",
    "category": "support",
    "move_type": "God Kia",
    "accuracy": 100,
    "confuse_turns": 3
}

monster = {
    "name": "Monster",
    "category": "support",
    "move_type": "God Kia",
    "accuracy": 100,
    "dot_damage": 20,
    "duration": 5
}

mind_beam = {
    "name": "Mind Beam",
    "category": "special",
    "move_type": "God Kia",
    "power": 55,
    "accuracy": 90
}

heavy_blade = {
    "name": "Heavy Blade",
    "category": "physical",
    "move_type": "Normal",
    "power": 30,
    "accuracy": 95
}

flamethrower = {
    "name": "Flamethrower",
    "category": "special",
    "move_type": "Fire",
    "power": 40,
    "accuracy": 90,
    "flame_move": True
}

orus_wrath = {
    "name": "Orus's Wrath",
    "category": "special",
    "move_type": "God Kia",
    "power": 75,
    "accuracy": 45
}

fury = {
    "name": "Fury",
    "category": "support",
    "move_type": "Fire",
    "accuracy": 100,
    "speed_boost": 7,
    "defense_boost": 5
}

nahach = {
    "name": "Nahach",
    "category": "support",
    "move_type": "Fire",
    "accuracy": 100,
    "flame_boost_multiplier": 1.5
}

waters_grace = {
    "name": "Water's Grace",
    "category": "support",
    "move_type": "Water",
    "accuracy": 100
}

water_strike = {
    "name": "Water Strike",
    "category": "special",
    "move_type": "Water",
    "power": 38,
    "accuracy": 92
}

bulk_up = {
    "name": "Bulk Up",
    "category": "support",
    "move_type": "Water",
    "accuracy": 100,
    "defense_boost": 20,
    "duration": 2
}

drown = {
    "name": "Drown",
    "category": "special",
    "move_type": "Water",
    "power": 78,
    "accuracy": 55
}

gaian_strength = {
    "name": "Gaian Strength",
    "category": "support",
    "move_type": "Earth",
    "accuracy": 100,
    "earth_boost_multiplier": 1.5,
    "defense_boost": 5
}

earth_shatter = {
    "name": "Earth Shatter",
    "category": "physical",
    "move_type": "Earth",
    "power": 60,
    "accuracy": 92
}

unstoppable = {
    "name": "Unstoppable",
    "category": "support",
    "move_type": "Earth",
    "accuracy": 100,
    "damage_reduction_multiplier": 0.8,
    "duration": 2
}

frontal_assault = {
    "name": "Frontal Assault",
    "category": "physical",
    "move_type": "Fight",
    "power": 34,
    "accuracy": 95
}



# CHARACTERS


emmanuel = {
    "name": "Emmanuel",
    "type": "Light",
    "max_hp": 300,
    "hp": 300,
    "attack": 75,
    "special_attack": 80,
    "defense": 80,
    "speed": 50,
    "base_max_hp": 300,
    "base_attack": 75,
    "base_special_attack": 80,
    "base_defense": 80,
    "base_speed": 50,
    "rage": False,
    "evasion_multiplier": 1.0,
    "next_accuracy_multiplier": 1.0,
    "confused_turns": 0,
    "monster_turns": 0,
    "monster_damage": 0,
    "flame_boost": 1.0,
    "earth_boost": 1.0,
    "temp_defense_turns": 0,
    "temp_defense_amount": 0,
    "moves": [judgement, heal, blinding_light, sword_arc],
    "color": LIGHT_BLUE
}

ryuzo = {
    "name": "Ryuzo",
    "type": "Fight",
    "max_hp": 350,
    "hp": 350,
    "attack": 90,
    "special_attack": 20,
    "defense": 70,
    "speed": 90,
    "base_max_hp": 350,
    "base_attack": 90,
    "base_special_attack": 20,
    "base_defense": 70,
    "base_speed": 90,
    "rage": False,
    "evasion_multiplier": 1.0,
    "next_accuracy_multiplier": 1.0,
    "confused_turns": 0,
    "monster_turns": 0,
    "monster_damage": 0,
    "flame_boost": 1.0,
    "earth_boost": 1.0,
    "temp_defense_turns": 0,
    "temp_defense_amount": 0,
    "moves": [the_ghost, berserking_strike, family, final_strike],
    "color": RED
}

shi_noia = {
    "name": "Shi-Noia",
    "type": "God Kia",
    "max_hp": 450,
    "hp": 450,
    "attack": 60,
    "special_attack": 95,
    "defense": 60,
    "speed": 75,
    "base_max_hp": 450,
    "base_attack": 60,
    "base_special_attack": 95,
    "base_defense": 60,
    "base_speed": 75,
    "rage": False,
    "evasion_multiplier": 1.0,
    "next_accuracy_multiplier": 1.0,
    "confused_turns": 0,
    "monster_turns": 0,
    "monster_damage": 0,
    "flame_boost": 1.0,
    "earth_boost": 1.0,
    "temp_defense_turns": 0,
    "temp_defense_amount": 0,
    "moves": [dream, monster, mind_beam, heavy_blade],
    "color": PURPLE
}

zarus = {
    "name": "King Zarus",
    "type": "Fire",
    "max_hp": 500,
    "hp": 500,
    "attack": 80,
    "special_attack": 80,
    "defense": 95,
    "speed": 85,
    "base_max_hp": 500,
    "base_attack": 80,
    "base_special_attack": 80,
    "base_defense": 95,
    "base_speed": 85,
    "rage": False,
    "evasion_multiplier": 1.0,
    "next_accuracy_multiplier": 1.0,
    "confused_turns": 0,
    "monster_turns": 0,
    "monster_damage": 0,
    "flame_boost": 1.0,
    "earth_boost": 1.0,
    "temp_defense_turns": 0,
    "temp_defense_amount": 0,
    "moves": [flamethrower, orus_wrath, fury, nahach],
    "color": ORANGE
}

jasmine = {
    "name": "Jasmine",
    "type": "Water",
    "max_hp": 300,
    "hp": 300,
    "attack": 70,
    "special_attack": 85,
    "defense": 80,
    "speed": 70,
    "base_max_hp": 300,
    "base_attack": 70,
    "base_special_attack": 85,
    "base_defense": 80,
    "base_speed": 70,
    "rage": False,
    "evasion_multiplier": 1.0,
    "next_accuracy_multiplier": 1.0,
    "confused_turns": 0,
    "monster_turns": 0,
    "monster_damage": 0,
    "flame_boost": 1.0,
    "earth_boost": 1.0,
    "temp_defense_turns": 0,
    "temp_defense_amount": 0,
    "moves": [waters_grace, water_strike, bulk_up, drown],
    "color": WATER_BLUE
}

alexander = {
    "name": "Alexander",
    "type": "Earth",
    "max_hp": 450,
    "hp": 450,
    "attack": 75,
    "special_attack": 80,
    "defense": 90,
    "speed": 80,
    "base_max_hp": 450,
    "base_attack": 75,
    "base_special_attack": 80,
    "base_defense": 90,
    "base_speed": 80,
    "rage": False,
    "evasion_multiplier": 1.0,
    "next_accuracy_multiplier": 1.0,
    "confused_turns": 0,
    "monster_turns": 0,
    "monster_damage": 0,
    "flame_boost": 1.0,
    "earth_boost": 1.0,
    "temp_defense_turns": 0,
    "temp_defense_amount": 0,
    "moves": [gaian_strength, earth_shatter, unstoppable, frontal_assault],
    "color": EARTH_BROWN
}

fighters = [emmanuel, ryuzo, shi_noia, zarus, jasmine, alexander]