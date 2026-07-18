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


# README.md 多引擎复合混淆工具双语文档

# Multi-Engine Python Obfuscator GUI
A bilingual multi-layer composite Python code obfuscation tool based on `python-obfuscator` + AES symmetric encryption + anti-debug detection, with complete Tkinter graphical interactive interface.
一款基于 python-obfuscator + AES对称加密 + 反调试检测构建的双语多层复合Python代码混淆工具，配套完整Tkinter图形交互界面。

## Project Overview | 项目概述
This tool abandons single single-library obfuscation and adopts multi-engine composite reinforcement pipeline, supporting single file obfuscation, batch multi-file processing, code real-time preview, drag-and-drop loading, dark theme switching, configuration import/export, log saving and other practical functions.
本工具摒弃单一库混淆，采用多引擎复合加固流水线，支持单文件混淆、批量多文件处理、代码实时预览、拖拽加载、深色主题切换、配置导入导出、日志保存等实用功能。

### Multi-layer Obfuscation Pipeline | 多层混淆流水线
1. Stage 1: Safe comment cleaning (only delete standalone line `#` comments, no damage to string internal symbols)
   阶段1：安全注释清除（仅删除独立行#注释，不破坏字符串内部符号）
2. Stage 2: Base grammar obfuscation via python-obfuscator (variable/function renaming, dead junk code, control flow flattening, hex/xor string encryption)
   阶段2：python-obfuscator基础语法混淆（变量/函数重命名、垃圾无效代码、控制流扁平化、十六进制/异或字符串加密）
3. Stage 3: AES-128 full text string symmetric encryption (optional, custom 16-bit encryption key supported)
   阶段3：AES-128全文字符串对称加密（可选，支持自定义16位加密密钥）
4. Stage 4: Inject cross-platform anti-debug detection code (block debugger attachment, auto exit program if detected)
   阶段4：注入跨平台反调试检测代码（阻断调试器附加，检测到调试自动退出程序）
5. Optional extra: Compile and export encrypted `.pyc` bytecode file for secondary anti-decompilation reinforcement
   可选附加：编译导出加密pyc字节码文件，二次反编译加固

## Core Functions | 核心功能清单
### 1. File Operation | 文件操作
- Single file selection & automatic output path filling
  单文件选择、输出路径自动填充
- Batch multi-python script one-click obfuscation
  批量多Python脚本一键混淆
- Drag-and-drop file import: Directly drag `.py` into the window to load source code
  拖拽文件导入：直接将py文件拖入窗口加载源码
- Real-time dual split code preview panel (raw source / obfuscated code)
  实时双分栏代码预览面板（原始代码 / 混淆后代码）
- Code difference comparison pop-up window, view text changes before and after obfuscation
  代码差异对比弹窗，查看混淆前后文本改动

### 2. Multi-engine Encryption & Obfuscation | 多引擎加密混淆模块
#### Base Obfuscation Module (python-obfuscator) 基础混淆模块
- String Hex Encrypt / 字符串十六进制加密
- Number Constant Encrypt / 数字常量运算伪装
- Rename Variables / 变量随机乱码重命名
- Rename Functions / 函数随机乱码重命名
- Inject Dead Junk Code / 插入不可执行垃圾分支代码
- Fake Exception Branches / 虚假异常捕获干扰逆向
- Control Flow Flatten / 控制流扁平化打乱原始逻辑
- String XOR Encrypt / 字符串异或二次加密
- Random Indent Disturb / 随机缩进干扰代码可读性
- Remove Type Annotations / 删除类型注解文本

#### Advanced Multi-engine Encryption Module 高级多引擎加密模块
- AES String Encrypt / AES-128对称加密全部明文字符串 (Custom key support 支持自定义密钥)
- Anti-Debug Detect / 跨平台反调试检测（Python trace hook + Windows IsDebuggerPresent API + stack debugger recognition）
- Export Encrypted Pyc / 导出加密字节码pyc文件，提升反编译难度

### 3. Auxiliary Practical Functions | 辅助实用功能
- Dark / Light dual theme switch, eye-care dark mode
  深色/浅色双主题切换，护眼暗色模式
