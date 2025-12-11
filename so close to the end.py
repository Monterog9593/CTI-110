import random
import time

# ========= Color helper =========
def color_text(text, category="default"):
    colors = {
        "default": "\033[0m",
        "player_hp": "\033[92m",   # green
        "enemy_hp": "\033[91m",    # red
        "damage": "\033[91m",      # red
        "gold": "\033[93m",        # yellow/gold
        "potion": "\033[92m",      # green
        "ether": "\033[94m",       # blue
        "mp": "\033[94m",          # blue
        "skill": "\033[95m",       # magenta/purple
        "info": "\033[96m",        # cyan
    }
    return f"{colors.get(category, colors['default'])}{text}{colors['default']}"

# ========= UI helpers =========
def boxed_text(text):
    line = "-" * (len(text) + 4)
    print(line)
    print(f"| {text} |")
    print(line)

# ========= Player creation =========
def create_player():
    name = "Hero"
    player_class = "Warrior"  # You can expand classes later
    player = {
        "name": name,
        "class": player_class,
        "level": 1,
        "exp": 0,
        "exp_to_next": 50,
        "hp": 100,
        "max_hp": 100,
        "mp": 30,
        "max_mp": 30,
        "str": 12,
        "def": 8,
        "gold": 20,
        "skills": ["Slash"],  # simple baseline skill
        "inventory": {"Potion": 2, "Ether": 1}
    }
    return player

# ========= Leveling =========
def gain_exp(player, amount):
    player["exp"] += amount
    boxed_text(color_text(f"You gained {amount} EXP!", "info"))
    while player["exp"] >= player["exp_to_next"]:
        player["exp"] -= player["exp_to_next"]
        player["level"] += 1
        player["exp_to_next"] = int(player["exp_to_next"] * 1.35)
        player["max_hp"] += 15
        player["hp"] = player["max_hp"]
        player["max_mp"] += 5
        player["mp"] = player["max_mp"]
        player["str"] += 3
        player["def"] += 2
        boxed_text(color_text(f"Level Up! You are now Lv {player['level']}", "info"))

# ========= Shop =========
def shop(player):
    boxed_text("🏪 Shop")
    items = [
        {"name": "Potion", "price": 10, "desc": "Restore 40 HP"},
        {"name": "Ether", "price": 15, "desc": "Restore 20 MP"},
    ]
    for i, it in enumerate(items, 1):
        print(f"{i}) {it['name']} - {it['price']} gold ({it['desc']})")
    print("9) Leave shop")
    choice = input("> ").strip()
    if choice in ["1", "2"]:
        idx = int(choice) - 1
        item = items[idx]
        if player["gold"] >= item["price"]:
            player["gold"] -= item["price"]
            player["inventory"][item["name"]] = player["inventory"].get(item["name"], 0) + 1
            boxed_text(color_text(f"Bought {item['name']} for {item['price']} gold.", "gold"))
        else:
            boxed_text("Not enough gold.")
    else:
        boxed_text("You leave the shop.")

# ========= Town menu =========
def town_menu(player):
    while True:
        boxed_text("Welcome Hero, Please explore the Fields and Forest to train. The Dragon Lord is Dwelling in the Cave, Use the inn to rest and Buy from the shop to prepare for your Adventure.")
        print("\n🏘️ Town")
        print("1) Rest at Inn (5 gold)")
        print("2) Explore Fields")
        print("3) Explore Forest")
        print("4) Explore Valley")
        print("5) Explore Mountain")
        print("6) Explore Cave")
        print("7) Visit Shop")
        print("8) View Status")
        print("9) Exit")
        choice = input("> ").strip()

        if choice == "1":
            if player["gold"] >= 5:
                player["gold"] -= 5
                player["hp"] = player["max_hp"]
                player["mp"] = player["max_mp"]
                boxed_text(color_text("You rest at the inn. HP and MP fully restored.", "info"))
            else:
                boxed_text("Not enough gold.")

        elif choice == "2":
            return "FIELDS"
        elif choice == "3":
            return "FOREST"
        elif choice == "4":
            return "VALLEY"
        elif choice == "5":
            return "MOUNTAIN"
        elif choice == "6":
            return "CAVE"
        elif choice == "7":
            shop(player)
        elif choice == "8":
            print(color_text(f"Name: {player['name']} ({player['class']})", "info"))
            print(color_text(f"Lv {player['level']}  HP {player['hp']}/{player['max_hp']}", "player_hp"))
            print(color_text(f"MP {player['mp']}/{player['max_mp']}", "mp"))
            print(f"STR {player['str']}  DEF {player['def']}  {color_text(f'Gold {player['gold']}', 'gold')}")
            print(color_text(f"Skills: {', '.join(player['skills'])}", "skill"))
            print(f"Inventory: {player['inventory']}")
        elif choice == "9":
            return "EXIT"
        else:
            boxed_text("Invalid choice.")

