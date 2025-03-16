import tkinter as tk
from tkinter import messagebox

# 类别和计数的初始化
key_scene = ["路口", "红绿灯", "上匝道", "汇入主路", "跟车", "大曲率弯道", "小曲率弯道"]
key_que = ["偏航", "绕行", "危险向左变道", "危险向右变道", "加塞", "刹不住"]

classifier_template = {
    "场景和问题": {},
    "场景": {},
    "问题": {},
    "其他": {'count': 0, 'descriptions': []}  # 确保初始结构
}


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

        for scene in key_scene:
            if scene in processed_scene[i]:
                scene_found = True
                scene_key = scene
                scene_count[scene] += 1
                break

        for que in key_que:
            if que in processed_que[i]:
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

    return classifier, scene_count, que_count


# 按钮点击事件
def on_classify_button_click():
    raw_data = input_text.get("1.0", 'end-1c')
    classifier, scene_count, que_count = classify_text(raw_data)

    # 显示结果
    result_text.delete("1.0", tk.END)  # 清空之前的结果
    result_text.insert(tk.END, "分类结果:\n")
    for category, items in classifier.items():
        result_text.insert(tk.END, f"{category}:\n")
        if isinstance(items, dict):
            if category == "其他":
                result_text.insert(tk.END, f"  - 出现 {items['count']} 次\n")
                for desc in items['descriptions']:
                    result_text.insert(tk.END, f"    - {desc}\n")
            else:
                for key, value in items.items():
                    count = value['count']
                    descriptions = value['descriptions']
                    scene, problem = key if isinstance(key, tuple) else (key, None)
                    result_text.insert(tk.END, f"  - 场景: '{scene}' 问题: '{problem}' 出现 {count} 次\n")
                    result_text.insert(tk.END, "    描述:\n")
                    for desc in descriptions:
                        result_text.insert(tk.END, f"    - {desc}\n")
                    result_text.insert(tk.END, "    " + "-" * 40 + "\n")

    # 打印统计结果
    result_text.insert(tk.END, "\n统计结果:\n")
    result_text.insert(tk.END, "场景关键词次数:\n")
    for scene, count in scene_count.items():
        result_text.insert(tk.END, f"  {scene}: {count}\n")

    result_text.insert(tk.END, "问题关键词次数:\n")
    for que, count in que_count.items():
        result_text.insert(tk.END, f"  {que}: {count}\n")


# 创建GUI
root = tk.Tk()
root.title("问题分类工具")

# 输入框
input_label = tk.Label(root, text="请输入问题:")
input_label.pack()

input_text = tk.Text(root, height=15, width=50)
input_text.pack()

# 分类按钮
classify_button = tk.Button(root, text="分类", command=on_classify_button_click)
classify_button.pack()

# 结果框
result_label = tk.Label(root, text="分类结果:")
result_label.pack()

result_text = tk.Text(root, height=20, width=70)
result_text.pack()

# 运行主循环
root.mainloop()
