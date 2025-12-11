import random
import sys

# ===== Icons and constants =====
CLASS_ICONS = {
    "warrior": "⚔️",
    "mage": "🪄",
    "rogue": "🗡️",
    "ninja": "🥷",
    "healer": "✨",
    "adventurer": "🧭",
}
AREA_ICONS = {
    "Town": "🏘️",
    "Fields": "🌾",
    "Forest": "🌲",
    "Cave": "⛰️",
    "Dragon's Lair": "🐉",
}
ITEM_ICONS = {
    "Potion": "🧪",
    "Ether": "🔷",
    "Elixir": "💎",
}

STARTING_GOLD = 50
MAX_INVENTORY = 20

# ===== Utility =====
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def ask(prompt, valid=None):
    while True:
        ans = input(prompt).strip()
        if not valid or ans in valid:
            return ans
        print("Invalid choice.")

def press_enter():
    input("\nPress Enter to continue...")

# ===== Character =====
class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.icon = CLASS_ICONS.get(char_class, "❓")

        # Base stats (assigned by class later)
        self.health = 10
        self.max_health = 10
        self.mp = 10
        self.max_mp = 10
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

        # Economy and items
        self.gold = STARTING_GOLD
        self.inventory = []

    def __str__(self):
        return (
            f"{self.icon} {self.name} the {self.char_class}\n"
            f"Level: {self.level}  EXP: {self.exp}/{self.exp_to_next}\n"
            f"❤️ HP: {self.health}/{self.max_health}  🔋 MP: {self.mp}/{self.max_mp}\n"
            f"💪 STR: {self.strength}  ⚡ SPD: {self.speed}  🛡️ DEF: {self.defense}\n"
            f"🔥 MAG: {self.magic_attack}  🔮 MDEF: {self.magic_defense}\n"
            f"✨ SPR: {self.spirit}  🎯 ACC: {self.accuracy}\n"
            f"💰 Gold: {self.gold}  🎒 Inventory: {[item['name'] for item in self.inventory]}"
        )

    def is_alive(self):
        return self.health > 0

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

        # Baseline growth
        self.max_health += 2
        self.max_mp += 2
        self.strength += 1
        self.speed += 1
        self.defense += 1
        self.magic_attack += 1
        self.magic_defense += 1
        self.spirit += 1
        self.accuracy += 1

        # Refill pools on level up
        self.health = self.max_health
        self.mp = self.max_mp

        # Class-specific growth
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
        else:
            self.max_health += 2; self.strength += 2; self.magic_attack += 1

        # Random variety
        rand = {
            "max_health": random.randint(0, 3),
            "max_mp": random.randint(0, 2),
            "strength": random.randint(0, 2),
            "speed": random.randint(0, 2),
            "defense": random.randint(0, 2),
            "magic_attack": random.randint(0, 2),
            "magic_defense": random.randint(0, 2),
            "spirit": random.randint(0, 2),
            "accuracy": random.randint(0, 2)
        }
        for k, v in rand.items():
            setattr(self, k, getattr(self, k) + v)

        # Refill again after random growth
        self.health = self.max_health
        self.mp = self.max_mp

        print("Extra random growth:", ", ".join([f"{k}+{v}" for k, v in rand.items()]))

# ===== Enemy =====
class Enemy:
    def __init__(self, name, icon, health, strength, defense, magic_attack, magic_defense, exp_reward, gold_reward=0):
        self.name = name
        self.icon = icon
        self.health = health
        self.max_health = health
        self.strength = strength
        self.defense = defense
        self.magic_attack = magic_attack
        self.magic_defense = magic_defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return (
            f"{self.icon} {self.name}\n"
            f"❤️ HP: {self.health}/{self.max_health}\n"
            f"💪 STR: {self.strength}  🛡️ DEF: {self.defense}\n"
            f"🔥 MAG: {self.magic_attack}  🔮 MDEF: {self.magic_defense}\n"
            f"Reward: EXP {self.exp_reward}, Gold {self.gold_reward}"
        )