# ========= Enemy generation per area =========
def area_enemies(area):
    if area == "FIELDS":
        boxed_text("🌾 You walk into the open Fields...")
        return [
            {"name": "Slime", "hp": 35, "max_hp": 35, "str": 7, "def": 3, "exp_reward": 12, "gold_reward": 8, "fleeable": True, "icon": "🟢"},
            {"name": "Wolf",  "hp": 45, "max_hp": 45, "str": 9, "def": 4, "exp_reward": 15, "gold_reward": 10, "fleeable": True, "icon": "🐺"},
        ]
    elif area == "FOREST":
        boxed_text("🌲 You enter the shadowed Forest...")
        return [
            {"name": "Goblin", "hp": 60, "max_hp": 60, "str": 11, "def": 6, "exp_reward": 20, "gold_reward": 15, "fleeable": True, "icon": "👺"},
            {"name": "Entling", "hp": 80, "max_hp": 80, "str": 10, "def": 8, "exp_reward": 25, "gold_reward": 20, "fleeable": True, "icon": "🌳"},
        ]
    elif area == "VALLEY":
        boxed_text("🌄 You go to the open Valley...")
        return [
            {"name": "Condor", "hp": 100, "max_hp": 100, "str": 20, "def": 16 + random.randint(2, 10), "exp_reward": 80, "gold_reward": 40, "fleeable": True, "icon": "🐦"},
            {"name": "Bandit", "hp": 150, "max_hp": 150, "str": 18 + random.randint(6, 20), "def": 20 + random.randint(2, 20), "exp_reward": 100, "gold_reward": 50 + random.randint(2, 30), "fleeable": True, "icon": "🥷"},
        ]
    elif area == "MOUNTAIN":
        boxed_text("⛰️ You climb up the Mountain...")
        return [
            {"name": "Zombie", "hp": 180, "max_hp": 180, "str": 30, "def": 40 + random.randint(2, 10), "exp_reward": 110, "gold_reward": 90, "fleeable": True, "icon": "🧟"},
            {"name": "Dragon Spawn", "hp": 200, "max_hp": 200, "str": 25 + random.randint(6, 20), "def": 30 + random.randint(2, 20), "exp_reward": 250, "gold_reward": 300, "fleeable": True, "icon": "🐉"},
        ]
    elif area == "CAVE":
        boxed_text("🕳️ You descend into the Cave...")
        return [
            {"name": "Bat", "hp": 70, "max_hp": 70, "str": 12, "def": 8, "exp_reward": 30, "gold_reward": 25, "fleeable": True, "icon": "🦇"},
            {"name": "Dragon Lord", "hp": 600, "max_hp": 600, "str": 45, "def": 40, "exp_reward": 500, "gold_reward": 500, "fleeable": False, "icon": "🐲"},
        ]
    else:
        return []

# ========= Simple combat =========
def use_item(player, item_name):
    inv = player["inventory"]
    if inv.get(item_name, 0) <= 0:
        boxed_text("You don't have that item.")
        return False

    if item_name == "Potion":
        heal = 40
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        inv[item_name] -= 1
        boxed_text(color_text(f"You used a Potion! Restored {heal} HP.", "potion"))
        return True
    elif item_name == "Ether":
        restore = 20
        player["mp"] = min(player["max_mp"], player["mp"] + restore)
        inv[item_name] -= 1
        boxed_text(color_text(f"You used an Ether! Restored {restore} MP.", "ether"))
        return True
    else:
        boxed_text("Nothing happens.")
        return False

