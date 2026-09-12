from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


# 1. Schema for user registration and full updates (All required fields)
class UserRegistration(BaseModel):
    username: str
    email: str
    password: str = Field(
        min_length=4, description="Password must be at least 4 characters"
    )
    age: int = Field(gt=0, le=120)
    is_subscribed: bool = False
    bio: Optional[str] = None


# 2. Schema for partial updates (All fields are optional)
class UserUpdatePartial(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=4)
    age: Optional[int] = Field(default=None, gt=0, le=120)
    is_subscribed: Optional[bool] = None
    bio: Optional[str] = None


# In-memory database simulation
users_db = []


# 3. Create a new user (POST)
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegistration):
    user_dict = user.model_dump()
    user_dict["id"] = len(users_db) + 1  # Auto-incrementing unique ID
    users_db.append(user_dict)

    # Return clean response without exposing password
    safe_data = {
        "id": user_dict["id"],
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "is_subscribed": user.is_subscribed,
        "bio": user.bio,
    }

    return {
        "status": "success",
        "message": f"User {user.username} registered successfully!",
        "data": safe_data,
    }


# 4. Completely replace an existing user (PUT)
@app.put("/users/{user_id}")
def update_user(
    user_id: int, user: UserRegistration, send_notification: bool = True
):
    # Find the target user using a standard for loop
    db_user = None
    for u in users_db:
        if u["id"] == user_id:
            db_user = u
            break

    # Return 404 if user does not exist
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    # Replace the existing dictionary completely with new data
    updated_dict = user.model_dump()
    updated_dict["id"] = user_id
    index = users_db.index(db_user)
    users_db[index] = updated_dict

    return {
        "user_id": user_id,
        "updated_data": updated_dict,
        "notification_sent": send_notification,
    }


# 5. Partially update an existing user (PATCH)
@app.patch("/users/{user_id}")
def patch_user(user_id: int, user_update: UserUpdatePartial):
    # Find the target user using a standard for loop
    db_user = None
    for u in users_db:
        if u["id"] == user_id:
            db_user = u
            break

    # Return 404 if user does not exist
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    # Extract only the fields explicitly provided in the request body
    update_data = user_update.model_dump(exclude_unset=True)

    if not update_data:
        return {"message": "No fields provided to update", "data": db_user}

    # Update only the matching keys in the database entry
    for key, value in update_data.items():
        db_user[key] = value

    return {
        "status": "success",
        "message": f"User {user_id} partially updated!",
        "updated_data": db_user,
    }