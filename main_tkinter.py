from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn
from time import sleep
import random
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

console = Console()
SAVE_FILE = "game_save.json"

# ========== 【原有数值配置完全不变】怪物、角色、装备、成就 ==========
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

EQUIPMENT = {
    "无装备": {"atk": 0, "def": 0, "price": 0},
    "铁剑": {"atk": 15, "def": 0, "price": 120},
    "皮甲": {"atk": 0, "def": 10, "price": 100},
    "精钢长剑": {"atk": 30, "def": 5, "price": 350},
    "骑士重甲": {"atk": 8, "def": 35, "price": 400},
    "黄金套装": {"atk": 40, "def": 25, "price": 600},
    "魔龙神装": {"atk": 80, "def": 60, "price": 1500}
}

ACHIEVEMENTS = {
    "初次狩猎": {"need": 1, "reward": 20, "done": False},
    "百人斩": {"need": 100, "reward": 300, "done": False},
    "屠龙勇士": {"need": 50, "reward": 800, "done": False},
    "满级战神": {"need": "传说战神", "reward": 1200, "done": False}
}

# ========== 全局游戏数据 ==========
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

# ========== 存档读档（逻辑不变） ==========
def save_game():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(game_data, f, ensure_ascii=False, indent=2)
    console.print("[green]✅ 存档成功！[/]")
    game_gui.log_text.insert(tk.END, "✅ 存档成功！\n")

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

# ========== 战斗核心逻辑（仅输出改为GUI日志） ==========
def monster_attack():
    p = game_data["player"]
    m = game_data["monster"]
    dodge = p["dodge_rate"]
    if random.random() < dodge:
        msg = "✨ 闪避成功！"
        console.print(Panel(msg, style="bright_green"))
        game_gui.log_text.insert(tk.END, msg + "\n")
        return
    dmg = max(m["attack"] - get_player_all_def(), 1)
    if random.random() < m["crit_rate"]:
        dmg = int(dmg * 1.8)
        msg = f"💥怪物暴击！-{dmg}"
        console.print(Panel(msg, style="red"))
    else:
        msg = f"👹怪物攻击 -{dmg}"
        console.print(Panel(msg, style="magenta"))
    game_gui.log_text.insert(tk.END, msg + "\n")
    p["hp"] -= dmg
    if p["hp"] <= 0:
        msg = "💀 你阵亡，游戏结束"
        console.print(Panel(msg, style="bold red"))
        game_gui.log_text.insert(tk.END, msg + "\n")
        messagebox.showerror("游戏结束", "你已阵亡，游戏将重置！")
        load_game()
        game_gui.refresh_ui()
        return
    game_gui.refresh_ui()

def player_normal_hit():
    m = game_data["monster"]
    atk = get_player_all_atk()
    dmg = max(atk - m["defend"], 1)
    crit_mult = game_data["player"]["crit_dmg"]
    if random.random() < 0.12:
        dmg = int(dmg * crit_mult)
        msg = f"🔥暴击！{dmg}伤害"
        console.print(Panel(msg, style="yellow"))
    else:
        msg = f"⚔普攻 {dmg}伤害"
        console.print(Panel(msg, style="cyan"))
    game_gui.log_text.insert(tk.END, msg + "\n")
    m["hp"] -= dmg
    game_gui.refresh_ui()
    check_monster_dead()

def player_rage_skill():
    if game_data["potion"] < 1:
        msg = "药水不足！"
        console.print("[red]" + msg + "[/]")
        game_gui.log_text.insert(tk.END, msg + "\n")
        return
    game_data["potion"] -= 1
    game_data["buff_rage"] = 3
    msg = "🩸狂暴3回合，攻击+50%"
    console.print(Panel(msg, style="dark_orange"))
    game_gui.log_text.insert(tk.END, msg + "\n")
    player_normal_hit()
    if game_data["in_battle"]:
        sleep(0.3)
        monster_attack()

def player_shield_skill():
    if game_data["potion"] < 1:
        msg = "药水不足！"
        console.print("[red]" + msg + "[/]")
        game_gui.log_text.insert(tk.END, msg + "\n")
        return
    game_data["potion"] -= 1
    game_data["buff_shield"] = 3
    msg = "🛡护盾3回合，防御翻倍"
    console.print(Panel(msg, style="blue"))
    game_gui.log_text.insert(tk.END, msg + "\n")
    game_gui.refresh_ui()

