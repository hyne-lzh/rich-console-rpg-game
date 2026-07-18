# -*- coding:utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinterdnd2 import TkinterDnD, DND_FILES
import json
import hashlib
import os
import subprocess
import sys

# 依赖自动检测
try:
    from python_obfuscator import Obfuscator, ObfuscationConfig
    HAS_OBF = True
except ImportError:
    HAS_OBF = False

class PyObfuscatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Obfuscator | Python高强度代码混淆工具")
        self.root.geometry("1300x820")
        self.root.resizable(True, True)
        self.is_dark = tk.BooleanVar(value=False)
        self.random_seed = tk.StringVar(value="")
        self.clear_comment = tk.BooleanVar(value=True)

        # 全局变量
        self.input_path = tk.StringVar(value="")
        self.output_path = tk.StringVar(value="")
        self.batch_files = []
        self.log_text = None
        self.raw_preview = None
        self.obf_preview = None
        self.progress_bar = None
        self.raw_md5 = ""
        self.obf_md5 = ""

        # 混淆功能勾选映射（名称：显示文本EN/CN）
        self.obf_options = {
            "string_encrypt": {"text": "String Hex Encrypt / 字符串十六进制加密", "var": tk.BooleanVar(value=True)},
            "num_encrypt": {"text": "Number Constant Encrypt / 数字常量加密", "var": tk.BooleanVar(value=True)},
            "rename_var": {"text": "Rename Variables / 变量随机重命名", "var": tk.BooleanVar(value=True)},
            "rename_func": {"text": "Rename Functions / 函数名乱码重命名", "var": tk.BooleanVar(value=True)},
            "dead_code": {"text": "Inject Dead Junk Code / 插入垃圾无效代码", "var": tk.BooleanVar(value=True)},
            "fake_except": {"text": "Fake Exception Branches / 虚假异常分支", "var": tk.BooleanVar(value=True)},
            "control_flat": {"text": "Control Flow Flatten / 控制流扁平化", "var": tk.BooleanVar(value=True)},
            "remove_annot": {"text": "Remove Type Annotations / 删除类型注解", "var": tk.BooleanVar(value=True)},
            "string_xor": {"text": "String XOR Encrypt / 字符串异或加密", "var": tk.BooleanVar(value=True)},
            "random_indent": {"text": "Random Indent Disturb / 随机缩进干扰", "var": tk.BooleanVar(value=False)},
        }
        self.build_ui()
        self.apply_theme()
        # 拖拽绑定
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_file)
        # 依赖缺失弹窗
        if not HAS_OBF:
            self.show_install_popup()

    def build_ui(self):
        # 顶部工具栏：主题、配置导入导出、日志保存
        top_tool = tk.Frame(self.root)
        top_tool.pack(fill="x", padx=10, pady=3)
        ttk.Checkbutton(top_tool, text="Dark Mode / 深色模式", variable=self.is_dark, command=self.apply_theme).pack(side="left", padx=5)
        tk.Button(top_tool, text="Save Config / 导出配置", command=self.export_config).pack(side="left", padx=5)
        tk.Button(top_tool, text="Load Config / 加载配置", command=self.load_config).pack(side="left", padx=5)
        tk.Button(top_tool, text="Save Log / 保存日志", command=self.save_log_file).pack(side="left", padx=5)
        tk.Label(top_tool, text="Random Seed / 随机种子:").pack(side="left", padx=10)
        tk.Entry(top_tool, textvariable=self.random_seed, width=10).pack(side="left")
        ttk.Checkbutton(top_tool, text="Clear All Comments / 清空注释", variable=self.clear_comment).pack(side="right", padx=5)

        # 1. 文件选择区域（单文件+批量）
        file_frame = tk.LabelFrame(self.root, text="File Select | 文件选择")
        file_frame.pack(fill="x", padx=10, pady=6)
        # 单文件
        tk.Label(file_frame, text="Source File | 待混淆源码：").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        tk.Entry(file_frame, textvariable=self.input_path, width=60).grid(row=0, column=1, padx=5)
        tk.Button(file_frame, text="Browse Single / 单选文件", command=self.select_input).grid(row=0, column=2, padx=4)
        tk.Button(file_frame, text="Batch Select / 批量多选", command=self.select_batch).grid(row=0, column=3, padx=4)
        # 输出文件
        tk.Label(file_frame, text="Output File | 混淆后输出：").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        tk.Entry(file_frame, textvariable=self.output_path, width=60).grid(row=1, column=1, padx=5)
        tk.Button(file_frame, text="Browse / 浏览", command=self.select_output).grid(row=1, column=2, padx=4)
        tk.Button(file_frame, text="Auto Fill / 自动填充", command=self.auto_fill_output).grid(row=1, column=3, padx=4)

        # 2. 混淆功能勾选面板
        opt_frame = tk.LabelFrame(self.root, text="Obfuscation Options | 混淆功能配置")
        opt_frame.pack(fill="x", padx=10, pady=6)
        row_idx = 0
        col_idx = 0
        for key, data in self.obf_options.items():
            cb = ttk.Checkbutton(opt_frame, text=data["text"], variable=data["var"])
            cb.grid(row=row_idx, column=col_idx, sticky="w", padx=8, pady=3)
            col_idx += 1
            if col_idx >= 2:
                col_idx = 0
                row_idx += 1
        # 快捷按钮：全选/取消全选/默认
        btn_opt_frame = tk.Frame(opt_frame)
        btn_opt_frame.grid(row=row_idx+1, column=0, columnspan=2, pady=5)
        tk.Button(btn_opt_frame, text="Enable All / 全选开启", command=self.enable_all).grid(row=0, column=0, padx=6)
        tk.Button(btn_opt_frame, text="Disable All / 全部关闭", command=self.disable_all).grid(row=0, column=1, padx=6)
        tk.Button(btn_opt_frame, text="Default Preset / 默认推荐配置", command=self.load_default).grid(row=0, column=2, padx=6)

        # 3. 预览双栏（原始代码 / 混淆代码）
        preview_frame = tk.LabelFrame(self.root, text="Code Preview | 代码预览")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=6)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(1, weight=1)
        tk.Label(preview_frame, text="Raw Source / 原始代码").grid(row=0, column=0)
        tk.Label(preview_frame, text="Obfuscated Source / 混淆代码").grid(row=0, column=1)
        self.raw_preview = scrolledtext.ScrolledText(preview_frame, wrap="word", height=12)
        self.raw_preview.grid(row=1, column=0, sticky="nsew", padx=3)
        self.obf_preview = scrolledtext.ScrolledText(preview_frame, wrap="word", height=12)
        self.obf_preview.grid(row=1, column=1, sticky="nsew", padx=3)

        # 进度条
        self.progress_bar = ttk.Progressbar(self.root, mode="determinate")
        self.progress_bar.pack(fill="x", padx=10, pady=2)

        # 4. 操作按钮区
        run_frame = tk.Frame(self.root)
        run_frame.pack(pady=8)
        tk.Button(run_frame, text="Start Obfuscate / 开始混淆", width=25, bg="#22aa22", fg="white", command=self.run_obfuscate).grid(row=0, column=0, padx=6)
        tk.Button(run_frame, text="Batch Obfuscate / 批量混淆", width=25, bg="#007acc", fg="white", command=self.run_batch).grid(row=0, column=1, padx=6)
        tk.Button(run_frame, text="Compare Diff / 对比差异", width=25, command=self.show_diff).grid(row=0, column=2, padx=6)
        tk.Button(run_frame, text="Clear Log / 清空日志", width=25, command=self.clear_log).grid(row=0, column=3, padx=6)
        tk.Button(run_frame, text="Help Info / 功能说明", width=25, command=self.show_help).grid(row=0, column=4, padx=6)
        tk.Button(run_frame, text="One-Click EXE Tip / EXE打包命令", width=28, command=self.show_pack_cmd).grid(row=0, column=5, padx=6)

        # 5. 运行日志框
        log_frame = tk.LabelFrame(self.root, text="Run Log | 运行日志")
        log_frame.pack(fill="x", padx=10, pady=6)
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap="word", height=6)
        self.log_text.pack(fill="both", expand=True, padx=4, pady=4)

    # 拖拽文件
    def drop_file(self, event):
        path = event.data.strip('{}')
        if path.endswith(".py"):
            self.input_path.set(path)
            self.auto_fill_output()
            self.load_raw_preview()
            self.log(f"Drop file loaded / 拖拽加载文件：{path}")

    # 主题切换
    def apply_theme(self):
        dark = self.is_dark.get()
        bg = "#2b2b2b" if dark else "#ffffff"
        fg = "#ffffff" if dark else "#000000"
        self.root.config(bg=bg)
        for widget in self.root.winfo_children():
            try:
                widget.config(bg=bg, fg=fg)
            except:
                pass

    # 依赖一键安装弹窗
    def show_install_popup(self):
        res = messagebox.askyesno("Dependency Missing / 依赖缺失",
        "Module python-obfuscator not found!\nMissing 混淆库未安装\nInstall now? / 是否一键执行安装命令？")
        if res:
            subprocess.Popen([sys.executable, "-m", "pip", "install", "python-obfuscator"])
            self.log("[Info] Installing python-obfuscator, restart tool after finish / 正在安装依赖，安装完成重启工具")

    # 配置导入导出
    def export_config(self):
        cfg = {}
        for k, v in self.obf_options.items():
            cfg[k] = v["var"].get()
        cfg["clear_comment"] = self.clear_comment.get()
        cfg["seed"] = self.random_seed.get()
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Json Config", "*.json")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
            self.log(f"Config exported / 配置导出成功：{path}")

    def load_config(self):
        path = filedialog.askopenfilename(filetypes=[("Json Config", "*.json")])
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            for k, val in cfg.items():
                if k in self.obf_options:
                    self.obf_options[k]["var"].set(val)
            self.clear_comment.set(cfg.get("clear_comment", True))
            self.random_seed.set(cfg.get("seed", ""))
            self.log(f"Config loaded / 配置加载完成：{path}")

    # 日志保存
    def save_log_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Log", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.log(f"Log saved / 日志保存至：{path}")

    # 快捷功能：全选/取消/默认
    def enable_all(self):
        for data in self.obf_options.values():
            data["var"].set(True)
        self.log("[Info] All obfuscation functions enabled / 已开启全部混淆策略")

    def disable_all(self):
        for data in self.obf_options.values():
            data["var"].set(False)
        self.log("[Warning] All obfuscation functions disabled / 已关闭所有混淆功能")

    def load_default(self):
        default_state = {
            "string_encrypt": True,
            "num_encrypt": True,
            "rename_var": True,
            "rename_func": True,
            "dead_code": True,
            "fake_except": True,
            "control_flat": True,
            "remove_annot": True,
            "string_xor": True,
            "random_indent": False,
        }
        for k, v in default_state.items():
            self.obf_options[k]["var"].set(v)
        self.clear_comment.set(True)
        self.random_seed.set("")
        self.log("[Info] Load default recommended preset / 已加载默认推荐混淆配置")

    # 文件选择
    def select_input(self):
        path = filedialog.askopenfilename(
            title="Select Source Python File | 选择待混淆py源码",
            filetypes=[("Python Script", "*.py"), ("All Files", "*.*")]
        )
        if path:
            self.input_path.set(path)
            self.auto_fill_output()
            self.load_raw_preview()
            self.log(f"Selected source file / 选中源码：{path}")

    def select_batch(self):
        paths = filedialog.askopenfilenames(filetypes=[("Python Script", "*.py")])
        if paths:
            self.batch_files = list(paths)
            self.log(f"Batch selected count / 批量选中文件数量：{len(self.batch_files)}")

    def select_output(self):
        path = filedialog.asksaveasfilename(
            title="Save Obfuscated File | 保存混淆后文件",
            defaultextension=".py",
            filetypes=[("Python Script", "*.py"), ("All Files", "*.*")]
        )
        if path:
            self.output_path.set(path)
            self.log(f"Output path set / 设置输出路径：{path}")

    def auto_fill_output(self):
        src = self.input_path.get().strip()
        if not src or not os.path.exists(src):
            return
        dirname, fname = os.path.split(src)
        new_name = f"obf_{fname}"
        out = os.path.join(dirname, new_name)
        self.output_path.set(out)

    # 加载原始代码预览
    def load_raw_preview(self):
        p = self.input_path.get()
        if not os.path.exists(p):
            return
        with open(p, "r", encoding="utf-8") as f:
            code = f.read()
        self.raw_preview.delete(1.0, tk.END)
        self.raw_preview.insert(tk.END, code[:3000])
        self.raw_md5 = self.calc_md5(code)

    # MD5哈希计算
    def calc_md5(self, text):
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    # 日志打印
    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        self.log("[Info] Log cleared / 日志已清空")

    # 帮助弹窗
    def show_help(self):
        help_content = """
=== Python Obfuscator Help / 工具功能说明 ===
1. String Hex Encrypt: Convert all string to hex literal
   字符串加密：将全部明文转为十六进制字符
2. Number Encrypt: Disguise constant numbers by calculation
   数字加密：常量数字通过运算伪装
3. Rename Var/Func: Random garbled name for identifiers
   变量/函数重命名：标识符替换无意义乱码
4. Dead Junk Code: Insert unreachable useless code blocks
   垃圾代码：大量无法执行的虚假分支
5. Fake Exception: Add meaningless try-except trap
   虚假异常：无意义异常捕获干扰逆向
6. Control Flow Flatten: Break original code structure
   控制流扁平化：打乱代码原有逻辑结构
7. String XOR: Secondary XOR encryption for strings
   字符串异或：二次加密字符串内容
8. Random Indent: Disturb code indent format
   随机缩进：轻微打乱代码缩进格式
Extra Feature:
- Batch Obfuscate: Multi py file one-click process 批量混淆
- Dark Theme: Eye-care dark interface 深色护眼模式
- Config Save/Load: Save your obfuscation preset 配置导出导入
- Code Preview: Real-time raw & obfuscated code view 双栏代码预览
- MD5 Checksum: Verify code modification 哈希校验文件改动
- Drag & Drop: Direct drag py into window 拖拽加载文件
"""
        messagebox.showinfo("Help / 功能说明", help_content)

    # EXE打包命令弹窗
    def show_pack_cmd(self):
        cmd = '''# 混淆后打包单文件exe命令
pip install pyinstaller
pyinstaller -F -w obf_target.py
# -F 单文件，-w 无黑窗口，移除-w保留控制台
'''
        messagebox.showinfo("PyInstaller Command / EXE打包命令", cmd)

    # 代码差异对比
    def show_diff(self):
        raw = self.raw_preview.get(1.0, tk.END).strip()
        obf = self.obf_preview.get(1.0, tk.END).strip()
        if not raw or not obf:
            messagebox.showwarning("Tip / 提示", "Run obfuscate first to generate compare content\n请先执行混淆生成对比代码")
            return
        diff_win = tk.Toplevel(self.root)
        diff_win.title("Diff Compare / 混淆前后差异")
        diff_text = scrolledtext.ScrolledText(diff_win, width=100, height=30)
        diff_text.pack()
        diff_text.insert(tk.END, "===== RAW CODE / 原始代码 =====\n")
        diff_text.insert(tk.END, raw[:2000])
        diff_text.insert(tk.END, "\n\n===== OBFUSCATED CODE / 混淆代码 =====\n")
        diff_text.insert(tk.END, obf[:2000])

    # 单文件混淆核心逻辑
    def obfuscate_single(self, source_code):
        conf = ObfuscationConfig.all_enabled()
        disable_list = []
        for key, data in self.obf_options.items():
            if not data["var"].get():
                disable_list.append(key)
        for item in disable_list:
            conf = conf.without(item)
        # 清空注释
        if self.clear_comment.get():
            import re
            source_code = re.sub(r'#.*', '', source_code)
            source_code = re.sub(r'""".*?"""', '', source_code, flags=re.DOTALL)
            source_code = re.sub(r"'''.*?'''", '', source_code, flags=re.DOTALL)
        obfuscator = Obfuscator(config=conf)
        if self.random_seed.get().strip():
            obfuscator.set_seed(int(self.random_seed.get()))
        obfuscated_source = obfuscator.obfuscate(source_code)
        return obfuscated_source

    # 单文件混淆入口
    def run_obfuscate(self):
        if not HAS_OBF:
            messagebox.showerror("Error / 错误", "Please install python-obfuscator first\n请先安装混淆依赖库")
            return
        in_path = self.input_path.get().strip()
        out_path = self.output_path.get().strip()
        if not in_path:
            messagebox.showerror("Error / 错误", "Please select source file first!\n请先选择待混淆Python源码！")
            return
        if not out_path:
            messagebox.showerror("Error / 错误", "Please set output save path!\n请设置混淆文件输出路径！")
            return
        self.log("="*60)
        self.log("[Start] Single file obfuscation task / 开始单文件混淆任务")
        self.progress_bar["value"] = 10
        try:
            self.log("[Step1] Read source file with UTF-8 encoding / 读取源码文件")
            with open(in_path, "r", encoding="utf-8") as f:
                source_code = f.read()
            self.log(f"Source code length / 源码字符长度：{len(source_code)}")
            self.progress_bar["value"] = 30
            self.log("[Step2] Running obfuscator engine / 执行混淆引擎处理")
            obfuscated_source = self.obfuscate_single(source_code)
            self.obf_md5 = self.calc_md5(obfuscated_source)
            self.obf_preview.delete(1.0, tk.END)
            self.obf_preview.insert(tk.END, obfuscated_source[:3000])
            self.log(f"Obfuscated code length / 混淆后字符长度：{len(obfuscated_source)}")
            self.log(f"Raw MD5 / 原始哈希：{self.raw_md5}")
            self.log(f"Obfuscated MD5 / 混淆哈希：{self.obf_md5}")
            self.progress_bar["value"] = 70
            self.log("[Step3] Write obfuscated code to output file / 写入混淆结果")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(obfuscated_source)
            self.progress_bar["value"] = 100
            self.log("✅ Obfuscation Complete! / 高强度混淆任务完成！")
            self.log(f"Output File Path / 输出文件：{out_path}")
            messagebox.showinfo("Success / 完成", f"Obfuscation finished successfully!\n混淆完成！\nSave Path：{out_path}")
        except Exception as e:
            err_msg = f"[Error] Obfuscate failed / 混淆执行异常：{str(e)}"
            self.log(err_msg)
            messagebox.showerror("Run Error / 运行报错", err_msg)
        self.progress_bar["value"] = 0

    # 批量混淆
    def run_batch(self):
        if not HAS_OBF:
            messagebox.showerror("Error / 错误", "Please install python-obfuscator first\n请先安装混淆依赖库")
            return
        if len(self.batch_files) == 0:
            messagebox.showwarning("Tip / 提示", "No batch files selected\n未选择批量文件，请点击【Batch Select】多选py文件")
            return
        total = len(self.batch_files)
        self.log(f"===== Batch Obfuscate Start, total {total} files / 批量混淆开始，共{total}个文件 =====")
        for idx, src_path in enumerate(self.batch_files):
            try:
                self.progress_bar["value"] = int((idx / total)*100)
                dirname, fname = os.path.split(src_path)
                out_name = f"obf_{fname}"
                out_path = os.path.join(dirname, out_name)
                with open(src_path, "r", encoding="utf-8") as f:
                    code = f.read()
                obf_code = self.obfuscate_single(code)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(obf_code)
                self.log(f"[{idx+1}/{total}] Success: {fname} -> {out_name}")
            except Exception as e:
                self.log(f"[{idx+1}/{total}] Fail {src_path}: {str(e)}")
        self.progress_bar["value"] = 100
        self.log("✅ All batch task finished / 全部批量混淆执行完毕")
        messagebox.showinfo("Batch Complete / 批量完成", f"Batch process finished!\nTotal: {total} files")
        self.progress_bar["value"] = 0

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PyObfuscatorGUI(root)
    root.mainloop()