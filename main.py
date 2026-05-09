import math
import random

# Classe de base représentant un bloc du monde (pierre, fer, etc.)
class Block:
    def __init__(self, name, durability, can_drop_item=True, xp=0, hardness=1.0, forbidden_tools=None):
        self.name = name
        self.durability = durability
        self.max_durability = durability
        self.state = "Intact"
        self.can_drop_item = can_drop_item
        self.xp = xp
        self.hardness = hardness
        self.forbidden_tools = forbidden_tools or []

    def take_damage(self, amount):
        if self.is_broken():
            return 0
        real_damage = max(1, int(amount / self.hardness))
        self.durability -= real_damage
        if self.durability <= 0:
            self.durability = 0
            self.state = "Broken"
        else:
            self.state = "Damaged"
        return real_damage

    def is_broken(self):
        return self.state == "Broken"

    def drop_item(self, tool):
        if not self.is_broken():
            return "Item not ready"
        if not self.can_drop_item:
            return "No item dropped"
        if tool.name in self.forbidden_tools:
            return "No item dropped"
        if tool.enchantment.get("SilkTouch"):
            return "Item collected (Silk Touch)"
        fortune = tool.enchantment.get("Fortune", 0)
        if fortune > 0:
            return f"Item collected x{fortune + 1} (Fortune)"
        return "Item collected"


# Bloc fragile qui se casse instantanément (ex: verre)
class FragileBlock(Block):
    def __init__(self, name):
        super().__init__(name, 1, can_drop_item=False, hardness=0.1)

    def take_damage(self, amount):
        self.durability = 0
        self.state = "Broken"
        return amount


# Bloc de pierre classique
class StoneBlock(Block):
    def __init__(self):
        super().__init__("Stone", 50, xp=5)


# Bloc de fer
class IronBlock(Block):
    def __init__(self):
        super().__init__("Iron", 100, xp=10)


# Bloc très résistant nécessitant un bon outil
class ObsidianBlock(Block):
    def __init__(self):
        super().__init__(
            "Obsidian", 200, xp=25,
            forbidden_tools=["Hand", "WoodPickaxe", "StonePickaxe", "IronPickaxe"]
        )


# Bloc de verre (fragile)
class GlassBlock(FragileBlock):
    def __init__(self):
        super().__init__("GlassBlock")



# Bloc de charbon 
class CoalBlock(Block):
    def __init__(self):
        super().__init__("Coal", 30, xp=8)



# Classe de base pour tous les outils
class Tool:
    def __init__(self, name, power, allowed_blocks=None, enchantment=None, durability=100):
        self.name = name
        self.power = power
        self.allowed_blocks = allowed_blocks or []
        self.enchantment = enchantment or {}
        self.durability = durability

    def calculate_damage(self, block):
        base_damage = 0
        if block.name in self.allowed_blocks:
            base_damage = self.power
        elif isinstance(block, FragileBlock):
            base_damage = block.durability * 20
        efficiency = self.enchantment.get("Efficiency", 1)
        return int(base_damage * efficiency)
        
    def use(self):
        return self.durability > 0

# Main du joueur (outil de base, durabilité infinie)
class Hand(Tool):
    def __init__(self):
        super().__init__("Hand", 2)
        self.durability = math.inf
        self.enchantment = {}

# Pioche en bois
class WoodPickaxe(Tool):
    def __init__(self):
        super().__init__("WoodPickaxe", 5, ["Stone"])

# Pioche en pierre
class StonePickaxe(Tool):
    def __init__(self):
        super().__init__("StonePickaxe", 8, ["Stone", "Iron"])

# Pioche en fer
class IronPickaxe(Tool):
    def __init__(self):
        super().__init__("IronPickaxe", 12, ["Stone", "Iron"])

# Pioche en diamant
class DiamondPickaxe(Tool):
    def __init__(self):
        super().__init__("DiamondPickaxe", 25,
                         ["Stone", "Iron", "Obsidian", "GlassBlock", "Coal"])



# Case de l'inventaire contenant un item et sa quantité
class InventorySlot:
    def __init__(self, item, quantity=1):
        self.item = item
        self.quantity = quantity

# Objet stockable dans l'inventaire
class Item:
    def __init__(self, name, max_stack=64, effect=None):
        self.name = name
        self.max_stack = max_stack
        self.effect = effect

# Inventaire du joueur
class Inventory:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.slots = []

    def add_item(self, item, quantity=1):
        for slot in self.slots:
            if slot.item.name == item.name and slot.quantity < item.max_stack:
                available = item.max_stack - slot.quantity
                to_add = min(available, quantity)
                slot.quantity += to_add
                quantity -= to_add
                if quantity == 0:
                    return
        while quantity > 0 and len(self.slots) < self.capacity:
            to_add = min(item.max_stack, quantity)
            self.slots.append(InventorySlot(item, to_add))
            quantity -= to_add
        if quantity > 0:
            print(f"Inventory full, could not add {quantity} {item.name}(s)")

    def show_inventory(self):
        print("\nInventory:")
        for slot in self.slots:
            print(f"- {slot.item.name} x{slot.quantity}")
        if not self.slots:
            print("Empty")



