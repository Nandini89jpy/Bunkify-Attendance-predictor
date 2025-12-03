from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "bunkify123"

# Dummy Users
users = {
    "akansha": "1234",
    "student": "0000"
}

# History storage
history = []

def bunkify_predictor(current_attendance, total_classes, bunk_classes):
    current_percent = (current_attendance / total_classes) * 100
    new_attendance = current_attendance - bunk_classes
    new_percent = (new_attendance / total_classes) * 100

    # Teacher reactions with emojis
    if new_percent >= 85:
        decision = "😎 Teacher: Go enjoy, topper!"
    elif new_percent >= 75:
        decision = "🙂 Teacher: Okay…but don’t make it a habit!"
    elif 65 <= new_percent < 75:
        decision = "😠 Teacher: I'm watching you..."
    else:
        decision = "🤬 Teacher: Detention is coming!"

    return round(current_percent, 2), round(new_percent, 2), decision


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="❌ Invalid Credentials")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html", history=history)


@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect("/")

    current = int(request.form["attended"])
    total = int(request.form["total"])
    bunk = int(request.form["bunk"])

    current_percent, new_percent, decision = bunkify_predictor(current, total, bunk)

    record = {
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "current": current_percent,
        "after_bunk": new_percent,
        "decision": decision
    }

    history.append(record)

    return render_template(
        "result.html",
        current=current_percent,
        new=new_percent,
        decision=decision
    )


@app.route("/clear_history", methods=["POST"])
def clear_history():
    if "user" not in session:
        return redirect("/")
    history.clear()
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
