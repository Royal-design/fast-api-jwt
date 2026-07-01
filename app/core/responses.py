from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    data=None,
    message="Success",
    status_code=200,
):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": jsonable_encoder(data),
        },
    )