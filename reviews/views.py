from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from products.models import Product
from .models import Review

# Create your views here.


class GetProductReviewsView(APIView):
    """
    Vista API para obtener todas las reseñas de un producto.

    Permite obtener todas las reseñas de un producto específico ordenadas por fecha de creación.
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        """
        Maneja peticiones GET para obtener reseñas de un producto.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - productId: ID del producto del cual se desean obtener las reseñas.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con reseñas del producto solicitado o mensaje de error.

        Si el producto existe y tiene reseñas, devuelve una respuesta JSON con la lista de reseñas
        ordenadas por fecha de creación.
        Si el producto no existe o no tiene reseñas, devuelve una respuesta JSON con un mensaje de
        error correspondiente.
        """

        try:
            product_id = int(productId)
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.get(id=product_id)

            results = []

            if Review.objects.filter(product=product).exists():
                reviews = Review.objects.order_by(
                    '-date_created'
                ).filter(product=product)

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['comment'] = review.comment
                    item['date_created'] = review.date_created
                    item['user'] = review.user.first_name

                    results.append(item)

            return Response(
                {'reviews': results},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'error': 'Something went wrong when retrieving reviews'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetProductReviewView(APIView):
    """
    Vista API para obtener una reseña de un producto por un usuario específico.

    Permite obtener la reseña de un producto realizada por un usuario específico.
    """

    def get(self, request, productId, format=None):
        """
        Maneja peticiones GET para obtener una reseña de un producto por un usuario.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - productId: ID del producto del cual se desea obtener la reseña.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con la reseña del producto o mensaje de error.

        Si la reseña existe, devuelve una respuesta JSON con los detalles de la reseña.
        Si la reseña no existe, devuelve una respuesta JSON con un mensaje de error indicando
        que la reseña no fue encontrada.
        """

        user = self.request.user

        try:
            product_id = int(productId)
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.get(id=product_id)

            result = {}

            if Review.objects.filter(user=user, product=product).exists():
                review = Review.objects.get(user=user, product=product)

                result['id'] = review.id
                result['rating'] = review.rating
                result['comment'] = review.comment
                result['date_created'] = review.date_created
                result['user'] = review.user.first_name

            return Response(
                {'review': result},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving review'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateProductReviewView(APIView):
    """
    Vista API para crear una nueva reseña de un producto.

    Permite a un usuario crear una nueva reseña para un producto especificado.
    """

    def post(self, request, productId, format=None):
        """
        Maneja peticiones POST para crear una nueva reseña de un producto.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - productId: ID del producto para el cual se crea la reseña.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con la nueva reseña creada o mensaje de error.

        Si la reseña se crea con éxito, devuelve una respuesta JSON con los detalles de la nueva reseña.
        Si no se proporciona la información necesaria para crear la reseña o si ya existe una reseña para
        el producto por el usuario, devuelve un mensaje de error correspondiente.
        """

        user = self.request.user
        data = self.request.data

        try:
            rating = float(data['rating'])
        except:
            return Response(
                {'error': 'Rating must be a decimal value'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            comment = str(data['comment'])
        except:
            return Response(
                {'error': 'Must pass a comment when creating review'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if not Product.objects.filter(id=productId).exists():
                return Response(
                    {'error': 'This Product does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.get(id=productId)

            result = {}
            results = []

            if Review.objects.filter(user=user, product=product).exists():
                return Response(
                    {'error': 'Review for this course already created'},
                    status=status.HTTP_409_CONFLICT
                )

            review = Review.objects.create(
                user=user,
                product=product,
                rating=rating,
                comment=comment
            )

            if Review.objects.filter(user=user, product=product).exists():
                result['id'] = review.id
                result['rating'] = review.rating
                result['comment'] = review.comment
                result['date_created'] = review.date_created
                result['user'] = review.user.first_name

                reviews = Review.objects.order_by('-date_created').filter(
                    product=product
                )

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['comment'] = review.comment
                    item['date_created'] = review.date_created
                    item['user'] = review.user.first_name

                    results.append(item)

            return Response(
                {'review': result, 'reviews': results},
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {'error': 'Something went wrong when creating review'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateProductReviewView(APIView):
    """
    Vista API para actualizar una reseña de un producto.

    Permite a un usuario actualizar una reseña existente para un producto especificado.
    """

    def put(self, request, productId, format=None):
        """
        Maneja peticiones PUT para actualizar una reseña de un producto.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - productId: ID del producto para el cual se actualiza la reseña.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con la reseña actualizada o mensaje de error.

        Si la reseña se actualiza con éxito, devuelve una respuesta JSON con los detalles de la reseña actualizada.
        Si la reseña no existe o no se proporciona la información necesaria para actualizarla, devuelve un mensaje
        de error correspondiente.
        """

        user = self.request.user
        data = self.request.data

        try:
            product_id = int(productId)
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            rating = float(data['rating'])
        except:
            return Response(
                {'error': 'Rating must be a decimal value'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            comment = str(data['comment'])
        except:
            return Response(
                {'error': 'Must pass a comment when creating review'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.get(id=product_id)

            result = {}
            results = []

            if not Review.objects.filter(user=user, product=product).exists():
                return Response(
                    {'error': 'Review for this product does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if Review.objects.filter(user=user, product=product).exists():
                Review.objects.filter(user=user, product=product).update(
                    rating=rating,
                    comment=comment
                )

                review = Review.objects.get(user=user, product=product)

                result['id'] = review.id
                result['rating'] = review.rating
                result['comment'] = review.comment
                result['date_created'] = review.date_created
                result['user'] = review.user.first_name

                reviews = Review.objects.order_by('-date_created').filter(
                    product=product
                )

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['comment'] = review.comment
                    item['date_created'] = review.date_created
                    item['user'] = review.user.first_name

                    results.append(item)

            return Response(
                {'review': result, 'reviews': results},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when updating review'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteProductReviewView(APIView):
    """
    Vista API para eliminar una reseña de un producto.

    Permite a un usuario eliminar su reseña existente para un producto especificado.
    """

    def delete(self, request, productId, format=None):
        """
        Maneja peticiones DELETE para eliminar una reseña de un producto.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - productId: ID del producto para el cual se elimina la reseña.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con las reseñas actualizadas después de la eliminación o mensaje de error.

        Si la reseña se elimina con éxito, devuelve una respuesta JSON con las reseñas actualizadas
        del producto.
        Si la reseña no existe o no se proporciona la información necesaria para eliminarla, devuelve
        un mensaje de error correspondiente.
        """

        user = self.request.user

        try:
            product_id = int(productId)
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.get(id=product_id)

            results = []

            if Review.objects.filter(user=user, product=product).exists():
                Review.objects.filter(user=user, product=product).delete()

                reviews = Review.objects.order_by('-date_created').filter(
                    product=product
                )

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['comment'] = review.comment
                    item['date_created'] = review.date_created
                    item['user'] = review.user.first_name

                    results.append(item)

                return Response(
                    {'reviews': results},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Review for this product does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except:
            return Response(
                {'error': 'Something went wrong when deleting product review'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FilterProductReviewsView(APIView):
    """
    Vista API para filtrar reseñas de un producto por valoración.

    Permite filtrar reseñas de un producto específico según un valor de valoración específico.
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        """
        Maneja peticiones GET para filtrar reseñas de un producto por valoración.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - productId: ID del producto del cual se desean filtrar las reseñas.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con las reseñas filtradas del producto o mensaje de error.

        Si las reseñas existen y se filtran según la valoración, devuelve una respuesta JSON con la lista
        de reseñas filtradas.
        Si el producto no existe o no se proporciona una valoración válida, devuelve un mensaje de error
        correspondiente.
        """
        
        try:
            product_id = int(productId)
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not Product.objects.filter(id=product_id).exists():
            return Response(
                {'error': 'This product does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        product = Product.objects.get(id=product_id)

        rating = request.query_params.get('rating')

        try:
            rating = float(rating)
        except:
            return Response(
                {'error': 'Rating must be a decimal value'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if not rating:
                rating = 5.0
            elif rating > 5.0:
                rating = 5.0
            elif rating < 0.5:
                rating = 0.5

            results = []

            if Review.objects.filter(product=product).exists():
                if rating == 0.5:
                    reviews = Review.objects.order_by('-date_created').filter(
                        rating=rating, product=product
                    )
                else:
                    reviews = Review.objects.order_by('-date_created').filter(
                        rating__lte=rating,
                        product=product
                    ).filter(
                        rating__gte=(rating - 0.5),
                        product=product
                    )

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['comment'] = review.comment
                    item['date_created'] = review.date_created
                    item['user'] = review.user.first_name

                    results.append(item)

            return Response(
                {'reviews': results},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when filtering reviews for product'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
