from robocorp.actions import action
from datetime import datetime, timedelta

DEADLINE = None
PASSCODE = None


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
    global DEADLINE, PASSCODE

    try:
        if DEADLINE is None:
            if user_name != "eric@robocorp.com":
                raise ValueError("Please try again, the user name was incorrect.")
            if user_passcode != "123456":
                raise ValueError("Please try again, the passcode was incorrect.")
        else:
            raise ValueError(
                f"Your authentication has expired, pleaes provide credentials to re-authenticate"
            )
    except ValueError as e:
        return str(e)

    PASSCODE = user_passcode
    DEADLINE = datetime.now() + timedelta(minutes=1)
    return f"Congrats! You have been authenticated access. You now hav the following, DEADLINE: {DEADLINE}"


@action(is_consequential=False)
def calculate_numbers(num_1: int, num_2: int, DEADLINE: str) -> str:
    """
    Receives a url to open for the user

    Args:
        num_1 (int): a random number provided
        num_2 (int): a random number provided
        deadline (str): a date time variable that comes from OpenAI

    Returns:
        str: A string providing a calculated number
    """
    global PASSCODE
    current_time = datetime.now()
    my_deadline = format_date(
        DEADLINE
    )  # datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")

    try:
        if current_time <= my_deadline:
            totes = num_1 + num_2
            return f"The total is {totes}"
        else:
            user_passcode = None
            PASSCODE = None
            DEADLINE = None
            raise ValueError(
                f"Current time is greater than the DEADLINE which was ({my_deadline}) and the current time is ({current_time})."
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
