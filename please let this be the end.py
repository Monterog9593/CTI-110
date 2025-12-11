import random
import time

# -----------------------------------
# Data
# -----------------------------------
AREA_ICONS = {
    "Fields": "🌾",
    "Forest": "🌲",
    "Cave": "🪨",
}

CLASSES = {
    "Warrior": {"hp": 40, "str": 7, "def": 5, "skills": ["Power Strike"]},
    "Mage": {"hp": 25, "str": 3, "def": 2, "skills": ["Fireball", "Heal"]},
    "Thief": {"hp": 30, "str": 5, "def": 3, "skills": ["Quick Stab", "Steal"]},
}

FINAL_BOSS_NAME = "Dragon Lord"

# -----------------------------------
# Player creation (dictionary)
# -----------------------------------
def create_player(name, cls_name="Warrior"):
    cls = CLASSES.get(cls_name, CLASSES["Warrior"])
    player = {
        "name": name,
        "class": cls_name,
        "level": 1,
        "hp": cls["hp"],
        "max_hp": cls["hp"],
        "str": cls["str"],
        "def": cls["def"],
        "exp": 0,
        "exp_to_next": 20,
        "gold": 0,
        "skills": list(cls["skills"]),
        "inventory": {"Potion": 2},  # dictionary inventory
        "defending": False,
    }
    return player

# -----------------------------------
# Enemy creation (dictionary)
# -----------------------------------
def make_enemy(name, icon, hp, strength, defense, exp_reward, gold_reward, fleeable=True):
    return {
        "name": name,
        "icon": icon,
        "hp": hp,
        "max_hp": hp,
        "str": strength,
        "def": defense,
        "exp_reward": exp_reward,
        "gold_reward": gold_reward,
        "fleeable": fleeable,
    }

# -----------------------------------
# Skills
# -----------------------------------
def use_skill(player, skill, target, enemies):
    if skill == "Power Strike":
        dmg = max(1, player["str"] * 2 - target["def"])
        dmg += random.randint(1, 6)  # variability
        target["hp"] = max(0, target["hp"] - dmg)
        return f"{player['name']} uses Power Strike! {target['name']} takes {dmg} damage."
    elif skill == "Fireball":
        dmg = random.randint(10, 16) + random.randint(1, 6)
        target["hp"] = max(0, target["hp"] - dmg)
        return f"{player['name']} casts Fireball! {target['name']} takes {dmg} damage."
    elif skill == "Heal":
        heal = random.randint(12, 18)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        return f"{player['name']} casts Heal! Restores {heal} HP."
    elif skill == "Quick Stab":
        dmg = max(1, player["str"] + 2 - target["def"])
        dmg += random.randint(1, 6)
        target["hp"] = max(0, target["hp"] - dmg)
        return f"{player['name']} performs Quick Stab! {target['name']} takes {dmg} damage."
    elif skill == "Steal":
        if random.random() < 0.7:
            gold = random.randint(3, 8)
            player["gold"] += gold
            return f"{player['name']} steals {gold} gold from {target['name']}!"
        else:
            return f"{player['name']} fails to steal anything."
    return f"{player['name']} hesitates..."
# -----------------------------------
# Encounters
# -----------------------------------
def encounter(area_name):
    if area_name == "Fields":
        return [make_enemy("Slime", "🫧", 20, 4, 2, 8, 6)]
    if area_name == "Forest":
        return [make_enemy("Goblin", "👹", 28, 6, 3, 12, 10)]
    if area_name == "Cave":
        if random.random() < 0.2:
            return [make_enemy(FINAL_BOSS_NAME, "🐉", 95, 13, 8, 60, 120, fleeable=False)]
        else:
            # occasionally two enemies for variety
            if random.random() < 0.5:
                return [
                    make_enemy("Bat", "🦇", 18, 5, 2, 6, 5),
                    make_enemy("Skeleton", "💀", 34, 7, 4, 18, 14),
                ]
            return [make_enemy("Skeleton", "💀", 34, 7, 4, 18, 14)]
    return []

# -----------------------------------
# Combat
# -----------------------------------

def boxed_text(message):
    width = len(message) + 4
    print("," + "=" * width + ",")
    print("| " + message + " |")
    print("'" + "=" * width + "'")




