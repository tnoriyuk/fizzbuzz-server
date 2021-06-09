from flask import Flask

from controllers.settingfiles import app as settingfiles

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

app.register_blueprint(settingfiles)


@app.route("/")
def index() -> str:
    return "running"


def main() -> None:
    app.run(host="127.0.0.1", port=60000, debug=True, load_dotenv=True)


if __name__ == "__main__":
    main()
