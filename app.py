from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"  # needed for sessions

# ---------------------------------------------------------
# ADMIN CREDENTIALS (prototype only)
# In a real deployment these would be hashed and stored in a
# database or environment variables, not hardcoded like this.
# ---------------------------------------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "suwasetha123"

# In-memory "database" for the demo/prototype.
# For a real system this would be replaced with a proper database (e.g. SQLite/MySQL).
patients = []

# ---------------------------------------------------------
# RULE-BASED TRIAGE LOGIC
# This is the "brain" of the prototype. Each incoming symptom
# description is checked against keyword lists to decide urgency.
# You can expand these lists based on end-user (nurse/doctor) feedback.
# ---------------------------------------------------------
HIGH_KEYWORDS = [
    "chest pain", "difficulty breathing", "shortness of breath",
    "unconscious", "unresponsive", "severe bleeding", "stroke",
    "seizure", "heart attack", "not breathing"
]

MEDIUM_KEYWORDS = [
    "high fever", "vomiting", "fracture", "broken bone",
    "severe pain", "dehydration", "allergic reaction", "burn"
]

LOW_KEYWORDS = [
    "mild cough", "cold", "headache", "sore throat",
    "minor cut", "rash", "mild fever"
]


def score_symptoms(text):
    """
    Takes the patient's typed symptom description and returns:
      - a numeric score (used for sorting the queue)
      - a human-readable priority label (shown on the dashboard)
    Rule-based keyword matching is used here instead of a full ML model,
    since a lightweight, explainable approach is more practical and safer
    for a hospital triage prototype at this stage.
    """
    text = text.lower()

    for kw in HIGH_KEYWORDS:
        if kw in text:
            return 3, "High"

    for kw in MEDIUM_KEYWORDS:
        if kw in text:
            return 2, "Medium"

    for kw in LOW_KEYWORDS:
        if kw in text:
            return 1, "Low"

    # Default fallback if no keyword matches - flagged for manual review
    return 1, "Low (Unmatched - please review)"


# ---------------------------------------------------------
# LOGIN PROTECTION
# ---------------------------------------------------------
def login_required(f):
    """Decorator that blocks access to a route unless the admin is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    """Admin login page."""
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """Logs the admin out."""
    session.pop("logged_in", None)
    return redirect(url_for("login"))


# ---------------------------------------------------------
# PATIENT-FACING ROUTES (public, no login needed)
# ---------------------------------------------------------
@app.route("/")
def index():
    """Patient-facing symptom entry form."""
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    """Handles form submission, scores the symptoms, and adds to the queue."""
    name = request.form.get("name", "").strip()
    symptoms = request.form.get("symptoms", "").strip()

    if not name or not symptoms:
        return redirect(url_for("index"))

    score, priority = score_symptoms(symptoms)

    patients.append({
        "name": name,
        "symptoms": symptoms,
        "score": score,
        "priority": priority,
        "time": datetime.now().strftime("%H:%M:%S"),
        "timestamp": datetime.now()
    })

    return redirect(url_for("index"))


# ---------------------------------------------------------
# STAFF-FACING ROUTES (protected, login required)
# ---------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    """Staff-facing dashboard: shows the queue sorted by urgency, then arrival time."""
    sorted_patients = sorted(patients, key=lambda p: (-p["score"], p["timestamp"]))
    return render_template("dashboard.html", patients=sorted_patients)


@app.route("/seen/<int:index>")
@login_required
def mark_seen(index):
    """Removes a patient from the queue once staff have attended to them."""
    sorted_patients = sorted(patients, key=lambda p: (-p["score"], p["timestamp"]))
    if 0 <= index < len(sorted_patients):
        patients.remove(sorted_patients[index])
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")