import numpy as np
import random
from tqdm import tqdm

def strict_portion(num_A,num_B,selection_n,loc_A, scale_A, loc_B, scale_B):
    # 生成正态分布分数
    #np.random.seed(42)  # 设置随机种子，确保结果可复现
    scores_A = np.random.normal(loc=loc_A, scale=scale_A, size=num_A)  # A人分数，均值为70，标准差为10
    scores_B = np.random.normal(loc=loc_B, scale=scale_B, size=num_B)  # B人分数，均值为60，标准差为15

    # 创建A人和B人的标识
    people_A = [('A', score) for score in scores_A]
    people_B = [('B', score) for score in scores_B]

    # 混合A人和B人
    all_people = people_A + people_B

    # 随机挑选200人
    random.shuffle(all_people)
    selected = all_people[:selection_n]

    # 按分数排序
    selected.sort(key=lambda x: x[1], reverse=True)

    # 从200人中筛选出分数最高的4个A和1个B
    result_A = []
    result_B = []
    for person in selected:
        if person[0] == 'A' and len(result_A) < 4:
            result_A.append(person)
        elif person[0] == 'B' and len(result_B) < 1:
            result_B.append(person)
        if len(result_A) == 4 and len(result_B) == 1:
            break

    # 输出结果
    # print("分数最高的4个A：")
    # for person in result_A:
    #     print(f"类型: {person[0]}, 分数: {person[1]:.2f}")
    #
    # print("\n分数最高的1个B：")
    # for person in result_B:
    #     print(f"类型: {person[0]}, 分数: {person[1]:.2f}")

    # print(scores_A.mean())
    # print(scores_B.mean())

    return result_A, result_B


def monte_carlo_simulation(num_trials,
                           num_A,num_B,
                           selection_n = 200,
                           loc_A = 70, scale_A = 10,
                           loc_B = 70, scale_B = 10):
    differences = []

    np.random.seed(25)

    for _ in tqdm(range(num_trials), desc="Monte Carlo Simulation Progress"):
        result_A, result_B = strict_portion(num_A,num_B,selection_n,loc_A, scale_A, loc_B, scale_B)
        avg_score_A = np.mean([score for _, score in result_A])  # 计算result_A的平均分数
        score_B = result_B[0][1]  # result_B只有一个元素，取其分数
        difference = avg_score_A - score_B  # 计算差异
        differences.append(difference)

    avg_difference = np.mean(differences)  # 计算所有差异的平均值
    return avg_difference

# 运行蒙特卡洛实验
num_trials = 100000
num_A = 10000
num_B = 1000
avg_difference = monte_carlo_simulation(num_trials,num_A, num_B)
print(f"经过{num_trials}次蒙特卡洛实验，result_A平均分数与result_B分数的平均差异为：{avg_difference:.4f}")