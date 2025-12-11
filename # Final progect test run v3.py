# Final progect test run v3




import random

import time

# Basic class icons
class_icons = {
    "warrior": "⚔️",
    "mage": "🪄",
    "rogue": "🗡️",
    "ninja": "🥷",
    "healer": "✨",
    "adventurer": "🧭"
}


class Character:
    def __init__(self, name, char_class, icon="❓"):
        self.name = name
        self.char_class = char_class
        self.icon = icon

        # Base stats (set later by class choice)
        self.health = 10
        self.strength = 5
        self.speed = 5
        self.defense = 5
        self.magic_attack = 5
        self.magic_defense = 5
        self.spirit = 5
        self.accuracy = 10

        # Progression
        self.level = 1
        self.exp = 0
        self.exp_to_next = 20

    def __str__(self):
        return (f"{self.icon} {self.name} the {self.char_class}\n"
                f"Level: {self.level}\n"
                f"EXP: {self.exp}/{self.exp_to_next}\n"
                f"❤️ Health: {self.health}\n"
                f"💪 Strength: {self.strength}\n"
                f"⚡ Speed: {self.speed}\n"
                f"🛡️ Defense: {self.defense}\n"
                f"🔥 Magic Attack: {self.magic_attack}\n"
                f"🔮 Magic Defense: {self.magic_defense}\n"
                f"✨ Spirit: {self.spirit}\n"
                f"🎯 Accuracy: {self.accuracy}")

    def gain_exp(self, amount):
        print(f"{self.icon} {self.name} gains {amount} EXP!")
        self.exp += amount
        while self.exp >= self.exp_to_next:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)
        print(f"\n{self.icon} {self.name} leveled up to Level {self.level}!")

        # Guaranteed baseline growth
        self.health += 2
        self.strength += 1
        self.speed += 1
        self.defense += 1
        self.magic_attack += 1
        self.magic_defense += 1
        self.spirit += 1
        self.accuracy += 1

        # Class-specific growth
        cc = self.char_class.lower()
        if cc == "warrior":
            self.health += 4; self.defense += 2; self.strength += 2
        elif cc == "mage":
            self.magic_attack += 3; self.spirit += 2
        elif cc == "rogue":
            self.speed += 3; self.accuracy += 2
        elif cc == "ninja":
            self.speed += 3; self.strength += 2
        elif cc == "healer":
            self.spirit += 3; self.magic_defense += 2
        else:  # adventurer fallback
            self.health += 2; self.strength += 2

        # Random growth for variety
        rand_health = random.randint(0, 3)
        rand_str = random.randint(0, 2)
        rand_spd = random.randint(0, 2)
        rand_def = random.randint(0, 2)
        rand_mag = random.randint(0, 2)
        rand_mdef = random.randint(0, 2)
        rand_spirit = random.randint(0, 2)
        rand_acc = random.randint(0, 2)

        self.health += rand_health
        self.strength += rand_str
        self.speed += rand_spd
        self.defense += rand_def
        self.magic_attack += rand_mag
        self.magic_defense += rand_mdef
        self.spirit += rand_spirit
        self.accuracy += rand_acc

        print(f"Extra random growth: ❤️+{rand_health}, 💪+{rand_str}, ⚡+{rand_spd}, 🛡️+{rand_def}, "
              f"🔥+{rand_mag}, 🔮+{rand_mdef}, ✨+{rand_spirit}, 🎯+{rand_acc}")

