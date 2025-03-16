import tkinter as tk
from tkinter import messagebox
from fuzzywuzzy import fuzz  # 导入 FuzzyWuzzy 库

# 类别和计数的初始化
key_scene = ["路口", "红绿灯", "上匝道", "汇入主路", "跟车", "大曲率弯道", "小曲率弯道", "专用道", "直道"]
key_que = ["偏航", "绕行", "危险向左变道", "危险向右变道", "加塞", "刹不住"]

classifier_template = {
    "场景和问题": {},
    "场景": {},
    "问题": {},
    "其他": {'count': 0, 'descriptions': []}  # 确保初始结构
}

# 历史记录
history = []


# 聚合相似问题函数
def aggregate_similar_questions(questions):
    aggregated = {}

    for question in questions:
        added = False
        for key in aggregated.keys():
            if fuzz.partial_ratio(key, question) >= 80:  # 阈值可以调整
                aggregated[key]["count"] += 1
                aggregated[key]["descriptions"].append(question)
                added = True
                break
        if not added:
            aggregated[question] = {"count": 1, "descriptions": [question]}

    return aggregated


# 分类函数
def classify_text(raw_data):
    processed_data = []
    processed_scene = []
    processed_que = []

    for entry in raw_data.splitlines():
        if entry.strip():  # 检查非空行
            processed_entry = entry.split(' ', 1)[1]  # 只保留数字后面的部分
            processed_data.append(processed_entry)

    for i in processed_data:
        split_word = i.split("，", 1)
        processed_scene.append(split_word[0])
        processed_que.append(split_word[1])

    classifier = classifier_template.copy()
    scene_count = {scene: 0 for scene in key_scene}
    que_count = {que: 0 for que in key_que}

    # 分类输入的问题
    for i in range(len(processed_data)):
        description = processed_data[i]
        scene_found = False
        que_found = False
        scene_key = None
        que_key = None

        # 使用模糊匹配进行场景查找
        for scene in key_scene:
            if fuzz.partial_ratio(scene, processed_scene[i]) >= 80:  # 设置模糊匹配的阈值
                scene_found = True
                scene_key = scene
                scene_count[scene] += 1
                break

        # 使用模糊匹配进行问题查找
        for que in key_que:
            if fuzz.partial_ratio(que, processed_que[i]) >= 80:  # 设置模糊匹配的阈值
                que_found = True
                que_key = que
                que_count[que] += 1
                break

        if scene_found and que_found:
            key = (scene_key, que_key)
            if key not in classifier["场景和问题"]:
                classifier["场景和问题"][key] = {
                    "count": 0,
                    "descriptions": []
                }
            classifier["场景和问题"][key]["count"] += 1
            classifier["场景和问题"][key]["descriptions"].append(description)

        elif scene_found:
            if scene_key not in classifier["场景"]:
                classifier["场景"][scene_key] = {
                    "count": 0,
                    "descriptions": []
                }
            classifier["场景"][scene_key]["count"] += 1
            classifier["场景"][scene_key]["descriptions"].append(description)

        elif que_found:
            # 尝试聚合相似的问题
            if que_key not in classifier["问题"]:
                classifier["问题"][que_key] = {
                    "count": 0,
                    "descriptions": []
                }
            classifier["问题"][que_key]["count"] += 1
            classifier["问题"][que_key]["descriptions"].append(description)

        else:
            classifier["其他"]['count'] += 1
            classifier["其他"]['descriptions'].append(description)

    # 聚合相似问题
    if "问题" in classifier:
        classifier["问题"] = aggregate_similar_questions(classifier["问题"].keys())

    return classifier, scene_count, que_count


