import uvicorn
import logging
import json
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from services.idcard_service import IdCardService
from middlewares.exception_handling_middleware import ExceptionHandlingMiddleware
from src.app.constants.http_msg_constants import NO_FRONT_FIELDS_DETECTED, NO_BACK_FIELDS_DETECTED
from src.app.exceptions.app_exception import AppException
from utils.gpu_utils import check_gpu

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
idcard_service = IdCardService()

app = FastAPI(title="Extract IdCard information API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(ExceptionHandlingMiddleware)

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.get("/api/ping", tags=["HealthCheck"])
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
    if result is None:
        raise AppException(NO_FRONT_FIELDS_DETECTED)
    return JSONResponse(
        status_code=200,
        content={"statusCode": 200, "result": result})


@app.post("/api/back-idcard-extract", tags=["IdCard"])
async def extract_back_idcard(back_card: UploadFile = File(...)):
    result = await idcard_service.idcard_extract_back(back_card)
    if result is None:
        raise AppException(NO_BACK_FIELDS_DETECTED)
    return JSONResponse(
        status_code=200,
        content={"statusCode": 200, "result": result})


if __name__ == "__main__":
    logger.info(json.dumps(check_gpu(), indent=4))
    uvicorn.run(app, host="0.0.0.0", port=2012)
