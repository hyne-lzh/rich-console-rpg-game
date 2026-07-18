# -*- coding:utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from python_obfuscator import Obfuscator, ObfuscationConfig

class PyObfuscatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Obfuscator | Python代码高强度混淆工具")
        self.root.geometry("980x720")
        self.root.resizable(True, True)

        # 全局变量
        self.input_path = tk.StringVar(value="")
        self.output_path = tk.StringVar(value="")
        self.log_text = None
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

    def build_ui(self):
        # 1. 文件选择区域
        file_frame = tk.LabelFrame(self.root, text="File Select | 文件选择")
        file_frame.pack(fill="x", padx=10, pady=6)

        # 输入文件
        tk.Label(file_frame, text="Source File | 待混淆源码：").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        tk.Entry(file_frame, textvariable=self.input_path, width=55).grid(row=0, column=1, padx=5)
        tk.Button(file_frame, text="Browse | 浏览", command=self.select_input).grid(row=0, column=2, padx=4)

        # 输出文件
        tk.Label(file_frame, text="Output File | 混淆后输出：").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        tk.Entry(file_frame, textvariable=self.output_path, width=55).grid(row=1, column=1, padx=5)
        tk.Button(file_frame, text="Browse | 浏览", command=self.select_output).grid(row=1, column=2, padx=4)

        # 2. 混淆功能勾选面板
        opt_frame = tk.LabelFrame(self.root, text="Obfuscation Options | 混淆功能配置")
        opt_frame.pack(fill="x", padx=10, pady=6)
        row_idx = 0
        col_idx = 0
        for key, data in self.obf_options.items():
            cb = tk.Checkbutton(opt_frame, text=data["text"], variable=data["var"])
            cb.grid(row=row_idx, column=col_idx, sticky="w", padx=8, pady=3)
            col_idx += 1
            if col_idx >= 2:
                col_idx = 0
                row_idx += 1

        # 快捷按钮：全选/取消全选
        btn_opt_frame = tk.Frame(opt_frame)
        btn_opt_frame.grid(row=row_idx+1, column=0, columnspan=2, pady=5)
        tk.Button(btn_opt_frame, text="Enable All / 全选开启", command=self.enable_all).grid(row=0, column=0, padx=6)
        tk.Button(btn_opt_frame, text="Disable All / 全部关闭", command=self.disable_all).grid(row=0, column=1, padx=6)
        tk.Button(btn_opt_frame, text="Default Preset / 默认推荐配置", command=self.load_default).grid(row=0, column=2, padx=6)

        # 3. 操作按钮区
        run_frame = tk.Frame(self.root)
        run_frame.pack(pady=8)
        tk.Button(run_frame, text="Start Obfuscate / 开始混淆", width=25, bg="#22aa22", fg="white", command=self.run_obfuscate).grid(row=0, column=0, padx=10)
        tk.Button(run_frame, text="Clear Log / 清空日志", width=25, command=self.clear_log).grid(row=0, column=1, padx=10)
        tk.Button(run_frame, text="Help Info / 功能说明", width=25, command=self.show_help).grid(row=0, column=2, padx=10)

        # 4. 运行日志框
        log_frame = tk.LabelFrame(self.root, text="Run Log | 运行日志")
        log_frame.pack(fill="both", expand=True, padx=10, pady=6)
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=4, pady=4)

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
        # 默认推荐配置
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
        self.log("[Info] Load default recommended preset / 已加载默认推荐混淆配置")

    # 文件选择
    def select_input(self):
        path = filedialog.askopenfilename(
            title="Select Source Python File | 选择待混淆py源码",
            filetypes=[("Python Script", "*.py"), ("All Files", "*.*")]
        )
        if path:
            self.input_path.set(path)
            self.log(f"Selected source file / 选中源码：{path}")

    def select_output(self):
        path = filedialog.asksaveasfilename(
            title="Save Obfuscated File | 保存混淆后文件",
            defaultextension=".py",
            filetypes=[("Python Script", "*.py"), ("All Files", "*.*")]
        )
        if path:
            self.output_path.set(path)
            self.log(f"Output path set / 设置输出路径：{path}")

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
"""
        messagebox.showinfo("Help / 功能说明", help_content)

    # 核心混淆执行
    def run_obfuscate(self):
        in_path = self.input_path.get().strip()
        out_path = self.output_path.get().strip()
        if not in_path:
            messagebox.showerror("Error / 错误", "Please select source file first!\n请先选择待混淆Python源码！")
            return
        if not out_path:
            messagebox.showerror("Error / 错误", "Please set output save path!\n请设置混淆文件输出路径！")
            return

        self.log("="*50)
        self.log("[Start] Start obfuscation task / 开始执行混淆任务")
        try:
            # 构建混淆配置
            conf = ObfuscationConfig.all_enabled()
            # 反向关闭未勾选功能
            disable_list = []
            for key, data in self.obf_options.items():
                if not data["var"].get():
                    disable_list.append(key)
            for item in disable_list:
                conf = conf.without(item)
            self.log(f"Disabled functions / 关闭的混淆模块：{disable_list if disable_list else 'None 无'}")

            # UTF8读取源码
            self.log("[Step1] Read source file with UTF-8 encoding / 读取源码文件")
            with open(in_path, "r", encoding="utf-8") as f:
                source_code = f.read()
            self.log(f"Source code length / 源码字符长度：{len(source_code)}")

            # 执行混淆
            self.log("[Step2] Running obfuscator engine / 执行混淆引擎处理")
            obfuscator = Obfuscator(config=conf)
            obfuscated_source = obfuscator.obfuscate(source_code)
            self.log(f"Obfuscated code length / 混淆后字符长度：{len(obfuscated_source)}")

            # 保存输出
            self.log("[Step3] Write obfuscated code to output file / 写入混淆结果")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(obfuscated_source)

            self.log("✅ Obfuscation Complete! / 高强度混淆任务完成！")
            self.log(f"Output File Path / 输出文件：{out_path}")
            messagebox.showinfo("Success / 完成", f"Obfuscation finished successfully!\n混淆完成！\nSave Path：{out_path}")
        except Exception as e:
            err_msg = f"[Error] Obfuscate failed / 混淆执行异常：{str(e)}"
            self.log(err_msg)
            messagebox.showerror("Run Error / 运行报错", err_msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = PyObfuscatorGUI(root)
    root.mainloop()