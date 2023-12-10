from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import subscription, permission, user

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(subscription.router, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(permission.router, prefix="/permissions", tags=["permissions"])
app.include_router(user.router, prefix="/users", tags=["users"])