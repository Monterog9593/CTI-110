import random
import time

FINAL_BOSS_NAME = "Dragon Lord"

def color_text(text, category="default"):
    colors = {
        "default": "\033[0m",
        "player_hp": "\033[92m",   # green
        "enemy_hp": "\033[91m",    # red
        "damage": "\033[91m",      # red
        "gold": "\033[93m",        # yellow/gold
        "potion": "\033[92m",      # green
        "either": "\033[94m",       # blue
        "mp": "\033[94m",          # blue
        "skill": "\033[95m",       # magenta/purple
    }
    return f"{colors.get(category, colors['default'])}{text}{colors['default']}"


# -----------------------------
# Core data: classes + unlocks
# -----------------------------
CLASSES = {
    "Warrior": {"hp": 50, "str": 11, "def": 8, "skills": ["Power Strike"]},
    "Mage":    {"hp": 35, "str": 7,  "def": 6, "skills": ["Fireball", "Heal"]},
    "Thief":   {"hp": 45, "str": 9,  "def": 7, "skills": ["Quick Stab", "Steal"]},
}

# Expanded skill progression notes integrated
SKILL_UNLOCKS = {
    "Warrior": {2: "Shield Bash", 4: "Whirlwind", 8: "Berserk"},
    "Mage":    {3: "Ice Shard",   5: "Lightning Bolt", 9: "Arcane Surge"},
    "Thief":   {2: "Poison Dagger", 4: "Smoke Bomb", 7: "Assassinate"},
}

# MP costs for displaying in menus
SKILL_MP_COSTS = {
    "Power Strike": 8,
    "Fireball": 6,
    "Heal": 5,
    "Quick Stab": 4,
    "Steal": 3,
    "Shield Bash": 4,
    "Whirlwind": 7,
    "Berserk": 8,
    "Ice Shard": 5,
    "Lightning Bolt": 8,
    "Arcane Surge": 10,
    "Poison Dagger": 4,
    "Smoke Bomb": 6,
    "Assassinate": 10,
}

# -----------------------------
# Utility visuals
# -----------------------------
def boxed_text(message):
    width = len(message) + 4
    print("," + "=" * width + ",")
    print("| " + message + " |")
    print("'" + "=" * width + "'")

# -----------------------------
# Player creation
# -----------------------------
def create_player(name, cls_name="Warrior"):
    cls = CLASSES.get(cls_name, CLASSES["Warrior"])
    return {
        "name": name,
        "class": cls_name,
        "level": 1,
        "hp": cls["hp"],
        "max_hp": cls["hp"],
        "mp": 20,
        "max_mp": 20,
        "str": cls["str"],
        "def": cls["def"],
        "exp": 0,
        "exp_to_next": 20,
        "gold": 0,
        "skills": list(cls["skills"]),
        "inventory": {"Potion": 2, "Ether": 0},
        "defending": False,
    }

# -----------------------------
# Shop
# -----------------------------
def shop(player):
    while True:
        boxed_text("\n🛒 Shop")
        print(color_text("1) Buy Potion (10 gold)"))
        print(color_text("2) Buy Ether (15 gold)"))
        print("3) Leave shop")
        choice = input("> ").strip()

        if choice == "1":
            if player["gold"] >= 10:
                player["gold"] -= 10
                player["inventory"]["Potion"] = player["inventory"].get("Potion", 0) + 1
                print(color_text("You bought a Potion!"))
            else:
                print(color_text("Not enough gold."))
        elif choice == "2":
            if player["gold"] >= 15:
                player["gold"] -= 15
                player["inventory"]["Ether"] = player["inventory"].get("Ether", 0) + 1
                print(color_text("You bought an Ether!"))
            else:
                print(color_text("Not enough gold."))
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

