import csv

# 读取 CSV 数据
def load_food_data(file_path):
    foods = []
    with open(file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 清理 name 和 tags
            row['name'] = row['name'].strip()
            row['tags'] = [tag.strip() for tag in row['tags'].split('|')]  # CSV 里用 | 分隔
            row['mood'] = row['mood'].strip()
            row['time'] = row['time'].strip()
            row['price'] = row['price'].strip()
            foods.append(row)
    return foods

# 计算匹配分数
def calculate_score(food, user_input):
    score = 0
    reasons = []

    # 口味匹配
    for taste in user_input['taste']:
        if taste in food['tags']:
            score += 2
            reasons.append(f"口味匹配：{taste}")

    # 心情匹配
    if user_input['mood'] == food['mood']:
        score += 2
        reasons.append(f"心情匹配：{food['mood']}")

    # 出餐速度匹配
    if user_input['time'] == food['time']:
        score += 1
        reasons.append(f"出餐速度匹配：{food['time']}")

    return score, reasons

# 用户输入校验
def get_user_input():
    valid_moods = ['解压', '开心', '自律', '普通', '赶时间']
    valid_tastes = ['辣', '清淡', '油炸', '健康', '家常', '健身', '快餐', '重口']
    valid_times = ['快', '中', '慢']

    # 心情输入
    while True:
        mood = input(f"请选择你的心情（{'/'.join(valid_moods)}）：").strip()
        if mood in valid_moods:
            break
        print("输入不合法，请重新选择心情。")

    # 口味输入
    while True:
        taste_input = input(f"请选择口味（可多选，用逗号分隔，如{','.join(valid_tastes)}）：").strip()
        tastes = [t.strip() for t in taste_input.split(',') if t.strip()]
        invalid = [t for t in tastes if t not in valid_tastes]
        if not tastes:
            print("请至少选择一个口味。")
        elif invalid:
            print(f"无效口味：{','.join(invalid)}，请重新选择。")
        else:
            break

    # 出餐时间输入
    while True:
        time = input(f"请选择出餐时间（{'/'.join(valid_times)}）：").strip()
        if time in valid_times:
            break
        print("输入不合法，请重新选择出餐时间。")

    return {'mood': mood, 'taste': tastes, 'time': time}

# 主推荐逻辑
def recommend_food(foods, user_input):
    scored_foods = []

    for food in foods:
        score, reasons = calculate_score(food, user_input)
        scored_foods.append({
            'name': food['name'],
            'price': food['price'],
            'score': score,
            'reasons': reasons
        })

    # 按匹配分数排序
    scored_foods.sort(key=lambda x: x['score'], reverse=True)
    return scored_foods[:3]

# 打印推荐结果
def print_recommendations(recommendations):
    print("\n🍽️ 推荐结果：")
    for i, food in enumerate(recommendations, start=1):
        reason_str = ' + '.join(food['reasons']) if food['reasons'] else "无特别匹配理由"
        print(f"{i}. {food['name']}（价格：{food['price']}元）——匹配分数：{food['score']}，理由：{reason_str}")

if __name__ == "__main__":
    file_path = "food_data.csv"
    foods = load_food_data(file_path)
    user_input = get_user_input()
    recommendations = recommend_food(foods, user_input)
    print_recommendations(recommendations)