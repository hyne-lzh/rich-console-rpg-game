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

# ========== 扩充怪物（6种，分层难度）==========
MONSTERS = {
    "史莱姆": {
        "attack": 8,
        "hp": 40,
        "max_hp": 40,
        "defend": 2,
        "gold": 3,
        "name_color": "light_green",
        "crit_rate": 0.03
    },
    "小怪": {
        "attack": 10,
        "hp": 50,
        "max_hp": 50,
        "defend": 3,
        "gold": 5,
        "name_color": "green",
        "crit_rate": 0.05
    },
    "野狼": {
        "attack": 18,
        "hp": 120,
        "max_hp": 120,
        "defend": 6,
        "gold": 12,
        "name_color": "orange",
        "crit_rate": 0.08
    },
    "大怪": {
        "attack": 20,
        "hp": 200,
        "max_hp": 200,
        "defend": 10,
        "gold": 20,
        "name_color": "yellow",
        "crit_rate": 0.1
    },
    "巨熊BOSS": {
        "attack": 28,
        "hp": 320,
        "max_hp": 320,
        "defend": 18,
        "gold": 30,
        "name_color": "dark_orange",
        "crit_rate": 0.12
    },
    "远古魔龙": {
        "attack": 38,
        "hp": 500,
        "max_hp": 500,
        "defend": 30,
        "gold": 60,
        "name_color": "red",
        "crit_rate": 0.18
    }
}

# ========== 扩充角色等级（5级养成线）==========
CHARACTERS = {
    "新手": {
        "attack": 10,
        "hp": 200,
        "max_hp": 200,
        "defend": 5,
        "crit_dmg": 1.5,
        "dodge_rate": 0.05,
        "upgrade": 0
    },
    "1级战士": {
        "attack": 20,
        "hp": 250,
        "max_hp": 250,
        "defend": 20,
        "crit_dmg": 1.6,
        "dodge_rate": 0.08,
        "upgrade": 200,
    },
    "2级勇士": {
        "attack": 50,
        "hp": 300,
        "max_hp": 300,
        "defend": 40,
        "crit_dmg": 1.8,
        "dodge_rate": 0.12,
        "upgrade": 500,
    },
    "3级骑士": {
        "attack": 70,
        "hp": 380,
        "max_hp": 380,
        "defend": 60,
        "crit_dmg": 2.0,
        "dodge_rate": 0.18,
        "upgrade": 999,
    },
    "传说战神": {
        "attack": 120,
        "hp": 500,
        "max_hp": 500,
        "defend": 90,
        "crit_dmg": 2.5,
        "dodge_rate": 0.25,
        "upgrade": 2000,
    },
}

# ========== 装备商店扩充 ==========
EQUIPMENT = {
    "无装备": {"atk": 0, "def": 0, "price": 0},
    "铁剑": {"atk": 15, "def": 0, "price": 120},
    "皮甲": {"atk": 0, "def": 10, "price": 100},
    "精钢长剑": {"atk": 30, "def": 5, "price": 350},
    "骑士重甲": {"atk": 8, "def": 35, "price": 400},
    "黄金套装": {"atk": 40, "def": 25, "price": 600},
    "魔龙神装": {"atk": 80, "def": 60, "price": 1500}
}

# ========== 成就系统 ==========
ACHIEVEMENTS = {
    "初次狩猎": {"need": 1, "reward": 20, "done": False},
    "百人斩": {"need": 100, "reward": 300, "done": False},
    "屠龙勇士": {"need": 50, "reward": 800, "done": False},
    "满级战神": {"need": "传说战神", "reward": 1200, "done": False}
}

# ========== 全局游戏存档数据 ==========
def init_game_data():
    return {
        "player_lv": "新手",
        "player": CHARACTERS["新手"].copy(),
        "monster_name": "史莱姆",
        "monster": MONSTERS["史莱姆"].copy(),
        "gold": 0,
        "potion": 5,
        "kill_count": 0,
        "equip": "无装备",
        "in_battle": False,
        "buff_rage": 0,
        "buff_shield": 0,
        "achievements": ACHIEVEMENTS.copy()
    }