def create_character():
    name = input("Enter your character's name: ")
    print("Choose a class: [warrior, mage, rogue, ninja, healer]")
    char_class = input("Enter class: ").lower()

    # Assign base stats by class
    if char_class == "warrior":
        stats = {"hp": 80, "str": 10, "spd": 4, "def": 9, "mag": 4, "mdef": 6, "spirit": 5, "acc": 10}
    elif char_class == "mage":
        stats = {"hp": 50, "str": 4, "spd": 6, "def": 4, "mag": 12, "mdef": 8, "spirit": 7, "acc": 11}
    elif char_class == "rogue":
        stats = {"hp": 65, "str": 7, "spd": 8, "def": 6, "mag": 5, "mdef": 6, "spirit": 6, "acc": 12}
    elif char_class == "ninja":
        stats = {"hp": 60, "str": 8, "spd": 9, "def": 6, "mag": 6, "mdef": 6, "spirit": 5, "acc": 13}
    elif char_class == "healer":
        stats = {"hp": 55, "str": 5, "spd": 5, "def": 5, "mag": 7, "mdef": 8, "spirit": 10, "acc": 11}
    else:
        print("Invalid choice, defaulting to adventurer.")
        char_class = "adventurer"
        stats = {"hp": 60, "str": 6, "spd": 6, "def": 6, "mag": 6, "mdef": 6, "spirit": 6, "acc": 10}

    # Create character with chosen stats
    player = Character(name, char_class)
    player.health = stats["hp"]
    player.strength = stats["str"]
    player.speed = stats["spd"]
    player.defense = stats["def"]
    player.magic_attack = stats["mag"]
    player.magic_defense = stats["mdef"]
    player.spirit = stats["spirit"]
    player.accuracy = stats["acc"]
    return player

# Example run
hero = create_character()
print("\n✨ Your Character ✨")
print(hero)


class Enemy:
    def __init__(self, name, icon, health, strength, defense, magic_attack, magic_defense, exp_reward):
        self.name = name
        self.icon = icon
        self.health = health
        self.strength = strength
        self.defense = defense
        self.magic_attack = magic_attack
        self.magic_defense = magic_defense
        self.exp_reward = exp_reward

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return (f"{self.icon} {self.name}\n"
                f"❤️ Health: {self.health}\n"
                f"💪 Strength: {self.strength}\n"
                f"🛡️ Defense: {self.defense}\n"
                f"🔥 Magic Attack: {self.magic_attack}\n"
                f"🔮 Magic Defense: {self.magic_defense}\n"
                f"EXP Reward: {self.exp_reward}")

goblin = Enemy("Goblin", "👹", health=20, strength=5, defense=3, magic_attack=2, magic_defense=1, exp_reward=10)
skeleton = Enemy("Skeleton", "💀", health=30, strength=6, defense=4, magic_attack=3, magic_defense=2, exp_reward=15)
dragon = Enemy("Dragon", "🐉", health=100, strength=15, defense=10, magic_attack=12, magic_defense=8, exp_reward=100)

def battle_victory(player, enemy):
    print(f"\n🏆 {player.name} defeated {enemy.name}!")
    player.gain_exp(enemy.exp_reward)

def basic_attack(attacker, target):
    dmg = max(1, attacker.strength - target.defense)
    target.health -= dmg
    print(f"{attacker.icon} {attacker.name} attacks! {target.name} takes {dmg} damage.")

def combat(player, enemy):
    print(f"\n⚔️ A wild {enemy.name} appears!")
    while player.health > 0 and enemy.health > 0:
        print(f"\n{player.icon} {player.name} HP: {player.health}")
        print(f"{enemy.icon} {enemy.name} HP: {enemy.health}")
        print("\nChoose your action:")
        print(" 1) Attack")
        print(" 2) Skill")
        print(" 3) Run")

        choice = input("> ").strip()

        if choice == "1":
            basic_attack(player, enemy)
        elif choice == "2":
            # For now, just placeholder skill use
            print(f"{player.icon} {player.name} tries a skill... (to be expanded)")
        elif choice == "3":
            print(f"{player.icon} {player.name} runs away!")
            return  # Exit combat loop

        # Enemy turn if still alive
        if enemy.health > 0:
            dmg = max(1, enemy.strength - player.defense)
            player.health -= dmg
            print(f"{enemy.icon} {enemy.name} attacks! {player.name} takes {dmg} damage.")

    # Outcome
    if player.health <= 0:
        print(f"\n💀 {player.name} was defeated...")
    elif enemy.health <= 0:
        print(f"\n🏆 {player.name} defeated {enemy.name}!")
        player.gain_exp(enemy.exp_reward)

