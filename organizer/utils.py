import uuid
import datetime

from django.conf import settings
from pymongo import MongoClient
from bson.json_util import dumps


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

# def retrive_records(obj):
#     obj = self.get_object()
#     course_code = obj.course_code
#     slot = obj.slot()
#     teacher = obj.teacher.user.registration_number
#
#     client = MongoClient(settings.URI)
#     db = client['attendance']
#     collection = db['attendance']
#     data = dumps(collection.find({
#         'teacher': teacher,
#         'slot': slot,
#         'course_code': course_code
#     }))