game_data = init_game_data()

# ========== 存档/读档功能 ==========
def save_game():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(game_data, f, ensure_ascii=False, indent=2)
    console.print("[green]✅ 存档成功！[/]")

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k in game_data:
            if k in data:
                game_data[k] = data[k]
        console.print("[green]✅ 读取存档完成[/]")
    else:
        console.print("[yellow]无存档文件，开启新游戏[/]")

# ========== 属性计算 ==========
def get_player_all_atk():
    base = game_data["player"]["attack"]
    add = EQUIPMENT[game_data["equip"]]["atk"]
    if game_data["buff_rage"] > 0:
        return int((base + add) * 1.5)
    return base + add

def get_player_all_def():
    base = game_data["player"]["defend"]
    add = EQUIPMENT[game_data["equip"]]["def"]
    if game_data["buff_shield"] > 0:
        return int((base + add) * 2)
    return base + add

# ========== UI渲染 ==========
def render_game_ui():
    table = Table(title="🎮 硬核控制台打怪游戏", show_lines=True)
    table.add_column("玩家信息", style="cyan", width=38)
    table.add_column("敌方怪物", style="magenta", width=38)

    p = game_data["player"]
    info_p = Text()
    info_p.append(f"等级：{game_data['player_lv']}\n", style="bold cyan")
    info_p.append(f"血量：{p['hp']}/{p['max_hp']}\n", style="green")
    info_p.append(f"总攻击：{get_player_all_atk()}\n", style="orange1")
    info_p.append(f"总防御：{get_player_all_def()}\n", style="blue")
    info_p.append(f"金币：{game_data['gold']}\n", style="gold1")
    info_p.append(f"药水：{game_data['potion']}瓶\n", style="hot_pink")
    info_p.append(f"装备：{game_data['equip']}\n", style="white")
    info_p.append(f"总击杀：{game_data['kill_count']}\n", style="gray")
    info_p.append(f"狂暴{game_data['buff_rage']}回合 | 护盾{game_data['buff_shield']}回合", style="red")

    m_name = game_data["monster_name"]
    m = game_data["monster"]
    info_m = Text()
    info_m.append(f"怪物：{m_name}\n", style=f"bold {m['name_color']}")
    info_m.append(f"血量：{m['hp']}/{m['max_hp']}\n", style="green")
    info_m.append(f"攻击：{m['attack']}\n", style="orange1")
    info_m.append(f"防御：{m['defend']}\n", style="blue")
    info_m.append(f"击杀金币：{m['gold']}", style="gold1")
    table.add_row(info_p, info_m)
    return table

