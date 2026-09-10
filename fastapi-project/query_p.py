from fastapi import FastAPI

app= FastAPI()


all_customers = [
    {"id":101, "name":"Ravi", "city":"chennai", "risk":"medium"},
    {"id":102, "name":"Sumit", "city":"bengluru", "risk":"low"},
    {"id":103, "name":"Nitish", "city":"kolkata", "risk":"low"},
    {"id":104, "name":"Himanshu", "city":"mumbai", "risk":"high"},
    {"id":105, "name":"Karn", "city":"rajasthan", "risk":"medium"},
    {"id":106, "name":"Abhi", "city":"bengluru", "risk":"low"},
    {"id":107, "name":"Vishal", "city":"Delhi", "risk":"high"},
    {"id":108, "name":"Amit", "city":"patna", "risk":"medium"},
]


@app.get("/customers")
def get_customers(city:str, risk:str):
    
    filtered = [
        c for c in all_customers
        
            if c["city"] == city and c["risk"] == risk
    ]
    
    
    return {
        "city":city,
        "risk":risk,
        "counts":len(filtered),
        "results": filtered
    }