from flask import Blueprint

app = Blueprint('settings', __name__, url_prefix='/settings')


@app.route('/a1')
def app_a1() -> str:
    return "hoge"


@app.route('/a2')
def app_a2() -> str:
    return "hoge"
