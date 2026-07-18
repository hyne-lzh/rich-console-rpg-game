# Rich Console GUI RPG | Rich 图形界面控制台打怪RPG
A Python RPG game built with Rich terminal styling + Tkinter graphical button UI, supporting clickable battle operations & bilingual display.
一款融合Rich美化终端与Tkinter可视化按钮窗口的Python角色扮演游戏，支持点击式战斗操作、全界面中英双语展示。

## Core Features | 功能特色
1. 6 tiered monsters & 5-tier character growth progression, full EN/CN bilingual naming
   6种梯度难度怪物、五阶角色养成体系，全部怪物/角色名称中英双语对照
2. Graphical window button combat, no raw keyboard required; original hotkey reserve support
   图形窗口按钮战斗，无需纯键盘操作，同时保留原版快捷键兼容
3. Complete shop system: gear shop & potion shop, critical hit, dodge & random gold loot drop
   完整商店体系：装备商店、药水商店，附带暴击、闪避、随机金币掉落机制
4. Dual buff mechanics: Rage (50% damage boost) & Shield (2x defense for 3 rounds)
   双增益Buff机制：狂暴增伤、护盾3回合防御翻倍
5. Unlockable achievement system with gold reward upon completing kill/level milestones
   可解锁成就系统，达成击杀、等级里程碑自动发放金币奖励
6. Local JSON persistent save, auto-save progress when closing game window
   本地JSON持久化存档，关闭游戏窗口自动保存全部进度
7. Visual stat panel, real-time battle log pop-up windows for shop/monster switch/achievement
   可视化属性面板、实时战斗日志，配套怪物切换、商店、成就独立弹窗

## Install Dependencies | 依赖安装
```bash
pip install rich keyboard
```
> Tkinter is built-in with standard Python installation, no extra installation needed.
> Tkinter为Python自带标准库，无需额外安装

## How to Run | 运行方式
```bash
python main_tkinter.py
```

## GUI Button Function Guide | 图形界面按钮功能说明
### Battle Skill Buttons | 战斗技能按钮
- Basic ATK / 普攻: Deal normal damage to enemy monster
  普通攻击：对敌方怪物造成基础伤害
- Rage / 狂暴: Consume 1 potion, raise attack by 50% for 3 rounds, trigger attack instantly
  狂暴技能：消耗1瓶药水，3回合攻击提升50%并立即发起攻击
- Shield / 护盾: Consume 1 potion, double defense stat for 3 rounds
  护盾技能：消耗1瓶药水，3回合内防御数值翻倍
- Heal / 回血: Consume 1 potion, restore 120 HP instantly
  回血技能：消耗1瓶药水，瞬间恢复120点血量
- Flee / 逃离: Exit current battle directly without taking monster counterattack
  逃离战斗：直接退出本场战斗，不会受到怪物反击

### System Function Buttons | 系统功能按钮
- Start Battle / 开始战斗: Enter combat mode and enable skill buttons
  开始战斗：进入战斗模式，解锁全部技能按钮
- Switch Monster / 切换怪物: Pop-up window to select target monster to fight
  切换怪物：弹出选择窗口，更换将要挑战的怪物
- Level Up / 角色升级: Spend gold to advance character tier and boost base stats
  角色升级：消耗金币提升角色阶位，永久提升基础攻防血量
- Potion Shop / 药水商店: Bulk purchase recovery potions with gold
  药水商店：使用金币批量购买战斗回血药水
- Equip Shop / 装备商店: Buy gears to permanently raise attack & defense
  装备商店：购买装备永久提升角色攻击、防御属性
- Achievements / 成就列表: View all unlocked & locked milestones with gold rewards
  成就列表：查看全部已解锁/未解锁成就与对应金币奖励
- Save Game / 手动存档: Manually write current game progress to JSON save file
  手动存档：将当前角色、金币、击杀进度写入本地存档文件
