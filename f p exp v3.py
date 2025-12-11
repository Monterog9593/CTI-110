import random

# -----------------------------------
# Data and helpers
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

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

# -----------------------------------
# Player
# -----------------------------------
class Player:
    def __init__(self, name, cls_name="Warrior"):
        self.name = name
        self.icon = "🧝"
        self.level = 1

        # Class stats
        cls = CLASSES.get(cls_name, CLASSES["Warrior"])
        self.max_health = cls["hp"]
        self.health = self.max_health
        self.strength = cls["str"]
        self.defense = cls["def"]
        self.skills = list(cls["skills"])  # copy

        self.gold = 0
        self.exp = 0
        self.exp_to_next = 20

        self.defending = False
        self.cls_name = cls_name

    def is_alive(self):
        return self.health > 0

    def gain_exp(self, amount):
        print(f"{self.name} gains {amount} EXP!")
        self.exp += amount
        while self.exp >= self.exp_to_next:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)

        # Generic growth; can be class‑specific later
        self.max_health += 5
        self.strength += 2
        self.defense += 1
        self.health = self.max_health

        print(f"🎉 Level up! {self.name} is now Level {self.level}.")
        print(f"Stats → HP {self.max_health}, STR {self.strength}, DEF {self.defense}")

        # Optional: unlock skills by level
        self._check_skill_unlocks()

    def _check_skill_unlocks(self):
        # Simple unlock example
        if self.cls_name == "Warrior" and self.level == 3 and "Rend Armor" not in self.skills:
            self.skills.append("Rend Armor")
            print("✨ New skill learned: Rend Armor")
        if self.cls_name == "Mage" and self.level == 3 and "Ice Spike" not in self.skills:
            self.skills.append("Ice Spike")
            print("✨ New skill learned: Ice Spike")
        if self.cls_name == "Thief" and self.level == 3 and "Smoke Bomb" not in self.skills:
            self.skills.append("Smoke Bomb")
            print("✨ New skill learned: Smoke Bomb")

    def show_progress(self):
        print(f"Progress → {self.cls_name} {self.name} | Lv {self.level} | EXP {self.exp}/{self.exp_to_next} | Gold {self.gold} | HP {self.health}/{self.max_health}")

# -----------------------------------
# Enemy
# -----------------------------------
class Enemy:
    def __init__(self, name, icon, health, strength, defense, exp_reward, gold_reward, fleeable=True):
        self.name = name
        self.icon = icon
        self.max_health = health
        self.health = health
        self.strength = strength
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.fleeable = fleeable

    def is_alive(self):
        return self.health > 0

# -----------------------------------
# Skills
# -----------------------------------
def use_skill(player, skill, target, enemies):
    # Return a message string
    if skill == "Power Strike":
        dmg = max(1, player.strength * 2 - target.defense)
        target.health = clamp(target.health - dmg, 0, target.max_health)
        return f"{player.name} uses Power Strike! {target.name} takes {dmg} damage."

    elif skill == "Rend Armor":
        # Reduce target defense temporarily (one battle; simple flat reduction)
        reduction = 2
        target.defense = max(0, target.defense - reduction)
        return f"{player.name} rends armor! {target.name}'s DEF drops by {reduction}."

    elif skill == "Fireball":
        dmg = random.randint(10, 16)
        target.health = clamp(target.health - dmg, 0, target.max_health)
        return f"{player.name} casts Fireball! {target.name} takes {dmg} damage."

    elif skill == "Ice Spike":
        dmg = random.randint(8, 12)
        target.health = clamp(target.health - dmg, 0, target.max_health)
        return f"{player.name} conjures Ice Spike! {target.name} takes {dmg} damage."

    elif skill == "Heal":
        heal = random.randint(12, 18)
        player.health = clamp(player.health + heal, 0, player.max_health)
        return f"{player.name} casts Heal! Restores {heal} HP."

    elif skill == "Quick Stab":
        dmg = max(1, player.strength + 2 - target.defense)
        target.health = clamp(target.health - dmg, 0, target.max_health)
        return f"{player.name} performs Quick Stab! {target.name} takes {dmg} damage."

    elif skill == "Steal":
        # Chance to steal extra gold; fail message if nothing
        if random.random() < 0.7:
            gold = random.randint(3, 8)
            player.gold += gold
            return f"{player.name} steals {gold} gold from {target.name}!"
        else:
            return f"{player.name} fails to steal anything."

    elif skill == "Smoke Bomb":
        # Attempt to flee even from multiple enemies (fails vs boss)
        if all(e.fleeable for e in enemies) and random.random() < 0.85:
            # Signal to combat we fled successfully
            return "SMOKE_BOMB_ESCAPE"
        else:
            return f"{player.name} throws a smoke bomb, but the enemies press on!"

    return f"{player.name} hesitates..."

# -----------------------------------
# Encounters (includes final boss)
# -----------------------------------
def encounter(area_name):
    if area_name == "Fields":
        return [Enemy("Slime", "🫧", 20, 4, 2, 8, 6)]
    if area_name == "Forest":
        # Weighted basic or tougher enemy
        if random.random() < 0.5:
            return [Enemy("Goblin", "👹", 28, 6, 3, 12, 10)]
        else:
            return [Enemy("Wolf", "🐺", 32, 7, 3, 14, 12)]
    if area_name == "Cave":
        # 20% chance of final boss
        if random.random() < 0.2:
            return [Enemy(FINAL_BOSS_NAME, "🐉", 95, 13, 8, 60, 120, fleeable=False)]
        else:
            # Sometimes two enemies
            if random.random() < 0.5:
                return [Enemy("Bat", "🦇", 18, 5, 2, 6, 5),
                        Enemy("Skeleton", "💀", 34, 7, 4, 18, 14)]
            else:
                return [Enemy("Skeleton", "💀", 34, 7, 4, 18, 14)]
    return []

