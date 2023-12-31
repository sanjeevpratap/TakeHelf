# settings.py

import spacy
from django.utils.deprecation import MiddlewareMixin

class SpaCyMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        # Load spaCy model during middleware initialization
        self.spacy_model = spacy.load('en_core_web_sm')

    def process_request(self, request):
        # Attach the spaCy model to the request
        request.spacy_model = self.spacy_model