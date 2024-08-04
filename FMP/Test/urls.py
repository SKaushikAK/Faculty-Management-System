from django.urls import path
from Testing.views import *

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('upload_single/', upload_detail),
    path('success/',suc),
    path('home/',home),
    path('search/',search),
    path('delete/',delete),
    path('delete_data/',delete_data),
    path('delete_search_data/',delete_search_data),
    path('',ma), 
    path('faculty/',faculty),
    path('update_faculty/<int:faculty_id>/', update_faculty, name='update_faculty'),
    path('search1/', search_view)
    # Add other URLs as needed
]