def player_heal_skill():
    if game_data["potion"] < 1:
        msg = "药水不足！"
        console.print("[red]" + msg + "[/]")
        game_gui.log_text.insert(tk.END, msg + "\n")
        return
    game_data["potion"] -= 1
    p = game_data["player"]
    heal = 120
    p["hp"] = min(p["hp"] + heal, p["max_hp"])
    msg = f"💚回血 +{heal}"
    console.print(Panel(msg, style="hot_pink"))
    game_gui.log_text.insert(tk.END, msg + "\n")
    game_gui.refresh_ui()

def check_monster_dead():
    m = game_data["monster"]
    if m["hp"] <= 0:
        gold = m["gold"]
        game_data["gold"] += gold
        game_data["kill_count"] += 1
        msg = f"✅ 击杀！获得 {gold} 金币"
        console.print(Panel(msg, style="green"))
        game_gui.log_text.insert(tk.END, msg + "\n")
        extra = random.randint(5, 30) if random.random() < 0.35 else 0
        if extra > 0:
            game_data["gold"] += extra
            msg2 = f"💰额外掉落 {extra} 金币"
            console.print(msg2)
            game_gui.log_text.insert(tk.END, msg2 + "\n")
        m["hp"] = m["max_hp"]
        game_data["in_battle"] = False
        check_achievement()
        game_gui.refresh_ui()
        return True
    return False

def check_achievement():
    kill = game_data["kill_count"]
    lv = game_data["player_lv"]
    ach = game_data["achievements"]
    if not ach["初次狩猎"]["done"] and kill >= 1:
        ach["初次狩猎"]["done"] = True
        game_data["gold"] += ach["初次狩猎"]["reward"]
        msg = "🏆解锁成就：初次狩猎，奖励20金币"
        console.print("[bold gold]" + msg + "[/]")
        game_gui.log_text.insert(tk.END, msg + "\n")
    if not ach["百人斩"]["done"] and kill >= 100:
        ach["百人斩"]["done"] = True
        game_data["gold"] += ach["百人斩"]["reward"]
        msg = "🏆解锁成就：百人斩，奖励300金币"
        console.print("[bold gold]" + msg + "[/]")
        game_gui.log_text.insert(tk.END, msg + "\n")
    if not ach["屠龙勇士"]["done"] and kill >= 50:
        ach["屠龙勇士"]["done"] = True
        game_data["gold"] += ach["屠龙勇士"]["reward"]
        msg = "🏆解锁成就：屠龙勇士，奖励800金币"
        console.print("[bold gold]" + msg + "[/]")
        game_gui.log_text.insert(tk.END, msg + "\n")
    if not ach["满级战神"]["done"] and lv == "传说战神":
        ach["满级战神"]["done"] = True
        game_data["gold"] += ach["满级战神"]["reward"]
        msg = "🏆解锁成就：满级战神，奖励1200金币"
        console.print("[bold gold]" + msg + "[/]")
        game_gui.log_text.insert(tk.END, msg + "\n")
    game_gui.refresh_ui()