# ===== Items =====
SHOP_ITEMS = [
    {"name": "Potion", "icon": ITEM_ICONS["Potion"], "price": 20, "use": lambda user: heal_item(user, 30)},
    {"name": "Ether", "icon": ITEM_ICONS["Ether"], "price": 25, "use": lambda user: mp_item(user, 15)},
    {"name": "Elixir", "icon": ITEM_ICONS["Elixir"], "price": 120, "use": lambda user: elixir_item(user)},
]

def heal_item(user, amount):
    before = user.health
    user.health = clamp(user.health + amount, 0, user.max_health)
    print(f"{ITEM_ICONS['Potion']} Restored {user.health - before} HP.")

def mp_item(user, amount):
    before = user.mp
    user.mp = clamp(user.mp + amount, 0, user.max_mp)
    print(f"{ITEM_ICONS['Ether']} Restored {user.mp - before} MP.")

def elixir_item(user):
    user.health = user.max_health
    user.mp = user.max_mp
    print(f"{ITEM_ICONS['Elixir']} Fully restored HP and MP!")

def use_item(user):
    if not user.inventory:
        print("Your inventory is empty.")
        return
    print("\nInventory:")
    for i, item in enumerate(user.inventory, 1):
        print(f" {i}) {item['icon']} {item['name']}")
    choice = input("> ").strip()
    if not choice.isdigit():
        print("Cancelled.")
        return
    idx = int(choice) - 1
    if 0 <= idx < len(user.inventory):
        item = user.inventory.pop(idx)
        item["use"](user)
    else:
        print("Invalid selection.")

# ===== Skills (status-effect free) =====
def warrior_power_strike(user, target):
    cost = 2
    if user.mp < cost: print("Not enough MP!"); return
    user.mp -= cost
    dmg = max(1, user.strength + 3 - target.defense)
    target.health -= dmg
    print(f"{user.icon} {user.name} uses Power Strike! {target.name} takes {dmg} damage.")

def warrior_shield_bash(user, target):
    cost = 3
    if user.mp < cost: print("Not enough MP!"); return
    user.mp -= cost
    dmg = max(1, user.strength + 2 - target.defense)
    target.health -= dmg
    print(f"{user.icon} {user.name} uses Shield Bash! {target.name} takes {dmg} damage.")

def mage_fireball(user, target):
    cost = 4
    if user.mp < cost: print("Not enough MP!"); return
    user.mp -= cost
    dmg = max(1, user.magic_attack + 5 - target.magic_defense)
    target.health -= dmg
    print(f"{user.icon} {user.name} casts Fireball! {target.name} takes {dmg} magic damage.")

def mage_arcane_blast(user, targets):
    cost = 6
    if user.mp < cost: print("Not enough MP!"); return
    user.mp -= cost
    total = 0
    for t in targets:
        dmg = max(1, user.magic_attack + 2 - t.magic_defense)
        t.health -= dmg
        total += dmg
        print(f"{t.name} takes {dmg} damage from Arcane Blast!")
    print(f"Total AoE damage: {total}")

