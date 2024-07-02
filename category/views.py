from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Category

# Create your views here.

class ListCategoriesView(APIView):
    """
    API endpoint para listar todas las categorías y sus subcategorías.

    Este endpoint devuelve una lista de todas las categorías principales
    junto con sus subcategorías anidadas, si las hay.
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        """
        Obtiene todas las categorías y subcategorías existentes.

        Returns:
            Response: Lista de categorías y sus subcategorías o mensaje de error si no hay categorías.
        """
        
        if Category.objects.all().exists():
            categories = Category.objects.all()

            result = []

            for category in categories:
                if not category.parent:
                    item = {}
                    item['id'] = category.id
                    item['name'] = category.name
                    
                    item['sub_categories'] = []
                    for cat in categories:
                        sub_item = {}
                        if cat.parent and cat.parent.id == category.id:
                            sub_item['id'] = cat.id
                            sub_item['name'] = cat.name
                            sub_item['sub_categories'] = []

                            item['sub_categories'].append(sub_item)
                    result.append(item)
            return Response({'categories': result}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No categories found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)