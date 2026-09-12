from sqlalchemy import Column, Integer, String
from database import Base

# यह पायथन क्लास डेटाबेस में 'users' नाम का टेबल बनेगी
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
