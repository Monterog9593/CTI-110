import random
import sys
from dataclasses import dataclass, field
from typing import List, Optional

# =========================
# Data models
# =========================

@dataclass
class Spell:
    name: str
    mp_cost: int
    power: int
    target: str  # "enemy" or "self"
    kind: str    # "damage" or "heal"

@dataclass
class Item:
    name: str
    kind: str    # "heal" or "escape"
    amount: int = 0

@dataclass
class Enemy:
    name: str
    max_hp: int
    atk: int
    defense: int
    exp_reward: int
    gold_reward: int
    fleeable: bool = True
    hp: int = field(init=False)

    def __post_init__(self):
        self.hp = self.max_hp

@dataclass
class Player:
    name: str
    level: int = 1
    max_hp: int = 30
    hp: int = 30
    max_mp: int = 10
    mp: int = 10
    atk: int = 8
    defense: int = 4
    exp: int = 0
    gold: int = 20
    inventory: List[Item] = field(default_factory=lambda: [Item("Herb", "heal", 25)])
    spells: List[Spell] = field(default_factory=lambda: [
        Spell("Fireball", 3, 12, "enemy", "damage"),
        Spell("Heal", 4, 18, "self", "heal"),
    ])

    def is_alive(self) -> bool:
        return self.hp > 0

    def gain_exp(self, amount: int):
        self.exp += amount
        self.check_level_up()

    def check_level_up(self):
        # Simple DQ-like curve: thresholds rise roughly quadratically
        thresholds = [0, 10, 30, 60, 100, 160, 240, 340, 460, 600]
        next_lv = self.level + 1
        if next_lv < len(thresholds) and self.exp >= thresholds[next_lv]:
            self.level += 1
            hp_gain = random.randint(5, 9)
            mp_gain = random.randint(2, 4)
            atk_gain = random.randint(2, 3)
            def_gain = random.randint(1, 2)

            self.max_hp += hp_gain
            self.max_mp += mp_gain
            self.atk += atk_gain
            self.defense += def_gain
            self.hp = self.max_hp
            self.mp = self.max_mp

            print(f"\n{self.name} reached Level {self.level}!")
            print(f"Max HP +{hp_gain}, Max MP +{mp_gain}, ATK +{atk_gain}, DEF +{def_gain}")
            # Learn a spell at certain levels
            if self.level == 3:
                self.spells.append(Spell("Blaze", 5, 20, "enemy", "damage"))
                print(f"{self.name} learned Blaze!")
            if self.level == 5:
                self.spells.append(Spell("Midheal", 6, 35, "self", "heal"))
                print(f"{self.name} learned Midheal!")

# =========================
# Combat system
# =========================

def physical_damage(attacker_atk: int, defender_def: int) -> int:
    base = attacker_atk - defender_def
    variance = random.randint(-2, 2)
    dmg = max(1, base + variance)
    return dmg

def use_spell(player: Player, spell: Spell, enemy: Enemy) -> Optional[str]:
    if player.mp < spell.mp_cost:
        return "Not enough MP."
    player.mp -= spell.mp_cost
    if spell.kind == "damage" and spell.target == "enemy":
        dmg = spell.power + random.randint(-3, 3)
        enemy.hp = max(0, enemy.hp - dmg)
        return f"{player.name} casts {spell.name}! It deals {dmg} damage."
    elif spell.kind == "heal" and spell.target == "self":
        heal = spell.power + random.randint(-2, 2)
        player.hp = min(player.max_hp, player.hp + heal)
        return f"{player.name} casts {spell.name}! Restored {heal} HP."
    return None

def use_item(player: Player, item_name: str) -> str:
    for i, it in enumerate(player.inventory):
        if it.name.lower() == item_name.lower():
            if it.kind == "heal":
                heal = it.amount + random.randint(0, 4)
                player.hp = min(player.max_hp, player.hp + heal)
                # Consume item
                player.inventory.pop(i)
                return f"{player.name} uses {it.name}. Restored {heal} HP."
            elif it.kind == "escape":
                player.inventory.pop(i)
                return "Smoke bomb! You make a swift escape..."
    return "You don't have that item."

