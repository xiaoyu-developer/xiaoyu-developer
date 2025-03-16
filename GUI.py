import tkinter as tk
from tkinter import scrolledtext


def process_question():
    # 获取输入框的内容并处理
    question = question_entry.get("1.0", tk.END).strip()
    # 示例处理逻辑：在内容前后添加说明
    processed_question = f"处理后的问题:\n{question}" if question else "请输入有效问题！"
    # 将处理后的问题设置到输出框中
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, processed_question)


# 创建主窗口
root = tk.Tk()
root.title("问题处理器")
root.geometry("800x400")  # 设置窗口大小
root.resizable(False, False)

# 创建主框架
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# 左侧输入框部分
left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=10)

question_label = tk.Label(left_frame, text="请输入问题：", font=("Arial", 14))
question_label.pack(anchor="nw", pady=5)

question_entry = scrolledtext.ScrolledText(left_frame, width=38, height=15, font=("Arial", 12))
question_entry.pack(fill=tk.BOTH, expand=True, pady=5)

# 中间按钮部分
button_frame = tk.Frame(main_frame)
button_frame.grid(row=0, column=1, sticky="ns", padx=5)  # 中间框架上下填充

process_button = tk.Button(button_frame, text="处理", command=process_question, font=("Arial", 12), width=10)
process_button.pack(pady=150)  # 上下居中按钮

# 右侧输出框部分
right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=10)

output_label = tk.Label(right_frame, text="处理后的问题：", font=("Arial", 14))
output_label.pack(anchor="nw", pady=5)

output_text = scrolledtext.ScrolledText(right_frame, width=38, height=15, font=("Arial", 12), state=tk.NORMAL)
output_text.pack(fill=tk.BOTH, expand=True, pady=5)

# 设置行和列的权重，以便在窗口调整大小时自动扩展
main_frame.columnconfigure(0, weight=1)  # 左侧输入框
main_frame.columnconfigure(1, weight=0)  # 中间按钮
main_frame.columnconfigure(2, weight=1)  # 右侧输出框
main_frame.rowconfigure(0, weight=1)  # 只有一行

# 启动主循环
root.mainloop()
