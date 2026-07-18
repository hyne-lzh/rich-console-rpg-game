# Rich Console RPG Game | 双语项目文档 README.md
# Rich Console GUI RPG Game
A bilingual Python role-playing game based on Rich terminal beautification + Tkinter graphical button interface.
一款基于Rich终端美化 + Tkinter图形按钮窗口开发的双语角色扮演游戏。

## Project Introduction | 项目介绍
This game abandons pure keyboard input operation in the original console version, and adds a complete graphical window interactive system. All monster, character, equipment, achievement names, interface buttons, battle logs and pop-up prompts support Chinese-English dual display.
本游戏摒弃原版控制台纯键盘输入操作，新增完整图形窗口交互系统；全部怪物、角色、装备、成就名称、界面按钮、战斗日志、弹窗提示均支持中英双语展示。

All core combat logic, numerical growth system, local JSON archive mechanism are fully retained, while adding visual attribute panels, real-time battle log box, independent pop-up windows for shops, monster switching and achievement query.
完整保留全部核心战斗逻辑、数值成长体系、本地JSON存档机制，同时新增可视化属性面板、实时战斗日志框、商店/怪物切换/成就查询独立弹窗。

## Core Features | 功能特色
1. 6 tiered difficulty monsters & 5-tier character progression system, all names bilingual (EN/CN)
   6种梯度难度怪物、五阶角色养成体系，全部名称中英双语对照
2. Graphical button combat operation, compatible with original shortcut key logic
   图形按钮式战斗操作，同时兼容原版快捷键逻辑
3. Complete shop system: potion shop & equipment shop, random gold drop after killing monsters
   完整商店体系：药水商店、装备商店，击杀怪物随机额外金币掉落
4. Dual buff mechanism: Rage (50% attack boost) & Shield (double defense for 3 rounds)
   双增益Buff机制：狂暴增伤、护盾3回合防御翻倍
5. Full achievement unlock system, automatically issue gold rewards when reaching kill/level milestones
   完整成就解锁系统，达成击杀、等级里程碑自动发放金币奖励
6. Local persistent JSON save file, auto-save & manual save function
   本地JSON持久化存档，支持自动重置存档、手动存档
7. Real-time visual stat panel, scrolling battle log, independent pop-up windows for all functional modules
   实时可视化属性面板、滚动战斗日志，全部功能模块配套独立弹窗

## Dependencies | 依赖安装
### Required Libraries | 必需库
```bash
pip install rich
```
- `rich`: Terminal text beautification, colored battle log output
  终端文本美化库，用于彩色战斗日志打印
- `tkinter`: Built-in standard library of Python, no extra installation needed, responsible for graphical window
  Python自带标准图形界面库，无需额外安装，负责窗口、按钮、弹窗渲染

## How to Run | 运行方式
1. Save the game code as `main_tkinter.py`
   将游戏源码保存为 `main_tkinter.py`
2. Execute the script in terminal
   终端执行脚本：
```bash
python main_tkinter.py
```
3. After startup, the graphical main window will pop up, and you can click buttons to complete all game operations
   启动后弹出图形主窗口，点击按钮即可完成全部游戏操作

## GUI Button Function Guide | 图形界面按钮功能说明
### Battle Skill Buttons | 战斗技能按钮
- Basic ATK (A) / 普攻
  English: Deal normal physical damage to the target monster
  中文：对敌方怪物造成基础物理伤害
- Rage (W) / 狂暴
  English: Consume 1 potion, raise attack by 50% for 3 rounds, trigger attack immediately
  中文：消耗1瓶药水，3回合攻击提升50%并立即发起攻击
- Shield (S) / 护盾
  English: Consume 1 potion, double defense value for 3 rounds
  中文：消耗1瓶药水，3回合内防御数值永久翻倍
- Heal (D) / 回血
  English: Consume 1 potion, instantly restore 120 HP, cannot exceed maximum HP
  中文：消耗1瓶药水，瞬间恢复120点血量，不可超出血量上限
- Flee (ESC) / 逃离
  English: Exit current battle directly without receiving monster counterattack
  中文：直接退出本场战斗，不会受到怪物反击伤害

### System Function Buttons | 系统功能按钮
- Start Battle / 开始战斗
  English: Enter combat mode and unlock all skill buttons
  中文：进入战斗模式，解锁全部技能操作按钮
- Switch Monster / 切换怪物
  English: Pop up a selection window to replace the monster to fight
  中文：弹出单选窗口，更换将要挑战的敌方怪物
- Level Up / 角色升级
  English: Spend gold to advance character tier and permanently raise base stats
  中文：消耗金币提升角色阶位，永久提升基础攻防血量属性
- Potion Shop / 药水商店
  English: Bulk purchase recovery potions with gold, unit price 15 gold
  中文：使用金币批量购买战斗回血药水，单价15金币
- Equip Shop / 装备商店
  English: Purchase gears to permanently increase attack and defense attributes
  中文：购买装备永久提升角色攻击、防御数值
- Achievements / 成就列表
  English: Pop up window to view all locked/unlocked achievements and corresponding gold rewards
  中文：弹窗查看全部已解锁、未解锁成就与对应金币奖励
- Save Game / 手动存档
  English: Write current character progress, gold, kill records to local JSON save file
  中文：将当前角色、金币、击杀进度写入本地存档文件

