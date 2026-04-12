from flask import Flask, request, render_template
import os
import pandas as pd
import pickle
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model
model_path = os.path.join(BASE_DIR, "best_model_pipeline.pkl")
model = pickle.load(open(model_path, "rb"))

# Columns
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

#  HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')

#  PREDICTION PAGE (form page)
@app.route('/predict')
def predict_page():
    return render_template('index.html')

#  MODEL PREDICTION
@app.route('/predictdata', methods=['POST'])
def predict_datapoint():
    try:
        data = request.form.to_dict()
        df = pd.DataFrame([data])

        # Convert numeric columns
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Add missing columns
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0

        # Correct order
        df = df[expected_cols]

        # Predict
        prediction = model.predict(df)[0]

        mapping = {0: "Low", 1: "High", 2: "Medium"}
        result = mapping.get(prediction, prediction)

        return render_template("index.html", result=f"Irrigation Need: {result}")

    except Exception as e:
        return render_template("index.html", result=f"Error: {str(e)}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)