def show_hp_bar(cur, max_hp, color):
    with Progress(
        TextColumn(""),
        BarColumn(complete_style=color),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as prog:
        t = prog.add_task("HP", total=max_hp)
        prog.update(t, completed=cur)

# ========== 战斗逻辑 ==========
def monster_attack():
    p = game_data["player"]
    m = game_data["monster"]
    dodge = p["dodge_rate"]
    if random.random() < dodge:
        console.print(Panel("✨ 闪避成功！", style="bright_green"))
        return
    dmg = max(m["attack"] - get_player_all_def(), 1)
    if random.random() < m["crit_rate"]:
        dmg = int(dmg * 1.8)
        console.print(Panel(f"💥怪物暴击！-{dmg}", style="red"))
    else:
        console.print(Panel(f"👹怪物攻击 -{dmg}", style="magenta"))
    p["hp"] -= dmg
    show_hp_bar(p["hp"], p["max_hp"], "green")
    if p["hp"] <= 0:
        console.print(Panel("💀 你阵亡，游戏结束", style="bold red"))
        exit()

def player_normal_hit():
    m = game_data["monster"]
    atk = get_player_all_atk()
    dmg = max(atk - m["defend"], 1)
    crit_mult = game_data["player"]["crit_dmg"]
    if random.random() < 0.12:
        dmg = int(dmg * crit_mult)
        console.print(Panel(f"🔥暴击！{dmg}伤害", style="yellow"))
    else:
        console.print(Panel(f"⚔普攻 {dmg}伤害", style="cyan"))
    m["hp"] -= dmg
    show_hp_bar(m["hp"], m["max_hp"], "red")
    check_monster_dead()

def player_rage_skill():
    if game_data["potion"] < 1:
        console.print("[red]药水不足！[/]")
        return
    game_data["potion"] -= 1
    game_data["buff_rage"] = 3
    console.print(Panel("🩸狂暴3回合，攻击+50%", style="dark_orange"))
    player_normal_hit()

def player_shield_skill():
    if game_data["potion"] < 1:
        console.print("[red]药水不足！[/]")
        return
    game_data["potion"] -= 1
    game_data["buff_shield"] = 3
    console.print(Panel("🛡护盾3回合，防御翻倍", style="blue"))

def player_heal_skill():
    if game_data["potion"] < 1:
        console.print("[red]药水不足！[/]")
        return
    game_data["potion"] -= 1
    p = game_data["player"]
    heal = 120
    p["hp"] = min(p["hp"] + heal, p["max_hp"])
    console.print(Panel(f"💚回血 +{heal}", style="hot_pink"))
    show_hp_bar(p["hp"], p["max_hp"], "green")

def check_monster_dead():
    m = game_data["monster"]
    if m["hp"] <= 0:
        gold = m["gold"]
        game_data["gold"] += gold
        game_data["kill_count"] += 1

        console.print(Panel(f"✅ 击杀！获得 {gold} 金币", style="green"))
        # 随机额外掉落
        extra = random.randint(5, 30) if random.random() < 0.35 else 0
        if extra > 0:
            game_data["gold"] += extra
            console.print(f"💰额外掉落 {extra} 金币")
        m["hp"] = m["max_hp"]
        game_data["in_battle"] = False
        check_achievement()
        return True
    return False

# 成就检测
def check_achievement():
    kill = game_data["kill_count"]
    lv = game_data["player_lv"]
    ach = game_data["achievements"]
    if not ach["初次狩猎"]["done"] and kill >= 1:
        ach["初次狩猎"]["done"] = True
        game_data["gold"] += ach["初次狩猎"]["reward"]
        console.print("[bold gold]🏆解锁成就：初次狩猎，奖励20金币[/]")
    if not ach["百人斩"]["done"] and kill >= 100:
        ach["百人斩"]["done"] = True
        game_data["gold"] += ach["百人斩"]["reward"]
        console.print("[bold gold]🏆解锁成就：百人斩，奖励300金币[/]")
    if not ach["屠龙勇士"]["done"] and kill >= 50:
        ach["屠龙勇士"]["done"] = True
        game_data["gold"] += ach["屠龙勇士"]["reward"]
        console.print("[bold gold]🏆解锁成就：屠龙勇士，奖励800金币[/]")
    if not ach["满级战神"]["done"] and lv == "传说战神":
        ach["满级战神"]["done"] = True
        game_data["gold"] += ach["满级战神"]["reward"]
        console.print("[bold gold]🏆解锁成就：满级战神，奖励1200金币[/]")

# 实时战斗循环
def battle_loop():
    game_data["in_battle"] = True
    console.clear()
    console.print(render_game_ui())
    tip = Panel("""
【战斗按键】
A=普攻  W=狂暴  S=护盾  D=回血  ESC=逃跑
""", style="bold yellow")
    console.print(tip)
    console.print("[green]进入战斗，直接按键盘操作[/]")
    while game_data["in_battle"]:
        if game_data["buff_rage"] > 0:
            game_data["buff_rage"] -= 1
        if game_data["buff_shield"] > 0:
            game_data["buff_shield"] -= 1
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
            console.print("[yellow]成功逃离战斗[/]")
            sleep(0.5)
        sleep(0.05)

# 升级系统
def level_up():
    lv_chain = [
        ("新手", "1级战士"),
        ("1级战士", "2级勇士"),
        ("2级勇士", "3级骑士"),
        ("3级骑士", "传说战神")
    ]
    cur = game_data["player_lv"]
    next_lv = None
    for old, new in lv_chain:
        if old == cur:
            next_lv = new
            break
    if not next_lv:
        console.print("[green]已满级：传说战神[/]")
        return
    cost = CHARACTERS[next_lv]["upgrade"]
    if game_data["gold"] >= cost:
        game_data["gold"] -= cost
        game_data["player_lv"] = next_lv
        game_data["player"] = CHARACTERS[next_lv].copy()
        console.print(Panel(f"🎉升级至 {next_lv}", style="green"))
        check_achievement()
    else:
        console.print(f"[red]金币不足，升级需要 {cost} 金币[/]")

# 切换怪物
def change_monster():
    console.print("[yellow]怪物列表："+"、".join(MONSTERS.keys())+"[/]")
    sel = Prompt.ask("输入怪物名称")
    if sel in MONSTERS:
        game_data["monster_name"] = sel
        game_data["monster"] = MONSTERS[sel].copy()
        console.print(f"[green]切换目标：{sel}[/]")
    else:
        console.print("[red]不存在该怪物[/]")

# 商店
def shop_potion():
    console.print(Panel("🏪药水商店 15金币/瓶", style="gold1"))
    num = Prompt.ask("购买数量(0退出)", default="0")
    try:
        n = int(num)
    except:
        console.print("[red]输入数字[/]")
        return
    if n <= 0:
        return
    total = n * 15
    if game_data["gold"] >= total:
        game_data["gold"] -= total
        game_data["potion"] += n
        console.print("[green]购买成功[/]")
    else:
        console.print("[red]金币不足[/]")

def shop_equip():
    console.print(Panel("🛡装备商店", style="gold1"))
    for name, attr in EQUIPMENT.items():
        if name != "无装备":
            console.print(f"{name} | 攻+{attr['atk']} 防+{attr['def']} | {attr['price']}金")
    sel = Prompt.ask("输入装备名购买，无装备退出", default="无装备")
    if sel == "无装备":
        return
    if sel not in EQUIPMENT:
        console.print("[red]装备不存在[/]")
        return
    cost = EQUIPMENT[sel]["price"]
    if game_data["gold"] >= cost:
        game_data["gold"] -= cost
        game_data["equip"] = sel
        console.print(f"[green]装备{sel}完成[/]")
    else:
        console.print("[red]金币不足[/]")

# 成就面板
def show_achievement():
    table = Table(title="🏆成就列表", show_lines=True)
    table.add_column("成就名称")
    table.add_column("完成条件")
    table.add_column("奖励金币")
    table.add_column("状态")
    for name, info in game_data["achievements"].items():
        cond = str(info["need"])
        status = "[green]已完成[/]" if info["done"] else "[red]未解锁[/]"
        table.add_row(name, cond, str(info["reward"]), status)
    console.print(table)

# 主菜单
def main_loop():
    load_game()
    while True:
        console.clear()
        console.print(render_game_ui())
        menu = Panel("""
[1] 实时按键战斗
[2] 切换挑战怪物
[3] 角色升级养成
[4] 药水商店
[5] 装备商店
[6] 查看成就系统
[7] 手动存档
[0] 退出游戏
""", title="主功能菜单", style="blue")
        console.print(menu)
        op = Prompt.ask("输入编号")
        if op == "1":
            battle_loop()
        elif op == "2":
            change_monster()
        elif op == "3":
            level_up()
        elif op == "4":
            shop_potion()
        elif op == "5":
            shop_equip()
        elif op == "6":
            show_achievement()
        elif op == "7":
            save_game()
        elif op == "0":
            save_game()
            console.print("[green]已自动存档，游戏退出[/]")
            break
        else:
            console.print("[red]无效输入[/]")
        Prompt.ask("\n回车返回主界面")

if __name__ == "__main__":
    main_loop()