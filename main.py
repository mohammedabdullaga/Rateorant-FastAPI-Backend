from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Controllers
from controllers.restaurants import router as RestaurantsRouter
from controllers.users import router as UserRouter
from controllers.notifications import router as NotificationsRouter

app = FastAPI()

# CORS ✅ Allow your React dev server(s) to call the API
origins = [
    "*"
    # "http://localhost:5173",
    # "http://127.0.0.1:5173",
    # Later, add your deployed frontend origin, e.g.:
    # "https://your-frontend.example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Which sites can call this API
    allow_methods=["*"],       # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],       # Allow all headers (e.g., Content-Type, Authorization)
    allow_credentials=True,
)


# ROUTES

app.include_router(RestaurantsRouter, prefix="/api")
app.include_router(UserRouter, prefix="/api")
app.include_router(NotificationsRouter, prefix="/api/notifications")

@app.get("/")
def home():
    return {
        "message": "Welcome to Restaurant Review Platform API"
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is running"}