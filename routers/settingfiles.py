import os
from typing import List, cast

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.responses import FileResponse

router = APIRouter(prefix="/settingfiles")

SAVE_DIRECTORY = cast(str, os.environ.get("SAVE_DIRECTORY"))

if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)


@router.get("/list")
def list() -> List[str]:
    files = [filename for filename in os.listdir(SAVE_DIRECTORY) if os.path.isfile(os.path.join(SAVE_DIRECTORY, filename)) and not filename.startswith(".")]
    return files


class CheckResult(BaseModel):
    isexists: bool
    isfile: bool


@router.get("/check/{filename}", response_model=CheckResult)
def check(filename: str) -> CheckResult:
    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if "/" in filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="サブディレクトリの指定は無効です。")

    return CheckResult(**{"isexists": os.path.exists(save_path), "isfile": os.path.isfile(save_path)})


@router.get("/get/{filename}")
def get(filename: str) -> FileResponse:

    if "/" in filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if not os.path.exists(save_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{filename}が存在しません。")

    if not os.path.isfile(save_path):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{filename}はファイルではありません。")

    return FileResponse(save_path)


@router.post("/post/{filename}")
def post(filename: str, file: UploadFile = File(...)) -> JSONResponse:

    if "/" in filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if os.path.exists(save_path):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{filename}は既に存在しています。")

    with open(save_path, "wb") as f:
        f.write(file.file.read())

    return JSONResponse(status_code=status.HTTP_201_CREATED)


@router.put("/put/{filename}")
def put(filename: str, file: UploadFile = File(...)) -> JSONResponse:

    if "/" in filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if not os.path.exists(save_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{filename}が存在しません。")

    if not os.path.isfile(save_path):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{filename}はファイルではありません。")

    with open(os.path.join(SAVE_DIRECTORY, filename), "wb") as f:
        f.write(file.file.read())

    return JSONResponse(status_code=status.HTTP_200_OK)


@router.delete("/delete/{filename}")
def delete(filename: str) -> JSONResponse:

    if "/" in filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if not os.path.exists(save_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{filename}が存在しません。")

    if not os.path.isfile(save_path):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{filename}はファイルではありません。")

    os.remove(os.path.join(SAVE_DIRECTORY, filename))

    return JSONResponse(status_code=status.HTTP_200_OK)
