import os
# import spacy
# from twapp.middleware import SpaCyMiddleware

from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'webapp' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweetme.settings')

# Load your spaCy model during middleware initialization
# SpaCyMiddleware.spacy_model = spacy.load('en_core_web_sm')

# Get the WSGI application
application = get_wsgi_application()
