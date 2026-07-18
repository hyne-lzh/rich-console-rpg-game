from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn
from time import sleep
import keyboard
import random
import json
import os

console = Console()
SAVE_FILE = "game_save.json"

# ========== Expanded Monster Data (6 Types, Tiered Difficulty) ==========
MONSTERS = {
    "Slime": {
        "attack": 8,
        "hp": 40,
        "max_hp": 40,
        "defend": 2,
        "gold": 3,
        "name_color": "light_green",
        "crit_rate": 0.03
    },
    "Small Monster": {
        "attack": 10,
        "hp": 50,
        "max_hp": 50,
        "defend": 3,
        "gold": 5,
        "name_color": "green",
        "crit_rate": 0.05
    },
    "Wild Wolf": {
        "attack": 18,
        "hp": 120,
        "max_hp": 120,
        "defend": 6,
        "gold": 12,
        "name_color": "orange",
        "crit_rate": 0.08
    },
    "Big Monster": {
        "attack": 20,
        "hp": 200,
        "max_hp": 200,
        "defend": 10,
        "gold": 20,
        "name_color": "yellow",
        "crit_rate": 0.1
    },
    "Giant Bear Boss": {
        "attack": 28,
        "hp": 320,
        "max_hp": 320,
        "defend": 18,
        "gold": 30,
        "name_color": "dark_orange",
        "crit_rate": 0.12
    },
    "Ancient Dragon": {
        "attack": 38,
        "hp": 500,
        "max_hp": 500,
        "defend": 30,
        "gold": 60,
        "name_color": "red",
        "crit_rate": 0.18
    }
}

# ========== Expanded Character Level Progression (5 Tiers) ==========
CHARACTERS = {
    "Novice": {
        "attack": 10,
        "hp": 200,
        "max_hp": 200,
        "defend": 5,
        "crit_dmg": 1.5,
        "dodge_rate": 0.05,
        "upgrade": 0
    },
    "Lvl 1 Warrior": {
        "attack": 20,
        "hp": 250,
        "max_hp": 250,
        "defend": 20,
        "crit_dmg": 1.6,
        "dodge_rate": 0.08,
        "upgrade": 200,
    },
    "Lvl 2 Veteran": {
        "attack": 50,
        "hp": 300,
        "max_hp": 300,
        "defend": 40,
        "crit_dmg": 1.8,
        "dodge_rate": 0.12,
        "upgrade": 500,
    },
    "Lvl 3 Knight": {
        "attack": 70,
        "hp": 380,
        "max_hp": 380,
        "defend": 60,
        "crit_dmg": 2.0,
        "dodge_rate": 0.18,
        "upgrade": 999,
    },
    "Legendary Warlord": {
        "attack": 120,
        "hp": 500,
        "max_hp": 500,
        "defend": 90,
        "crit_dmg": 2.5,
        "dodge_rate": 0.25,
        "upgrade": 2000,
    },
}

# ========== Expanded Equipment Shop Data ==========
EQUIPMENT = {
    "No Equipment": {"atk": 0, "def": 0, "price": 0},
    "Iron Sword": {"atk": 15, "def": 0, "price": 120},
    "Leather Armor": {"atk": 0, "def": 10, "price": 100},
    "Fine Steel Longsword": {"atk": 30, "def": 5, "price": 350},
    "Knight Heavy Plate": {"atk": 8, "def": 35, "price": 400},
    "Golden Armor Set": {"atk": 40, "def": 25, "price": 600},
    "Dragon God Armor": {"atk": 80, "def": 60, "price": 1500}
}

# ========== Achievement System ==========
ACHIEVEMENTS = {
    "First Hunt": {"need": 1, "reward": 20, "done": False},
    "Century Slayer": {"need": 100, "reward": 300, "done": False},
    "Dragon Slayer": {"need": 50, "reward": 800, "done": False},
    "Max Level Warlord": {"need": "Legendary Warlord", "reward": 1200, "done": False}
}

# ========== Global Game Save Data Initialization ==========
def init_game_data():
    return {
        "player_lv": "Novice",
        "player": CHARACTERS["Novice"].copy(),
        "monster_name": "Slime",
        "monster": MONSTERS["Slime"].copy(),
        "gold": 0,
        "potion": 5,
        "kill_count": 0,
        "equip": "No Equipment",
        "in_battle": False,
        "buff_rage": 0,
        "buff_shield": 0,
        "achievements": ACHIEVEMENTS.copy()
    }

game_data = init_game_data()

