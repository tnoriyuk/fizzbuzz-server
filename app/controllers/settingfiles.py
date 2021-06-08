from typing import Tuple, cast
from flask import Flask, request, abort, jsonify, send_from_directory
from flask import Blueprint
import os

import flask
app = Blueprint("settingfiles", __name__, url_prefix="/settingfiles")

SAVE_DIRECTORY = cast(str, os.environ.get("SAVE_DIRECTORY"))

if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)


api = Flask(__name__)


@api.route("/list", methods=["GET"])
def list() -> flask.Response:
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(SAVE_DIRECTORY):
        path = os.path.join(SAVE_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route("/isexist/<str:filename>", methods=["GET"])
def isexist(filename: str) -> flask.Response:
    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if "/" in filename:
        abort(400, "サブディレクトリの指定は無効です。")

    return jsonify({"isexists": os.path.exists(save_path), "isfile": os.path.isfile(save_path)})


@api.route("/get/<str:filename>", methods=["GET"])
def get(filename: str) -> flask.Response:

    if "/" in filename:
        abort(400, "サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if not os.path.exists(save_path):
        abort(404, f"{filename}が存在しません。")

    if not os.path.isfile(save_path):
        abort(400, f"{filename}はファイルではありません。")

    return send_from_directory(SAVE_DIRECTORY, filename, as_attachment=True)


@api.route("/post/<str:filename>", methods=["POST"])
def post(filename: str) -> Tuple[str, int]:
    """Upload a file."""

    if "/" in filename:
        abort(400, "サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if os.path.exists(save_path):
        abort(409, f"{filename}は既に存在しています。")

    with open(save_path, "wb") as f:
        f.write(request.data)

    # Return 201 CREATED
    return "", 201


@api.route("/put/<str:filename>", methods=["PUT"])
def put(filename: str) -> str:

    if "/" in filename:
        abort(400, "サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if not os.path.exists(save_path):
        abort(404, f"{filename}が存在しません。")

    if not os.path.isfile(save_path):
        abort(400, f"{filename}はファイルではありません。")

    with open(os.path.join(SAVE_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    return ""


@api.route("/delete/<str:filename>", methods=["DELETE"])
def delete(filename: str) -> str:
    """Upload a file."""

    if "/" in filename:
        abort(400, "サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if not os.path.exists(save_path):
        abort(404, f"{filename}が存在しません。")

    if not os.path.isfile(save_path):
        abort(400, f"{filename}はファイルではありません。")

    os.remove(os.path.join(SAVE_DIRECTORY, filename))

    return ""
