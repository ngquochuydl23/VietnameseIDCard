import uvicorn
import logging
import json
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse, RedirectResponse
from services.idcard_service import IdCardService
from middlewares.exception_handling_middleware import ExceptionHandlingMiddleware
from utils.gpu_utils import check_gpu

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

idcard_service = IdCardService()

app = FastAPI(title="Extract IdCard information API")
app.add_middleware(ExceptionHandlingMiddleware)


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.get("/api/ping", tags=["HealthChecks"])
async def ping():
    return "Pong"


@app.post("/api/idcard-extract", tags=["IdCard"])
async def extract_idcard(front_card: UploadFile = File(...), back_card: UploadFile = File(...)):
    result = await idcard_service.idcard_extract_combine(front_card, back_card)
    return JSONResponse(
        status_code=200,
        content={"statusCode": 200, "result": result})


@app.post("/api/front-idcard-extract", tags=["IdCard"])
async def extract_front_idcard(front_card: UploadFile = File(...)):
    result = await idcard_service.idcard_extract_front(front_card)
    return JSONResponse(
        status_code=200,
        content={"statusCode": 200, "result": result})


@app.post("/api/back-idcard-extract", tags=["IdCard"])
async def extract_back_idcard(back_card: UploadFile = File(...)):
    result = await idcard_service.idcard_extract_back(back_card)
    return JSONResponse(
        status_code=200,
        content={"statusCode": 200, "result": result})


if __name__ == "__main__":
    logger.info(json.dumps(check_gpu(), indent=4))
    uvicorn.run(app, port=2012)
