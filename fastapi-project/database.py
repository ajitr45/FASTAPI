# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# # 1. यह हमारी Empty List है जो डेटाबेस का काम करेगी
# FAKE_DATABASE = []

# # 2. Pydantic Model (यह तय करता है कि नया डेटा आते समय उसका फ़ॉर्मेट क्या होगा)
# class UserSchema(BaseModel):
#     name: str
#     email: str

# # 3. सर्वर शुरू होते ही लिस्ट में 5 डमी यूज़र्स अपने आप डालने के लिए
# @app.on_event("startup")
# def populate_fake_data():
#     # बिना Faker के मैन्युअल डमी डेटा लिस्ट
#     dummy_names = ["Rahul Kumar", "Amit Sharma", "Priya Singh", "Neha Verma", "Vikas Yadav"]
#     dummy_emails = ["rahul@example.com", "amit@example.com", "priya@example.com", "neha@example.com", "vikas@example.com"]
    
#     for i in range(5):
#         fake_user = {
#             "id": i + 1,
#             "name": dummy_names[i],
#             "email": dummy_emails[i]
#         }
#         FAKE_DATABASE.append(fake_user)

# # 4. GET API: लिस्ट का सारा डेटा देखने के लिए
# @app.get("/users")
# def get_all_users():
#     return {"total_users": len(FAKE_DATABASE), "data": FAKE_DATABASE}

# # 5. POST API: इस एम्प्टी लिस्ट में नया डेटा बाहर से जोड़ने के लिए
# @app.post("/add-user")
# def create_user(user: UserSchema):
#     # नया ID तय करना (लिस्ट की लंबाई + 1)
#     new_id = len(FAKE_DATABASE) + 1
    
#     # नया यूज़र ऑब्जेक्ट बनाना
#     new_user = {
#         "id": new_id,
#         "name": user.name,
#         "email": user.email
#     }
    
#     # लिस्ट में डेटा सेव (Append) करना
#     FAKE_DATABASE.append(new_user)
    
#     return {"message": "User added successfully to the list!", "user": new_user}


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# असली SQLite डेटाबेस फाइल (my_database.db) का रास्ता
SQLALCHEMY_DATABASE_URL = "sqlite:///./my_database.db"

# इंजन बनाना (connect_args केवल SQLite के लिए ज़रूरी है)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# डेटाबेस से बातचीत करने के लिए Session क्लास
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# इसी बेस क्लास से हमारे मॉडल्स (Tables) बनेंगे
Base = declarative_base()

# डेटाबेस सेशन को मैनेज करने के लिए एक फंक्शन (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
