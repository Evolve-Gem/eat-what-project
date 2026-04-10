from flask import Flask, render_template, request
from recommend2 import load_food_data, recommend_food  # 调用你现有逻辑

app = Flask(__name__)
foods = load_food_data("food_data.csv")  # 加载一次 CSV

# 首页路由
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# 推荐路由
@app.route("/recommend", methods=["POST"])
def recommend():
    # 获取表单数据
    mood = request.form.get("mood")
    tastes = request.form.getlist("taste")  # 多选返回列表
    time = request.form.get("time")

    # 构造用户输入字典
    user_input = {"mood": mood, "taste": tastes, "time": time}

    # 调用原来的推荐逻辑
    recommendations = recommend_food(foods, user_input)

    return render_template("index.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)