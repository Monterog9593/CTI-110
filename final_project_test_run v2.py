import random

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
    def __init__(self, name, char_class, icon="❓"):
        self.name = name
        self.char_class = char_class
        self.icon = icon

        # Core pools
        self.max_health = 10
        self.health = 10
        self.max_mp = 10
        self.mp = 10

        # Physical + magical stats
        self.strength = 5
        self.defense = 5
        self.magic_attack = 5
        self.magic_defense = 5

        # Utility stats
        self.spirit = 5
        self.accuracy = 10
        self.speed = 5  # make sure speed exists (used in class-based growth)

        # Progression
        self.level = 1
        self.exp = 0
        self.exp_to_next = 20

        # Inventory
        self.inventory = []

    def __str__(self):
        return (
            f"{self.icon} {self.name} the {self.char_class}\n"
            f"Level: {self.level}\n"
            f"EXP: {self.exp}/{self.exp_to_next}\n"
            f"❤️ Health: {self.health}/{self.max_health}\n"
            f"🔋 MP: {self.mp}/{self.max_mp}\n"
            f"💪 Strength: {self.strength}\n"
            f"🛡️ Defense: {self.defense}\n"
            f"🔥 Magic Attack: {self.magic_attack}\n"
            f"🔮 Magic Defense: {self.magic_defense}\n"
            f"✨ Spirit: {self.spirit}\n"
            f"🎯 Accuracy: {self.accuracy}\n"
            f"⚡ Speed: {self.speed}\n"
            f"Inventory: {self.inventory}"
        )

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
        self.max_health += 2
        self.max_mp += 1
        self.strength += 1
        self.defense += 1
        self.magic_attack += 1
        self.magic_defense += 1
        self.spirit += 1
        self.accuracy += 1
        self.speed += 1

        # Class-focused bonuses
        cc = self.char_class.lower()
        if cc == "warrior":
            self.max_health += 4; self.defense += 2; self.strength += 2
        elif cc == "mage":
            self.max_mp += 3; self.magic_attack += 3; self.spirit += 2
        elif cc == "rogue":
            self.speed += 3; self.accuracy += 2; self.strength += 1
        elif cc == "ninja":
            self.speed += 3; self.strength += 2; self.accuracy += 2
        elif cc == "healer":
            self.max_health += 2; self.spirit += 3; self.magic_defense += 2
        else:  # adventurer / fallback
            self.max_health += 2; self.strength += 2; self.magic_attack += 1

        # Random growth — ensure we adjust max pools then sync current
        rand_health = random.randint(0, 3)
        rand_mp = random.randint(0, 2)
        rand_str = random.randint(0, 2)
        rand_def = random.randint(0, 2)
        rand_mag = random.randint(0, 2)
        rand_mdef = random.randint(0, 2)
        rand_spirit = random.randint(0, 2)
        rand_acc = random.randint(0, 2)
        rand_speed = random.randint(0, 2)

        self.max_health += rand_health
        self.max_mp += rand_mp
        self.strength += rand_str
        self.defense += rand_def
        self.magic_attack += rand_mag
        self.magic_defense += rand_mdef
        self.spirit += rand_spirit
        self.accuracy += rand_acc
        self.speed += rand_speed

        # Refill to new max pools after level
        self.health = self.max_health
        self.mp = self.max_mp

        print(
            f"Extra random growth: "
            f"❤️+{rand_health}, 🔋+{rand_mp}, "
            f"💪+{rand_str}, 🛡️+{rand_def}, "
            f"🔥+{rand_mag}, 🔮+{rand_mdef}, "
            f"✨+{rand_spirit}, 🎯+{rand_acc}, ⚡+{rand_speed}"
        )


def create_character():
    name = input("Enter your character's name: ")
    print("Choose a class: [warrior, mage, rogue, ninja, healer]")
    char_class = input("Enter class: ").lower()

    if char_class == "warrior":
        stats = {"hp": 80, "mp": 8, "str": 10, "def": 9, "mag": 4, "mdef": 6, "spirit": 5, "acc": 10}
    elif char_class == "mage":
        stats = {"hp": 50, "mp": 16, "str": 4, "def": 4, "mag": 12, "mdef": 8, "spirit": 7, "acc": 11}
    elif char_class == "rogue":
        stats = {"hp": 65, "mp": 9, "str": 7, "def": 6, "mag": 5, "mdef": 6, "spirit": 6, "acc": 12}
    elif char_class == "ninja":
        stats = {"hp": 60, "mp": 10, "str": 8, "def": 6, "mag": 6, "mdef": 6, "spirit": 5, "acc": 13}
    elif char_class == "healer":
        stats = {"hp": 55, "mp": 14, "str": 5, "def": 5, "mag": 7, "mdef": 8, "spirit": 10, "acc": 11}
    else:
        print("Invalid choice, defaulting to adventurer.")
        char_class = "adventurer"
        stats = {"hp": 60, "mp": 10, "str": 6, "def": 6, "mag": 6, "mdef": 6, "spirit": 6, "acc": 10}

    player = Character(name, char_class)
    player.max_health = stats["hp"]
    player.health = stats["hp"]
    player.max_mp = stats["mp"]
    player.mp = stats["mp"]
    player.strength = stats["str"]
    player.defense = stats["def"]
    player.magic_attack = stats["mag"]
    player.magic_defense = stats["mdef"]
    player.spirit = stats["spirit"]
    player.accuracy = stats["acc"]
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
