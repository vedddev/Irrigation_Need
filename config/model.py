from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "best_model_pipeline.pkl"

model = joblib.load(MODEL_PATH)