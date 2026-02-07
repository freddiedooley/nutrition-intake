# app.py
# Amateur Boxer Intake - Flask + SQLite (JSON storage)

from __future__ import annotations

import json
import sqlite3
import os
import base64
from datetime import datetime, timezone
from pathlib import Path
from functools import wraps
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, redirect, url_for, Response, abort, send_from_directory

from questions import FORM_SECTIONS, flatten_questions

# ------------------------------------------------------------
# App setup
# ------------------------------------------------------------

app = Flask(__name__)

# ---------------- Upload config ----------------

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}
MAX_FILE_SIZE_MB = 10

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ------------------------------------------------------------
# Coach Basic Auth (protect summary/export)
# ------------------------------------------------------------

COACH_USER = os.environ.get("COACH_USER", "coach")
COACH_PASS = os.environ.get("COACH_PASS", "change-me")

def check_basic_auth(auth_header: str | None) -> bool:
    if not auth_header or not auth_header.startswith("Basic "):
        return False

    try:
        encoded = auth_header.split(" ", 1)[1].strip()
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
    except Exception:
        return False

    return username == COACH_USER and password == COACH_PASS


def require_basic_auth(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not check_basic_auth(auth_header):
            return Response(
                "Authentication required",
                401,
                {"WWW-Authenticate": 'Basic realm="Coach Area"'},
            )
        return view_func(*args, **kwargs)
    return wrapper


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "intakes.sqlite3"

def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def save_uploaded_files(files, prefix: str, intake_id: int):
    saved = []

    for f in files:
        if not f or f.filename == "":
            continue

        if not allowed_file(f.filename):
            continue

        filename = secure_filename(f.filename)
        stored_name = f"{intake_id}_{prefix}_{filename}"

        path = os.path.join(app.config["UPLOAD_FOLDER"], stored_name)
        f.save(path)

        saved.append(stored_name)

    return saved


# ------------------------------------------------------------
# Database helpers
# ------------------------------------------------------------

def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS intakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at_utc TEXT NOT NULL,
                athlete_name TEXT,
                email TEXT,
                data_json TEXT NOT NULL
            );
            """
        )
        connection.commit()


def insert_intake(athlete_name: str | None, email: str | None, data: dict) -> int:
    created_at_utc = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO intakes (created_at_utc, athlete_name, email, data_json)
            VALUES (?, ?, ?, ?)
            """,
            (created_at_utc, athlete_name, email, json.dumps(data, ensure_ascii=False)),
        )
        connection.commit()
        return int(cursor.lastrowid)


def fetch_intake(intake_id: int) -> sqlite3.Row | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM intakes WHERE id = ?",
            (intake_id,),
        ).fetchone()
        return row


def fetch_all_intakes() -> list[sqlite3.Row]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM intakes ORDER BY id DESC"
        ).fetchall()
        return list(rows)


