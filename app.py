from flask import Flask, request, render_template, redirect, session
import os
import pandas as pd
import joblib
import sqlite3
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = "agrisense_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================= MODEL =================
model_path = os.path.join(BASE_DIR, "best_model_pipeline.pkl")
model = joblib.load(model_path)

expected_cols = [
    'Soil_Type', 'Soil_pH', 'Soil_Moisture', 'Organic_Carbon',
    'Electrical_Conductivity', 'Temperature_C', 'Humidity', 'Rainfall_mm',
    'Sunlight_Hours', 'Wind_Speed_kmh', 'Crop_Type', 'Crop_Growth_Stage',
    'Season', 'Irrigation_Type', 'Water_Source', 'Field_Area_hectare',
    'Mulching_Used', 'Previous_Irrigation_mm', 'Region'
]

num_cols = [
    'Soil_pH', 'Soil_Moisture', 'Organic_Carbon',
    'Electrical_Conductivity', 'Temperature_C', 'Humidity', 'Rainfall_mm',
    'Sunlight_Hours', 'Wind_Speed_kmh', 'Field_Area_hectare',
    'Previous_Irrigation_mm'
]

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= HOME =================
@app.route("/")
def home():
    return render_template("home.html")

# ================= PREDICT PAGE =================
@app.route("/predict")
def predict_page():
    return render_template("index.html")

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match"

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            conn.commit()
        except:
            return "Email already exists"
        finally:
            conn.close()

        return redirect("/login")

    return render_template("register.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/")
        else:
            return "Invalid email or password"

    return render_template("login.html")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ================= ML PREDICTION =================
@app.route("/predictdata", methods=["POST"])
def predict_datapoint():
    try:
        data = request.form.to_dict()
        df = pd.DataFrame([data])

        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0

        df = df[expected_cols]

        prediction = model.predict(df)[0]

        mapping = {0: "Low", 1: "High", 2: "Medium"}
        result = mapping.get(prediction, prediction)

        return render_template("index.html", result=f"Irrigation Need: {result}")

    except Exception as e:
        return render_template("index.html", result=f"Error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)