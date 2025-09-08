from fastapi import FastAPI
from api.routes.routes import router as api_router

app = FastAPI(title="Auth Service")
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup():
    from core.kafka_producer import producer
    await producer.start()


@app.on_event("shutdown")
async def shutdown():
    from core.kafka_producer import producer
    await producer.stop()