## Game Mechanism Explanation | 游戏机制说明
### 1. Damage Calculation Rule | 伤害计算公式
- Player damage = Total Attack (Base ATK + Equipment ATK) - Monster Defense, minimum damage 1
  玩家伤害 = 总攻击（基础攻击+装备攻击）- 怪物防御，最低造成1点伤害
- Monster damage = Monster Attack - Total Defense (Base DEF + Equipment DEF), minimum damage 1
  怪物伤害 = 怪物攻击 - 总防御（基础防御+装备防御），最低造成1点伤害
- Critical hit: Multiply damage by character critical damage multiplier
  暴击判定：伤害 × 角色暴击倍率
- Dodge: Completely ignore monster attack damage according to character dodge rate
  闪避判定：依据角色闪避概率完全规避怪物伤害

### 2. Buff Duration Rule | Buff回合机制
- Rage / Shield buffs will consume 1 round count after each skill cast
  狂暴、护盾两类增益Buff，每次释放技能后自动扣除1回合持续时间
- Buff effect will be cleared automatically when rounds drop to 0
  回合数归零后，对应增益效果自动失效

### 3. Save File Rule | 存档机制
- Save file name: `game_save.json`, UTF-8 encoding, supports reading and writing Chinese bilingual text
  存档文件名：`game_save.json`，UTF-8编码，支持读写中英双语文本
- Automatically load progress when opening the game; reset progress to initial state if the player dies
  打开游戏自动读取存档；角色阵亡后重置所有进度至初始状态
- Manual save button can save progress at any time to avoid data loss
  手动存档按钮可随时保存进度，防止游戏数据丢失

## Monster Data List | 怪物数据清单
| Monster Name | ATK | HP | DEF | Gold Reward | Critical Rate |
| ---- | ---- | ---- | ---- | ---- | ---- |
| Slime / 史莱姆 | 8 | 40 | 2 | 3 | 3% |
| Small Monster / 小怪 | 10 | 50 | 3 | 5 | 5% |
| Wild Wolf / 野狼 | 18 | 120 | 6 | 12 | 8% |
| Big Monster / 大怪 | 20 | 200 | 10 | 20 | 10% |
| Giant Bear Boss / 巨熊BOSS | 28 | 320 | 18 | 30 | 12% |
| Ancient Dragon / 远古魔龙 | 38 | 500 | 30 | 60 | 18% |

## Character Tier Data List | 角色阶位数值表
| Tier Name | Base ATK | Base HP | Base DEF | Critical Multiplier | Dodge Rate | Upgrade Cost |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| Novice / 新手 | 10 | 200 | 5 | 1.5x | 5% | 0 |
| Lvl 1 Warrior / 1级战士 | 20 | 250 | 20 | 1.6x | 8% | 200 Gold |
| Lvl 2 Veteran / 2级勇士 | 50 | 300 | 40 | 1.8x | 12% | 500 Gold |
| Lvl 3 Knight / 3级骑士 | 70 | 380 | 60 | 2.0x | 18% | 999 Gold |
| Legendary Warlord / 传说战神 | 120 | 500 | 90 | 2.5x | 25% | 2000 Gold |

## Equipment Shop Data List | 装备商店数据
| Equipment Name | ATK Bonus | DEF Bonus | Price |
| ---- | ---- | ---- | ---- |
| Iron Sword / 铁剑 | +15 | 0 | 120 Gold |
| Leather Armor / 皮甲 | 0 | +10 | 100 Gold |
| Fine Steel Longsword / 精钢长剑 | +30 | +5 | 350 Gold |
| Knight Heavy Plate / 骑士重甲 | +8 | +35 | 400 Gold |
| Golden Armor Set / 黄金套装 | +40 | +25 | 600 Gold |
| Dragon God Armor / 魔龙神装 | +80 | +60 | 1500 Gold |

## Achievement List | 成就清单
| Achievement Name | Unlock Condition | Gold Reward |
| ---- | ---- | ---- |
| First Hunt / 初次狩猎 | Kill 1 monster | 20 Gold |
| Century Slayer / 百人斩 | Total kill count ≥ 100 | 300 Gold |
| Dragon Slayer / 屠龙勇士 | Total kill count ≥ 50 | 800 Gold |
| Max Level Warlord / 满级战神 | Reach tier Legendary Warlord / 传说战神 | 1200 Gold |


## File Structure | 项目文件结构
```
console_game/
├─ main_tkinter.py    # Main bilingual GUI game source code 双语图形界面游戏主程序
├─ game_save.json     # Local persistent save file 本地持久化存档文件 (auto-generated after first run)
├─ .gitignore         # Git ignore configuration (shield cache, save file, IDE folders)
└─ README.md          # Bilingual project documentation (this file)
```

## Notes | 注意事项
1. The save file `game_save.json` will be automatically generated after the first run, do not manually edit the file to avoid data damage
   存档文件`game_save.json`首次运行自动生成，请勿手动编辑文件，防止数据损坏
2. Tkinter window may lag slightly during sleep delay after skill release, this is normal combat round simulation logic
   释放技能后sleep延迟期间Tkinter窗口会轻微卡顿，属于正常战斗回合模拟逻辑
3. All text supports Chinese and English switching simultaneously, no extra language configuration required
   全部文本同步支持中英双语展示，无需额外语言切换配置
4. If KeyError appears during startup, check whether the monster/character dictionary key name is `defend` (not `def`)
   启动出现KeyError报错时，检查怪物/角色字典防御字段键名应为`defend`，不可简写为Python keyword `def`