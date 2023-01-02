import json

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CloudTokenObtainPairSerializer
from rest_framework.views import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User


# Create your views here.
class CloudTokenObtainPairView(TokenObtainPairView):
    serializer_class = CloudTokenObtainPairSerializer


@csrf_exempt
@api_view(["PUT"])
def update(request):
    body = json.loads(request.body.decode("utf-8"))
    if (
        "password" not in body
        or "first_name" not in body
        or "last_name" not in body
        or "id" not in body
    ):
        return Response(
            {
                "error": [
                    "Missing required fields password, first_name, last_name, id."
                ]
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.filter(id=body["id"]).first()
    if not user:
        return Response(
            {"user_id": ["user id is incorrect."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(body["password"])
    user.first_name = body["first_name"]
    user.last_name = body["last_name"]
    user.save()
    return Response({}, status=status.HTTP_200_OK)