def enemy_turn(player: Player, enemy: Enemy) -> str:
    # Simple AI: 80% attack, 20% defend (reduces player next hit)
    if random.random() < 0.8:
        dmg = physical_damage(enemy.atk, player.defense)
        player.hp = max(0, player.hp - dmg)
        return f"{enemy.name} attacks! {player.name} takes {dmg} damage."
    else:
        # Temporary defend state could be added; here just flavor
        return f"{enemy.name} braces for impact."

def try_flee(enemy: Enemy) -> bool:
    if not enemy.fleeable:
        return False
    # Chance improves with level
    chance = 0.35 + 0.03  # modest baseline
    return random.random() < chance

def battle(player: Player, enemy: Enemy) -> bool:
    print(f"\nA {enemy.name} appears!")
    while player.is_alive() and enemy.hp > 0:
        print(f"\n{player.name} HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp}")
        print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
        print("Choose an action:")
        print("1) Attack  2) Spells  3) Items  4) Defend  5) Flee")

        choice = input("> ").strip()
        print()
        if choice == "1":
            dmg = physical_damage(player.atk, enemy.defense)
            enemy.hp = max(0, enemy.hp - dmg)
            print(f"{player.name} attacks! {enemy.name} takes {dmg} damage.")
        elif choice == "2":
            if not player.spells:
                print("You don't know any spells.")
            else:
                print("Spells:")
                for idx, sp in enumerate(player.spells, start=1):
                    print(f"{idx}) {sp.name} (MP {sp.mp_cost})")
                try:
                    sidx = int(input("> ").strip()) - 1
                    if 0 <= sidx < len(player.spells):
                        msg = use_spell(player, player.spells[sidx], enemy)
                        print(msg or "Nothing happens...")
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid selection.")
        elif choice == "3":
            if not player.inventory:
                print("You have no items.")
            else:
                print("Items:")
                for idx, it in enumerate(player.inventory, start=1):
                    print(f"{idx}) {it.name}")
                try:
                    iidx = int(input("> ").strip()) - 1
                    if 0 <= iidx < len(player.inventory):
                        msg = use_item(player, player.inventory[iidx].name)
                        print(msg)
                        # Escape item ends battle if it triggers
                        if "escape" in msg.lower():
                            return True
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid selection.")
        elif choice == "4":
            # Defend reduces next enemy attack
            print(f"{player.name} defends! Incoming damage will be reduced.")
            # Apply reduction for one enemy hit
            dmg_msg = enemy_turn(player, enemy)
            if "attacks" in dmg_msg:
                # halve damage effect retroactively by adding HP back
                # crude but effective for a simple loop
                parts = dmg_msg.split("takes ")
                try:
                    taken = int(parts[1].split(" ")[0])
                    reduced = max(1, taken // 2)
                    player.hp = min(player.max_hp, player.hp + (taken - reduced))
                    dmg_msg = dmg_msg.replace(f"takes {taken}", f"takes {reduced}")
                except Exception:
                    pass
            print(dmg_msg)
            continue  # skip enemy turn duplication
        elif choice == "5":
            if try_flee(enemy):
                print("You fled successfully!")
                return True
            else:
                print("Couldn't get away!")
        else:
            print("You hesitate...")

        # Enemy takes turn if alive
        if enemy.hp > 0:
            print(enemy_turn(player, enemy))

    if player.is_alive():
        print(f"\n{enemy.name} is defeated!")
        print(f"You gain {enemy.exp_reward} EXP and {enemy.gold_reward} gold.")
        player.gain_exp(enemy.exp_reward)
        player.gold += enemy.gold_reward
        return True
    else:
        print("\nYou have fallen...")
        return False

# =========================
# World & game loop
# =========================

@dataclass
class Area:
    name: str
    encounter_rate: float  # 0.0 in safe zones
    enemy_table: List[Enemy]
    description: str
    is_town: bool = False
    boss: Optional[Enemy] = None

def gen_enemy(slug: str) -> Enemy:
    if slug == "slime":
        return Enemy("Blue Slime", 18, 6, 2, 8, 5)
    if slug == "dracky":
        return Enemy("Dracky", 24, 8, 3, 14, 8)
    if slug == "skeleton":
        return Enemy("Skeleton", 32, 11, 5, 24, 12)
    if slug == "goblin_king":
        return Enemy("Goblin King", 60, 14, 7, 100, 50, fleeable=False)
    return Enemy("Mysterious Fog", 20, 6, 3, 5, 3)

def build_world() -> List[Area]:
    town = Area(
        name="Oakmere",
        encounter_rate=0.0,
        enemy_table=[],
        description="A quiet village. An inn, a shop, and rumors of a Goblin King in the hills.",
        is_town=True
    )
    field = Area(
        name="Greenfield",
        encounter_rate=0.25,
        enemy_table=[gen_enemy("slime"), gen_enemy("dracky")],
        description="Rolling fields swaying under a lazy sun."
    )
    forest = Area(
        name="Thornwood",
        encounter_rate=0.35,
        enemy_table=[gen_enemy("dracky"), gen_enemy("skeleton")],
        description="Dense and dim. The air hums with old magic."
    )
    cave = Area(
        name="Bramble Cave",
        encounter_rate=0.45,
        enemy_table=[gen_enemy("skeleton")],
        description="Echoes, dripping water, and the clatter of bones."
    )
    boss_lair = Area(
        name="King's Rise",
        encounter_rate=0.15,
        enemy_table=[gen_enemy("dracky"), gen_enemy("skeleton")],
        description="Wind-swept cliffs. A crude throne of stone awaits.",
        boss=gen_enemy("goblin_king")
    )
    return [town, field, forest, cave, boss_lair]

def town_menu(player: Player):
    while True:
        print(f"\n-- Oakmere --")
        print("1) Inn (10 gold)  2) Shop  3) Gossip  4) Leave town")
        choice = input("> ").strip()
        if choice == "1":
            if player.gold >= 10:
                player.gold -= 10
                player.hp = player.max_hp
                player.mp = player.max_mp
                print("You rest at the inn. HP/MP fully restored.")
            else:
                print("Not enough gold.")
        elif choice == "2":
            print("\nShop inventory:")
            shop_items = [
                ("Herb", 8, Item("Herb", "heal", 25)),
                ("Smoke Bomb", 12, Item("Smoke Bomb", "escape")),
            ]
            for i, (name, price, _) in enumerate(shop_items, start=1):
                print(f"{i}) {name} - {price} gold")
            print("Buy which? (number) or B to go back")
            sel = input("> ").strip().lower()
            if sel == "b":
                continue
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(shop_items):
                    name, price, obj = shop_items[idx]
                    if player.gold >= price:
                        player.gold -= price
                        player.inventory.append(obj)
                        print(f"Purchased {name}.")
                    else:
                        print("Not enough gold.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid selection.")
        elif choice == "3":
            print("Villager: 'They say the Goblin King fell from nobility to hunger. Now he hoards power like a child hoards sweets.'")
            print("Villager: 'If your fire is true and your heart steady, he cannot weather your blaze.'")
        elif choice == "4":
            print("You leave the town.")
            break
        else:
            print("You linger in the square...")

def travel(world: List[Area], current_idx: int) -> int:
    print("\nWhere will you go?")
    for i, area in enumerate(world):
        here = " (current)" if i == current_idx else ""
        print(f"{i+1}) {area.name}{here}")
    try:
        choice = int(input("> ").strip()) - 1
        if 0 <= choice < len(world):
            return choice
    except ValueError:
        pass
    print("You stay where you are.")
    return current_idx

def maybe_encounter(area: Area) -> Optional[Enemy]:
    if area.encounter_rate <= 0.0:
        return None
    if random.random() < area.encounter_rate:
        # choose a fresh enemy from table
        proto = random.choice(area.enemy_table)
        return Enemy(proto.name, proto.max_hp, proto.atk, proto.defense,
                     proto.exp_reward, proto.gold_reward, proto.fleeable)
    return None

def boss_sequence(player: Player, area: Area) -> bool:
    if not area.boss:
        return True
    print("\nA shadow looms. The Goblin King descends his stone throne, eyes burning with want.")
    boss = Enemy(area.boss.name, area.boss.max_hp, area.boss.atk, area.boss.defense,
                 area.boss.exp_reward, area.boss.gold_reward, area.boss.fleeable)
    win = battle(player, boss)
    if win and player.is_alive():
        print("\nWith a final roar, the Goblin King crumbles. The hills breathe easy again.")
        print("Villagers will sing your name, if you’ll let them.")
        return True
    return False

def print_status(player: Player):
    print(f"\n{player.name} — LV {player.level}")
    print(f"HP {player.hp}/{player.max_hp} | MP {player.mp}/{player.max_mp} | ATK {player.atk} | DEF {player.defense}")
    print(f"EXP {player.exp} | Gold {player.gold}")
    if player.inventory:
        inv = ", ".join([it.name for it in player.inventory])
        print(f"Items: {inv}")
    else:
        print("Items: (none)")

def main():
    print("Dragon Quest-like Text RPG")
    print("Name your hero:")
    pname = input("> ").strip() or "Hero"
    player = Player(name=pname)

    world = build_world()
    idx = 0  # Start in town

    print(f"\nWelcome, {player.name}. Oakmere is quiet, for now.")
    while True:
        area = world[idx]
        print_status(player)

        if area.is_town:
            town_menu(player)
        else:
            print(f"\n-- {area.name} --")
            print(area.description)
            # Random encounter
            enemy = maybe_encounter(area)
            if enemy:
                survived = battle(player, enemy)
                if not survived:
                    print("\nYour adventure ends here. Try again with a steadier heart.")
                    break

        # Boss check if in boss lair
        if world[idx].name == "King's Rise":
            progressed = boss_sequence(player, world[idx])
            if not progressed:
                print("\nThe peak remains under a grim rule.")
                break
            else:
                print("\nYou have won a quiet peace. Credits roll in your mind.")
                # Let player continue roaming or quit
                print("1) Return to Oakmere  2) Keep exploring  3) Quit")
                post = input("> ").strip()
                if post == "1":
                    idx = 0
                    continue
                elif post == "2":
                    pass
                else:
                    print("Thank you for playing.")
                    break

        # Travel prompt
        print("\nWhat next?")
        print("1) Travel  2) Use item  3) Rest (if town)  4) Quit")
        cmd = input("> ").strip()
        if cmd == "1":
            idx = travel(world, idx)
        elif cmd == "2":
            if not player.inventory:
                print("No items to use.")
            else:
                print("Your items:")
                for i, it in enumerate(player.inventory, start=1):
                    print(f"{i}) {it.name}")
                try:
                    use = int(input("> ").strip()) - 1
                    if 0 <= use < len(player.inventory):
                        print(use_item(player, player.inventory[use].name))
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid selection.")
        elif cmd == "3":
            if world[idx].is_town:
                print("You take a short rest by the fountain. It helps a little.")
                heal = random.randint(4, 8)
                player.hp = min(player.max_hp, player.hp + heal)
                print(f"Recovered {heal} HP.")
            else:
                print("Not a safe place to rest.")
        elif cmd == "4":
            print("Farewell, traveler.")
            break
        else:
            print("You watch the clouds for a moment...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame closed.")
        sys.exit(0)