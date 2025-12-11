import random

# -----------------------------------
# Data and helpers
# -----------------------------------
AREA_ICONS = {
    "Fields": "🌾",
    "Forest": "🌲",
    "Cave": "🪨",
}

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

# -----------------------------------
# Player
# -----------------------------------
class Player:
    def __init__(self, name, strength=5, defense=3):
        self.name = name
        self.icon = "🧝"
        self.level = 1

        self.max_health = 30
        self.health = self.max_health
        self.strength = strength
        self.defense = defense

        self.gold = 0
        self.exp = 0
        self.exp_to_next = 20

        # simple state for defend action
        self.defending = False

    def is_alive(self):
        return self.health > 0

    def gain_exp(self, amount):
        print(f"{self.name} gains {amount} EXP!")
        self.exp += amount
        # loop allows multiple level-ups if enough EXP is gained
        while self.exp >= self.exp_to_next:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)

        self.max_health += 5
        self.strength += 2
        self.defense += 1
        self.health = self.max_health

        print(f"🎉 Level up! {self.name} is now Level {self.level}.")
        print(f"Stats → HP {self.max_health}, STR {self.strength}, DEF {self.defense}")

    def show_progress(self):
        print(f"Progress → Level {self.level} | EXP {self.exp}/{self.exp_to_next} | Gold {self.gold} | HP {self.health}/{self.max_health}")

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
# Encounters
# -----------------------------------
def encounter(area_name):
    # You can expand these pools freely; rewards travel with enemy instances
    if area_name == "Fields":
        return [Enemy("Slime", "🫧", 20, 4, 2, 8, 6)]
    if area_name == "Forest":
        return [Enemy("Goblin", "👹", 28, 6, 3, 12, 10)]
    if area_name == "Cave":
        # Example: two enemies in one fight
        return [
            Enemy("Bat", "🦇", 18, 5, 2, 6, 5),
            Enemy("Skeleton", "💀", 34, 7, 4, 18, 14),
        ]
    return []

# -----------------------------------
# Combat
# -----------------------------------
def combat(player, enemies):
    print("\n⚔️ Battle start!")
    for e in enemies:
        print(f" - {e.icon} {e.name} (HP {e.health}/{e.max_health})")

    while player.is_alive() and any(e.is_alive() for e in enemies):
        # --- Player turn ---
        print(f"\n{player.icon} {player.name} HP: {player.health}/{player.max_health}")
        print("Choose an action:")
        print("1) Attack  2) Defend  3) Flee")
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
            # Flee succeeds if all enemies are fleeable and chance succeeds
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

        # Progress tracker after battle
        player.show_progress()
        return True
    else:
        print("\n💀 You were defeated...")
        return False

# -----------------------------------
# Exploration
# -----------------------------------
def explore_area(player, area_name):
    print(f"\n{AREA_ICONS.get(area_name, '🧭')} You venture into the {area_name}...")
    # 65% chance of battle, else chance of finding gold or nothing
    if random.random() < 0.65:
        enemies = encounter(area_name)
        if enemies:
            combat(player, enemies)
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
            explore_area(player, "Cave")
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
# Main
# -----------------------------------
def main():
    print("Welcome to Dragon Quest–style Text RPG!")
    name = input("Enter your name: ").strip() or "Adventurer"
    player = Player(name)
    print(f"\n✨ Your Journey Begins ✨\n{player.name} the adventurer (Level {player.level})")
    player.show_progress()
    town_menu(player)

if __name__ == "__main__":
    main()