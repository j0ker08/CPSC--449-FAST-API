from fastapi import APIRouter, HTTPException
from models import UserSubscription
from database import users_collection

router = APIRouter()

user_subscriptions = []


@router.post("/", response_model=UserSubscription)
async def create_user(user: UserSubscription):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    result = users_collection.insert_one(user.dict())
    created_user = users_collection.find_one({"_id": result.inserted_id})
    return created_user

@router.get("/{username}", response_model=UserSubscription)
async def get_user(username: str):
    user = users_collection.find_one({"username": username})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{username}", response_model=UserSubscription)
async def update_user(username: str, updated_user: UserSubscription):
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        users_collection.update_one(
            {"username": username},
            {"$set": updated_user.dict(exclude_unset=True)}
        )
        return {**existing_user, **updated_user.dict(), "username": username}
    else:
        raise HTTPException(status_code=404, detail="User not found")