# TODO notes

# stablize app!
review 
docker-compose configuration
urls
# look into automated
adding users 

restuser
gendo
brand0n

from src.users.models import User


# from django.contrib.auth.models import User

def config_dev():
    user=User.objects.create_user('gendo', password='lucie')
    user.is_superuser=True
    user.is_staff=True
    user.save()
    user=User.objects.create_user('restsuper', password='lucie')
    user.is_superuser=True
    user.is_staff=True
    user.save()
    user=User.objects.create_user('restuser', password='brandon')
    user.is_superuser=false
    user.is_staff=True
    user.save()

config_dev()



# adding folder to nginx
- file permissions set correctly
- location added to  app.conf
- order of location in app.conf
- verify .htacess?
- restart nginx
# adding folder to nginx - docker considerations
- add volume to docker-compose.yml
- ** WARINING ** -if adding volume containers must be recreated! 
- i.e stop containers and verify removed



# angular notes
scp -r -i "~/.ssh/cloud_key.pem" ~/dev/code/blog-angular/dist/ ec2-user@ec2-44-205-48-243.compute-1.amazonaws.com:/home/ec2-user/python-django-drf-starter/angular/

scp -r -i "~/.ssh/cloud_key.pem" ~/dev/code/blog-angular/dist/* ec2-user@ec2-44-205-48-243.compute-1.amazonaws.com:/home/ec2-user/python-django-drf-starter/angular/

# let's encrypt notes:
# clone github repo

https://github.com/wmnnd/nginx-certbot.git (push)

- update files
init-letsencrypt.sh
data/nginx/app.conf



# Readme

Hello and Welcome!
 

My name is Brandon. Thank you for your visit today.

 

On this secure site (hosted on AWS) you will find an online porfolio of my work (utilizing utlizing docker, nginx, postgres, DJango Rest Framework) that serves a couple of purposes

- to share software development knowledge/concepts with my peers and

- to tangibly demonstrate some of capabilities/skills I possess with non-proprietary code and live server sample.

Before we get to the description of the projects, I would like to thank all of the contributors of open source code that have made these projects possible in such a short amount of time!

Please find the following projects

    CSharp language documentation - This material (more than 45 articles on CSharp language features with code examples) was originally published some years ago when I found online resources/documentation lacking.

    GitHub Source Code Repository for a Sample Rest API - a fork and modification to add a simple api Github REST Framework project (Python)

    Test Coverage for Sample Rest API code - of particular interest is test cases in the src/taskapi folder.

    Live secure working deployment of the Sample REST API with documentation.  Try it!

 

I plan to add more references in the future.  Please feel free to contact me with comments or questions.

 

 

Regards,

Brandon D’Souza


** Please note some minor modifications of the following configuration files to minimize and enhance "sample live deployment".

        modified:   docker-compose.yml
        modified:   src/config/common.py
        modified:   src/urls.py


# swagger image update
.topbar-wrapper img[alt="Swagger UI"], .topbar-wrapper span {
    visibility: collapse;
}

.topbar-wrapper .link:before {
    content: url('/blog/assets/cs.jpg');
}

# swagger favicon location
static/drf-yasg/swagger-ui-dist/favicon-32x32.png


# project location


https://github.com/Vivify-Ideas/python-django-drf-boilerplate

# github dev ops REST automation goals per commit
- opinioned formatting (black)
- test coverage report
- versioning
- easily deployable "commit environment spin up" 

# django rest framework querydef, permissions notes

when calculating applicable permissions (apply the following)
- consider querydef filtering data (eg by user) may result in 404
permissions can be
- applied to endpoint (eg IsAuthenticated, or AllowAny)
- applied on data after querydef filter (eg creater/owner permission)

# reset migrations

python manage.py taskapi zero
python manage.py taskapi showmigrations
python manage.py makemigrations
python manage.py migrate

# adding to swagger framework

# task app rest api recipe
create a model with lots of default behavior 
- app
python manage startapp taskapp
- model
define task in models.py
- serializer
define 2 serializers - create and default
- permissions
define access to model
- view
define view in views.py
create viewset(s), pass in "mixins" and , viewsets.GenericViewSet

- register urls
define router and register in urls.py
tasks_router = SimpleRouter()
tasks_router.register(r'tasks', TaskDetailViewSet)

in project/main url.py  
from src.taskapi.urls import tasks_router
router.registry.extend(tasks_router.registry)

- admin
register to view/modify Task in admin site
admin.site.register(Task)

# boilerplate test coverage notes
coverage run ./manage.py test
output to screen:
coverage -m 
out in html (htmlcov folder)
coverage html


# codespace notes

# minmimally create user & log in
./manage.py createsuperuser

# set .env DB_HOST to access progressdb container
DB_HOST=host.docker.internal

# dev config/environment possibilities 

1) ability to quickly test rest api
dev container code space!
no db?

2) ability to test rest api in container


3) ability to test rest api against container


# critical need

item 1


curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "restuser", "password": "restuser"}' \
  http://localhost:80/api/token/ > cresponse.html


host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("Hostname :  ",host_name)
print("IP : ",host_ip)

from django.apps import apps
from django.conf import settings

User = apps.get_model(settings.AUTH_USER_MODEL)
users = User.objects.all()

from taskapi.models import Task
Task = apps.get_model(Task)
tasks = Task.objects.all()


    User.create_user(username="createuser",  email="createuser@someprovider.com", password="createuser")



# pre-requiste

apt get-update
apt install python3.8-venv

python, django installed,  postgress db available via docker?

# create folder
mkdir django

# add requirements.txt

Django==2.1.4
djangorestframework==3.9.0
psycopg2

# install dependencies
pip install -r /requirements.txt

# Modify todoproj/settings.py in the Django Project.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'host.docker.internal',
        'PORT': 5432,
    }
}


# create "django project"
django-admin.py startproject todoproj .


# create "django app"
python manage.py startapp taskapi

# create data model (taskapi/models.py)
from django.db import models

from datetime import date

# Create the Task class to describe the model.
class Task(models.Model):
    """Stores a task."""
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=50)

    # Date the task was created.
    created_on = models.DateField(default=date.today)

    # Due date.
    due_date = models.DateField(default=date.today)

    # Meta data about the database table.
    class Meta:
        # Set the table name.
        db_table = 'task'

        # Set default ordering
        ordering = ['id']

    # Define what to output when the model is printed as a string.
    def __str__(self):
        return self.title

# Modify todoproj/settings.py 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'taskapi',
]

# make migrations initial
python manage.py makemigrations

# create serializer file taskapi/serializers.py containing:
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'content', 'created_on',  'due_date')

# make migrations
python manage.py migrate

# Create a new file taskapi/serializers.py containing:

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'content', 'created_on',  'due_date')


# Creating the API View (taskapi/views.py)

from .models import Task
from .serializers import TaskSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

class TaskList(APIView):
    """
    View all tasks.
    """
    def get(self, request, format=None):
        """
        Return a list of all tasks.
        """
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

# Create dummy data migration file
python manage.py makemigrations --empty taskapi --name dummy_tasks

# change taskapi/migrations/0002_dummy_tasks.py 
from django.db import migrations

def create_dummy_tasks(apps, schema_editor):
    Task = apps.get_model('taskapi', 'Task')

    Task(title='Workout', content='Squat, bench press, deadlift.').save()
    Task(title='Shopping', content='Whey protein, creatine, BCAAs.').save()
    Task(title='Counting', content='1, 2, 3 and so on.').save()

class Migration(migrations.Migration):

    dependencies = [
        ('taskapi', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_dummy_tasks),
    ]

# apply (dummy) migration file
python manage.py migrate


# map the new view to a URL, so edit todoproj/urls.py:
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/task/', taskapi_views.TaskList.as_view(), name='task-list'),
    path('api/task/<int:task_id>/', taskapi_views.TaskDetail.as_view(), name='task-detail'),
] 


# **** CORS in django project ****

# Add django-cors-headers to django/requirements.txt:
Django==2.1.4
djangorestframework==3.9.0
django-cors-headers==3.2.1
psycopg2

# add the corsheaders app to todoproj/settings.py:
INSTALLED_APPS = [
	[...]
	'corsheaders',
]

# add corsheaders.middleware.CorsMiddleware to the middleware list in todoproj/settings.py:
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    [...]
]

# add CORS_ORIGIN_WHITELIST section following at the end of the file todoproj/settings.py, :
CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
    'http://localhost:8080',
)


# HOARDER!

docker run -v /host/path/to/certs:/container/path/to/certs -d 2644fdf13037 "update-ca-certificates"
c2-18-209-168-49.compute-1.amazonaws.com 


https://bansalanuj.com/https-aws-ec2-without-custom-domain

44.205.48.243.nip.io {
    reverse_proxy localhost:8000
}


sudo hostnamectl set-hostname brandon-ec2.localdomain

HOSTNAME=brandon-ec2.localdomain

127.0.0.1 brandon-ec2.localdomain brandon-ec2 localhost4 localhost4.localdomain4

127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4



ns-663.awsdns-18.net.
ns-1655.awsdns-14.co.uk.
ns-208.awsdns-26.com.
ns-1339.awsdns-39.org.


ns-1655.awsdns-14.co.uk

ns.inmotionhosting.com
ns2.inmotionhosting.com


docker run \
  -v certbot_conf:/etc/letsencrypt \
  -v acme-challenge:/var/www/challenge/.well-known/acme-challenge \
  --name certbot \
  "certbot/certbot" \
  certonly --webroot -w /var/www/challenge -d code-sage.com -m brandon@associationwebdesign.com --agree-tos

       location /api {
                uwsgi_pass 127.0.0.1:8001;


    location /api {
      proxy_pass 127.0.0.1:8001;
      rewrite ^/api(.*)$ $1 break;
    }
 


  nginx:
    image: nginx:1.15-alpine
    restart: unless-stopped
    volumes:
      - ./data/nginx:/etc/nginx/conf.d
      - ./data/certbot/conf:/etc/letsencrypt
      - ./data/certbot/www:/var/www/certbot
    ports:
      - "80:80"
      - "443:443"
    command: "/bin/sh -c 'while :; do sleep 6h & wait $${!}; nginx -s reload; done & nginx -g \"daemon off;\"'"
  certbot:
    image: certbot/certbot
    restart: unless-stopped
    volumes:
      - ./data/certbot/conf:/etc/letsencrypt
      - ./data/certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"


upstream web {
    server web:8001;
}

   location / {
        proxy_pass         http://web;
        proxy_redirect     off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
    }

location /blog/ {    
    autoindex on;    
    alias ./blog/; 
}


VALIDATOR_URL


doc_expansion
enabled_methods
exclude_url_names
exclude_namespaces
info
is_authenticated
is_superuser
unauthenticated_user
permission_denied_handler
relative_paths
resource_access_handler
token_type
YAML Docstring
Miscellaneous
Examples
Sponsored: Sourcegraph
Learn the 5 key elements for a successful monolith to microservices migration. 5 minute read.
Ad by EthicalAds   ·   Host these ads
Docs » SWAGGER_SETTINGS Edit on GitHub
SWAGGER_SETTINGS
A dictionary containing all configuration of django-rest-swagger.

Example:

SWAGGER_SETTINGS = {
	SwaggerUI

    'exclude_url_names': [],
    'exclude_namespaces': [],
    'api_version': '0.1',
    'api_path': '/',
    'relative_paths': False,
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
    'permission_denied_handler': None,
    'resource_access_handler': None,
    'base_path':'helloreverb.com/docs',
    'info': {
        'contact': 'apiteam@wordnik.com',
        'description': 'This is a sample server Petstore server. '
                       'You can find out more about Swagger at '
                       '<a href="http://swagger.wordnik.com">'
                       'http://swagger.wordnik.com</a> '
                       'or on irc.freenode.net, #swagger. '
                       'For this sample, you can use the api key '
                       '"special-key" to test '
                       'the authorization filters',
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'termsOfServiceUrl': 'http://helloreverb.com/terms/',
        'title': 'Swagger Sample App',
    },
    'doc_expansion': 'none',
}
https://code-sage.com/accounts/l'