from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, posts

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API",
    description="A simple blog API with users and posts",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Blog API",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users",
            "posts": "/posts",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
