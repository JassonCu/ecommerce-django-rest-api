from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Shipping
from .serializers import ShippingSerializer

# Create your views here.


class GetShippingView(APIView):
    """
    Vista API para obtener opciones de envío.

    Este endpoint permite la obtención de opciones de envío ordenadas por precio.
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        """
        Maneja peticiones GET para obtener opciones de envío.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con opciones de envío o mensaje de error.

        Si existen opciones de envío, devuelve una respuesta JSON con una lista de opciones
        de envío ordenadas por precio.
        Si no existen opciones de envío, devuelve una respuesta JSON con un mensaje de error
        indicando que no hay opciones de envío disponibles.
        """

        if Shipping.objects.all().exists():
            shipping_options = Shipping.objects.order_by('price').all()
            shipping_options = ShippingSerializer(shipping_options, many=True)

            return Response(
                {'shipping_options': shipping_options.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'No shipping options available'},
                status=status.HTTP_404_NOT_FOUND
            )
