from pydantic import BaseModel
from typing import List

class SubscriptionPlan(BaseModel):
    name: str
    description: str
    permissions: List[str]
    usage_limit: int

class Permission(BaseModel):
    name: str
    endpoint: str
    description: str

class UserSubscription(BaseModel):
    username: str
    plan_name: str