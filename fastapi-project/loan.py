from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoanApplication(BaseModel):
    age:int
    income:float
    loan_amount: float
    employeement_year: int
    
@app.post("/predict")
def predict_loan(application: LoanApplication):
    
    
    #pretend this trained model
    
    if application.income > 50000 and application.employeement_year > 2:
        decision = "approved"
    else:
        decision = "rejected"
        
    return {
        "application_age": application.age,
        "decision": decision
    }