# Effet temporaire appliqué au joueur
class StatusEffect:
    def __init__(self, name, duration, effect_function=None):
        self.name = name
        self.duration = duration
        self.effect_function = effect_function

    def apply(self, player):
        if self.effect_function:
            self.effect_function(player)
        self.duration -= 1


def haste_effect(player):
    player.mining_speed = 2
    print(f"{player.name} is under Haste! Mining speed doubled.")


def mining_fatigue_effect(player):
    player.mining_speed = 0.5
    print(f"{player.name} is under Mining Fatigue! Mining speed halved.")



# Joueur principal
class Player:
    def __init__(self, name="Steve"):
        self.name = name
        self.level = 1
        self.xp = 0
        self.inventory = Inventory()
        self.status_effects = []
        self.mining_speed = 1

    def xp_required(self):
        return self.level * 20

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_required():
            self.xp -= self.xp_required()
            self.level += 1

    def add_status(self, status):
        self.status_effects.append(status)
        print(f"{self.name} gained {status.name} for {status.duration} turns.")

    def update_statuses(self):
        self.mining_speed = 1
        for status in self.status_effects[:]:
            status.apply(self)
            if status.duration <= 0:
                print(f"{status.name} wore off.")
                self.status_effects.remove(status)

    def mine_block(self, block, tool):
        self.update_statuses()
    
        if tool.durability <= 0:
            print(f"{tool.name} is broken!")
            tool = Hand()
            print(f"{self.name} now uses {tool.name} (infinite durability)")
    
        damage = tool.calculate_damage(block) * self.mining_speed
        applied = block.take_damage(damage)
    
        xp_gained = block.xp if block.is_broken() else 0
        if xp_gained:
            self.add_xp(xp_gained)
    
        item_status = block.drop_item(tool)
    
        print("\n[ MINING RESULT ]")
        print(f"Player        : {self.name}")
        print(f"Block         : {block.name}")
        print(f"Damage dealt  : {applied}")
        print(f"Block state   : {block.state}")
        print(f"Drop status   : {item_status}")
        print(f"XP gained     : {xp_gained}")
        print(f"Mining speed  : {self.mining_speed}")
    
       
        if not isinstance(tool, Hand) and applied > 0:
            unbreaking = tool.enchantment.get("Unbreaking", 0)
            chance_to_preserve = unbreaking / (unbreaking + 1) if unbreaking > 0 else 0
            if random.random() > chance_to_preserve:
                tool.durability -= 1
            if tool.durability <= 0:
                print(f"{tool.name} broke and is removed from inventory!")
                self.inventory.slots = [
                    slot for slot in self.inventory.slots
                    if not (slot.item.name == tool.name)
                ]
                tool = Hand()
                print(f"{self.name} now uses {tool.name} (infinite durability)")


# ------ PLAYER -------
player = Player()

# Ajout initial dans l'inventaire
player.inventory.add_item(Item("Apple"), 70)
player.inventory.add_item(Item("Iron Pickaxe"), 1)
player.inventory.show_inventory()

# Application des effets temporaires
haste = StatusEffect("Haste", 2, haste_effect)
fatigue = StatusEffect("Mining Fatigue", 1, mining_fatigue_effect)
player.add_status(haste)
player.add_status(fatigue)

# Création des blocs à miner
stone = StoneBlock()
iron = IronBlock()
obsidian = ObsidianBlock()
glass = GlassBlock()
coal = CoalBlock()

# Création des pioche enchantées
diamond_eff = DiamondPickaxe()
diamond_eff.enchantment = {"Efficiency": 2}

diamond_fortune = DiamondPickaxe()
diamond_fortune.enchantment = {"Fortune": 3}

diamond_unbreaking = DiamondPickaxe()
diamond_unbreaking.enchantment = {"Unbreaking": 2}

# Création des items correspondants pour l'inventaire
stone_item = Item("Stone")
iron_item = Item("Iron")
coal_item = Item("Coal")

# Fonction pour miner un bloc jusqu'à ce qu'il se casse
def mine_until_broken(player, block, tool, item):
    while not block.is_broken():
        player.mine_block(block, tool)
    # Ajout de l'item à l'inventaire si drop réussi
    drop_status = block.drop_item(tool)
    if "collected" in drop_status:
        if "x" in drop_status:
            quantity = int(drop_status.split("x")[1].split()[0])
        else:
            quantity = 1
        player.inventory.add_item(item, quantity)


print("\n--- Mining Demo ---")

# Miner Stone, Iron, Obsidian, Glass et Coal
mine_until_broken(player, stone, diamond_eff, stone_item)
mine_until_broken(player, iron, diamond_fortune, iron_item)
mine_until_broken(player, obsidian, diamond_unbreaking, Item("Obsidian"))
mine_until_broken(player, glass, diamond_unbreaking, Item("GlassBlock"))
mine_until_broken(player, coal, diamond_fortune, coal_item)

# Affichage final de l'inventaire
player.inventory.show_inventory()
