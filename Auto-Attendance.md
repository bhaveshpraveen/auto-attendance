# Auto-Attendance

Auto-Attendance, an attempt to automate the process of taking attendance through facial recognition.  

Teachers and Students can register through the [Android Application](https://github.com/MINOSai/FaceCheck).  

The Students are then asked to provide images of themselves uh.... Sigh. Selfies. You can upload Selfies (or any other image). You can upload it through the android app.

The faces are detected using [TInyFace](https://github.com/cydonia999/Tiny_Faces_in_Tensorflow). 

[Kairos Services](http://www.kairos.com/) are used for recognizing the person.

The attendance is then posted. This feature is still a bit rusty. I've used MondoDB making use of [MLabs](https://mlab.com/) services to keep track of attendance. The application makes an api call to [MLabs](https://mlab.com/) to post attendance.



**Why MongoDB ?  Why not Postgres or some DB that is supported by Django ?**

Cause, I'm a lazy person. AND I didn't know how to model the attendance system and didn't want to brick anything else in the process. Yeah! No Unit Tests. *Eff-me*. And I was running on a deadline. This was just a quick fix. JK, it actually had nothing to do with deadlines. My university teachers are so cool that they'd find millions ways to screw you only to leave you screeching on the ground until a train, or the effing shuttle cab(VIT things) runs you over.



**Face detection using an ML model ?? And also an API call for every image uploaded? BLASPHEMY !! You expect users to wait ? Eff-You!!**

Not exactly. I've got a secret weapon up my sleeve. 

**...Drumrolls….**

![alt text](https://github.com/bhaveshpraveen/auto-attendance/tree/master/readme_assets/god.jpg "My Idol")

And I've also used [Celery](http://www.celeryproject.org/). But mostly thanks to Chuck. He thought me to live with my pretty **coughs coughs** face. And I'd like to thank every one who made this moment possible, my dad, my mom, my neighbour's daughter, my …………No ? Okay.

Celery basically makes your application asynchronous. 



### To all the Noobs (future self)

1. Install the dependencies in the `requirements.txt` file.

```shell
pip install -r requirements.txt
```

2. Install OpenCV. (This one is effing tought. Exiting vim is easier.)

3. Download the model [here](https://www.cs.cmu.edu/%7Epeiyunh/tiny/hr_res101.mat)

4. After downloading

   ```shell
   python matconvnet_hr101_to_pickle.py 
           --matlab_model_path /path/to/pretrained_model 
           --weight_file_path  /path/to/pickle_file
   ```

   I shamelessly copied this from [here](https://github.com/cydonia999/Tiny_Faces_in_Tensorflow). If you prefer to follow the original source go [here](https://github.com/cydonia999/Tiny_Faces_in_Tensorflow). Do whatever but make sure that the pickle file is in the same folder as `tiny_face_eval` (Tiny_Faces_in_Tensorflow directory) and also name it as `pickle.pickle`

5.  Install [Redis](https://redis.io/)

6. Run redis

```shell
redis-server
```

7. Type in the following commands

```shell
python manage.py migrate
python manage.py runserver
```

8. Again in a separate terminal type this shit

```shell
celery -A auto_attendance worker -l DEBUG
```



### Credits

- The API's are heavily influenced by this [talk](https://www.youtube.com/watch?v=2LWheXmsmHg&t=1036s)
- [Django Rest Framework](http://www.django-rest-framework.org/)
- [Djoser](https://djoser.readthedocs.io/)
- [Anaconda](https://anaconda.org/)
- [Django](http://djangoproject.com/)
- And all other packages
- The friendly **coughs** community over at StackoverFlow.
-  And also this [Dickhead](https://github.com/MINOSai/). He made the android application.













