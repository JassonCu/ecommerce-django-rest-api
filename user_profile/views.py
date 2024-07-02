from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer

# Create your views here.

class GetUserProfileView(APIView):
    """
    Vista API para obtener el perfil de usuario.

    Permite a un usuario autenticado recuperar su propio perfil de usuario.
    """

    def get(self, request, format=None):
        """
        Maneja peticiones GET para obtener el perfil de usuario.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con el perfil de usuario o mensaje de error.

        Si el perfil de usuario se encuentra, devuelve una respuesta JSON con el perfil del usuario.
        Si el perfil de usuario no existe o no se puede recuperar, devuelve un mensaje de error correspondiente.
        """

        try:
            user = self.request.user
            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response(
                {'profile': user_profile.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateUserProfileView(APIView):
    """
    Vista API para actualizar el perfil de usuario.

    Permite a un usuario autenticado actualizar su propio perfil de usuario.
    """

    def put(self, request, format=None):
        """
        Maneja peticiones PUT para actualizar el perfil de usuario.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con el perfil de usuario actualizado o mensaje de error.

        Si el perfil de usuario se actualiza correctamente, devuelve una respuesta JSON con el perfil actualizado.
        Si hay campos faltantes en la solicitud PUT o se produce un error durante la actualización, devuelve un mensaje de error correspondiente.
        """
        
        try:
            user = self.request.user
            data = self.request.data

            address_line_1 = data['address_line_1']
            address_line_2 = data['address_line_2']
            city = data['city']
            state_province_region = data['state_province_region']
            zipcode = data['zipcode']
            phone = data['phone']
            country_region = data['country_region']

            UserProfile.objects.filter(user=user).update(
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state_province_region=state_province_region,
                zipcode=zipcode,
                phone=phone,
                country_region=country_region
            )

            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response(
                {'profile': user_profile.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when updating profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )