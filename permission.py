from fastapi import APIRouter, HTTPException
from models import Permission
from database import permissions_collection
from typing import List
from bson import ObjectId 

router = APIRouter()

permissions = []

@router.post("/", response_model=Permission)
async def create_permission(permission: Permission):
    result = permissions_collection.insert_one(permission.dict())
    created_permission = permissions_collection.find_one({"_id": result.inserted_id})
    return created_permission

@router.get("/", response_model=List[Permission])
async def get_permissions():
    permissions = permissions_collection.find()
    return permissions

@router.get("/{permission_id}", response_model=Permission)
async def get_permission(permission_id: str):
    permission = permissions_collection.find_one({"_id": ObjectId(permission_id)})
    if permission:
        return permission
    else:
        raise HTTPException(status_code=404, detail="Permission not found")

@router.put("/{permission_id}", response_model=Permission)
async def update_permission(permission_id: str, updated_permission: Permission):
    existing_permission =  permissions_collection.find_one({"_id": ObjectId(permission_id)})
    if existing_permission:
        permissions_collection.update_one(
            {"_id": ObjectId(permission_id)},
            {"$set": updated_permission.dict(exclude_unset=True)}
        )
        return {**existing_permission, **updated_permission.dict(), "_id": ObjectId(permission_id)}
    else:
        raise HTTPException(status_code=404, detail="Permission not found")

@router.delete("/{permission_id}", response_model=dict)
async def delete_permission(permission_id: str):
    result = permissions_collection.delete_one({"_id": ObjectId(permission_id)})
    if result.deleted_count:
        return {"message": "Permission deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Permission not found")