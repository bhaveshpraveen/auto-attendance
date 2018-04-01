import os
import json

from requests import post
from celery import shared_task

from organizer.models import Photo
from Tiny_Faces_in_Tensorflow import tiny_face_eval


ENROLL_URL = 'https://api.kairos.com/enroll'
RECOGNIZE_URL = 'https://api.kairos.com/recognize'


def get_object_photo_model(pk):
    """Return the Photo model instance"""
    return Photo.objects.get(pk=pk)


def json_to_dictionary(json_res):
    """Converts the api response(json) to dictionary"""
    return json.loads(json_res)

def split_path_into_directory_and_image(img_path):
    return os.path.split(img_path)

def add_to_gallery(img_path, regno):
    """To add a student to the gallery
    Returns the result as a dictionary
    """
    directory, image_name = split_path_into_directory_and_image(img_path)
    headers = {
        'app_id': 'f8740eaf',
        'app_key': '88ba573be0ab1dca57a4a10ac0a404f2'
    }
    files = {'image': (image_name, open(img_path, 'rb'), 'image/jpg', {'Expires': '0'})}
    payload = {
        "subject_id": regno,
        "gallery_name": "test"
    }
    res = post(ENROLL_URL, data=payload, files=files, headers=headers)
    return res


def get_fade_id_from_api(response):
    """Returns the face_id from the dictionary of the api response"""
    return response['face_id']

def create_photo_instance(**kwargs):
    return Photo.objects.create(**kwargs, commit=False)


def handle_student_upload(obj):
    img_path = obj.img.path
    student = obj.student
    regno = student.registration_number

    directory, image_name = split_path_into_directory_and_image(img_path)
    img = open(img_path, 'rb')
    img = tiny_face_eval.evaluate(img=img_path, display=False)

    #TODO: Run the model to crop the face
    #TODO: save his face
    #TODO delete the previous image, check the link below. Use create_photo_instance helper function
    response = add_to_gallery(img_path=img_path, regno=regno)
    dict_resp = json_to_dictionary(response)
    face_id = get_fade_id_from_api(dict_resp)

    obj.identification = face_id
    obj.img = img #Todo: Change this to the processed image
    obj.save()

@shared_task
def process_photo(pk):
    # obj = Photo.objects.get(id=pk)


# to find the location of the file
# https://stackoverflow.com/questions/48146443/resize-crop-an-image-using-celery-in-django-in-django-admin-and-outside