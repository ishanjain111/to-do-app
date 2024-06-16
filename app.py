from flask import Flask, render_template, request, url_for, redirect
from collections import defaultdict
import datetime

app = Flask(__name__)
habits = ["Test"]
completions = defaultdict(list)

@app.context_processor
def add_cal_date_range():
    def date_range(start: datetime.date):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    
    return {"date_range": date_range}

@app.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()
    return render_template("index.html", habits=habits, title="To-Do App Home", selected_date=selected_date, completions=completions[selected_date])

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        habit = request.form.get('habit')
        if habit:
            habits.append(habit)
    return render_template("add.html", title="To-Do tracker -- Add Item", selected_date=datetime.date.today())

@app.post("/complete")
def complete():
    date_string = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_string)
    
    if habit in completions[date]:
        completions[date].remove(habit)
    else:
        completions[date].append(habit)

    return redirect(url_for("index", date=date_string))

if __name__ == "__main__":
    app.run(debug=True)
