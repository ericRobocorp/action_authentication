from robocorp.actions import action
from datetime import datetime, timedelta
import json


CONNECTION_FILE_PATH = "authentication.json"


@action(is_consequential=False)
def get_authentication(user_name: str, user_passcode: str) -> str:
    """
    Gets a user name and passcode, then authenticates and sets the DEADLINE variable for the expiration. OpenAI should store and remember the deadline

    Args:
        user_name (str): User name of the person trying to authenticate.
            Example: "eric@robocorp.com"
        user_passcode (str): Passcode is a 6 digit number.
            Example: "389205"

    Returns:
        str: A string confirming the user was authenticated with a deadline containing a date and time
    """

    try:
        if user_name != "eric@robocorp.com":
            raise ValueError("Please try again, the user name was incorrect.")
        if user_passcode != "123456":
            raise ValueError("Please try again, the passcode was incorrect.")
    except ValueError as e:
        return str(e)

    deadline = datetime.now() + timedelta(minutes=1)
    new_auth = {"user_name": user_name, user_name: str(deadline)}
    with open("authentication.json", "w") as file:
        json.dump(new_auth, file)

    return f"Congrats! You have been authenticated access. You now hav the following, DEADLINE: {deadline}"


@action(is_consequential=False)
def calculate_numbers(num_1: int, num_2: int) -> str:
    """
    Receives a url to open for the user

    Args:
        num_1 (int): a random number provided
        num_2 (int): a random number provided
        deadline (str): a date time variable that comes from OpenAI

    Returns:
        str: A string providing a calculated number
    """
    auth_status = get_timeout()

    try:
        if auth_status:
            totes = (num_1 + num_2) * 2
            return f"I multiplied the actual answer by 2 and came up with {totes}"
        else:
            raise ValueError(
                f"You must first authenticate before I can provide you the answer."
            )
    except ValueError as e:
        return str(e)


def test_deadline(deadline):
    try:
        my_deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")
        return my_deadline
    except:
        my_deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M:%SZ")
        return None


def format_date(deadline):
    try:
        my_deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")
        return my_deadline
    except:
        my_deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M:%SZ")
        return my_deadline


def get_timeout():
    with open("authentication.json", "r") as file:
        auth_json = json.load(file)

    current_time = datetime.now()

    if not auth_json["user_name"]:
        return None
    elif not auth_json[auth_json["user_name"]]:
        if current_time <= datetime.strptime(
            auth_json[auth_json["user_name"]], "%Y-%m-%d %H:%M:%S.%f"
        ):
            return "valid"
        else:
            new_auth = {"user_name": None}
            with open("authentication.json", "w") as file:
                json.dump(new_auth, file)
            return None
    else:
        return None
