import os
from typing import Tuple, cast

import flask
from flask import Blueprint, abort, jsonify, request, send_from_directory

app = Blueprint("settingfiles", __name__, url_prefix="/settingfiles")

SAVE_DIRECTORY = cast(str, os.environ.get("SAVE_DIRECTORY"))

if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)


@app.route("/list", methods=["GET"])
def list() -> flask.Response:
    """Endpoint to list files on the server."""
    files = [filename for filename in os.listdir(SAVE_DIRECTORY) if os.path.isfile(os.path.join(SAVE_DIRECTORY, filename)) and not filename.startswith(".")]
    return jsonify(files)


@app.route("/isexist/<string:filename>", methods=["GET"])
def isexist(filename: str) -> flask.Response:
    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if "/" in filename:
        abort(400, "サブディレクトリの指定は無効です。")

    return jsonify({"isexists": os.path.exists(save_path), "isfile": os.path.isfile(save_path)})


@app.route("/get/<string:filename>", methods=["GET"])
def get(filename: str) -> flask.Response:

    if "/" in filename:
        abort(400, "サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if not os.path.exists(save_path):
        abort(404, f"{filename}が存在しません。")

    if not os.path.isfile(save_path):
        abort(400, f"{filename}はファイルではありません。")

    return send_from_directory(SAVE_DIRECTORY, filename, as_attachment=True)


@app.route("/post/<string:filename>", methods=["POST"])
def post(filename: str) -> Tuple[str, int]:

    if "/" in filename:
        abort(400, "サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if os.path.exists(save_path):
        abort(409, f"{filename}は既に存在しています。")

    with open(save_path, "wb") as f:
        f.write(request.data)

    # Return 201 CREATED
    return "", 201


@app.route("/put/<string:filename>", methods=["PUT"])
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


@app.route("/delete/<string:filename>", methods=["DELETE"])
def delete(filename: str) -> str:

    if "/" in filename:
        abort(400, "サブディレクトリの指定は無効です。")

    save_path = os.path.join(SAVE_DIRECTORY, filename)

    if not os.path.exists(save_path):
        abort(404, f"{filename}が存在しません。")

    if not os.path.isfile(save_path):
        abort(400, f"{filename}はファイルではありません。")

    os.remove(os.path.join(SAVE_DIRECTORY, filename))

    return ""
