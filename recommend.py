import csv

foods = []
with open('food_data.csv', encoding='utf-8-sig') as f:  # 加上 utf-8-sig 解决 BOM 问题
    reader = csv.DictReader(f)
    print("列名检测：", reader.fieldnames)  # 打印看看列名
    for row in reader:
        foods.append(row)

# 用户输入
user_mood = input("你现在的心情是？（解压/开心/自律/普通/赶时间）：")
user_tag = input("你想吃什么口味？（辣/清淡/油炸/健康等）：")
user_time = input("你希望出餐时间？（快/中/慢）：")

# 推荐逻辑
def calculate_score(food):
    score = 0
    
    if user_mood in food['mood']:
        score += 3
        
    if user_tag in food['tags']:
        score += 2
        
    if user_time == food['time']:
        score += 2
        
    return score

# 排序推荐
foods.sort(key=calculate_score, reverse=True)

# 输出结果
print("\n为你推荐：")
for food in foods[:3]:
    print(f"{food['name']}（价格：{food['price']}元）")