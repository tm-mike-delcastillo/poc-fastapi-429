from fastapi import FastAPI

from app.lib.redis import  should_rate_limit_message

app = FastAPI()

@app.get("/")
async def root():
    should_rate_limit = should_rate_limit_message("test")
    return {"should_rate_limit": should_rate_limit}
