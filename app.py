from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import random
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MULTIPLIER = 14

@app.get("/")
def home():
    return {"status": "KENLY DEV API ONLINE"}

# streaming generator
async def generate_logs(target, batches, delay):
    total_ops = batches * MULTIPLIER

    for i in range(total_ops):
        await asyncio.sleep(delay / MULTIPLIER)

        current_batch = (i // MULTIPLIER) + 1
        current_op = (i % MULTIPLIER) + 1

        yield json.dumps({
            "batch": current_batch,
            "operation": current_op,
            "status": random.choice(["SUCCESS", "FAILED"])
        }) + "\n"

@app.post("/run")
async def run(data: dict):
    return StreamingResponse(
        generate_logs(
            data.get("target"),
            int(data.get("batches")),
            int(data.get("delay"))
        ),
        media_type="text/plain"
    )
