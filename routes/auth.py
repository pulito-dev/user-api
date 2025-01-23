import re
import boto3
import json
from .. import crud
from typing import Any
from ..models import *
from .deps import get_session
from sqlmodel import Session
from ..auth.client import auth_cl
from auth0 import TokenValidationError
from fastapi import APIRouter, Depends, HTTPException, Request, Response


auth_router = APIRouter()


@auth_router.get("/")
async def get_forward_auth_req(
    request: Request,
    response: Response,
    session: Session = Depends(get_session)
) -> Any:
    
    auth_header = request.headers.get("authorization")

    # token not present
    if auth_header is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token, token not present in 'Authorization' header"
        )
    
    # auth header value format
    # \w    = [a-zA-Z0-9_]
    # +     = {1,} 
    token_search: re.Match = re.search(r"^Bearer ([\w-]+.[\w-]+.[\w-]+)$", auth_header)

    # invalid token 
    if token_search is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token, token format should be 'Bearer <token>'"
        )
   
    # get first match (yes, 1 is for getting a first matched group ¯\_(ツ)_/¯)
    auth_token = token_search.group(1)

    # verify the token
    try:
        decoded_token = auth_cl.verify_token(auth_token)
    except TokenValidationError as e:
        print(e)
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    
    # get user
    idp_id = decoded_token.get("sub")
    user = await crud.get_user_by_idp_id(session, idp_id)

    # if user doesn't exist, insert a new user with provided data
    if user is None:
        idp_user = auth_cl.get_idp_user(idp_id)

        # FIXME: hardcoded way of instatiaing admin on login
        if "sakyyt" in idp_user.get("nickname"):
            role = await crud.get_role_by_name(session, "ADMIN")
        else:
            role = await crud.get_role_by_name(session, "REGULAR")

        user_create = CreateUpdateUser(
            idp_id=idp_id,
            first_name=idp_user.get("given_name"),
            last_name=idp_user.get("family_name"),
            email=idp_user.get("email"),
            nickname=idp_user.get("nickname"),
            picture=idp_user.get("picture"),
            role_id=role.id
        )

        user = await crud.create_user(session, user_create)

        # invoke a lambda function for creating dummy accommodations
        lambda_client = boto3.client("lambda")
        lambda_client.invoke_async(
            FunctionName="importAccommodations",
            InvokeArgs=json.dumps({"user_id": user.id}).encode()
        )
    
    # set headers for other services to identify a user
    response.headers["x-forwarded-user"] = str(user.id)

    # headers in this response are forwarded to proper service
    return {}