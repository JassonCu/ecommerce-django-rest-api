from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FixedPriceCoupon, PercentageCoupon
from .serializers import FixedPriceCouponSerializer, PercentageCouponSerializer

# Create your views here.


class CheckCouponView(APIView):
    """
    API endpoint para verificar la validez de un cupón por su nombre.

    Este endpoint permite verificar si un cupón existe y devuelve los detalles del cupón
    si se encuentra, ya sea un cupón de precio fijo o un cupón de porcentaje.
    """

    def get(self, request, format=None):
        
        """
        Verifica la existencia y detalles de un cupón por su nombre.

        Args:
            request: Objeto de solicitud HTTP.
            format: Formato de respuesta deseado (predeterminado es None).

        Returns:
            Response: Detalles del cupón si se encuentra, o mensaje de error si no se encuentra el cupón.
        """
        
        try:
            coupon_name = request.query_params.get('coupon_name')

            if FixedPriceCoupon.objects.filter(name=coupon_name).exists():
                coupon = FixedPriceCoupon.objects.get(name=coupon_name)
                coupon = FixedPriceCouponSerializer(coupon)

                return Response(
                    {'coupon': coupon.data},
                    status=status.HTTP_200_OK
                )
            elif PercentageCoupon.objects.filter(name=coupon_name).exists():
                coupon = PercentageCoupon.objects.get(name=coupon_name)
                coupon = PercentageCouponSerializer(coupon)

                return Response(
                    {'coupon': coupon.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Coupon code not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except:
            return Response(
                {'error': 'Something went wrong when checking coupon'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
