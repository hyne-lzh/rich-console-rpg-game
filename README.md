# Rich控制台实时按键打怪RPG
一款Python控制台文字冒险游戏，基于rich美化UI，支持全局键盘实时战斗。

## 功能特色
1. 6种梯度怪物，5阶角色养成系统
2. 实时键盘战斗：A普攻/W狂暴/S护盾/D回血/ESC逃跑
3. 装备商店、药水商店、暴击、闪避、随机金币掉落
4. Buff增益系统：狂暴增伤、护盾双倍防御
5. 成就系统，完成目标领取金币奖励
6. 本地JSON存档，退出自动保存进度

## 依赖安装
```bash
pip install rich keyboard
运行方式
bash
运行
python game.py
战斗按键说明
A：普通攻击
W：狂暴技能（消耗药水，3 回合攻击 + 50%）
S：护盾技能（消耗药水，3 回合防御翻倍）
D：瞬间回血 120 血量
ESC：逃离当前战斗

# Rich Real-Time Keypress Combat RPG (Console Edition)
A text-based adventure game built for Python console, styled with Rich library, featuring global real-time keyboard combat controls.

## Core Features
1. Six tiered monsters & five-tier character progression system
2. Real-time keyboard combat controls: A for basic attack / W for Rage buff / S for Shield buff / D for instant HP restore / ESC to flee battle
3. Gear shop, potion shop, critical hit system, dodge mechanic & random gold drop rewards
4. Buff mechanics: Rage (50% damage boost) and Shield (2x defense multiplier)
5. Achievement system with gold rewards upon milestone completion
6. Local JSON save system; progress auto-saves on exit

## Dependency Installation
```bash
pip install rich keyboard
```

## Launch Command
```bash
python game.py
```

## Combat Hotkey Guide
- A: Basic Attack
- W: Rage Skill (Consumes 1 potion, boosts attack damage by 50% for 3 rounds)
- S: Shield Skill (Consumes 1 potion, doubles defense stat for 3 rounds)
- D: Instant HP Recovery (Restores 120 health points)
- ESC: Escape the current combat encounter