# -----------------------------
# Skills
# -----------------------------
def use_skill(player, skill, target, enemies):
    def spend_mp(cost):
        if player["mp"] < cost:
            return False
        player["mp"] -= cost
        return True

    # Warrior
    if skill == "Power Strike":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return f"Not enough MP to use {skill}!"
        dmg = max(1, player["str"] * 2 - target["def"]) + random.randint(1, 6)
        target["hp"] = max(0, target["hp"] - dmg)
        return f"{player['name']} uses Power Strike! {target['name']} takes {dmg} damage."

    if skill == "Shield Bash":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return f"Not enough MP to use {skill}!"
        dmg = max(1, player["str"] + random.randint(1, 4) * 1.5 - target["def"]) + random.randint(1, 3)
        target["hp"] = max(0, target["hp"] - dmg)
        # Simple stun: target skips next attack turn via a flag
        target["stunned"] = 1
        return f"{player['name']} slams a Shield Bash! {target['name']} takes {dmg} damage and is stunned!"

    if skill == "Whirlwind":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return f"Not enough MP to use {skill}!"
        total_msg = []
        for e in enemies:
            if e["hp"] > 0:
                dmg = max(1, player["str"] + 7 + random.randint(0, 12) - e["def"]) + random.randint(1, 4)
                e["hp"] = max(0, e["hp"] - dmg)
                total_msg.append(f"{e['name']} takes {dmg}")
        return f"{player['name']} spins into Whirlwind! " + "; ".join(total_msg) + "."

    if skill == "Berserk":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return f"Not enough MP to use {skill}!"
        # Buff STR, lower DEF for 3 turns
        player["berserk_turns"] = 3
        return f"{player['name']} enters Berserk! STR up, DEF down for 3 turns."

    # Mage
    if skill == "Fireball":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return "Not enough MP to cast Fireball!"
        dmg = random.randint(10, 20) + random.randint(1, 8)
        target["hp"] = max(0, target["hp"] - dmg)
        return f"{player['name']} casts Fireball! {target['name']} takes {dmg} damage."

    if skill == "Heal":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return "Not enough MP to cast Heal!"
        heal = random.randint(12, 18)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        return f"{player['name']} casts Heal! Restores {heal} HP."

    if skill == "Ice Shard":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return "Not enough MP to cast Ice Shard!"
        dmg = max(1, player["str"] * random.randint(1, 3) + 4 - target["def"]) + random.randint(6, 12)
        target["hp"] = max(0, target["hp"] - dmg)
        target["str_down_turns"] = 2
        target["str_down_amount"] = 2
        return f"{player['name']} launches Ice Shard! {target['name']} takes {dmg} damage and their STR falls!"

    if skill == "Lightning Bolt":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return "Not enough MP to cast Lightning Bolt!"
        # Ignores part of DEF
        effective_def = max(0, target["def"] - 3)
        dmg = max(1, player["str"] * random.randint(2, 5) + 12 - effective_def) + random.randint(5, 10)
        target["hp"] = max(0, target["hp"] - dmg)
        return f"{player['name']} strikes with Lightning Bolt! {target['name']} takes {dmg} damage."

    if skill == "Arcane Surge":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return "Not enough MP to cast Arcane Surge!"
        # Restore some MP and boost skill damage for 3 turns
        restored = random.randint(20, 32)
        player["mp"] = min(player["max_mp"], player["mp"] + restored)
        player["arcane_surge_turns"] = 3
        return f"{player['name']} channels Arcane Surge! Restores {restored} MP and empowers skills for 3 turns."

    # Thief
    if skill == "Quick Stab":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return "Not enough MP to use Quick Stab!"
        dmg = max(1, player["str"] * 2 + 4 - target["def"]) + random.randint(3, 8)
        target["hp"] = max(0, target["hp"] - dmg)
        return f"{player['name']} performs Quick Stab! {target['name']} takes {dmg} damage."

    if skill == "Steal":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return "Not enough MP to use Steal!"
        if random.random() < 0.7:
            gold = random.randint(20, 80)
            player["gold"] += gold
            return f"{player['name']} steals {gold} gold from {target['name']}!"
        else:
            return f"{player['name']} fails to steal anything."

    if skill == "Poison Dagger":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return "Not enough MP to use Poison Dagger!"
        dmg = max(1, player["str"] * 2 + 4 - target["def"]) + random.randint(1, 24)
        target["hp"] = max(0, target["hp"] - dmg)
        target["poison_turns"] = 3
        target["poison_damage"] = 3
        return f"{player['name']} strikes with Poison Dagger! {target['name']} takes {dmg} and is poisoned!"

    if skill == "Smoke Bomb":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return "Not enough MP to use Smoke Bomb!"
        # Chance to auto-flee or reduce enemy accuracy (simulate via reduced damage)
        if random.random() < 0.5:
            player["smoke_bomb_flee"] = True
            return f"{player['name']} uses Smoke Bomb and slips away!"
        else:
            for e in enemies:
                e["smoke_weakness_turns"] = 2
            return f"{player['name']} uses Smoke Bomb! Enemies' attacks weaken temporarily!"

    if skill == "Assassinate":
        cost = SKILL_MP_COSTS[skill]
        if not spend_mp(cost):
            return "Not enough MP to use Assassinate!"
        if target["hp"] <= target["max_hp"] // 2:
            dmg = max(1, player["str"] * 3 - target["def"]) + random.randint(4, 16)
            target["hp"] = max(0, target["hp"] - dmg)
            return f"{player['name']} performs Assassinate! {target['name']} takes {dmg} massive damage!"
        else:
            return f"Assassinate fails — {target['name']}'s HP is too high."

    return f"{player['name']} hesitates..."

