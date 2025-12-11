import random
import time
# Emoji dictionary for class icons
class_icons = {
    "warrior": "⚔️",
    "mage": "🪄",
    "rogue": "🗡️",
    "ninja": "🥷",
    "healer": "✨",
    "adventurer": "🧭"
}

class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.icon = class_icons.get(char_class, "❓")  # fallback if class not found
        self.health = 10
        self.strength = 5
        self.speed = 5
        self.defense = 5
        self.inventory = []
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
                f"Inventory: {self.inventory}")

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

        # Guaranteed growth
        self.health += 1
        self.strength += 1
        self.speed += 1
        self.defense += 1

        # Class-based bonus growth
        if self.char_class == "warrior":
            self.health += 2; self.defense += 1
        elif self.char_class == "mage":
            self.strength += 2; self.speed += 1
        elif self.char_class == "rogue":
            self.speed += 2; self.strength += 1
        elif self.char_class == "ninja":
            self.speed += 2; self.strength += 2
        elif self.char_class == "healer":
            self.health += 2; self.defense += 2
        else:
            self.health += 1; self.strength += 1

        # Random growth
        rand_health = random.randint(0, 4)
        rand_strength = random.randint(0, 4)
        rand_speed = random.randint(0, 4)
        rand_defense = random.randint(0, 4)

        self.health += rand_health
        self.strength += rand_strength
        self.speed += rand_speed
        self.defense += rand_defense

        print(f"Extra random growth: ❤️+{rand_health}, 💪+{rand_strength}, ⚡+{rand_speed}, 🛡️+{rand_defense}")



def create_character():
    name = input("Enter your character's name: ")
    print("Choose a class: [warrior, mage, rogue, ninja, healer]")
    char_class = input("Enter class: ").lower()

    if char_class == "warrior":
        health, strength, speed, defense = 15, 7, 4, 8
    elif char_class == "mage":
        health, strength, speed, defense = 8, 10, 6, 3
    elif char_class == "rogue":
        health, strength, speed, defense = 12, 6, 8, 5
    elif char_class == "ninja":
        health, strength, speed, defense = 10, 9, 9, 4
    elif char_class == "healer":
        health, strength, speed, defense = 12, 4, 5, 7
    else:
        print("Invalid choice, defaulting to adventurer.")
        health, strength, speed, defense = 10, 5, 5, 5
        char_class = "adventurer"

    player = Character(name, char_class)
    player.health = health
    player.strength = strength
    player.speed = speed
    player.defense = defense
    return player

def create_party():
    party = []
    max_members = 4

    print("Let's build your party! (up to 4 members)")
    while len(party) < max_members:
        member = create_character()
        party.append(member)

        print("\nCurrent Party Roster:")
        for i, char in enumerate(party, 1):
            print(f"\nMember {i}:\n{char}")

        # Ask if they want to add another
        if len(party) < max_members:
            cont = input("\nAdd another member? (yes/no): ").lower()
            if cont != "yes":
                break

    print("\n✨ Final Party ✨")
    for i, char in enumerate(party, 1):
        print(f"\nMember {i}:\n{char}")

    return party



party = create_party()

# Add Goblin to class_icons
class_icons["goblin"] = "👹"

def create_goblin():
    goblin = Character("Goblin", "goblin")
    goblin.health = 12     # fragile but not too weak
    goblin.strength = 4    # modest attack
    goblin.speed = 3       # slower than most party members
    goblin.defense = 2     # low defense
    return goblin

def attack(attacker, defender):
    base_damage = attacker.strength - defender.defense
    damage = max(1, base_damage + random.randint(-2, 2))  # small variation
    defender.health -= damage
    print(f"{attacker.icon} {attacker.name} attacks {defender.name} for {damage} damage!")
    if defender.health <= 0:
        print(f"{defender.icon} {defender.name} has been defeated!")



def walk_and_check_encounter(steps_taken):
    if steps_taken <= 7:
        print(f"Step {steps_taken}: Safe, no encounter yet.")
        return False
    
    # Die size shrinks after step 7
    die_size = max(2, 50 - (steps_taken - 7))
    roll = random.randint(1, die_size)
    
    # Random trigger number each roll
    trigger_number = random.randint(1, die_size)
    
    print(f"Step {steps_taken}: Rolled a d{die_size} → {roll} (Trigger: {trigger_number})")
    
    if roll == trigger_number:
        print("👹 An enemy appears! Encounter triggered!")
        return True
    return False

# Example walking loop
steps = 0
while steps < 20:
    steps += 1
    if walk_and_check_encounter(steps):
        print("⚔️ Battle begins!")
        steps = 0  # reset after encounter





def battle(party, enemies):
    print("\n⚔️ Battle Start! ⚔️")
    
    while any(member.health > 0 for member in party) and any(enemy.health > 0 for enemy in enemies):
        combatants = party + enemies
        combatants = [c for c in combatants if c.health > 0]
        combatants.sort(key=lambda c: c.speed, reverse=True)

        for fighter in combatants:
            if fighter in party and fighter.health > 0:
                target = random.choice([e for e in enemies if e.health > 0])
                attack(fighter, target)
            elif fighter in enemies and fighter.health > 0:
                target = random.choice([p for p in party if p.health > 0])
                attack(fighter, target)

            # Check victory conditions
            if not any(enemy.health > 0 for enemy in enemies):
                print("\n🎉 Victory! The party wins!")
                reward_exp = 30   # Goblin gives 30 EXP total
                distribute_exp =(party, reward_exp)
                reward_item = "Goblin Fang"
                print(f"The party found a {reward_item}!")
                for member in party:
                    member.inventory.append(reward_item)
                return
            if not any(member.health > 0 for member in party):
                print("\n💀 Defeat... The party has fallen.")
                return


