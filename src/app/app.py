import os
import sys
import uvicorn
import shutil
import logging
from constants.http_constants import HTTP_OK_STATUS
from fastapi import FastAPI, File, UploadFile, Request, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from services.idcard_service import IdCardService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="EKYC Service")

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

@app.get("/api/ping", tags=["HealthChecks"])
async def ping():
    return "Pong"

@app.post("/api/idcard-extract", tags=["IdCard"])
async def extract_idcard(id_card: UploadFile = File(...), face: UploadFile = File(...)):
    return JSONResponse(
        status_code=HTTP_OK_STATUS,
        content={
            "statusCode": HTTP_OK_STATUS,
            "result": {
                "execution_time": 0,
                "front": {
                    "match_result": '',
                    "face_url": ''
                },
                "back": {

                }
            }
        })