# -----------------------------
# Combat
# -----------------------------
def combat(player, enemies):
    boxed_text("⚔️ Battle start!")
    for e in enemies:
        boxed_text(f"{e.get('icon', '👾')} {e['name']} (HP {e['hp']}/{e['max_hp']})")

    while player["hp"] > 0 and any(e["hp"] > 0 for e in enemies):
        # Apply ongoing player buffs/debuffs at start of turn
        # Berserk effect
        effective_str = player["str"]
        effective_def = player["def"]
        if player.get("berserk_turns", 0) > 0:
            effective_str += 3
            effective_def = max(0, effective_def - 2)

        # Arcane Surge boosts skill damage (we'll add small bonus inside skill where appropriate)
        surge_active = player.get("arcane_surge_turns", 0) > 0

        print(f"\n🧝 {player['name']} HP: {player['hp']}/{player['max_hp']}  |  MP: {player['mp']}/{player['max_mp']}")
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
                dmg = max(1, effective_str + random.randint(1, 7) - target["def"]) + random.randint(1, 3)
                if surge_active:
                    dmg += 2
                target["hp"] = max(0, target["hp"] - dmg)
                boxed_text(color_text(f"{player['name']} attacks! {target['name']} takes {dmg} damage."))
                boxed_text(color_text(f"{target['name']} HP: {target['hp']}/{target['max_hp']}"))
                time.sleep(0.3)

        elif choice == "2":
            player["defending"] = True
            boxed_text(f"{player['name']} braces for impact.")
            time.sleep(0.3)

        elif choice == "3":
            if not player["skills"]:
                boxed_text("You don't know any skills.")
            else:
                print("\nSkills:")
                for idx, sk in enumerate(player["skills"], start=1):
                    mp_cost = SKILL_MP_COSTS.get(sk, "?")
                    boxed_text(f"{idx}) {sk} (MP {mp_cost})")
                try:
                    sidx = int(input("> ").strip()) - 1
                    if 0 <= sidx < len(player["skills"]):
                        target = next((e for e in enemies if e["hp"] > 0), None)
                        skill_name = player["skills"][sidx]
                        if target:
                            msg = use_skill(player, skill_name, target, enemies)
                            boxed_text(msg)
                            boxed_text(f"{target['name']} HP: {target['hp']}/{target['max_hp']}")
                            time.sleep(0.3)
                except ValueError:
                    boxed_text("Invalid selection.")

        elif choice == "4":
            boxed_text(f"Inventory: Potions {player['inventory'].get('Potion',0)} | Ethers {player['inventory'].get('Ether',0)}")
            boxed_text("Choose item: 1) Potion  2) Ether  3) Back")
            item_choice = input("> ").strip()
            if item_choice == "1" and player["inventory"].get("Potion", 0) > 0:
                heal_amount = 10 + (player["level"] * 2) + random.randint(5, 10)
                before = player["hp"]
                player["hp"] = min(player["max_hp"], player["hp"] + heal_amount)
                player["inventory"]["Potion"] -= 1
                boxed_text(f"You use a Potion! Restores {player['hp'] - before} HP.")
            elif item_choice == "2" and player["inventory"].get("Ether", 0) > 0:
                mp_restore = 10 + (player["level"] * 2) + random.randint(2, 10)
                before = player["mp"]
                player["mp"] = min(player["max_mp"], player["mp"] + mp_restore)
                player["inventory"]["Ether"] -= 1
                boxed_text(f"You use an Ether! Restores {player['mp'] - before} MP.")
            elif item_choice == "3":
                pass
            else:
                boxed_text("No item available.")

        elif choice == "5":
            # Smoke Bomb special flee
            if player.get("smoke_bomb_flee"):
                boxed_text("You slip away under the cover of smoke!")
                player["smoke_bomb_flee"] = False
                return False
            if all(e.get("fleeable", True) for e in enemies) and random.random() < 0.55:
                boxed_text("You fled successfully!")
                return False
            else:
                boxed_text("Couldn't get away!")

        # Enemy turn
        for e in enemies:
            if e["hp"] > 0:
                # Apply ongoing enemy effects
                if e.get("poison_turns", 0) > 0:
                    e["hp"] = max(0, e["hp"] - e.get("poison_damage", 3))
                    e["poison_turns"] -= 1
                    boxed_text(f"{e['name']} suffers {e.get('poison_damage',3)} poison damage.")

                if e.get("stunned", 0) > 0:
                    boxed_text(f"{e['name']} is stunned and can't attack!")
                    e["stunned"] -= 1
                    continue

                base = max(1, e["str"] - effective_def)
                # Debuff from Ice Shard
                if e.get("str_down_turns", 0) > 0:
                    base = max(1, base - e.get("str_down_amount", 2))
                    e["str_down_turns"] -= 1

                # Smoke Bomb weakening
                if e.get("smoke_weakness_turns", 0) > 0:
                    base = max(1, base - 2)
                    e["smoke_weakness_turns"] -= 1

                bonus = random.randint(1, 6) if e["name"] == FINAL_BOSS_NAME else random.randint(1, 3)
                dmg = base + bonus
                if player["defending"]:
                    dmg = max(1, dmg // 2)
                player["hp"] = max(0, player["hp"] - dmg)
                boxed_text(f"{e['name']} attacks! {player['name']} takes {dmg} damage.")
                time.sleep(0.3)

        # Reset defending
        player["defending"] = False

        # Tick down player buffs
        if player.get("berserk_turns", 0) > 0:
            player["berserk_turns"] -= 1
        if player.get("arcane_surge_turns", 0) > 0:
            player["arcane_surge_turns"] -= 1

    # End-of-battle resolution
    if player["hp"] > 0:
        total_exp = sum(e.get("exp_reward", 0) for e in enemies)
        total_gold = sum(e.get("gold_reward", 0) for e in enemies)
        boxed_text("🏆 Victory!")

        for e in enemies:
            boxed_text(f"{e['name']} defeated! +{e.get('exp_reward',0)} EXP, +{e.get('gold_reward',0)} Gold")
            if random.random() < 0.3:
                player["inventory"]["Potion"] = player["inventory"].get("Potion", 0) + 1
                boxed_text(f"💊 {e['name']} dropped a Potion!")

        player["exp"] += total_exp
        player["gold"] += total_gold

        # Level up sequence
        while player["exp"] >= player["exp_to_next"]:
            player["level"] += 1
            player["exp"] -= player["exp_to_next"]
            player["exp_to_next"] = int(player["exp_to_next"] * 1.3)
            player["max_hp"] += 5 + random.randint(2, 10)
            player["str"] += 3 + random.randint(2, 10)
            player["def"] += 2 + random.randint(2, 10)
            player["max_mp"] += 4 + random.randint(2, 10)
            player["hp"] = player["max_hp"]
            player["mp"] = player["max_mp"]
            boxed_text(f"🎉 {player['name']} leveled up to Level {player['level']}!")
            boxed_text(f"Max HP:{player ["max_hp"]}, STR:{player ["str"]}, DEF:{player ["def"]}, Max MP:{player ["max_mp"]},")
            # Skill unlock checks
            unlocks = SKILL_UNLOCKS.get(player["class"], {})
            if player["level"] in unlocks:
                new_skill = unlocks[player["level"]]
                if new_skill not in player["skills"]:
                    player["skills"].append(new_skill)
                    boxed_text(f"✨ {player['name']} learned a new skill: {new_skill}!")

        boxed_text(f"Progress → Lv {player['level']} | EXP {player['exp']}/{player['exp_to_next']} | Gold {player['gold']} | HP {player['hp']}/{player['max_hp']} | MP {player['mp']}/{player['max_mp']}")

        if any(e["name"] == FINAL_BOSS_NAME for e in enemies):
            boxed_text("🌟 You have defeated the Dragon Lord! The land is saved!")
            boxed_text("🎉 Congratulations, you completed the adventure!")
            return "GAME_WON"

        return True
    else:
        boxed_text("💀 You were defeated...")
        return "GAME_OVER"

# -----------------------------
# Exploration
# -----------------------------
def explore_area(area, player):
    if area == "FIELDS":
        boxed_text("🌾 You venture into the Fields...")
        enemies = [
            {"name": "Slime", "hp": 25, "max_hp": 25, "str": 3, "def": 6, "exp_reward": 15 + random.randint(2, 7), "gold_reward": 3 + random.randint(2, 7), "fleeable": True, "icon": "👾"},
            {"name": "Bee", "hp": 18, "max_hp": 18, "str": 3, "def": 3, "exp_reward": 6 + random.randint(2, 7), "gold_reward": 2 + random.randint(2, 7), "fleeable": True, "icon": "🐝"},
            {"name": "Bee", "hp": 18, "max_hp": 18, "str": 3, "def": 3, "exp_reward": 6 + random.randint(2, 7), "gold_reward": 2 + random.randint(2, 7), "fleeable": True, "icon": "🐝"}
        ]
    elif area == "FOREST":
        boxed_text("🌲 You enter the dark Forest...")
        enemies = [
            {"name": "Goblin", "hp": 70, "max_hp": 70, "str": 15 + random.randint(2, 20), "def": 18 + random.randint(2, 30), "exp_reward": 18 + random.randint(2, 10), "gold_reward": 20 + random.randint(2, 10), "fleeable": True, "icon": "👹"},
            {"name": "Wolf", "hp": 65, "max_hp": 65, "str": 13 + random.randint(2, 20), "def": 16 + random.randint(2, 30), "exp_reward": 19 + random.randint(2, 10), "gold_reward": 20 + random.randint(2, 8), "fleeable": True, "icon": "🐺"},
            {"name": "Killer Bee", "hp": 30, "max_hp": 30, "str": 6, "def": 4, "exp_reward": 12 + random.randint(2, 7), "gold_reward": 14 + random.randint(2, 12), "fleeable": True, "icon": "🐝"},
            {"name": "Dragon Spawn", "hp": 150, "max_hp": 150, "str": 18 + random.randint(2, 20), "def": 15 + random.randint(2, 20), "exp_reward": 100, "gold_reward": 20, "fleeable": True, "icon": "🐉"}
        ]
    elif area == "CAVE":
        boxed_text("🪨 You descend into the Cave...")
        enemies = [
            {"name": "Bat", "hp": 15, "max_hp": 15, "str": 5, "def": 2 + random.randint(2, 10), "exp_reward": 7, "gold_reward": 4, "fleeable": True, "icon": "🦇"},
            {"name": "Dragon Spawn", "hp": 150, "max_hp": 150, "str": 18 + random.randint(2, 20), "def": 15 + random.randint(2, 20), "exp_reward": 100, "gold_reward": 20, "fleeable": True, "icon": "🐉"},
            {"name": FINAL_BOSS_NAME, "hp": 1000, "max_hp": 1000, "str": 60 + random.randint(2, 20), "def": 65 + random.randint(2, 20), "exp_reward": 500, "gold_reward": 20, "fleeable": False, "icon": "🐉"},
        ]
    else:
        boxed_text("Nothing to explore here...")
        return

    # Start combat
    result = combat(player, enemies)
    return result

# -----------------------------
# Town
# -----------------------------
def town_menu(player):
    while True:
        boxed_text(f"Welcome Hero, Please explore the Fields and Forest to train. The Dragon Lord is Dwelling in the Cave, Use the inn to rest and Buy from the shop to prepare for your Adventure.")
        print("\n🏘️ Town")
        print("1) Rest at Inn (5 gold)")
        print("2) Explore Fields")
        print("3) Explore Forest")
        print("4) Explore Cave")
        print("5) Visit Shop")
        print("6) View Status")
        print("7) Exit")
        choice = input("> ").strip()

        if choice == "1":
            if player["gold"] >= 5:
                player["gold"] -= 5
                player["hp"] = player["max_hp"]
                player["mp"] = player["max_mp"]
                boxed_text("You rest at the inn. HP and MP fully restored.")
            else:
                boxed_text("Not enough gold.")

        elif choice == "2":
            return "FIELDS"
        elif choice == "3":
            return "FOREST"
        elif choice == "4":
            return "CAVE"

        elif choice == "5":
            shop(player)

        elif choice == "6":
            print(f"Name: {player['name']} ({player['class']})")
            print(f"Lv {player['level']}  HP {player['hp']}/{player['max_hp']}  MP {player['mp']}/{player['max_mp']}")
            print(f"STR {player['str']}  DEF {player['def']}  Gold {player['gold']}")
            print(f"Skills: {', '.join(player['skills'])}")
            print(f"Inventory: {player['inventory']}")

        elif choice == "7":
            return "EXIT"

        else:
            boxed_text("Invalid choice.")

# -----------------------------
# Main loop
# -----------------------------
def main():
    while True:
        start_time = time.time()   # track start of run

        # Create player
        boxed_text('Hello, adventure! Please name your Hero')
        name = input("Enter your hero's name: ").strip() or "Hero"
        boxed_text("Choose class: 1) Warrior  2) Mage  3) Thief")
        cls_choice = input("> ").strip()
        cls_map = {"1": "Warrior", "2": "Mage", "3": "Thief"}
        cls_name = cls_map.get(cls_choice, "Warrior")
        player = create_player(name, cls_name)

        # Town loop
        result = None
        while True:
            selection = town_menu(player)

            if selection == "EXIT":
                result = "EXIT"
                break
            elif selection in ("FIELDS", "FOREST", "CAVE"):
                result = explore_area(selection, player)
                if result in ("GAME_WON", "GAME_OVER"):
                    break

        # End time + elapsed
        end_time = time.time()
        elapsed = int(end_time - start_time)
        minutes, seconds = divmod(elapsed, 60)

        # Outcome messages
        if result == "GAME_WON":
            boxed_text("\n🌟 You completed your adventure!")
        elif result == "GAME_OVER":
            boxed_text("\n💀 Your adventure has ended.")
        else:
            boxed_text("\n👋 You left the adventure for now.")

        boxed_text(f"⏱️ Time spent on your adventure: {minutes}m {seconds}s")
        boxed_text("Thanks for playing!")

        # Retry prompt
        again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if again != "y":
            break

if __name__ == "__main__":
    main()