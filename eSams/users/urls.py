from django.urls import path

from users.views import (SetProfileInfo, update_profileInfo, get_profile, get_user, get_lecturers, compare_faces_api)

urlpatterns = [
    path('SetProfileInfo/', SetProfileInfo.as_view(), name="SetProfileInfo"),
    path('updateProfileInfo/', update_profileInfo, name="updateProfileInfo"),
    path('getProfile/', get_profile, name="getProfile"),
    path('getUser/', get_user, name="getUser"),
    path('getLecturers/', get_lecturers, name="getLecturers"),
    path('compare_faces_api/', compare_faces_api, name="compare_faces_api"),

]