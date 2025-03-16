class QuestionClassifier:
    def __init__(self):
        # 定义场景和问题的关键词
        self.scenes_keywords = {
            "红绿灯": ["红灯", "绿灯"],
            "场景B": ["关键词B1", "关键词B2"],
            "场景C": ["关键词C1", "关键词C2"],
        }

        self.problems_keywords = {
            "横向": ["压线", "侧偏"],
            "问题类型2": ["问题关键词3", "问题关键词4"],
            "问题类型3": ["问题关键词5", "问题关键词6"],
        }

        # 创建分类结果的字典
        self.classifications = {
            "场景+问题": [],
            **{scene: [] for scene in self.scenes_keywords.keys()},
            **{problem: [] for problem in self.problems_keywords.keys()},
            "其他": []
        }

    def classify_question(self, question):
        found_scenes = []
        found_problems = []

        # 检查场景关键词
        for scene, keywords in self.scenes_keywords.items():
            if any(keyword in question for keyword in keywords):
                found_scenes.append(scene)

        # 检查问题关键词
        for problem, keywords in self.problems_keywords.items():
            if any(keyword in question for keyword in keywords):
                found_problems.append(problem)

        # 分类问题并附加问题描述
        if found_scenes and found_problems:
            for scene in found_scenes:
                for problem in found_problems:
                    self.classifications["场景+问题"].append((scene, problem, question))
        elif found_scenes:
            for scene in found_scenes:
                self.classifications[scene].append(question)
        elif found_problems:
            for problem in found_problems:
                self.classifications[problem].append(question)
        else:
            self.classifications["其他"].append(question)

    def display_results(self):
        print("分类结果:")
        for category, questions in self.classifications.items():
            print(f"{category}: {len(questions)}个问题")
            for question in questions:
                if isinstance(question, tuple):
                    print(f"  {question[0]} + {question[1]}: {question[2]}")
                else:
                    print(f"  {question}")


# 测试
if __name__ == "__main__":
    classifier = QuestionClassifier()

    # 输入测试问题
    test_questions = [
        "这是一个场景A的问题关键词1的描述",
        "路口红绿灯，这里是问题关键词2的描述",
        "没有任何相关关键词的问题",
        "场景A，问题关键词3的描述",
        "路口红绿灯，压线问题关键词5的描述",
        "路口红绿灯，关键词A2压线，问题关键词4的描述",
        "场景X，没有匹配的关键词",
        "问题关键词1没有场景的描述",
        "场景B，关键词B1，问题关键词3的描述"
    ]

    for question in test_questions:
        classifier.classify_question(question)

    classifier.display_results()