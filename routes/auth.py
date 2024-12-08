from .. import crud
from typing import Any
from ..models import *
from .deps import get_db
from ..rabbit.client import mq_cl
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, Request

auth_router = APIRouter()

@auth_router.get("/")
async def get_forward_auth_req(request: Request) -> Any:
    for k,v in request.headers.items():
        if "listing" in k or "listing" in v:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"{k}: {v}")
    print(request.path_params)
    return {}