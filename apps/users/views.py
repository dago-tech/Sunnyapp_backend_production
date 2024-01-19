from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateAPIView(generics.CreateAPIView):
    """
    Crear un nuevo usuario si sus datos son válidos
    """
    serializer_class = CustomUserSerializer

    def post(self, request, format="json"):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListAPIView(generics.ListAPIView):
    """
    Lista de usuarios usando el método GET
    """
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class GetUserEmailAPIView(APIView):
    """
    Obtiene el email del user_id que reciba en los parametros de la solicitud
    """
    serializer_class = CustomUser

    def get(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        user = CustomUser.objects.filter(id=user_id).first()

        if user is not None:
            email = user.email
            return Response(email, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class BlacklistTokenUpdateView(APIView):
    """
    Guarda el token de refresco en la base de datos para que no vuelva a ser usado
    """

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)