- Obfuscation configuration export & import (save preset as `.json`)
  混淆配置导出/导入（将预设方案保存为json文件）
- Complete running log box, support log export to local txt file
  完整运行日志框，支持日志导出本地txt存档
- One-click full dependency installation button (auto install all missing libraries)
  一键全依赖安装按钮（自动批量安装缺失库）
- MD5 hash calculation, verify text modification before and after obfuscation
  MD5哈希值计算，校验混淆前后文本改动
- Real-time progress bar to display obfuscation execution progress
  实时进度条展示混淆执行进度
- Built-in PyInstaller EXE packaging command prompt pop-up
  内置PyInstaller打包EXE命令提示弹窗
```
## Dependencies Installation | 依赖安装命令
```bash
pip install python-obfuscator tkinterdnd2 pycryptodome astor
```
### Library Function Description | 库作用说明
1. `python-obfuscator`: Base syntax obfuscation core library
   基础语法混淆核心库
2. `tkinterdnd2`: Window drag-and-drop file loading support
   窗口拖拽文件加载支持
3. `pycryptodome`: AES symmetric string encryption engine
   AES对称字符串加密引擎
4. `astor`: Abstract syntax tree parsing tool for string encryption
   字符串加密所需抽象语法树解析工具
5. `tkinter`: Built-in Python GUI library, no extra installation required
   Python自带图形界面库，无需额外安装

## How to Run | 运行方式
1. Save the code as `run_obf.py`
   将源码保存为 run_obf.py
2. Execute the script in terminal
   终端执行脚本：
```bash
python run_obf.py
```
3. After startup, operate through graphical buttons, all text supports Chinese-English dual display
   启动后通过图形按钮操作，全部界面文本支持中英双语同步展示

## GUI Button Guide | 图形界面按钮功能说明
### Top Toolbar | 顶部工具栏
- Dark Mode / 深色模式: Switch light/dark interface theme
  切换亮/暗界面主题
- Save Config / 导出配置: Save current obfuscation switch preset as json file
  将当前混淆勾选预设保存为json文件
- Load Config / 加载配置: Read saved json configuration preset
  读取已保存的json配置预设
- Save Log / 保存日志: Export all running log text to local txt
  将全部运行日志文本导出本地txt
- Custom AES Key / 自定义加密密钥: Input 16-bit custom key for AES string encryption
  输入16位自定义密钥用于AES字符串加密
- Random Seed / 随机种子: Reserved parameter, disabled (python-obfuscator has no set_seed method)
  随机种子：预留参数，已禁用（库无set_seed接口）
- Clear All Comments / 清空注释: Toggle safe single-line comment clearing function
  开关安全单行注释清除功能

### File Selection Area | 文件选择区域
- Source File | 待混淆源码: Input box to display selected single python script path
  输入框展示选中的单个Python脚本路径
- Browse Single / 单选文件: Pop up file selector to pick single source file
  弹出文件选择器选取单个源码文件
- Batch Select / 批量多选: Multi-select multiple `.py` files for batch obfuscation
  多选多个py文件用于批量混淆处理
- Output File | 混淆后输出: Input box to display output save path
  输入框展示输出保存路径
- Browse / 浏览: Pop up save file selector to customize output path
  弹出保存选择器自定义输出路径
- Auto Fill / 自动填充: Auto generate `obf_xxx.py` output path based on source file
  根据源码自动生成 obf_xxx.py 输出路径

### Obfuscation Options Panel | 混淆配置面板
#### Base Obfuscate | 基础语法混淆
Dual-column check box group for all python-obfuscator native obfuscation functions, support one-click full enable/disable
双栏复选框组，包含全部python-obfuscator原生混淆功能，支持一键全开启/全关闭

#### Advanced Multi-Engine Encrypt | 高级多引擎加密
- AES String Encrypt / AES字符串加密: Toggle AES full text string symmetric encryption module
  开关AES全文字符串对称加密模块
- Anti-Debug Detect / 反调试检测: Toggle injection of anti-debug code at file header
  开关在文件头部注入反调试检测代码
- Export Encrypted Pyc / 导出加密字节码: Auto compile `.pyc` bytecode after obfuscation completes
  混淆完成后自动编译pyc字节码文件

#### Preset Shortcut Buttons | 预设快捷按钮
- Enable All / 全选开启: Check all obfuscation & encryption switches
  勾选全部混淆加密开关
- Disable All / 全部关闭: Uncheck all obfuscation & encryption switches
  取消全部混淆加密开关
- Default Preset / 默认推荐配置: Load balanced high-strength composite obfuscation preset
  加载均衡高强度复合混淆预设
- Install All Dependencies / 一键安装全部依赖: Background batch install missing required libraries
  后台批量安装缺失的所需依赖库

### Operation Buttons Area | 操作按钮区
- Start Obfuscate / 开始混淆: Execute multi-layer composite obfuscation for single selected file
  对选中单个文件执行多层复合混淆
- Batch Obfuscate / 批量混淆: Process all batch-selected python files one by one
  逐个处理所有批量选中的Python文件
- Compare Diff / 对比差异: Pop up window to view raw & obfuscated code snippet comparison
  弹窗查看原始与混淆后代码片段对比
- Clear Log / 清空日志: Clear all text in running log box
  清空运行日志框全部文本
- Help Info / 功能说明: Pop up full bilingual function introduction document
  弹窗完整双语功能说明文档
- One-Click EXE Tip / EXE打包命令: Pop up PyInstaller single-file packaging command template
  弹窗PyInstaller单文件打包命令模板

## Fixed Critical Bug List | 已修复关键漏洞清单
1. Removed invalid `set_seed()` call (python-obfuscator library does not support this instance method, eliminate attribute error)
   移除无效set_seed()调用（python-obfuscator库不支持该实例方法，消除属性不存在报错）
2. Rewrote comment cleaning regular expression, only match standalone line `#` comments, avoid truncating string internal text (fix `unterminated string literal` syntax parsing error)
   重写注释清除正则，仅匹配独立行#注释，避免截断字符串内部文本（修复未闭合字符串字面量语法解析报错）
