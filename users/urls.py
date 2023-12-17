from django.urls import path
from . import views
from .views import ImageToTextView

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('text-generator/', views.TextGeneratorView.as_view(), name='text_generator'),
    path('image-to-text/', ImageToTextView.as_view(), name='image_to_text'),
]
