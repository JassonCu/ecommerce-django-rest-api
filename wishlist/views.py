from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart, CartItem
from .models import WishList, WishListItem
from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.

class GetItemsView(APIView):
    """
    Vista API para obtener los elementos de la lista de deseos de un usuario.

    Permite a un usuario autenticado recuperar todos los elementos de su lista de deseos.
    """

    def get(self, request, format=None):
        """
        Maneja peticiones GET para obtener los elementos de la lista de deseos.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con los elementos de la lista de deseos o mensaje de error.

        Si la lista de deseos y sus elementos se encuentran, devuelve una respuesta JSON con los elementos de la lista de deseos.
        Si la lista de deseos no existe o no se pueden recuperar sus elementos, devuelve un mensaje de error correspondiente.
        """

        user = self.request.user

        try:
            wishlist = WishList.objects.get(user=user)
            wishlist_items = WishListItem.objects.filter(wishlist=wishlist)
            result = []

            if WishListItem.objects.filter(wishlist=wishlist).exists():
                for wishlist_item in wishlist_items:
                    item = {}
                    item['id'] = wishlist_item.id
                    product = Product.objects.get(id=wishlist_item.product.id)
                    product = ProductSerializer(product)
                    item['product'] = product.data
                    result.append(item)
            return Response(
                {'wishlist': result},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving wishlist items'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddItemView(APIView):
    """
    Vista API para añadir un elemento a la lista de deseos de un usuario.

    Permite a un usuario autenticado añadir un producto específico a su lista de deseos.
    """

    def post(self, request, format=None):
        """
        Maneja peticiones POST para añadir un elemento a la lista de deseos.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con los elementos de la lista de deseos actualizados o mensaje de error.

        Si el producto se añade correctamente a la lista de deseos, devuelve una respuesta JSON con los elementos actualizados.
        Si el producto no existe, ya está en la lista de deseos o se produce algún error durante el proceso, devuelve un mensaje de error correspondiente.
        """
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])
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
            wishlist = WishList.objects.get(user=user)

            if WishListItem.objects.filter(wishlist=wishlist, product=product).exists():
                return Response(
                    {'error': 'Item already in wishlist'},
                    status=status.HTTP_409_CONFLICT
                )

            WishListItem.objects.create(
                product=product,
                wishlist=wishlist
            )

            if WishListItem.objects.filter(product=product, wishlist=wishlist).exists():
                total_items = int(wishlist.total_items) + 1
                WishList.objects.filter(user=user).update(
                    total_items=total_items
                )

                cart = Cart.objects.get(user=user)
            
                if CartItem.objects.filter(cart=cart, product=product).exists():
                    CartItem.objects.filter(
                        cart=cart,
                        product=product
                    ).delete()

                    if not CartItem.objects.filter(cart=cart, product=product).exists():
                        # actualizar items totales ene l carrito
                        total_items = int(cart.total_items) - 1
                        Cart.objects.filter(user=user).update(
                            total_items=total_items
                        )

            wishlist_items = WishListItem.objects.filter(wishlist=wishlist)
            result = []

            for wishlist_item in wishlist_items:
                item = {}

                item['id'] = wishlist_item.id
                product = Product.objects.get(id=wishlist_item.product.id)
                product = ProductSerializer(product)

                item['product'] = product.data

                result.append(item)
            
            return Response(
                {'wishlist': result},
                status=status.HTTP_201_CREATED
            )

        except:
            return Response(
                {'error': 'Something went wrong when adding item to wishlist'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetItemTotalView(APIView):
    """
    Vista API para obtener el número total de elementos en la lista de deseos de un usuario.

    Permite a un usuario autenticado obtener el conteo total de elementos en su lista de deseos.
    """

    def get(self, request, format=None):
        """
        Maneja peticiones GET para obtener el número total de elementos en la lista de deseos.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con el número total de elementos en la lista de deseos o mensaje de error.

        Si se encuentra la lista de deseos del usuario, devuelve una respuesta JSON con el total de elementos.
        Si la lista de deseos no existe o se produce un error durante la operación, devuelve un mensaje de error correspondiente.
        """

        user = self.request.user

        try:
            wishlist = WishList.objects.get(user=user)
            total_items = wishlist.total_items

            return Response(
                {'total_items': total_items},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving total number of wishlist items'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RemoveItemView(APIView):
    """
    Vista API para eliminar un elemento de la lista de deseos de un usuario.

    Permite a un usuario autenticado eliminar un producto específico de su lista de deseos.
    """

    def delete(self, request, format=None):
        """
        Maneja peticiones DELETE para eliminar un elemento de la lista de deseos.

        Args:
        - request: Objeto de solicitud enviado por el cliente.
        - format: Sufijo de formato opcional.

        Returns:
        - Respuesta con los elementos de la lista de deseos actualizados o mensaje de error.

        Si el producto se elimina correctamente de la lista de deseos, devuelve una respuesta JSON con los elementos actualizados.
        Si el producto no existe en la lista de deseos o se produce un error durante la operación, devuelve un mensaje de error correspondiente.
        """
        
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            wishlist = WishList.objects.get(user=user)
            if not Product.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'Product with this ID does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            product = Product.objects.get(id=product_id)
            if not WishListItem.objects.filter(wishlist=wishlist, product=product).exists():
                return Response(
                    {'error': 'This product is not in your wishlist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            WishListItem.objects.filter(
                wishlist=wishlist,
                product=product
            ).delete()

            if not WishListItem.objects.filter(wishlist=wishlist, product=product).exists():
                # Actualiizar el total de items en el wishlist
                total_items = int(wishlist.total_items) - 1
                WishList.objects.filter(user=user).update(
                    total_items=total_items
                )
            
            wishlist_items = WishListItem.objects.filter(wishlist=wishlist)

            result = []

            if WishListItem.objects.filter(wishlist=wishlist).exists():
                for wishlist_item in wishlist_items:
                    item = {}

                    item['id'] = wishlist_item.id
                    product = Product.objects.get(id=wishlist_item.product.id)
                    product = ProductSerializer(product)

                    item['product'] = product.data

                    result.append(item)

            return Response(
                {'wishlist': result},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when removing wishlist item'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
