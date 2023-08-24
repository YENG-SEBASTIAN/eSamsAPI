from django.urls import path

from users.views import (SetProfileInfo, update_profileInfo,  
                         get_profile, get_user, get_all_user,
                        compare_faces_api, get_all_userProfileInfo,
                         )

urlpatterns = [
    path('SetProfileInfo/', SetProfileInfo.as_view(), name="SetProfileInfo"),
    path('updateProfileInfo/', update_profileInfo, name="updateProfileInfo"),

    path('getProfile/', get_profile, name="getProfile"),
    path('getUser/', get_user, name="getUser"),
    path('allUsers/', get_all_user, name="allUsers"),
    path('get_all_userProfileInfo/', get_all_userProfileInfo, name="get_all_userProfileInfo"),
    
    path('compare_faces_api/', compare_faces_api, name="compare_faces_api"),

]


        # return StreamingHttpResponse(content_type="multiple/x-mixed-replace;boundary=frame")
