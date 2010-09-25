from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User

import sampleapp.models
from sampleapp.models import BlogPost

def load_sample_data(signal, sender, app, created_models, **kwargs):
    sample_users = [{'username':'jack',
                     'email':'jack@example.com',
                     'password':'jack'},
                    {'username':'jill',
                     'email':'jill@example.com',
                     'password':'jill'}]
    for user in sample_users:
        try:
            User.objects.get(username=user['username'])
        except User.DoesNotExist:
            User.objects.create_user(**user)

    sample_data = [{'slug':'fun-stuff',
                    'title':'Fun Stuff!',
                    'body':'This is the fun stuff blog post',
                    'author':User.objects.get(username='jack')},
                   {'slug':'sweetness-is-great',
                    'title':'Sweetness is Great!',
                    'body':'Sweetness is a great way to do class based views in Django.',
                    'author':User.objects.get(username='jill')},]
    for data in sample_data:
        BlogPost.objects.get_or_create(**data)

post_syncdb.connect(load_sample_data, sender=sampleapp.models)