def player_attack(player, enemy):
    dmg = max(1, player["str"] + random.randint(0, 6) - enemy["def"] // 4)
    enemy["hp"] = max(0, enemy["hp"] - dmg)
    print(color_text(f"You hit {enemy['name']} for {dmg} damage!", "damage"))

def enemy_attack(player, enemy):
    dmg = max(1, enemy["str"] + random.randint(0, 5) - player["def"] // 4)
    player["hp"] = max(0, player["hp"] - dmg)
    print(color_text(f"{enemy['name']} hits you for {dmg} damage!", "damage"))

def use_skill(player, enemy, enemies):
    # Minimal baseline skill; you can expand later
    if "Slash" in player["skills"]:
        if player["mp"] >= 5:
            player["mp"] -= 5
            dmg = max(1, player["str"] + random.randint(5, 10) - enemy["def"] // 4)
            enemy["hp"] = max(0, enemy["hp"] - dmg)
            print(color_text(f"You used Slash! {enemy['name']} takes {dmg} damage!", "skill"))
        else:
            print("Not enough MP!")
    else:
        print("No usable skills.")

def show_status(player, enemy):
    print(color_text(f"{player['name']} HP: {player['hp']}/{player['max_hp']}", "player_hp"))
    print(color_text(f"MP: {player['mp']}/{player['max_mp']}", "mp"))
    print(color_text(f"{enemy['icon']} {enemy['name']} HP: {enemy['hp']}/{enemy['max_hp']}", "enemy_hp"))

def battle(player, enemy, enemies_in_area):
    boxed_text(f"Encounter! {enemy['icon']} {enemy['name']} appears!")
    while player["hp"] > 0 and enemy["hp"] > 0:
        show_status(player, enemy)
        print("\n1) Attack  2) Skill  3) Use Potion  4) Use Ether  5) Flee")
        choice = input("> ").strip()

        if choice == "1":
            player_attack(player, enemy)
        elif choice == "2":
            use_skill(player, enemy, enemies_in_area)
        elif choice == "3":
            use_item(player, "Potion")
        elif choice == "4":
            use_item(player, "Ether")
        elif choice == "5":
            if enemy.get("fleeable", True):
                if random.random() < 0.6:
                    boxed_text("You fled successfully!")
                    return "fled"
                else:
                    boxed_text("Failed to flee!")
            else:
                boxed_text("You cannot flee this battle!")
        else:
            print("Invalid choice.")

        # Enemy turn if alive
        if enemy["hp"] > 0:
            enemy_attack(player, enemy)

        # Check defeat
        if player["hp"] <= 0:
            boxed_text("You have fallen...")
            return "defeat"

    # Victory
    boxed_text(color_text(f"🏆 Victory! You defeated {enemy['name']}.", "info"))
    gain_exp(player, enemy["exp_reward"])
    player["gold"] += enemy["gold_reward"]
    print(color_text(f"You earned {enemy['gold_reward']} gold.", "gold"))

    # Boss win condition
    if enemy["name"] == "Dragon Lord":
        boxed_text("The Dragon Lord is vanquished. Peace returns to the land.")
        return "boss_defeated"

    return "victory"

# ========= Explore area =========
def explore_area(area, player):
    enemies = area_enemies(area)
    if not enemies:
        boxed_text("It's quiet here...")
        return

    # Pick random enemy (avoid always landing on boss in cave)
    pool = enemies.copy()
    if area == "CAVE":
        # Weight normal enemies higher
        choices = [enemies[0]] * 3 + [enemies[1]]
        enemy = random.choice(choices)
    else:
        enemy = random.choice(pool)

    outcome = battle(player, enemy, enemies)
    if outcome in ["defeat", "boss_defeated"]:
        return
    # After battle, chance of a second encounter in tougher zones
    if area in ["VALLEY", "MOUNTAIN"] and random.random() < 0.30 and player["hp"] > 0:
        boxed_text("Another foe approaches!")
        enemy = random.choice(pool)
        battle(player, enemy, enemies)

# ========= Main loop =========
def main():
    player = create_player()
    boxed_text("A new adventure begins!")
    while True:
        area = town_menu(player)
        if area == "EXIT":
            boxed_text("Thanks for playing!")
            break
        elif area in ["FIELDS", "FOREST", "VALLEY", "MOUNTAIN", "CAVE"]:
            explore_area(area, player)

if __name__ == "__main__":
    main()