# Smart Irrigation Need Prediction System

A Machine Learning based web application that predicts irrigation requirements for crops using soil, weather, crop, and field conditions.

## Live Demo
https://irrigation-need-4.onrender.com

---

## Features

- Predicts irrigation need as:
  - Low
  - Medium
  - High

- Uses inputs such as:
  - Soil Type
  - Soil Moisture
  - Soil pH
  - Organic Carbon
  - Temperature
  - Humidity
  - Rainfall
  - Sunlight Hours
  - Crop Type
  - Growth Stage
  - Irrigation Type
  - Water Source
  - Region

- Mobile responsive web interface  
- Flask-based deployment  
- Random Forest Machine Learning model  
- Preprocessing Pipeline using Scikit-learn  

---

## Machine Learning Workflow

### Data Preprocessing
- Missing value handling using `SimpleImputer`
- Numerical feature scaling using `StandardScaler`
- Categorical encoding using `OneHotEncoder`
- Combined using `ColumnTransformer`

### Model Used
- Random Forest Classifier

### Final Performance

| Metric | Score |
|--------|-------|
| Training Accuracy | 93.83% |
| Testing Accuracy | 93.05% |
| F1 Score | 86.46% |

Model tuned using:
- `n_estimators`
- `max_depth`

---

## Tech Stack

- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- HTML
- CSS
- Render

---

## Project Structure

```bash
Irrigation_Need/
│
├── app.py
├── requirements.txt
├── runtime.txt
├── best_model_pipeline.pkl
│
├── templates/
│   ├── home.html
│   └── index.html
│
├── Model_training.ipynb
├── EDA.ipynb
└── README.md
```

---

## Installation

Clone repository:

```bash
git clone https://github.com/vedddev/Irrigation_Need.git
cd Irrigation_Need
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
python app.py
```

Open:

```bash
http://127.0.0.1:5000
```

---

## Deployment

Deployed using Render.

Start Command:

```bash
gunicorn app:app
```

Python Version:

```txt
3.11.9
```

---

## Future Improvements

- Real-time weather API integration  
- IoT sensor integration  
- Smart irrigation scheduling  
- Crop recommendation support  
- Farmer advisory chatbot  

---

## Author

Vedant Shelake

GitHub: https://github.com/vedddev

---

## License

This project is for educational and research purposes.
