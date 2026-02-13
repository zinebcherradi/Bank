from config import Base, engine
from fastapi import FastAPI
from controllers import router_users, router_accounts, router_transactions, router_auth
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

def init_db():
    metadata = getattr(Base, 'metadata')
    metadata.create_all(bind=engine)

app = FastAPI(title="Banking API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Base de données initialisée")

app.include_router(router_auth, tags=["Authentification"])
app.include_router(router_users, tags=["Utilisateurs"])
app.include_router(router_accounts, tags=["Comptes"])
app.include_router(router_transactions, tags=["Transactions"])

@app.get("/")
def root():
    return {"message": "Banking API is running", "version": "1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