# ========== Save & Load System ==========
def save_game():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(game_data, f, ensure_ascii=False, indent=2)
    console.print("[green]✅ Game saved successfully![/]")

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key in game_data:
            if key in data:
                game_data[key] = data[key]
        console.print("[green]✅ Save file loaded[/]")
    else:
        console.print("[yellow]No save file found, starting new game[/]")

# ========== Stat Calculation Functions ==========
def get_player_all_atk():
    base_atk = game_data["player"]["attack"]
    equip_atk = EQUIPMENT[game_data["equip"]]["atk"]
    if game_data["buff_rage"] > 0:
        return int((base_atk + equip_atk) * 1.5)
    return base_atk + equip_atk

def get_player_all_def():
    base_def = game_data["player"]["defend"]
    equip_def = EQUIPMENT[game_data["equip"]]["def"]
    if game_data["buff_shield"] > 0:
        return int((base_def + equip_def) * 2)
    return base_def + equip_def

# ========== Game UI Rendering ==========
def render_game_ui():
    table = Table(title="🎮 Hardcore Console RPG Game", show_lines=True)
    table.add_column("Player Info", style="cyan", width=38)
    table.add_column("Enemy Monster", style="magenta", width=38)

    player = game_data["player"]
    player_text = Text()
    player_text.append(f"Level: {game_data['player_lv']}\n", style="bold cyan")
    player_text.append(f"HP: {player['hp']}/{player['max_hp']}\n", style="green")
    player_text.append(f"Total Attack: {get_player_all_atk()}\n", style="orange1")
    player_text.append(f"Total Defense: {get_player_all_def()}\n", style="blue")
    player_text.append(f"Gold: {game_data['gold']}\n", style="gold1")
    player_text.append(f"Potions: {game_data['potion']}\n", style="hot_pink")
    player_text.append(f"Equipped: {game_data['equip']}\n", style="white")
    player_text.append(f"Total Kills: {game_data['kill_count']}\n", style="gray")
    player_text.append(f"Rage Buff: {game_data['buff_rage']} turns | Shield Buff: {game_data['buff_shield']} turns", style="red")

    monster_name = game_data["monster_name"]
    monster = game_data["monster"]
    monster_text = Text()
    monster_text.append(f"Monster: {monster_name}\n", style=f"bold {monster['name_color']}")
    monster_text.append(f"HP: {monster['hp']}/{monster['max_hp']}\n", style="green")
    monster_text.append(f"Attack: {monster['attack']}\n", style="orange1")
    monster_text.append(f"Defense: {monster['defend']}\n", style="blue")
    monster_text.append(f"Gold Reward: {monster['gold']}", style="gold1")
    table.add_row(player_text, monster_text)
    return table