# -----------------------------------
# Combat
# -----------------------------------
def combat(player, enemies):
    print("\n⚔️ Battle start!")
    for e in enemies:
        print(f" - {e.icon} {e.name} (HP {e.health}/{e.max_health}, STR {e.strength}, DEF {e.defense})")

    while player.is_alive() and any(e.is_alive() for e in enemies):
        # --- Player turn ---
        print(f"\n{player.icon} {player.name} HP: {player.health}/{player.max_health}")
        print("Choose an action:")
        print("1) Attack  2) Defend  3) Skills  4) Flee")
        choice = input("> ").strip()

        if choice == "1":
            target = next((e for e in enemies if e.is_alive()), None)
            if target:
                dmg = max(1, player.strength - target.defense)
                target.health = clamp(target.health - dmg, 0, target.max_health)
                print(f"{player.name} attacks! {target.name} takes {dmg} damage.")

        elif choice == "2":
            player.defending = True
            print(f"{player.name} braces for impact. Incoming damage will be reduced.")

        elif choice == "3":
            if not player.skills:
                print("You don't know any skills.")
            else:
                print("Choose a skill:")
                for idx, sk in enumerate(player.skills, start=1):
                    print(f"{idx}) {sk}")
                try:
                    sidx = int(input("> ").strip()) - 1
                    if 0 <= sidx < len(player.skills):
                        target = next((e for e in enemies if e.is_alive()), None)
                        skill_name = player.skills[sidx]
                        if target:
                            msg = use_skill(player, skill_name, target, enemies)
                            if msg == "SMOKE_BOMB_ESCAPE":
                                print("You vanish in smoke and escape!")
                                return False
                            else:
                                print(msg)
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid selection.")

        elif choice == "4":
            if all(e.fleeable for e in enemies) and random.random() < 0.55:
                print("You fled successfully!")
                return False
            else:
                print("Couldn't get away!")
        else:
            print("You hesitate...")

        # --- Enemy turn ---
        for e in enemies:
            if e.is_alive():
                base = max(1, e.strength - player.defense)
                dmg = base if not player.defending else max(1, base // 2)
                player.health = clamp(player.health - dmg, 0, player.max_health)
                print(f"{e.name} attacks! {player.name} takes {dmg} damage.")

        # defend lasts one enemy phase
        player.defending = False

    # --- Victory / Defeat ---
    if player.is_alive():
        # Rewards calculated BEFORE any enemy cleanup
        total_exp = sum(e.exp_reward for e in enemies)
        total_gold = sum(e.gold_reward for e in enemies)

        print("\n🏆 Victory!")
        for e in enemies:
            print(f"{e.name} defeated! +{e.exp_reward} EXP, +{e.gold_reward} Gold")
        print(f"Total: +{total_exp} EXP, +{total_gold} Gold")

        player.gain_exp(total_exp)
        player.gold += total_gold
        player.show_progress()

        # Final objective check
        if any(e.name == FINAL_BOSS_NAME for e in enemies):
            print("\n🌟 You have defeated the Dragon Lord! The land is saved!")
            print("🎉 Congratulations, you completed the adventure!")
            # End the game cleanly
            return "GAME_WON"

        return True
    else:
        print("\n💀 You were defeated...")
        return False

# -----------------------------------
# Exploration
# -----------------------------------
def explore_area(player, area_name):
    print(f"\n{AREA_ICONS.get(area_name, '🧭')} You venture into the {area_name}...")
    if random.random() < 0.65:
        enemies = encounter(area_name)
        if enemies:
            result = combat(player, enemies)
            if result == "GAME_WON":
                return "GAME_WON"
        else:
            print("It's eerily quiet...")
    else:
        if random.random() < 0.6:
            found = random.randint(5, 25)
            player.gold += found
            print(f"You find a pouch with {found} gold!")
            player.show_progress()
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
        print("4) Rest at Inn")
        print("5) View Status")
        print("6) Quit")

        choice = input("> ").strip()
        if choice == "1":
            explore_area(player, "Fields")
        elif choice == "2":
            explore_area(player, "Forest")
        elif choice == "3":
            res = explore_area(player, "Cave")
            if res == "GAME_WON":
                break
        elif choice == "4":
            player.health = player.max_health
            print("You rest and recover your health.")
            player.show_progress()
        elif choice == "5":
            player.show_progress()
        elif choice == "6":
            print("Farewell, adventurer!")
            break
        else:
            print("Invalid selection.")

# -----------------------------------
# Character creation
# -----------------------------------
def create_character():
    print("Welcome to Dragon Quest–style Text RPG!")
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
    player = Player(name, cls_choice)
    print(f"\n✨ Your Journey Begins ✨\n{player.cls_name} {player.name} (Level {player.level})")
    player.show_progress()
    return player

# -----------------------------------
# Main
# -----------------------------------
def main():
    player = create_character()
    town_menu(player)
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()