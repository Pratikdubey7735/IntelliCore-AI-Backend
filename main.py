from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.query_routes import router as query_router
from routes.dashboard_routes import router as dashboard_router
from routes.saved_routes import router as saved_router
from routes.history_routes import router as history_router
from routes.admin_features_routes import router as admin_features_router

app = FastAPI(title="Intellicore AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://intelli-core-ai-eight.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(query_router, prefix="/api", tags=["Query"])
app.include_router(dashboard_router, prefix="/api", tags=["Dashboard"])
app.include_router(saved_router, prefix="/api", tags=["Saved"])
app.include_router(history_router, prefix="/api", tags=["History"])
app.include_router(admin_features_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Intellicore AI Backend is Running"}