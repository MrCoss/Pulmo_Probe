# backend/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from huggingface_hub import hf_hub_download
import os

app = FastAPI(title="PulmoProbe AI API")

# Add CORS middleware to allow your Vercel app to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Download and Load Model from Hugging Face Hub ---
# This points to your model repository
MODEL_REPO_ID = "costaspinto/PulmoProbe" 
MODEL_FILENAME = "best_model.joblib"

print("Downloading model from Hugging Face Hub...")
model_path = hf_hub_download(repo_id=MODEL_REPO_ID, filename=MODEL_FILENAME)
model = joblib.load(model_path)
print("Model loaded successfully.")

# --- Define Input Data Model ---
class PatientData(BaseModel):
    age: float
    gender: str
    country: str
    cancer_stage: str
    family_history: int
    smoking_status: str
    bmi: float
    cholesterol_level: float
    hypertension: int
    asthma: int
    cirrhosis: int
    other_cancer: int
    treatment_type: str

# --- Define API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the PulmoProbe AI API"}

@app.post("/predict")
def predict(data: PatientData):
    try:
        input_df = pd.DataFrame([data.dict()])
        probabilities = model.predict_proba(input_df)[0]
        confidence_high_risk = probabilities[0]
        risk_level = "High Risk of Non-Survival" if confidence_high_risk > 0.5 else "Low Risk of Non-Survival"

        return {
            "risk": risk_level,
            "confidence": f"{confidence_high_risk * 100:.1f}"
        }
    except Exception as e:
        return {"error": str(e)}