# 按钮点击事件
def on_classify_button_click():
    raw_data = input_text.get("1.0", 'end-1c')
    classifier, scene_count, que_count = classify_text(raw_data)

    # 显示结果
    result_text.delete("1.0", tk.END)  # 清空之前的结果
    result_text.insert(tk.END, "分类结果:\n")

    # 添加标签定义
    result_text.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
    result_text.tag_configure("large", font=("TkDefaultFont", 12, "bold"))
    result_text.tag_configure("highlight", font=("TkDefaultFont", 10, "italic"), foreground="blue")

    for category, items in classifier.items():
        result_text.insert(tk.END, f"{category}:\n", 'large')
        if isinstance(items, dict):
            if category == "其他":
                result_text.insert(tk.END, f"  - 出现 {items['count']} 次\n")
                for desc in items['descriptions']:
                    result_text.insert(tk.END, f"    - 描述: {desc}\n")
            else:
                for key, value in items.items():
                    count = value['count']
                    descriptions = value['descriptions']
                    scene, problem = key if isinstance(key, tuple) else (key, None)
                    result_text.insert(tk.END, f"  - 场景: '{scene}' \n")
                    result_text.insert(tk.END, f"    问题: ", 'highlight')
                    result_text.insert(tk.END, f"'{problem}'", 'bold')  # 使问题部分加粗
                    result_text.insert(tk.END, f" 出现 {count} 次\n")
                    result_text.insert(tk.END, "    描述:\n")

                    if descriptions:  # 确保有描述后再添加
                        for desc in descriptions:
                            result_text.insert(tk.END, f"      - {desc}\n")
                    result_text.insert(tk.END, "    " + "-" * 46 + "\n\n")  # 明确的分隔和空行

        result_text.insert(tk.END, "\n")  # 空白行

    # 添加历史记录
    history.append((raw_data, classifier))
    history_label.config(text=f"历史记录: {len(history)} 条")

    # 打印统计结果
    result_text.insert(tk.END, "\n统计结果:\n")
    result_text.insert(tk.END, "场景关键词次数:\n")
    for scene, count in scene_count.items():
        result_text.insert(tk.END, f"  {scene}: {count}\n")

    result_text.insert(tk.END, "问题关键词次数:\n")
    for que, count in que_count.items():
        result_text.insert(tk.END, f"  {que}: {count}\n")


def update_keywords():
    global key_scene, key_que
    key_scene_input = scene_keywords_text.get("1.0", 'end-1c').strip().splitlines()
    key_que_input = question_keywords_text.get("1.0", 'end-1c').strip().splitlines()

    key_scene = [kw for kw in key_scene_input if kw]
    key_que = [qw for qw in key_que_input if qw]

    messagebox.showinfo("成功", "关键词已更新！")


# 创建GUI
root = tk.Tk()
root.title("问题分类工具")

# 主容器
main_frame = tk.Frame(root, padx=10, pady=12)
main_frame.pack()

# 输入和结果的Frame
input_frame = tk.Frame(main_frame)
input_frame.pack(side=tk.LEFT, padx=5)

result_frame = tk.Frame(main_frame)
result_frame.pack(side=tk.RIGHT, padx=5)

# 输入区域
input_label = tk.Label(input_frame, text="请输入问题:")
input_label.pack()

input_text = tk.Text(input_frame, height=15, width=50)
input_text.pack()

classify_button = tk.Button(input_frame, text="分类", command=on_classify_button_click)
classify_button.pack(pady=10)

# 更新关键词区域
update_label = tk.Label(input_frame, text="动态更新关键词:")
update_label.pack(pady=(10, 0))

scene_keywords_label = tk.Label(input_frame, text="场景关键词：")
scene_keywords_label.pack()
scene_keywords_text = tk.Text(input_frame, height=5, width=50)
scene_keywords_text.pack(pady=(0, 10))

question_keywords_label = tk.Label(input_frame, text="问题关键词：")
question_keywords_label.pack()
question_keywords_text = tk.Text(input_frame, height=5, width=50)
question_keywords_text.pack(pady=(0, 10))

update_button = tk.Button(input_frame, text="更新关键词", command=update_keywords)
update_button.pack(pady=10)

# 结果区域
result_label = tk.Label(result_frame, text="分类结果:")
result_label.pack()

# 扩大结果文本框的高度
result_text = tk.Text(result_frame, height=40, width=50)  # 修改了高度
result_text.pack()

# 历史记录标签
history_label = tk.Label(main_frame, text="历史记录: 0 条")
history_label.pack(pady=(0, 0))  # 调整向上移动

# 运行主循环
root.mainloop()
