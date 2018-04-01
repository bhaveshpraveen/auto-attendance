import os
import json
import glob

from django.conf import settings
from django.utils import timezone

from requests import post
from celery import shared_task
from PIL import Image
from pymongo import MongoClient
# import datetime

from organizer.models import Photo
from Tiny_Faces_in_Tensorflow import tiny_face_eval


def return_values(file_name):
    """Return a list containing two values.
    First value is the first line in the file specified
    Second calue is the second line in the given file
    """
    with open(file_name) as f:
        lines = f.readlines()
        # remove carriage return characters
        lines = [line.strip() for line in lines]
        return lines


ENROLL_URL = 'https://api.kairos.com/enroll'
RECOGNIZE_URL = 'https://api.kairos.com/recognize'

app_id, app_key = return_values('kairos_cred.txt')

HEADERS = {
    'app_id': app_id,
    'app_key': app_key
}

user_name, password = return_values('mlab_cred.txt')

URI = 'mongodb://%s:%s@ds119268.mlab.com:19268/attendance' %(user_name, password)



def get_object_photo_model(pk):
    """Return the Photo model instance"""
    return Photo.objects.get(pk=pk)


def json_to_dictionary(json_res):
    print(json_res)
    """Converts the api response(json) to dictionary"""
    return json.loads(json_res.decode('utf-8'))


def split_path_into_directory_and_image(img_path):
    return os.path.split(img_path)


def get_jpg_files(path):
    """Returns a list of jpg files present in the path"""
    return glob.glob(os.path.join(path, '*.jpg'))


def add_to_gallery(img_path, regno):
    """To add a student to the gallery
    Returns the result as a dictionary
    """
    directory, image_name = split_path_into_directory_and_image(img_path)

    files = {'image': (image_name, open(img_path, 'rb'), 'image/jpg', {'Expires': '0'})}
    payload = {
        "subject_id": regno,
        "gallery_name": "test"
    }
    res = post(ENROLL_URL, data=payload, files=files, headers=HEADERS)
    return res.content


def get_face_id_from_api(response):
    """Returns the face_id from the dictionary of the api response"""
    return response['face_id']


def create_photo_instance(**kwargs):
    return Photo.objects.create(**kwargs, commit=False)


def directory_exists(path):
    return os.path.isdir(os.path.join(path))


def delete_files_in_dir(location):
    filelist = [f for f in os.listdir(location)]
    for f in filelist:
        os.remove(os.path.join(location, f))


def handle_student_upload(obj):
    img_path = obj.img.path
    student = obj.student
    user = student.user
    regno = user.registration_number

    directory, image_name = split_path_into_directory_and_image(img_path)
    img = open(img_path, 'rb')

    # place where the users pics are saved temporarily
    location = os.path.join(os.path.join(settings.BASE_DIR, 'images_dir'), regno)

    if not directory_exists(location):
        os.makedirs(location)
    # img now contains the image with the only face
    # img = tiny_face_eval.evaluate(img=img_path, display=False)
    tiny_face_eval.evaluate(img=img_path, output_dir=location)

    for num, img_path in enumerate(get_jpg_files(location)):

        #TODO delete the previous image, check the link below. Use create_photo_instance helper function
        response = add_to_gallery(img_path=img_path, regno=regno)
        dict_resp = json_to_dictionary(response)

        # Face not detected in the image
        if dict_resp.get('Errors', None):
            continue

        # if there is more than 1 image.
        if num > 1:
            obj.pk = None

        face_id = get_face_id_from_api(dict_resp)
        obj.identification = face_id
        obj.save()
    delete_files_in_dir(location)
    os.removedirs(location)


def face_recognition(img_path, regno):

    directory, image_name = split_path_into_directory_and_image(img_path)

    files = {'image': (image_name, open(img_path, 'rb'), 'image/jpg', {'Expires': '0'})}
    payload = {
        "gallery_name": "test"
    }
    res = post(RECOGNIZE_URL, data=payload, files=files, headers=HEADERS)
    return res.content


def highest_confidence_match(dic):
    """Returns a dictionary of the user with the highest confidence for the facial match
    Return:
        {'confidence': 0.69066435,
        'enrollment_timestamp': '1519029374415',
        'face_id': '51aec5247b2047e7b60',
        'subject_id': 'bhavesh'}
    """
    return dic['images'][0]['candidates'][0]


def upload_to_mlab(record):
    client = MongoClient(URI)
    db = client['attendance']
    collection = db['attendance']
    c = collection.insert_one(record)


def handle_teacher_upload(obj):
    img_path = obj.img.path
    course = obj.course
    teacher = course.teacher
    user = teacher.user
    regno = user.registration_number

    directory, image_name = split_path_into_directory_and_image(img_path)
    img = open(img_path, 'rb')
    location = os.path.join(os.path.join(os.path.join(settings.BASE_DIR, 'images_dir'), regno), str(course.id))

    if not directory_exists(location):
        os.makedirs(location)

    tiny_face_eval.evaluate(img=img_path, output_dir=location)

    record = {
        'teacher': 'regno',
        'slot': course.slot,
        'course_code': course.course_code,
        'date': obj.timestamp,
    }

    for num, img_path in enumerate(get_jpg_files(location)):

        response = face_recognition(img_path=img_path, regno=regno)
        dict_resp = json_to_dictionary(response)
        print(dict_resp)

        # Face not detected in the image
        if dict_resp.get('Errors') or (not dict_resp['images'][0].get('candidates')):
            continue

        best_candidate = highest_confidence_match(dict_resp)
        regno = best_candidate['subject_id']

        record[regno] = 'p'

    upload_to_mlab(record)

    delete_files_in_dir(location)
    os.removedirs(location)




# @shared_task
def process_photo(pk):
    obj = Photo.objects.get(id=pk)
    if obj.student:
        handle_student_upload(obj)
    else:
        handle_teacher_upload(obj)


# to find the location of the file
# https://stackoverflow.com/questions/48146443/resize-crop-an-image-using-celery-in-django-in-django-admin-and-outside

#TODO: multiple faces exception
#TODO Exceptions for api