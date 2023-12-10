from fastapi import APIRouter, HTTPException
from models import SubscriptionPlan
from typing import List
from database import subscriptions_collection
from bson import ObjectId

router = APIRouter()

subscription_plans = []

@router.post("/", response_model=SubscriptionPlan)
async def create_subscription(subscription: SubscriptionPlan):
    result = subscriptions_collection.insert_one(subscription.dict())
    return {**subscription.dict(), "_id": result.inserted_id}

@router.get("/", response_model=List[SubscriptionPlan])
async def get_all_subscriptions():
    subscriptions = subscriptions_collection.find()
    return subscriptions

@router.get("/{plan_name}", response_model=SubscriptionPlan)
async def get_subscription(plan_name: str):
    subscription = subscriptions_collection.find_one({"name": plan_name})
    if subscription:
        return subscription
    else:
        raise HTTPException(status_code=404, detail="Subscription not found")


@router.put("/{plan_name}", response_model=SubscriptionPlan)
async def update_subscription(plan_name: str, updated_subscription: SubscriptionPlan):
    existing_subscription = subscriptions_collection.find_one({"name": plan_name})
    if existing_subscription:
        subscriptions_collection.update_one(
            {"name": plan_name},
            {"$set": updated_subscription.dict(exclude_unset=True)}
        )
        return {**existing_subscription, **updated_subscription.dict(), "name": plan_name}
    else:
        raise HTTPException(status_code=404, detail="Subscription not found")

@router.delete("/{plan_name}", response_model=dict)
async def delete_subscription(plan_name: str):
    result = subscriptions_collection.delete_one({"name": plan_name})
    if result.deleted_count:
        return {"message": "Subscription deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Subscription not found")
