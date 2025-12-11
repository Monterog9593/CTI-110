import random

# -----------------------------
# Player Class
# -----------------------------
class Player:
    def __init__(self, name, strength=5, defense=3):
        self.name = name
        self.icon = "🧝"
        self.max_health = 30
        self.health = self.max_health
        self.strength = strength
        self.defense = defense
        self.gold = 0
        self.exp = 0
        self.level = 1
        self.exp_to_next = 20

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
        self.max_health += 5
        self.strength += 2
        self.defense += 1
        self.health = self.max_health
        print(f"🎉 {self.name} leveled up to Level {self.level}!")
        print(f"Stats: HP={self.max_health}, STR={self.strength}, DEF={self.defense}")

# -----------------------------
# Enemy Class
# -----------------------------
class Enemy:
    def __init__(self, name, icon, health, strength, defense, exp_reward, gold_reward):
        self.name = name
        self.icon = icon
        self.max_health = health
        self.health = health
        self.strength = strength
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward

    def is_alive(self):
        return self.health > 0

# -----------------------------
# Encounter Function
# -----------------------------
def encounter(area_name):
    if area_name == "Fields":
        return [Enemy("Slime", "🫧", 20, 4, 2, 8, 6)]
    if area_name == "Forest":
        return [Enemy("Goblin", "👹", 30, 6, 3, 12, 10)]
    if area_name == "Cave":
        return [Enemy("Skeleton", "💀", 40, 7, 4, 18, 14)]
    return []

# -----------------------------
# Combat Function
# -----------------------------
def combat(player, enemies):
    print(f"\n⚔️ Battle start!")
    for e in enemies:
        print(f" - {e.icon} {e.name} (HP {e.health}/{e.max_health})")

    while player.is_alive() and any(e.is_alive() for e in enemies):
        # Player attacks first living enemy
        target = next((e for e in enemies if e.is_alive()), None)
        if target:
            dmg = max(1, player.strength - target.defense)
            target.health = max(0, target.health - dmg)
            print(f"{player.name} attacks! {target.name} takes {dmg} damage.")

        # Enemies attack
        for e in enemies:
            if e.is_alive():
                dmg = max(1, e.strength - player.defense)
                player.health = max(0, player.health - dmg)
                print(f"{e.name} attacks! {player.name} takes {dmg} damage.")

    # Victory / Defeat
    if player.is_alive():
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

# -----------------------------
# Main Game Loop
# -----------------------------
def main():
    print("Welcome to Dragon Quest–style Text RPG!")
    player = Player("Gabriel")
    print(f"\n✨ Your Journey Begins ✨\n{player.name} the adventurer (Level {player.level})")

    # Test battle in Fields
    enemies = encounter("Fields")
    combat(player, enemies)

    print(f"\nFinal Stats: Level {player.level}, EXP {player.exp}/{player.exp_to_next}, Gold {player.gold}")

if __name__ == "__main__":
    main()