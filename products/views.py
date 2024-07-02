from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from products.models import Product
from products.serializers import ProductSerializer
from category.models import Category
from django.db.models import Q

# Create your views here.


class ProductDetailView(APIView):
    """
    Vista para obtener detalles de un producto específico por su ID.
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        """
        Obtiene los detalles de un producto.

        Parámetros:
        - productId: ID del producto (entero).

        Retorna:
        - 200 OK: Detalles del producto en formato JSON.
        - 404 Not Found: Si el producto con el ID proporcionado no existe o el ID es inválido.
        """
        try:
            product_id = int(productId)
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)

            product = ProductSerializer(product)

            return Response({'product': product.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Product with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class ListProductsView(APIView):
    """
    Vista para listar productos con opciones de ordenamiento y límite.
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        """
        Lista productos con opciones de ordenamiento y límite.

        Parámetros de Consulta:
        - sortBy: Campo por el cual ordenar los productos ('date_created', 'price', 'sold', 'name').
        - order: Orden de los productos ('asc' para ascendente, 'desc' para descendente).
        - limit: Número máximo de productos a retornar (entero).

        Retorna:
        - 200 OK: Lista de productos en formato JSON según los parámetros especificados.
        - 404 Not Found: Si no se encuentran productos que coincidan con los criterios.
        """

        sortBy = request.query_params.get('sortBy')

        if not (sortBy == 'date_created' or sortBy == 'price' or sortBy == 'sold' or sortBy == 'name'):
            sortBy = 'date_created'

        order = request.query_params.get('order')
        limit = request.query_params.get('limit')

        if not limit:
            limit = 6

        try:
            limit = int(limit)
        except:
            return Response(
                {'error': 'Limit must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        if limit <= 0:
            limit = 6

        if order == 'desc':
            sortBy = '-' + sortBy
            products = Product.objects.order_by(sortBy).all()[:int(limit)]
        elif order == 'asc':
            products = Product.objects.order_by(sortBy).all()[:int(limit)]
        else:
            products = Product.objects.order_by(sortBy).all()

        products = ProductSerializer(products, many=True)

        if products:
            return Response({'products': products.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'No products to list'},
                status=status.HTTP_404_NOT_FOUND)


class ListSearchView(APIView):
    """
    Vista para realizar búsquedas filtradas de productos por nombre, descripción y/o categoría.
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        """
        Realiza una búsqueda filtrada de productos.

        Parámetros de Entrada (en el cuerpo de la solicitud):
        - search: Cadena de búsqueda para buscar en el nombre o descripción del producto.
        - category_id: ID de la categoría por la cual filtrar los productos (entero).

        Retorna:
        - 200 OK: Productos que coinciden con los criterios de búsqueda y filtros aplicados en formato JSON.
        - 404 Not Found: Si la categoría especificada no existe o si el ID de la categoría no es válido.
        """

        data = self.request.data

        try:
            category_id = int(data['category_id'])
        except:
            return Response(
                {'error': 'Category ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        search = data['search']

        # Chequear si algo input ocurrio en la busqueda
        if len(search) == 0:
            # mostrar todos los productos si no hay input en la busqueda
            search_results = Product.objects.order_by('-date_created').all()
        else:
            # Si hay criterio de busqueda, filtramos con dicho criterio usando Q
            search_results = Product.objects.filter(
                Q(description__icontains=search) | Q(name__icontains=search)
            )

        if category_id == 0:
            search_results = ProductSerializer(search_results, many=True)
            return Response(
                {'search_products': search_results.data},
                status=status.HTTP_200_OK)

        # revisar si existe categoria
        if not Category.objects.filter(id=category_id).exists():
            return Response(
                {'error': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND)

        category = Category.objects.get(id=category_id)

        # si la categoria tiene apdre, fitlrar solo por la categoria y no el padre tambien
        if category.parent:
            search_results = search_results.order_by(
                '-date_created'
            ).filter(category=category)

        else:
            # si esta categoria padre no tiene hijjos, filtrar solo la categoria
            if not Category.objects.filter(parent=category).exists():
                search_results = search_results.order_by(
                    '-date_created'
                ).filter(category=category)

            else:
                categories = Category.objects.filter(parent=category)
                filtered_categories = [category]

                for cat in categories:
                    filtered_categories.append(cat)

                filtered_categories = tuple(filtered_categories)

                search_results = search_results.order_by(
                    '-date_created'
                ).filter(category__in=filtered_categories)

        search_results = ProductSerializer(search_results, many=True)
        return Response({'search_products': search_results.data}, status=status.HTTP_200_OK)


class ListRelatedView(APIView):
    """
    Vista para obtener productos relacionados a partir del ID de un producto dado.
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        """
        Obtiene productos relacionados a partir del ID de un producto dado.

        Parámetros:
        - productId: ID del producto del cual se desean obtener productos relacionados (entero).

        Retorna:
        - 200 OK: Productos relacionados en formato JSON.
        - 404 Not Found: Si no se encuentra el producto con el ID proporcionado o si no hay productos relacionados.
        """

        try:
            product_id = int(productId)
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        # Existe product id
        if not Product.objects.filter(id=product_id).exists():
            return Response(
                {'error': 'Product with this product ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)

        category = Product.objects.get(id=product_id).category

        if Product.objects.filter(category=category).exists():
            # Si la categoria tiene padrem filtrar solo por la categoria y no el padre tambien
            if category.parent:
                related_products = Product.objects.order_by(
                    '-sold'
                ).filter(category=category)
            else:
                if not Category.objects.filter(parent=category).exists():
                    related_products = Product.objects.order_by(
                        '-sold'
                    ).filter(category=category)

                else:
                    categories = Category.objects.filter(parent=category)
                    filtered_categories = [category]

                    for cat in categories:
                        filtered_categories.append(cat)

                    filtered_categories = tuple(filtered_categories)
                    related_products = Product.objects.order_by(
                        '-sold'
                    ).filter(category__in=filtered_categories)

            # Excluir producto que estamos viendo
            related_products = related_products.exclude(id=product_id)
            related_products = ProductSerializer(related_products, many=True)

            if len(related_products.data) > 3:
                return Response(
                    {'related_products': related_products.data[:3]},
                    status=status.HTTP_200_OK)
            elif len(related_products.data) > 0:
                return Response(
                    {'related_products': related_products.data},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'No related products found'},
                    status=status.HTTP_200_OK)

        else:
            return Response(
                {'error': 'No related products found'},
                status=status.HTTP_200_OK)


class ListBySearchView(APIView):
    """
    Vista para realizar búsquedas filtradas de productos por categoría, rango de precio y orden.
    """

    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        """
        Realiza una búsqueda filtrada de productos según los criterios especificados.

        Parámetros de Entrada (en el cuerpo de la solicitud):
        - category_id: ID de la categoría por la cual filtrar los productos (entero).
        - price_range: Rango de precios para filtrar los productos ('1 - 19', '20 - 39', '40 - 59', '60 - 79', 'More than 80').
        - sort_by: Campo por el cual ordenar los productos ('date_created', 'price', 'sold', 'name').
        - order: Orden de los productos ('asc' para ascendente, 'desc' para descendente).

        Retorna:
        - 200 OK: Productos filtrados que coinciden con los criterios en formato JSON.
        - 404 Not Found: Si la categoría especificada no existe o si no se encuentran productos que coincidan con los criterios.
        """
        
        data = self.request.data

        try:
            category_id = int(data['category_id'])
        except:
            return Response(
                {'error': 'Category ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        price_range = data['price_range']
        sort_by = data['sort_by']

        if not (sort_by == 'date_created' or sort_by == 'price' or sort_by == 'sold' or sort_by == 'name'):
            sort_by = 'date_created'

        order = data['order']

        # Si categoryID es = 0, filtrar todas las categorias
        if category_id == 0:
            product_results = Product.objects.all()
        elif not Category.objects.filter(id=category_id).exists():
            return Response(
                {'error': 'This category does not exist'},
                status=status.HTTP_404_NOT_FOUND)
        else:
            category = Category.objects.get(id=category_id)
            if category.parent:
                # Si la categoria tiene padrem filtrar solo por la categoria y no el padre tambien
                product_results = Product.objects.filter(category=category)
            else:
                if not Category.objects.filter(parent=category).exists():
                    product_results = Product.objects.filter(category=category)
                else:
                    categories = Category.objects.filter(parent=category)
                    filtered_categories = [category]

                    for cat in categories:
                        filtered_categories.append(cat)

                    filtered_categories = tuple(filtered_categories)
                    product_results = Product.objects.filter(
                        category__in=filtered_categories)

        # Filtrar por precio
        if price_range == '1 - 19':
            product_results = product_results.filter(price__gte=1)
            product_results = product_results.filter(price__lt=20)
        elif price_range == '20 - 39':
            product_results = product_results.filter(price__gte=20)
            product_results = product_results.filter(price__lt=40)
        elif price_range == '40 - 59':
            product_results = product_results.filter(price__gte=40)
            product_results = product_results.filter(price__lt=60)
        elif price_range == '60 - 79':
            product_results = product_results.filter(price__gte=60)
            product_results = product_results.filter(price__lt=80)
        elif price_range == 'More than 80':
            product_results = product_results.filter(price__gte=80)

        # Filtrar producto por sort_by
        if order == 'desc':
            sort_by = '-' + sort_by
            product_results = product_results.order_by(sort_by)
        elif order == 'asc':
            product_results = product_results.order_by(sort_by)
        else:
            product_results = product_results.order_by(sort_by)

        product_results = ProductSerializer(product_results, many=True)

        if len(product_results.data) > 0:
            return Response(
                {'filtered_products': product_results.data},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'No products found'},
                status=status.HTTP_404_NOT_FOUND)
