#  Minecraft Mining Simulation 

##  Author
**Name:** Meryem Khiari

---

##  Project Description

This project is a **Minecraft-inspired mining simulation system** developed in Python using **Object-Oriented Programming (OOP)** SIMPLE principles.

It simulates the interaction between a player, tools, and blocks in a dynamic environment where mining actions depend on tool efficiency, block resistance, enchantments, and player status effects.

The system demonstrates advanced OOP concepts such as inheritance, polymorphism, encapsulation, and state management.

---

##  Features

###  Block System
- Multiple block types with unique properties:
  - Stone
  - Iron
  - Coal
  - Obsidian
  - Glass (fragile)
- Each block has:
  - Durability
  - XP reward
  - Drop rules
  - Hardness factor

---

###  Tool System
- Different mining tools:
  - Hand (basic tool)
  - Wooden Pickaxe
  - Stone Pickaxe
  - Iron Pickaxe
  - Diamond Pickaxe
- Tools include:
  - Power
  - Durability
  - Allowed block types
  - Enchantments:
    - Efficiency
    - Fortune
    - Unbreaking
    - Silk Touch

---

###  Inventory System
- Slot-based inventory
- Item stacking system
- Capacity management
- Automatic item merging

---

###  Player System
- Experience points (XP)
- Level progression system
- Tool usage
- Inventory management
- Status effects handling

---

###  Status Effects
- Temporary effects applied to the player:
  - **Haste** → increases mining speed
  - **Mining Fatigue** → decreases mining speed

---

##  How It Works

1. The player selects a tool  
2. The player mines a block  
3. The system calculates:
   - Tool efficiency
   - Block resistance
   - Enchantments
   - Status effects
4. Block durability decreases  
5. If the block is destroyed:
   - Items are dropped
   - XP is awarded
6. The inventory is updated automatically  

---

##  Technologies Used

- Python 3
- Object-Oriented Programming (OOP)
- Random module
- Math module

---

## Project Structure


minecraft-mining-simulator/
├── .venv/
├── main.py
└── requirements.txt


---

## Notes

- `.venv` is excluded from GitHub (virtual environment)
- No external libraries required
- Fully built with Python standard library