def show_hp_bar(current_hp, max_hp, bar_color):
    with Progress(
        TextColumn(""),
        BarColumn(complete_style=bar_color),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("HP", total=max_hp)
        progress.update(task, completed=current_hp)

# ========== Combat Logic ==========
def monster_attack():
    player = game_data["player"]
    monster = game_data["monster"]
    dodge_chance = player["dodge_rate"]
    if random.random() < dodge_chance:
        console.print(Panel("✨ Dodge Successful!", style="bright_green"))
        return
    damage = max(monster["attack"] - get_player_all_def(), 1)
    if random.random() < monster["crit_rate"]:
        damage = int(damage * 1.8)
        console.print(Panel(f"💥 Monster Critical Hit! -{damage}", style="red"))
    else:
        console.print(Panel(f"👹 Monster Attacks -{damage}", style="magenta"))
    player["hp"] -= damage
    show_hp_bar(player["hp"], player["max_hp"], "green")
    if player["hp"] <= 0:
        console.print(Panel("💥 You have perished, game over", style="bold red"))
        exit()

def player_normal_hit():
    monster = game_data["monster"]
    attack_power = get_player_all_atk()
    damage = max(attack_power - monster["defend"], 1)
    crit_multiplier = game_data["player"]["crit_dmg"]
    if random.random() < 0.12:
        damage = int(damage * crit_multiplier)
        console.print(Panel(f"🔥 Critical Hit! {damage} Damage", style="yellow"))
    else:
        console.print(Panel(f"⚔ Basic Attack {damage} Damage", style="cyan"))
    monster["hp"] -= damage
    show_hp_bar(monster["hp"], monster["max_hp"], "red")
    check_monster_dead()

def player_rage_skill():
    if game_data["potion"] < 1:
        console.print("[red]Not enough potions![/]")
        return
    game_data["potion"] -= 1
    game_data["buff_rage"] = 3
    console.print(Panel("🩸 Rage activated, +50% attack for 3 turns", style="dark_orange"))
    player_normal_hit()

def player_shield_skill():
    if game_data["potion"] < 1:
        console.print("[red]Not enough potions![/]")
        return
    game_data["potion"] -= 1
    game_data["buff_shield"] = 3
    console.print(Panel("🛡 Shield activated, double defense for 3 turns", style="blue"))

def player_heal_skill():
    if game_data["potion"] < 1:
        console.print("[red]Not enough potions![/]")
        return
    game_data["potion"] -= 1
    player = game_data["player"]
    heal_amount = 120
    player["hp"] = min(player["hp"] + heal_amount, player["max_hp"])
    console.print(Panel(f"💚 Heal +{heal_amount} HP", style="hot_pink"))
    show_hp_bar(player["hp"], player["max_hp"], "green")

def check_monster_dead():
    monster = game_data["monster"]
    if monster["hp"] <= 0:
        gold_reward = monster["gold"]
        game_data["gold"] += gold_reward
        game_data["kill_count"] += 1

        console.print(Panel(f"✅ Enemy Slain! Earned {gold_reward} Gold", style="green"))
        # Random extra gold drop
        extra_gold = random.randint(5, 30) if random.random() < 0.35 else 0
        if extra_gold > 0:
            game_data["gold"] += extra_gold
            console.print(f"💰 Extra Loot: {extra_gold} Gold")
        monster["hp"] = monster["max_hp"]
        game_data["in_battle"] = False
        check_achievement()
        return True
    return False

# Check Unlockable Achievements
def check_achievement():
    total_kills = game_data["kill_count"]
    current_level = game_data["player_lv"]
    achievements = game_data["achievements"]
    if not achievements["First Hunt"]["done"] and total_kills >= 1:
        achievements["First Hunt"]["done"] = True
        game_data["gold"] += achievements["First Hunt"]["reward"]
        console.print("[bold gold]🏆 Achievement Unlocked: First Hunt, Reward +20 Gold[/]")
    if not achievements["Century Slayer"]["done"] and total_kills >= 100:
        achievements["Century Slayer"]["done"] = True
        game_data["gold"] += achievements["Century Slayer"]["reward"]
        console.print("[bold gold]🏆 Achievement Unlocked: Century Slayer, Reward +300 Gold[/]")
    if not achievements["Dragon Slayer"]["done"] and total_kills >= 50:
        achievements["Dragon Slayer"]["done"] = True
        game_data["gold"] += achievements["Dragon Slayer"]["reward"]
        console.print("[bold gold]🏆 Achievement Unlocked: Dragon Slayer, Reward +800 Gold[/]")
    if not achievements["Max Level Warlord"]["done"] and current_level == "Legendary Warlord":
        achievements["Max Level Warlord"]["done"] = True
        game_data["gold"] += achievements["Max Level Warlord"]["reward"]
        console.print("[bold gold]🏆 Achievement Unlocked: Max Level Warlord, Reward +1200 Gold[/]")

# Real-time Battle Input Loop
def battle_loop():
    game_data["in_battle"] = True
    console.clear()
    console.print(render_game_ui())
    hint_panel = Panel("""
【Battle Hotkeys】
A = Basic Attack | W = Rage Skill | S = Shield Skill | D = Heal | ESC = Flee
""", style="bold yellow")
    console.print(hint_panel)
    console.print("[green]Battle started, use keyboard to act directly[/]")
    while game_data["in_battle"]:
        # Decrement buff turn counters
        if game_data["buff_rage"] > 0:
            game_data["buff_rage"] -= 1
        if game_data["buff_shield"] > 0:
            game_data["buff_shield"] -= 1
        # Keyboard Input Detection
        if keyboard.is_pressed("a"):
            player_normal_hit()
            if game_data["in_battle"]:
                sleep(0.3)
                monster_attack()
            sleep(0.4)
        elif keyboard.is_pressed("w"):
            player_rage_skill()
            sleep(0.4)
        elif keyboard.is_pressed("s"):
            player_shield_skill()
            sleep(0.4)
        elif keyboard.is_pressed("d"):
            player_heal_skill()
            sleep(0.4)
        elif keyboard.is_pressed("esc"):
            game_data["in_battle"] = False
            console.print("[yellow]Successfully fled from battle[/]")
            sleep(0.5)
        sleep(0.05)

# Character Level Up System
def level_up():
    level_chain = [
        ("Novice", "Lvl 1 Warrior"),
        ("Lvl 1 Warrior", "Lvl 2 Veteran"),
        ("Lvl 2 Veteran", "Lvl 3 Knight"),
        ("Lvl 3 Knight", "Legendary Warlord")
    ]
    current_lv = game_data["player_lv"]
    target_lv = None
    for old_lv, new_lv in level_chain:
        if old_lv == current_lv:
            target_lv = new_lv
            break
    if not target_lv:
        console.print("[green]Max Level Reached: Legendary Warlord[/]")
        return
    upgrade_cost = CHARACTERS[target_lv]["upgrade"]
    if game_data["gold"] >= upgrade_cost:
        game_data["gold"] -= upgrade_cost
        game_data["player_lv"] = target_lv
        game_data["player"] = CHARACTERS[target_lv].copy()
        console.print(Panel(f"🎉 Level Up to {target_lv}", style="green"))
        check_achievement()
    else:
        console.print(f"[red]Insufficient Gold, Upgrade requires {upgrade_cost} Gold[/]")

# Switch Target Monster
def change_monster():
    console.print("[yellow]Monster List: " + ", ".join(MONSTERS.keys()) + "[/]")
    selection = Prompt.ask("Input monster name to switch")
    if selection in MONSTERS:
        game_data["monster_name"] = selection
        game_data["monster"] = MONSTERS[selection].copy()
        console.print(f"[green]Target switched to: {selection}[/]")
    else:
        console.print("[red]This monster does not exist[/]")

# Shop Systems
def potion_shop():
    console.print(Panel("🏪 Potion Shop | 15 Gold per Potion", style="gold1"))
    buy_count = Prompt.ask("Purchase quantity (0 to close shop)", default="0")
    try:
        count = int(buy_count)
    except ValueError:
        console.print("[red]Please enter a valid number[/]")
        return
    if count <= 0:
        return
    total_cost = count * 15
    if game_data["gold"] >= total_cost:
        game_data["gold"] -= total_cost
        game_data["potion"] += count
        console.print("[green]Purchase Complete[/]")
    else:
        console.print("[red]Insufficient Gold[/]")

def equipment_shop():
    console.print(Panel("🛡 Equipment Shop", style="gold1"))
    for equip_name, stats in EQUIPMENT.items():
        if equip_name != "No Equipment":
            console.print(f"{equip_name} | ATK +{stats['atk']} DEF +{stats['def']} | {stats['price']} Gold")
    selection = Prompt.ask("Input equipment name to buy, input 'No Equipment' to exit", default="No Equipment")
    if selection == "No Equipment":
        return
    if selection not in EQUIPMENT:
        console.print("[red]This equipment does not exist[/]")
        return
    equip_cost = EQUIPMENT[selection]["price"]
    if game_data["gold"] >= equip_cost:
        game_data["gold"] -= equip_cost
        game_data["equip"] = selection
        console.print(f"[green]Equipped {selection} Successfully[/]")
    else:
        console.print("[red]Insufficient Gold[/]")

# View All Achievements UI
def show_achievement_list():
    table = Table(title="🏆 Achievement List", show_lines=True)
    table.add_column("Achievement Name")
    table.add_column("Unlock Condition")
    table.add_column("Gold Reward")
    table.add_column("Status")
    for ach_name, ach_data in game_data["achievements"].items():
        condition_text = str(ach_data["need"])
        unlock_status = "[green]Completed[/]" if ach_data["done"] else "[red]Locked[/]"
        table.add_row(ach_name, condition_text, str(ach_data["reward"]), unlock_status)
    console.print(table)

# Main Game Menu Loop
def main_loop():
    load_game()
    while True:
        console.clear()
        console.print(render_game_ui())
        menu_panel = Panel("""
[1] Real-time Keyboard Combat
[2] Switch Target Monster
[3] Character Level Up & Progression
[4] Potion Shop
[5] Equipment Shop
[6] View Achievement List
[7] Manual Save Game
[0] Exit Game
""", title="Main Function Menu", style="blue")
        console.print(menu_panel)
        option = Prompt.ask("Input menu number")
        if option == "1":
            battle_loop()
        elif option == "2":
            change_monster()
        elif option == "3":
            level_up()
        elif option == "4":
            potion_shop()
        elif option == "5":
            equipment_shop()
        elif option == "6":
            show_achievement_list()
        elif option == "7":
            save_game()
        elif option == "0":
            save_game()
            console.print("[green]Progress auto-saved, exiting game[/]")
            break
        else:
            console.print("[red]Invalid input number[/]")
        Prompt.ask("\nPress Enter to return to main menu")

if __name__ == "__main__":
    main_loop()