# ========== GUI图形界面主类（窗口、按钮、面板、刷新） ==========
class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("控制台RPG - 图形按钮版")
        self.root.geometry("1100x750")

        # 顶部左右分栏：玩家信息 / 怪物信息
        top_frame = tk.Frame(root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        # 玩家面板
        self.player_frame = tk.LabelFrame(top_frame, text="玩家信息", width=520, height=220)
        self.player_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.player_labels = {}
        info_list = ["等级", "血量", "总攻击", "总防御", "金币", "药水", "装备", "总击杀", "狂暴回合", "护盾回合"]
        for idx, name in enumerate(info_list):
            lbl = tk.Label(self.player_frame, text=f"{name}: ")
            lbl.grid(row=idx, column=0, sticky="w", padx=8, pady=3)
            val_lbl = tk.Label(self.player_frame, text="0")
            val_lbl.grid(row=idx, column=1, sticky="w", padx=8)
            self.player_labels[name] = val_lbl

        # 怪物面板
        self.monster_frame = tk.LabelFrame(top_frame, text="敌方怪物", width=520, height=220)
        self.monster_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        self.monster_labels = {}
        m_info = ["怪物名称", "血量", "攻击", "防御", "击杀金币"]
        for idx, name in enumerate(m_info):
            lbl = tk.Label(self.monster_frame, text=f"{name}: ")
            lbl.grid(row=idx, column=0, sticky="w", padx=8, pady=6)
            val_lbl = tk.Label(self.monster_frame, text="0")
            val_lbl.grid(row=idx, column=1, sticky="w", padx=8)
            self.monster_labels[name] = val_lbl

        # 中部战斗日志框
        log_frame = tk.LabelFrame(root, text="战斗日志")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.log_text = tk.Text(log_frame, height=12)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        # 底部功能按钮区
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill=tk.X, padx=10, pady=8)

        # 战斗技能按钮
        tk.Button(btn_frame, text="普攻(A)", width=12, command=lambda: self.do_battle_skill("atk")).grid(row=0, column=0, padx=4)
        tk.Button(btn_frame, text="狂暴(W)", width=12, command=lambda: self.do_battle_skill("rage")).grid(row=0, column=1, padx=4)
        tk.Button(btn_frame, text="护盾(S)", width=12, command=lambda: self.do_battle_skill("shield")).grid(row=0, column=2, padx=4)
        tk.Button(btn_frame, text="回血(D)", width=12, command=lambda: self.do_battle_skill("heal")).grid(row=0, column=3, padx=4)
        tk.Button(btn_frame, text="逃离战斗(ESC)", width=12, command=self.flee_battle).grid(row=0, column=4, padx=4)

        # 系统功能按钮
        tk.Button(btn_frame, text="开始战斗", width=12, command=self.start_battle).grid(row=1, column=0, padx=4, pady=4)
        tk.Button(btn_frame, text="切换怪物", width=12, command=self.select_monster).grid(row=1, column=1, padx=4, pady=4)
        tk.Button(btn_frame, text="角色升级", width=12, command=self.upgrade_lv).grid(row=1, column=2, padx=4, pady=4)
        tk.Button(btn_frame, text="药水商店", width=12, command=self.open_potion_shop).grid(row=1, column=3, padx=4, pady=4)
        tk.Button(btn_frame, text="装备商店", width=12, command=self.open_equip_shop).grid(row=1, column=4, padx=4, pady=4)
        tk.Button(btn_frame, text="查看成就", width=12, command=self.show_ach).grid(row=1, column=5, padx=4, pady=4)
        tk.Button(btn_frame, text="手动存档", width=12, command=save_game).grid(row=1, column=6, padx=4, pady=4)

        self.refresh_ui()

    # 刷新全部面板数值
    def refresh_ui(self):
        p_data = game_data["player"]
        m_data = game_data["monster"]
        all_atk = get_player_all_atk()
        all_def = get_player_all_def()

        # 更新玩家面板
        self.player_labels["等级"].config(text=game_data["player_lv"])
        self.player_labels["血量"].config(text=f"{p_data['hp']}/{p_data['max_hp']}")
        self.player_labels["总攻击"].config(text=str(all_atk))
        self.player_labels["总防御"].config(text=str(all_def))
        self.player_labels["金币"].config(text=str(game_data["gold"]))
        self.player_labels["药水"].config(text=str(game_data["potion"]))
        self.player_labels["装备"].config(text=game_data["equip"])
        self.player_labels["总击杀"].config(text=str(game_data["kill_count"]))
        self.player_labels["狂暴回合"].config(text=str(game_data["buff_rage"]))
        self.player_labels["护盾回合"].config(text=str(game_data["buff_shield"]))

        # 更新怪物面板
        self.monster_labels["怪物名称"].config(text=game_data["monster_name"])
        self.monster_labels["血量"].config(text=f"{m_data['hp']}/{m_data['max_hp']}")
        self.monster_labels["攻击"].config(text=str(m_data["attack"]))
        self.monster_labels["防御"].config(text=str(m_data["defend"]))
        self.monster_labels["击杀金币"].config(text=str(m_data["monster"]["gold"]))

    # 开启战斗
    def start_battle(self):
        if game_data["in_battle"]:
            messagebox.showinfo("提示", "你正在战斗中！")
            return
        game_data["in_battle"] = True
        self.log_text.insert(tk.END, "===== 战斗开始 =====\n")
        self.refresh_ui()

    # 释放战斗技能
    def do_battle_skill(self, skill_type):
        if not game_data["in_battle"]:
            messagebox.showwarning("警告", "请先点击【开始战斗】！")
            return
        # 回合buff自动递减
        if game_data["buff_rage"] > 0:
            game_data["buff_rage"] -= 1
        if game_data["buff_shield"] > 0:
            game_data["buff_shield"] -= 1
        if skill_type == "atk":
            player_normal_hit()
            if game_data["in_battle"]:
                self.root.update()
                sleep(0.3)
                monster_attack()
        elif skill_type == "rage":
            player_rage_skill()
        elif skill_type == "shield":
            player_shield_skill()
        elif skill_type == "heal":
            player_heal_skill()
        self.refresh_ui()

    # 逃跑
    def flee_battle(self):
        if not game_data["in_battle"]:
            return
        game_data["in_battle"] = False
        self.log_text.insert(tk.END, "成功逃离战斗\n===== 战斗结束 =====\n")
        self.refresh_ui()

    # 切换怪物弹窗
    def select_monster(self):
        win = tk.Toplevel(self.root)
        win.title("选择挑战怪物")
        monster_list = list(MONSTERS.keys())
        var = tk.StringVar(value=monster_list[0])
        for name in monster_list:
            tk.Radiobutton(win, text=name, variable=var, value=name).pack(anchor="w", padx=10, pady=2)
        def confirm():
            sel = var.get()
            game_data["monster_name"] = sel
            game_data["monster"] = MONSTERS[sel].copy()
            self.log_text.insert(tk.END, f"切换目标怪物：{sel}\n")
            self.refresh_ui()
            win.destroy()
        tk.Button(win, text="确认选择", command=confirm).pack(pady=8)

    # 角色升级
    def upgrade_lv(self):
        lv_chain = [("新手", "1级战士"), ("1级战士", "2级勇士"), ("2级勇士", "3级骑士"), ("3级骑士", "传说战神")]
        cur = game_data["player_lv"]
        next_lv = None
        for old, new in lv_chain:
            if old == cur:
                next_lv = new
                break
        if not next_lv:
            messagebox.showinfo("提示", "已满级：传说战神")
            return
        cost = CHARACTERS[next_lv]["upgrade"]
        if game_data["gold"] >= cost:
            game_data["gold"] -= cost
            game_data["player_lv"] = next_lv
            game_data["player"] = CHARACTERS[next_lv].copy()
            self.log_text.insert(tk.END, f"🎉升级至 {next_lv}\n")
            check_achievement()
        else:
            messagebox.showerror("金币不足", f"升级需要 {cost} 金币")
        self.refresh_ui()

    # 药水商店弹窗
    def open_potion_shop(self):
        win = tk.Toplevel(self.root)
        win.title("药水商店 15金币/瓶")
        tk.Label(win, text="输入购买数量(0关闭)").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=3)
        def buy():
            try:
                num = int(entry.get())
            except:
                messagebox.showerror("错误", "请输入数字")
                return
            if num <= 0:
                win.destroy()
                return
            total = num * 15
            if game_data["gold"] >= total:
                game_data["gold"] -= total
                game_data["potion"] += num
                self.log_text.insert(tk.END, f"购买{num}瓶药水成功\n")
            else:
                messagebox.showerror("金币不足", f"总价{total}金币")
            self.refresh_ui()
        tk.Button(win, text="确认购买", command=buy).pack(pady=6)

    # 装备商店弹窗
    def open_equip_shop(self):
        win = tk.Toplevel(self.root)
        win.title("装备商店")
        equip_list = [k for k in EQUIPMENT.keys() if k != "无装备"]
        var = tk.StringVar(value=equip_list[0])
        for name in equip_list:
            attr = EQUIPMENT[name]
            tk.Radiobutton(win, text=f"{name} 攻+{attr['atk']} 防+{attr['def']} 价格{attr['price']}",
                           variable=var, value=name).pack(anchor="w", padx=10, pady=2)
        def buy():
            sel = var.get()
            cost = EQUIPMENT[sel]["price"]
            if game_data["gold"] >= cost:
                game_data["gold"] -= cost
                game_data["equip"] = sel
                self.log_text.insert(tk.END, f"装备{sel}成功\n")
            else:
                messagebox.showerror("金币不足", f"装备售价{cost}金币")
            self.refresh_ui()
            win.destroy()
        tk.Button(win, text="购买装备", command=buy).pack(pady=8)

    # 成就弹窗
    def show_ach(self):
        win = tk.Toplevel(self.root)
        win.title("成就列表")
        row = 0
        tk.Label(win, text="成就名称", width=12).grid(row=row, column=0, padx=5, pady=3)
        tk.Label(win, text="条件", width=10).grid(row=row, column=1, padx=5, pady=3)
        tk.Label(win, text="奖励金币", width=10).grid(row=row, column=2, padx=5, pady=3)
        tk.Label(win, text="状态", width=8).grid(row=row, column=3, padx=5, pady=3)
        row += 1
        for name, info in game_data["achievements"].items():
            cond = str(info["need"])
            status = "已完成" if info["done"] else "未解锁"
            tk.Label(win, text=name).grid(row=row, column=0)
            tk.Label(win, text=cond).grid(row=row, column=1)
            tk.Label(win, text=str(info["reward"])).grid(row=row, column=2)
            tk.Label(win, text=status).grid(row=row, column=3)
            row += 1

# ========== 程序入口 ==========
game_gui = None
if __name__ == "__main__":
    load_game()
    root = tk.Tk()
    game_gui = GameGUI(root)
    root.mainloop()