def update_payload(intake_id: int, payload: dict) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE intakes
            SET data_json = ?
            WHERE id = ?
            """,
            (json.dumps(payload), intake_id),
        )



# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@app.route("/uploads/<filename>")
@require_basic_auth
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


@app.route("/", methods=["GET"])
def form():
    # All questions (for rendering + validation hints)
    flat_questions = flatten_questions(FORM_SECTIONS)

    return render_template(
        "form.html",
        sections=FORM_SECTIONS,
        flat_questions=flat_questions,
    )


@app.route("/submit", methods=["POST"])
def submit():
    # Collect all form fields into a dict
    payload: dict[str, object] = {}

    # Basic “identity” helpers (optional)
    athlete_name = (request.form.get("athlete_name") or "").strip() or None
    email = (request.form.get("email") or "").strip() or None

    # Capture every posted key/value
    # For multi-select checkboxes, Flask uses getlist()
    for key in request.form.keys():
        if key in ("athlete_name", "email"):
            continue

        values = request.form.getlist(key)

        if len(values) == 1:
            payload[key] = values[0].strip()
        else:
            payload[key] = [v.strip() for v in values if v.strip()]

    # Add metadata
    payload["_meta"] = {
        "submitted_at_utc": datetime.now(timezone.utc).isoformat(),
        "user_agent": request.headers.get("User-Agent", ""),
    }

    intake_id = insert_intake(athlete_name, email, payload)
    
    # -------- Handle uploads AFTER intake exists --------

    food_files = request.files.getlist("food_diary_upload")
    supp_files = request.files.getlist("supplement_labels_upload")
    weigh_files = request.files.getlist("weighin_sheet_upload")

    food_saved = save_uploaded_files(food_files, "food", intake_id)
    supp_saved = save_uploaded_files(supp_files, "supp", intake_id)
    weigh_saved = save_uploaded_files(weigh_files, "weigh", intake_id)

    # Add filenames into payload
    payload["food_uploads"] = food_saved
    payload["supp_uploads"] = supp_saved
    payload["weigh_uploads"] = weigh_saved

    # Update database with new payload including filenames
    update_payload(intake_id, payload)


    return redirect(url_for("thankyou", intake_id=intake_id))


@app.route("/thankyou/<int:intake_id>", methods=["GET"])
def thankyou(intake_id: int):
    row = fetch_intake(intake_id)
    if row is None:
        return "Not found", 404
    return render_template("thankyou.html", intake_id=intake_id)


@app.route("/summary/<int:intake_id>", methods=["GET"])
@require_basic_auth
def summary(intake_id: int):
    row = fetch_intake(intake_id)
    if row is None:
        return "Not found", 404

    data = json.loads(row["data_json"])

    # A few useful computed flags (simple + practical)
    def to_float(value: str | None) -> float | None:
        if value is None:
            return None
        value = str(value).strip()
        if value == "":
            return None
        try:
            return float(value)
        except ValueError:
            return None

    walk_around = to_float(data.get("walk_around_weight"))
    comp_weight = to_float(data.get("current_bodyweight"))
    weight_class = data.get("competition_weight_class")

    cut_amount = to_float(data.get("typical_cut_amount"))
    cut_percent = None
    if walk_around and cut_amount is not None and walk_around > 0:
        cut_percent = (cut_amount / walk_around) * 100.0

    red_flags = []
    methods = set(data.get("cut_methods", []) if isinstance(data.get("cut_methods"), list) else [])
    symptoms = set(data.get("cut_symptoms", []) if isinstance(data.get("cut_symptoms"), list) else [])

    if "Laxatives or diuretics" in methods:
        red_flags.append("Uses laxatives/diuretics during cuts")
    if "Dizziness or fainting" in symptoms:
        red_flags.append("Dizziness/fainting during cuts")
    if "Missed weight" in symptoms:
        red_flags.append("History of missed weight")
    if "Injury occurrence during cuts" in symptoms:
        red_flags.append("Injury occurrence during cuts")
    if cut_percent is not None and cut_percent >= 5:
        red_flags.append(f"Typical cut ≥ 5% of walk-around ({cut_percent:.1f}%)")

    summary_data = {
        "created_at_utc": row["created_at_utc"],
        "athlete_name": row["athlete_name"],
        "email": row["email"],
        "weight_class": weight_class,
        "walk_around_weight": data.get("walk_around_weight"),
        "current_bodyweight": data.get("current_bodyweight"),
        "typical_cut_amount": data.get("typical_cut_amount"),
        "cut_percent_of_walk_around": (f"{cut_percent:.1f}%" if cut_percent is not None else None),
        "next_fight_date": data.get("next_fight_date"),
        "fights_per_year": data.get("fights_per_year"),
        "training_hours_week": data.get("weekly_training_hours"),
        "red_flags": red_flags,
        "raw": data,
    }

    return render_template("summary.html", intake_id=intake_id, s=summary_data)


@app.route("/export/csv", methods=["GET"])
@require_basic_auth
def export_csv():
    rows = fetch_all_intakes()

    # Build a stable header from known questions
    flat_questions = flatten_questions(FORM_SECTIONS)
    field_names = ["id", "created_at_utc", "athlete_name", "email"] + [q["name"] for q in flat_questions]

    # CSV creation (manual, to keep dependencies at zero)
    def csv_escape(value: object) -> str:
        if value is None:
            return ""
        if isinstance(value, (list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        text = str(value)
        text = text.replace('"', '""')
        return f'"{text}"'

    lines = []
    lines.append(",".join(csv_escape(h) for h in field_names))

    for row in rows:
        data = json.loads(row["data_json"])
        record = {
            "id": row["id"],
            "created_at_utc": row["created_at_utc"],
            "athlete_name": row["athlete_name"],
            "email": row["email"],
        }
        for q in flat_questions:
            record[q["name"]] = data.get(q["name"])

        lines.append(",".join(csv_escape(record.get(h)) for h in field_names))

    csv_text = "\n".join(lines)

    return Response(
        csv_text,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=intakes.csv"},
    )


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

