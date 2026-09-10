from fastapi import FastAPI
from pydantic import BaseModel, Field


app= FastAPI(title="Health Insurance Predictor ")

class HealthInsurance(BaseModel):
    
    name: str
    age: int = Field( gt=0, le=100, description="Age between 1 and 100")
    weight_kg: float = Field( gt=10.0, description="Weight in kilogram......")
    height_m: float = Field( gt= 0.5, description="Height in meters..")
    is_smoker:  bool = False
    has_per_existing_disease: bool = False
    
    
@app.post("/predict")
def predict_insurance(data: HealthInsurance):
    
    bmi= round((data.weight_kg / data.height_m**2), 2)
    base_premimum = 5500.0
    age_cost = data.age * 250
    
    #Check BMI factor
    
    if bmi < 18.5:
        bmi_category = "Underweight"
        bmi_cost = 1000.0
    elif bmi <= 18.5 and bmi <= 24.9:
        bmi_category = "Normal"
        bmi_cost = 0.0
    elif bmi <= 25.0 and bmi <= 29.9:
        bmi_category = "Overweight"
        bmi_cost = 3500
    else:
        bmi_category = "obese"
        

    # lifestyle and Mesical factor 

    smoker_cost = 12000.0 if data.is_smoker else 0
    disease_cost = 8000.0 if data.has_per_existing_disease else 0
    
    total_premium = (base_premimum + age_cost + bmi_cost + smoker_cost + disease_cost)
    
    
    # Risk Assessment & Decision
    
    if data.is_smoker and (bmi >= 30.0 or data.has_per_existing_disease):
        risk_level = "Very Heigh"
        decision = "Required Manual Medical Review"
    elif data.is_smoker or bmi >= 30.0 or data.has_per_existing_disease:
        risk_level = "heigh"
        decision = "approved High Premium"
    elif bmi >= 25.0 or data.age > 50:
        risk_level = "Medium"
        decision = "Approved (Standard Premium)"
    else:
        risk_level = "Low"
        decision = "Approved Discounted Premimum"
        
    return {
        "applicant_name ": data.name,
        "calculated_bmi": bmi,
        "bmi_category": bmi_category,
        "risk_level":risk_level,
        "estimated_annual_premimum_inr": total_premium,
        "decision": decision
    }
    
    