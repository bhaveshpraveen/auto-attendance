import uuid
import datetime


def generate_random_string():
    """Generate a random string. """
    return uuid.uuid4()


def get_current_date():
    """Get the date in dd/mm/yyyy format"""
    return datetime.datetime.now().strftime("%X-%d-%m-%Y")


def get_unique_identificaton(instance):
    """Get unique identification in the format registration_number:dd/mm/yyyy"""
    string = "{}:{}".format(instance.__str__(), get_current_date())
    print(string)
    return string