def rogue_backstab(user, target):
    cost = 3
    if user.mp < cost: print("Not enough MP!"); return
    user.mp -= cost
    dmg = max(1, user.strength + user.accuracy // 2 - target.defense)
    target.health -= dmg
    print(f"{user.icon} {user.name} uses Backstab! {target.name} takes {dmg} damage.")

def rogue_quick_stab(user, target):
    cost = 2
    if user.mp < cost: print("Not enough MP!"); return
    user.mp -= cost
    dmg = max(1, user.strength + 1 - target.defense)
    target.health -= dmg
    print(f"{user.icon} {user.name} uses Quick Stab! {target.name} takes {dmg} damage.")

def ninja_multi_slash(user, target):
    cost = 5
    if user.mp < cost: print("Not enough MP!"); return
    user.mp -= cost
    hits = random.randint(2, 3)
    total = 0
    for _ in range(hits):
        dmg = max(1, user.strength - target.defense)
        target.health -= dmg
        total += dmg
    print(f"{user.icon} {user.name} uses Multi-Slash! {target.name} takes {total} damage over {hits} hits.")

def ninja_shadow_strike(user, target):
    cost = 6
    if user.mp < cost: print("Not enough MP!"); return
    user.mp -= cost
    dmg = max(1, user.strength + 4 - target.defense)
    target.health -= dmg
    print(f"{user.icon} {user.name} uses Shadow Strike! {target.name} takes {dmg} damage.")

def healer_heal(user, ally):
    cost = 4
    if user.mp < cost: print("Not enough MP!"); return
    user.mp -= cost
    heal = user.spirit + user.magic_attack
    before = ally.health
    ally.health = clamp(ally.health + heal, 0, ally.max_health)
    print(f"{user.icon} {user.name} heals {ally.name} for {ally.health - before} HP!")

def healer_group_heal(user, party):
    cost = 6
    if user.mp < cost: print("Not enough MP!"); return
    user.mp -= cost
    for ally in party:
        before = ally.health
        ally.health = clamp(ally.health + user.spirit, 0, ally.max_health)
        print(f"{ally.name} recovers {ally.health - before} HP from Group Heal!")

SKILL_BOOK = {
    "warrior": [
        ("Power Strike", warrior_power_strike, "single"),
        ("Shield Bash", warrior_shield_bash, "single"),
    ],
    "mage": [
        ("Fireball", mage_fireball, "single"),
        ("Arcane Blast", mage_arcane_blast, "multi"),
    ],
    "rogue": [
        ("Backstab", rogue_backstab, "single"),
        ("Quick Stab", rogue_quick_stab, "single"),
    ],
    "ninja": [
        ("Multi-Slash", ninja_multi_slash, "single"),
        ("Shadow Strike", ninja_shadow_strike, "single"),
    ],
    "healer": [
        ("Heal", healer_heal, "ally_single"),
        ("Group Heal", healer_group_heal, "ally_multi"),
    ],
    "adventurer": [
        ("Power Strike", warrior_power_strike, "single"),
        ("Fireball", mage_fireball, "single"),
    ],
}

# ===== Combat helpers =====
def basic_attack(attacker, target):
    dmg = max(1, attacker.strength - target.defense)
    target.health -= dmg
    print(f"{attacker.icon} {attacker.name} attacks! {target.name} takes {dmg} damage.")

def enemy_attack(enemy, player):
    # Simple enemy chooses physical attack
    dmg = max(1, enemy.strength - player.defense)
    player.health -= dmg
    print(f"{enemy.icon} {enemy.name} attacks! {player.name} takes {dmg} damage.")

def choose_target(enemies):
    alive = [e for e in enemies if e.is_alive()]
    if not alive:
        return None
    print("\nChoose target:")
    for i, e in enumerate(alive, 1):
        print(f" {i}) {e.icon} {e.name} ({e.health}/{e.max_health} HP)")
    choice = input("> ").strip()
    if not choice.isdigit():
        print("Cancelled.")
        return None
    idx = int(choice) - 1
    if 0 <= idx < len(alive):
        return alive[idx]
    print("Invalid selection.")
    return None

def choose_skill(player):
    skills = SKILL_BOOK.get(player.char_class, [])
    if not skills:
        print("No skills available.")
        return None
    print("\nChoose skill:")
    for i, (name, _, _) in enumerate(skills, 1):
        print(f" {i}) {name}")
    choice = input("> ").strip()
    if not choice.isdigit():
        print("Cancelled.")
        return None
    idx = int(choice) - 1
    if 0 <= idx < len(skills):
        return skills[idx]
    print("Invalid selection.")
    return None

# ===== Combat loop (single hero vs group of enemies) =====
def combat(player, enemies, party=None):
    if party is None:
        party = [player]
    print(f"\n⚔️ Battle start!")
    for e in enemies:
        print(f" - {e.icon} {e.name} (HP {e.health}/{e.max_health})")

    while player.is_alive() and any(e.is_alive() for e in enemies):
        # Player turn
        print(f"\n{player.icon} {player.name} HP: {player.health}/{player.max_health}, MP: {player.mp}/{player.max_mp}")
        print("Actions:")
        print(" 1) Attack")
        print(" 2) Skill")
        print(" 3) Item")
        print(" 4) Run")
        choice = input("> ").strip()

        if choice == "1":
            target = next((e for e in enemies if e.health > 0), None)
            if target:
                dmg = max(1, player.strength - target.defense)
                target.health = max(0, target.health - dmg)
                print(f"{player.name} attacks! {target.name} takes {dmg} damage.")

        elif choice == "2":
            skill = choose_skill(player)
            if skill:
                name, fn, scope = skill
                if scope == "single":
                    target = choose_target(enemies)
                    if target: fn(player, target)
                elif scope == "multi":
                    fn(player, [e for e in enemies if e.is_alive()])
                elif scope == "ally_single":
                    # choose ally (only one hero now, so self)
                    fn(player, player)
                elif scope == "ally_multi":
                    fn(player, party)
        elif choice == "3":
            use_item(player)
        elif choice == "4":
            print("You fled the battle!")
            return False
        else:
            print("Turn skipped.")

        # Enemy turns
        for e in enemies:
            if e.health > 0:
                dmg = max(1, e.strength - player.defense)
                if getattr(player, "defending", False):
                    dmg = max(1, dmg // 2)
                    player.defending = False
                player.health = max(0, player.health - dmg)
                print(f"{e.name} attacks! {player.name} takes {dmg} damage.")


        # Cleanup fallen enemies
        enemies = [e for e in enemies if e.is_alive()]

    # Victory check
    if player.is_alive():
        # Calculate rewards BEFORE removing defeated enemies
        total_exp = sum(e.exp_reward for e in enemies)
        total_gold = sum(e.gold_reward for e in enemies)

        print("\n🏆 Victory!")
        print(f"Rewards: +{total_exp} EXP, +{total_gold} Gold")

        player.gain_exp(total_exp)
        player.gold += total_gold
        return True
    else:
        print("\n💀 You were defeated...")
        return False

# ===== World and progression =====
def create_character():
    print("Enter your character's name:")
    name = input("> ").strip()
    print("Choose a class: warrior, mage, rogue, ninja, healer")
    char_class = input("> ").strip().lower()
    if char_class not in CLASS_ICONS:
        char_class = "adventurer"

    player = Character(name, char_class)

    # Assign base stats by class
    if char_class == "warrior":
        player.max_health = 80; player.health = 80
        player.max_mp = 12; player.mp = 12
        player.strength = 10; player.speed = 4; player.defense = 9
        player.magic_attack = 4; player.magic_defense = 6; player.spirit = 5; player.accuracy = 10
    elif char_class == "mage":
        player.max_health = 50; player.health = 50
        player.max_mp = 18; player.mp = 18
        player.strength = 4; player.speed = 6; player.defense = 4
        player.magic_attack = 12; player.magic_defense = 8; player.spirit = 7; player.accuracy = 11
    elif char_class == "rogue":
        player.max_health = 65; player.health = 65
        player.max_mp = 12; player.mp = 12
        player.strength = 7; player.speed = 8; player.defense = 6
        player.magic_attack = 5; player.magic_defense = 6; player.spirit = 6; player.accuracy = 12
    elif char_class == "ninja":
        player.max_health = 60; player.health = 60
        player.max_mp = 14; player.mp = 14
        player.strength = 8; player.speed = 9; player.defense = 6
        player.magic_attack = 6; player.magic_defense = 6; player.spirit = 5; player.accuracy = 13
    elif char_class == "healer":
        player.max_health = 55; player.health = 55
        player.max_mp = 16; player.mp = 16
        player.strength = 5; player.speed = 5; player.defense = 5
        player.magic_attack = 7; player.magic_defense = 8; player.spirit = 10; player.accuracy = 11
    else:  # adventurer fallback
        player.max_health = 60; player.health = 60
        player.max_mp = 12; player.mp = 12
        player.strength = 6; player.speed = 6; player.defense = 6
        player.magic_attack = 6; player.magic_defense = 6; player.spirit = 6; player.accuracy = 10

    return player





def encounter(area_name):
    if area_name == "Fields":
        # Enemy(name, icon, health, strength, defense, magic_attack, magic_defense, exp_reward, gold_reward)
        return [Enemy("Slime", "🫧", 20, 4, 2, 2, 1, 8, 6)]
    if area_name == "Forest":
        return [Enemy("Goblin", "👹", 30, 6, 3, 3, 2, 12, 10)]
    if area_name == "Cave":
        return [Enemy("Skeleton", "💀", 40, 7, 4, 4, 3, 18, 14)]
    if area_name == "Dragon's Lair":
        return [Enemy("Dragon", "🐉", 120, 15, 10, 12, 8, 120, 100)]
    return []


def explore_area(player, area_name):
    print(f"\n{AREA_ICONS[area_name]} You venture into the {area_name}...")
    # 60% chance of battle
    if random.random() < 0.6:
        enemies = encounter(area_name)
        if not enemies:
            print("It is eerily quiet...")
            return
        result = combat(player, enemies)
        if not result:
            print("You retreat to town to recover...")
            player.health = max(1, player.health)  # limp back
    else:
        # Find random gold or nothing
        if random.random() < 0.5:
            found = random.randint(5, 20)
            player.gold += found
            print(f"You find a pouch with {found} gold!")
        else:
            print("You find nothing of interest.")

def visit_inn(player):
    cost = 10
    print(f"\n🏨 The Inn — Rest for {cost} gold? (y/n)")
    if ask("> ", valid=["y","n"]) == "y":
        if player.gold >= cost:
            player.gold -= cost
            player.health = player.max_health
            player.mp = player.max_mp
            print("You feel refreshed. HP and MP fully restored.")
        else:
            print("Not enough gold.")

def visit_shop(player):
    print("\n🛒 The Shop — buy items:")
    for i, it in enumerate(SHOP_ITEMS, 1):
        print(f" {i}) {it['icon']} {it['name']} — {it['price']} gold")
    print(f"Your gold: {player.gold}")
    print("Choose item number to buy, or 'b' to go back.")
    choice = input("> ").strip()
    if choice == "b":
        return
    if not choice.isdigit():
        print("Cancelled.")
        return
    idx = int(choice) - 1
    if 0 <= idx < len(SHOP_ITEMS):
        it = SHOP_ITEMS[idx]
        if len(player.inventory) >= MAX_INVENTORY:
            print("Inventory is full.")
            return
        if player.gold >= it["price"]:
            player.gold -= it["price"]
            player.inventory.append({"name": it["name"], "icon": it["icon"], "use": it["use"]})
            print(f"Purchased {it['name']}.")
        else:
            print("Not enough gold.")
    else:
        print("Invalid selection.")

def town_menu(player):
    while True:
        print(f"\n{AREA_ICONS['Town']} Town — What will you do?")
        print(" 1) Visit Inn")
        print(" 2) Visit Shop")
        print(" 3) Venture to Fields")
        print(" 4) Venture to Forest")
        print(" 5) Venture to Cave")
        print(" 6) Challenge Dragon's Lair")
        print(" 7) View Hero")
        print(" 8) Use Item")
        print(" 9) Quit")
        choice = input("> ").strip()

        if choice == "1":
            visit_inn(player)
        elif choice == "2":
            visit_shop(player)
        elif choice == "3":
            explore_area(player, "Fields")
        elif choice == "4":
            explore_area(player, "Forest")
        elif choice == "5":
            explore_area(player, "Cave")
        elif choice == "6":
            # Gate the lair behind level suggestion
            if player.level < 3:
                print("You sense overwhelming danger. Recommended level: 3+.")
                confirm = ask("Enter anyway? (y/n) ", valid=["y","n"])
                if confirm == "n":
                    continue
            explore_area(player, "Dragon's Lair")
            # Victory condition: if dragon defeated, show ending
            # We check by giving a special token: after battle, if player survived, show ending
            if player.is_alive():
                # Not perfect check for dragon kill, but good enough for prototype:
                print("\nIf you triumphed over the Dragon, the kingdom sings your name!")
        elif choice == "7":
            print("\n✨ Your Hero ✨")
            print(player)
            press_enter()
        elif choice == "8":
            use_item(player)
        elif choice == "9":
            print("Farewell, adventurer.")
            sys.exit(0)
        else:
            print("Invalid choice.")

# ===== Game entry point =====
def main():
    print("Welcome to Dragon Quest–style Text RPG!")
    player = create_character()
    print("\n✨ Your Journey Begins ✨")
    print(player)
    press_enter()
    town_menu(player)

    enemies = encounter("Fields")   # <-- defines enemies from encounter()
    

    
    combat(player, enemies)

    
if __name__ == "__main__":
    main()