# -*- coding:utf-8 -*-
from python_obfuscator import Obfuscator, ObfuscationConfig

# 1. 加载全部混淆策略（默认所有强化功能全部开启，无需手动赋值）
# 若需要关闭某一项，使用 .without("混淆器名称")，示例：
# conf = ObfuscationConfig.all_enabled().without("dead_code_injector")
conf = ObfuscationConfig.all_enabled()

# 2. UTF-8读取源码，彻底解决GBK编码报错
with open("test2.py", "r", encoding="utf-8") as f:
    source_code = f.read()

# 3. 执行混淆
obfuscator = Obfuscator(config=conf)
obfuscated_source = obfuscator.obfuscate(source_code)

# 4. UTF-8保存混淆文件
output_file = "obf_test2.py"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(obfuscated_source)

print("✅ 高强度混淆完成！输出文件：", output_file)
print("已启用全部混淆策略：")
print("- 字符串十六进制加密、数字常量加密")
print("- 全局/局部变量、函数名随机乱码重命名")
print("- 插入大量无效垃圾代码、虚假异常分支")
print("- 控制流扁平化、删除全部类型注解")