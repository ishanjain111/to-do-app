from flask import Blueprint, render_template, request, url_for, redirect, current_app
import uuid
import datetime

pages = Blueprint("to-do", __name__, template_folder="templates", static_folder="static")


@pages.context_processor
def add_cal_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    
    return {"date_range": date_range}

def today_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)

@pages.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = today_at_midnight()

    habit_on_date = current_app.db.todo.find({"added": {"$eq": selected_date}})
    
    completions = [
        habit['habit']
        for habit in current_app.db.completions.find({"date": selected_date})
    ]

    return render_template("index.html", habits=habit_on_date, title="To-Do App Home", selected_date=selected_date, completions=completions)

@pages.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        selected_date = request.form.get("date")
        if request.form:
            current_app.db.todo.insert_one(
                {
                    "_id": uuid.uuid4().hex,
                    "added": selected_date,
                    "name": request.form.get("habit")
                }
            )
    return render_template("add.html", title="To-Do tracker -- Add Item", selected_date=datetime.datetime.today())

@pages.post("/complete")
def complete():
    date_string = request.form.get("date")
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_string)
    current_app.db.completions.insert_one({"date": date, "habit": habit})

    return redirect(url_for("to-do.index", date=date_string))

