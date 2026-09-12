from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db

# 1. डेटाबेस में टेबल को असलियत में क्रिएट करना
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic Model इनपुट डेटा को वैलिडेट करने के लिए
class UserCreate(BaseModel):
    name: str
    email: str

# 2. GET API: डेटाबेस से सारे यूज़र्स की लिस्ट निकालना
@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# 3. POST API: पायथन ऑब्जेक्ट बनाकर डेटाबेस में आसानी से सेव करना
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # चेक करें कि ईमेल पहले से तो नहीं है
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # शुद्ध पायथन ऑब्जेक्ट बनाना (SQLAlchemy इसे खुद SQL में बदल देगा)
    new_user = models.User(name=user.name, email=user.email)
    
    db.add(new_user)     # सेशन में जोड़ना
    db.commit()          # डेटाबेस में सेव करना
    db.refresh(new_user) # नई ID के साथ ऑब्जेक्ट को अपडेट करना
    
    return {"message": "User saved in database successfully!", "user": new_user}