def combat(player, enemies):
    boxed_text("⚔️ Battle start!")
    for e in enemies:
        boxed_text(f"{e['icon']} {e['name']} (HP {e['hp']}/{e['max_hp']})")

    while player["hp"] > 0 and any(e["hp"] > 0 for e in enemies):
        print(f"\n🧝 {player['name']} HP: {player['hp']}/{player['max_hp']}")
        print(",==============================,")
        print("| 1) Attack                    |")
        print("| 2) Defend                    |")
        print("| 3) Skills                    |")
        print("| 4) Inventory                 |")
        print("| 5) Flee                      |")
        print("'=============================='")
        choice = input("> ").strip()

        if choice == "1":
            target = next((e for e in enemies if e["hp"] > 0), None)
            if target:
                dmg = max(1, player["str"] - target["def"])
                dmg += random.randint(1, 3)  # variability
                target["hp"] = max(0, target["hp"] - dmg)
                boxed_text(f"{player['name']} attacks! {target['name']} takes {dmg} damage.")
                time.sleep(0.5)

        elif choice == "2":
            player["defending"] = True
            boxed_text(f"{player['name']} braces for impact.")
            time.sleep(0.5)

        elif choice == "3":
            if not player["skills"]:
                boxed_text("You don't know any skills.")
            else:
                print("Choose a skill:")
                for idx, sk in enumerate(player["skills"], start=1):
                    print(f"{idx}) {sk}")
                try:
                    sidx = int(input("> ").strip()) - 1
                    if 0 <= sidx < len(player["skills"]):
                        target = next((e for e in enemies if e["hp"] > 0), None)
                        skill_name = player["skills"][sidx]
                        if target:
                            boxed_text(use_skill(player, skill_name, target, enemies))
                            time.sleep(0.5)
                except ValueError:
                    boxed_text("Invalid selection.")

        elif choice == "4":
            boxed_text(f"Inventory: {player['inventory']}")
            if player["inventory"].get("Potion", 0) > 0:
                player["hp"] = min(player["max_hp"], player["hp"] + 10)
                player["inventory"]["Potion"] -= 1
                boxed_text("You use a Potion! Restores 10 HP.")
                time.sleep(0.5)
            else:
                boxed_text("No potions left.")

        elif choice == "5":
            if all(e["fleeable"] for e in enemies) and random.random() < 0.55:
                boxed_text("You fled successfully!")
                return False
            else:
                boxed_text("Couldn't get away!")

        # Enemy turn
        for e in enemies:
            if e["hp"] > 0:
                base = max(1, e["str"] - player["def"])
                if e["name"] == FINAL_BOSS_NAME:
                    bonus = random.randint(1, 6)
                else:
                    bonus = random.randint(1, 3)
                dmg = base + bonus
                if player["defending"]:
                    dmg = max(1, dmg // 2)
                player["hp"] = max(0, player["hp"] - dmg)
                boxed_text(f"{e['name']} attacks! {player['name']} takes {dmg} damage.")
                time.sleep(0.5)

        player["defending"] = False

    # Victory / Defeat
    if player["hp"] > 0:
        total_exp = sum(e["exp_reward"] for e in enemies)
        total_gold = sum(e["gold_reward"] for e in enemies)
        boxed_text("🏆 Victory!")

        for e in enemies:
            boxed_text(f"{e['name']} defeated! +{e['exp_reward']} EXP, +{e['gold_reward']} Gold")
            if random.random() < 0.3:
                player["inventory"]["Potion"] = player["inventory"].get("Potion", 0) + 1
                boxed_text(f"💊 {e['name']} dropped a Potion!")

        player["exp"] += total_exp
        player["gold"] += total_gold

        while player["exp"] >= player["exp_to_next"]:
            player["level"] += 1
            player["exp"] -= player["exp_to_next"]
            player["exp_to_next"] = int(player["exp_to_next"] * 1.5)
            player["max_hp"] += 5
            player["str"] += 2
            player["def"] += 1
            player["hp"] = player["max_hp"]
            boxed_text(f"🎉 {player['name']} leveled up to Level {player['level']}!")

        boxed_text(f"Progress → Lv {player['level']} | EXP {player['exp']}/{player['exp_to_next']} | Gold {player['gold']} | HP {player['hp']}/{player['max_hp']}")

        if any(e["name"] == FINAL_BOSS_NAME for e in enemies):
            boxed_text("🌟 You have defeated the Dragon Lord! The land is saved!")
            boxed_text("🎉 Congratulations, you completed the adventure!")
            return "GAME_WON"

        return True
    else:
        boxed_text("💀 You were defeated...")
        return "GAME_OVER"

# -----------------------------------
# Exploration
# -----------------------------------
def explore_area(player, area_name):
    print(f"\n{AREA_ICONS.get(area_name, '🧭')} You venture into the {area_name}...")
    # 65% chance of battle, else chance of finding gold or nothing
    if random.random() < 0.65:
        enemies = encounter(area_name)
        if enemies:
            result = combat(player, enemies)
            if result in ("GAME_WON", "GAME_OVER"):
                return result
        else:
            print("It's eerily quiet...")
    else:
        if random.random() < 0.6:
            found = random.randint(5, 25)
            player["gold"] += found
            print(f"You find a pouch with {found} gold!")
            print(f"Progress → Lv {player['level']} | EXP {player['exp']}/{player['exp_to_next']} | Gold {player['gold']} | HP {player['hp']}/{player['max_hp']}")
        else:
            print("You find nothing of interest.")

# -----------------------------------
# Town menu
# -----------------------------------
def town_menu(player):
    while True:
        print("\n🏘️ Town Menu")
        print("1) Venture to Fields")
        print("2) Venture to Forest")
        print("3) Venture to Cave")
        print("4) Rest at Inn (10 gold)")
        print("5) View Status")
        print("6) Quit")

        choice = input("> ").strip()
        if choice == "1":
            res = explore_area(player, "Fields")
            if res in ("GAME_WON", "GAME_OVER"):
                return res
        elif choice == "2":
            res = explore_area(player, "Forest")
            if res in ("GAME_WON", "GAME_OVER"):
                return res
        elif choice == "3":
            res = explore_area(player, "Cave")
            if res in ("GAME_WON", "GAME_OVER"):
                return res
        elif choice == "4":
            cost = 10
            if player["gold"] >= cost:
                player["gold"] -= cost
                player["hp"] = player["max_hp"]
                print(f"You rest at the inn for {cost} gold. HP fully restored.")
                time.sleep(0.5)
            else:
                print("Not enough gold to rest at the inn!")
        elif choice == "5":
            print(f"Progress → Lv {player['level']} | EXP {player['exp']}/{player['exp_to_next']} | Gold {player['gold']} | HP {player['hp']}/{player['max_hp']}")
            print("Inventory:", player["inventory"])
        elif choice == "6":
            print("Farewell, adventurer!")
            return "QUIT"
        else:
            print("Invalid selection.")

# -----------------------------------
# Character creation
# -----------------------------------
def create_character():
    name = input("Enter your name: ").strip() or "Adventurer"
    print("\nChoose your class:")
    options = list(CLASSES.keys())
    for i, cls in enumerate(options, 1):
        base = CLASSES[cls]
        print(f"{i}) {cls} — HP {base['hp']}, STR {base['str']}, DEF {base['def']}, Skills: {', '.join(base['skills'])}")
    cls_choice = "Warrior"
    try:
        pick = int(input("> ").strip())
        if 1 <= pick <= len(options):
            cls_choice = options[pick - 1]
    except ValueError:
        pass
    player = create_player(name, cls_choice)
    print(f"\n✨ Your Journey Begins ✨\n{player['class']} {player['name']} (Level {player['level']})")
    print(f"Progress → Lv {player['level']} | EXP {player['exp']}/{player['exp_to_next']} | Gold {player['gold']} | HP {player['hp']}/{player['max_hp']}")
    return player

# -----------------------------------
# Main
# -----------------------------------
def main():
    while True:
        start_time = time.time()
        player = create_character()
        result = town_menu(player)
        end_time = time.time()
        elapsed = int(end_time - start_time)
        minutes, seconds = divmod(elapsed, 60)

        if result == "GAME_WON":
            print("\n🌟 You completed your adventure!")
        elif result == "GAME_OVER":
            print("\n💀 Your adventure has ended.")
        else:
            print("\n👋 You left the adventure for now.")

        print(f"⏱️ Time spent on your adventure: {minutes}m {seconds}s")
        print("Thanks for playing!")

        again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if again != "y":
            break
if __name__ == "__main__":
    main()