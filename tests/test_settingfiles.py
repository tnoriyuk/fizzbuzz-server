import requests

API_URL = "http://127.0.0.1:60000/settingfiles"


def test_settingfiles_list() -> None:
    response = requests.get("{}/list".format(API_URL))

    print(response.json())


def test_settingfiles_isexist() -> None:
    response = requests.get("{}/isexist/{}".format(API_URL, "newdata.csv"))

    print(response.json())


def test_settingfiles_get() -> None:
    response = requests.get("{}/get/{}".format(API_URL, "newdata.csv"))

    print(response.text)


def test_settingfiles_post() -> None:
    with open("tests/newdata.csv") as fp:
        content = fp.read()

    response = requests.post(
        "{}/post/{}".format(API_URL, "newdata.csv"), data=content
    )

    print(response.status_code)


def test_settingfiles_put() -> None:
    with open("tests/newdata.csv") as fp:
        content = fp.read()

    response = requests.put(
        "{}/put/{}".format(API_URL, "newdata.csv"), data=content
    )

    print(response.status_code)


def test_settingfiles_delete() -> None:
    response = requests.delete("{}/delete/{}".format(API_URL, "newdata.csv"))

    print(response.status_code)


def main() -> None:
    try:
        test_settingfiles_list()
        test_settingfiles_isexist()
        test_settingfiles_get()
        test_settingfiles_post()
        test_settingfiles_put()
        # test_settingfiles_delete()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
