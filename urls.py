from django.urls import path
from otree.urls import urlpatterns
import instructions.pages


urlpatterns.append(path('static_instructions/', instructions.pages.static_instructions))
