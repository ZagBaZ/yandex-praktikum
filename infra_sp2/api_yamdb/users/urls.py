from django.urls import path


from api.v1.views import (
    auth_token,
    get_confirmation_code
)

app_name = 'users'

urlpatterns = [
    path('signup/', get_confirmation_code),
    path('token/', auth_token),
]
