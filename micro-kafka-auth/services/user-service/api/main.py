from fastapi import FastAPI
from api.routes.routes import router as api_router
from core.kafka_consumer import consumer_task

app = FastAPI(title='User Service')
app.include_router(api_router, prefix='/api')


@app.on_event('startup')
async def startup():
    import asyncio
    app.state.consumer_task = asyncio.create_task(consumer_task())


@app.on_event('shutdown')
async def shutdown():
    task = app.state.consumer_task
    task.cancel()