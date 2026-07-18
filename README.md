# Rich Console Real-Time Keypress RPG | Rich控制台实时按键打怪RPG
A Python text adventure game optimized with the Rich library for polished terminal UI, supporting global real-time keyboard combat input.
一款Python控制台文字冒险游戏，基于Rich库美化终端界面，支持全局键盘实时战斗操作。

## Core Features | 功能特色
1. 6 tiered monster types and a 5-stage character progression system
   6种梯度怪物，五阶角色养成体系
2. Instant keyboard combat shortcuts: A = Basic Attack, W = Rage, S = Shield, D = Heal, ESC = Flee
   实时战斗快捷键：A普攻 / W狂暴 / S护盾 / D回血 / ESC逃跑
3. Gear shop, potion shop, critical strikes, evasion, and random gold loot drops
   装备商店、药水商店、暴击机制、闪避判定、随机金币掉落
4. Permanent buff system: Rage (increased damage) & Shield (doubled defense)
   增益Buff系统：狂暴增伤、护盾双倍防御
5. Achievement system that grants gold bonuses after completing milestones
   成就系统，达成目标可领取金币奖励
6. Local JSON save file; your progress automatically saves when exiting the game
   本地JSON存档，退出游戏时自动保存进度

## Install Dependencies | 依赖安装
```bash
pip install rich keyboard
```

## How to Run | 运行方式
```bash
python game.py
```

## Combat Hotkey Reference | 战斗按键说明
- A: Basic Attack | 普通攻击
- W: Rage Skill (Consumes 1 potion, increases attack damage by 50% for 3 turns)
  狂暴技能（消耗1瓶药水，3回合内攻击力提升50%）
- S: Shield Skill (Consumes 1 potion, doubles your defense stat for 3 turns)
  护盾技能（消耗1瓶药水，3回合内防御值翻倍）
- D: Instant Heal (Restores 120 HP)
  瞬间回血（恢复120点血量）
- ESC: Escape from the ongoing battle
  逃离当前战斗