3. Retained AES encryption module but fixed AST string replacement syntax compatibility defects, no longer generate broken cross-line string nodes
   保留AES加密模块，修复AST字符串替换语法兼容缺陷，不再生成破损跨行字符串节点
4. Optimized multi-layer obfuscation execution order, strictly separate comment cleaning, base obfuscation, AES encryption, anti-debug injection to avoid syntax damage
   优化多层混淆执行顺序，严格分隔注释清除、基础混淆、AES加密、反调试注入流程，避免语法损坏
5. Optimized batch processing logic, single file processing failure will not interrupt the entire batch task, log separate record failure file information
   优化批量处理逻辑，单个文件处理失败不会中断整批任务，日志单独记录失败文件信息


## Project File Structure | 项目文件目录
```
obfuscator-tool/
├─ run_obf.py          # Main multi-engine obfuscator GUI source code 多引擎混淆图形工具主程序
├─ README.md           # Bilingual project documentation 本双语项目说明文档
├─ .gitignore          # Git ignore configuration (shield cache, temporary files, pyc, log)
└─ obf_config.json     # Optional custom obfuscation preset configuration file 可选自定义混淆预设配置文件
```

## Notes | 注意事项
1. When using AES string encryption, the target source code cannot contain incomplete escape characters or unclosed triple quotation strings, otherwise AST parsing will fail
   使用AES字符串加密时，目标源码不能包含残缺转义字符、未闭合三引号字符串，否则AST解析会失败
2. The anti-debug code only blocks conventional debuggers, cannot completely prevent reverse analysis; it is recommended to match AES + python-obfuscator composite reinforcement for best effect
   反调试代码仅阻断常规调试器，无法彻底杜绝逆向分析，建议搭配AES+python-obfuscator复合加固效果最优
3. If the obfuscation reports syntax error, you can temporarily uncheck `Clear All Comments` and `AES String Encrypt` to narrow down the problematic module
   若混淆报语法错误，可临时取消勾选「清空注释」「AES字符串加密」缩小故障模块范围
4. The exported `.pyc` bytecode can only run under the same Python major version as the compilation environment
   导出的pyc字节码仅能在编译环境相同大版本Python下运行