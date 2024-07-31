from django.db.models import Q
from exceptions.custom_apiexception_class import *
from utils.unique_response import process_data
from .models import Rating
from .serializers import *
from .models import *
from django.db.models import Q
from rest_framework import status
from drf_yasg import openapi
from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated,  AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from utils.custom_response import custom_response
from utils.custom_permission import IsStaff

User = get_user_model()


class MenuItemTagView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            menu_tags = [
                menu_tag.name for menu_tag in MenuItemTag.objects.all()]
            processed_data = process_data(menu_tags)
            return custom_response(status_code=status.HTTP_200_OK, message="Success", data=processed_data)
        except Exception as e:
            return CustomAPIException(detail=str(
                e), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()


class MenuItemImageView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    @swagger_auto_schema(
        operation_description="Upload images for a specific menu item.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'menu_item_id': openapi.Schema(type=openapi.TYPE_STRING, description="ID of the menu item to associate images with."),
                'images': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_FILE), description="List of images to upload.")
            },
            required=['menu_item_id', 'images'],

        ),
        responses={
            201: openapi.Response(
                description="Successfully uploaded images.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                        'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                            'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the image'),
                            'image': openapi.Schema(type=openapi.TYPE_STRING, description='URL of the image'),
                            'menu_item': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the associated menu item')
                        }))
                    }
                )
            ),
            400: openapi.Response(
                description="Invalid request payload."
            ),
            404: openapi.Response(
                description="Menu item not found."
            ),
            500: openapi.Response(
                description="Internal server error."
            )
        }
    )
    def post(self, request):
        try:
            images = request.FILES.getlist('images')
            menu_item_id = request.data.get('menu_item_id')

            menu_item_instance = MenuItem.objects.get(id=menu_item_id)
            serialized_data = []

            for image in images:
                img = MenuItemImage.objects.create(
                    menu_item=menu_item_instance, image=image)
                serializer = MenuItemImageSerializer(img)
                serialized_data.append(serializer.data)
            return custom_response(status_code=status.HTTP_201_CREATED, message="Success", data=serialized_data)

        except Exception as e:
            return CustomAPIException(detail=str(
                e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

    @swagger_auto_schema(
        request_body=MenuItemImageSerializer,
        operation_description="Update a specific menu item image by its ID.",
        responses={
            200: openapi.Response(
                description="Successfully updated the menu item image.",
                schema=MenuItemImageSerializer
            ),
            404: openapi.Response(
                description="Menu item image not found."
            ),
            400: openapi.Response(
                description="Invalid request payload or validation errors."
            ),
            500: openapi.Response(
                description="Internal server error."
            )
        }
    )
    def patch(self, request):
        try:
            image_id = request.data.get('id')
            image_instance = MenuItemImage.objects.get(id=image_id)
            serializer = MenuItemImageSerializer(
                image_instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_201_CREATED, message="Success", data=serializer.data)
            else:
                return CustomAPIException(detail=str(serializer.errors), status_code=status.HTTP_404_NOT_FOUND).get_full_details()

        except MenuItemImage.DoesNotExist:
            return CustomAPIException(detail="Menu item image not found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()

        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

    @swagger_auto_schema(
        operation_description="Delete a specific menu item image by its ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the menu item image to delete.')
            },
            required=['id']
        ),
        responses={
            204: openapi.Response(
                description="Menu item image successfully deleted."
            ),
            404: openapi.Response(
                description="Menu item image not found."
            ),
            400: openapi.Response(
                description="Invalid request payload."
            ),
            500: openapi.Response(
                description="Internal server error, custom error message."
            )
        }
    )
    def delete(self, request):
        try:
            image_id = request.data.get('id')
            image_instance = MenuItemImage.objects.get(id=image_id)
            image_instance.delete()

            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Successfully deleted the menu item image.", data=None)

        except MenuItemImage.DoesNotExist:
            return CustomAPIException(detail="Menu item image not found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()

        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()


class MenuItemCreateView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    @swagger_auto_schema(request_body=MenuItemSerializer)
    def post(self, request):
        try:
            tags = request.data.pop('tags', [])
            menu_item_serializer = MenuItemSerializer(data=request.data)
            if menu_item_serializer.is_valid():
                menu_item = menu_item_serializer.save()
                # Create or get special tags
                special_tags = [MenuItemTag.objects.get_or_create(name=tag.get('name'))[
                    0] for tag in tags]
                menu_item.tags.set(special_tags)
                menu_item.save()
                return custom_response(status_code=status.HTTP_201_CREATED, message="Menu successfully created", data=menu_item_serializer.data)
            return CustomAPIException(detail=str(menu_item_serializer.errors), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()
        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()


class MenuItemEditView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    @swagger_auto_schema(request_body=MenuItemSerializer)
    def patch(self, request, pk):
        try:
            tags = request.data.pop('tags', [])
            menu_item = MenuItem.objects.get(pk=pk)
            menu_item_serializer = MenuItemSerializer(
                menu_item, data=request.data, partial=True)
            if menu_item_serializer.is_valid():
                menu_item = menu_item_serializer.save()
                # Update or create special tags
                special_tags = [MenuItemTag.objects.get_or_create(name=tag.get('name'))[
                    0] for tag in tags]
                menu_item.tags.set(special_tags)
                menu_item.save()

                return custom_response(status_code=status.HTTP_201_CREATED, message="Menu successfully updated", data=menu_item_serializer.data)
            return CustomAPIException(detail=str(menu_item_serializer.errors), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()
        except MenuItem.DoesNotExist:
            return CustomAPIException(detail="MenuItem not found.", status_code=status.HTTP_400_BAD_REQUEST).get_full_details()
        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()


class GetMenuItemByIDView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: MenuItemSerializer()})
    def get(self, request, pk):
        try:
            menu_item = get_object_or_404(MenuItem, id=pk)
            # Fetch associated menu item images
            menu_item_images = MenuItemImage.objects.filter(menu_item_id=pk)
            # Serialize menu item and menu item images
            menu_item_serializer = MenuItemSerializer(menu_item)
            image_serializer = MenuItemImageSerializer(
                menu_item_images, many=True)
            # Include menu item images in the response data
            menu_item_data = menu_item_serializer.data
            image_data = image_serializer.data
            for image in image_data:
                image_id = image['id']
                image['image'] = f"{image['image']}?id={image_id}"
            menu_item_data['images'] = image_data
            # Calculate and add average rating
            menu_item_ratings = Rating.objects.filter(menu_item_id=pk)
            rating_sum = menu_item_ratings.aggregate(Avg('rating'))[
                'rating__avg']
            menu_item_data["rating"] = rating_sum
            return custom_response(status_code=status.HTTP_200_OK, message="Successful", data=menu_item_data)
        except MenuItem.DoesNotExist:
            return CustomAPIException(detail="MenuItem not found.", status_code=status.HTTP_400_BAD_REQUEST).get_full_details()
        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()


class GetAllMenuItemsView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of all menu items with optional filters.",
        manual_parameters=[
            openapi.Parameter(
                'search_query', openapi.IN_QUERY, description="Search for menu items by name, category, description, or tags.",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'min_price', openapi.IN_QUERY, description="Filter menu items by minimum price.",
                type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL
            ),
            openapi.Parameter(
                'max_price', openapi.IN_QUERY, description="Filter menu items by maximum price.",
                type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL
            ),
            openapi.Parameter(
                'availability', openapi.IN_QUERY, description="Filter menu items by availability (true/false).",
                type=openapi.TYPE_BOOLEAN
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully retrieved the list of menu items.",
                schema=MenuItemSerializer(many=True)
            ),
            500: openapi.Response(
                description="Internal server error, custom error message."
            ),
        }
    )
    def get(self, request):
        try:
            # Filter queryset based on request parameters
            query_params = request.query_params
            menu_items_query = MenuItem.objects.all()
            search_query = query_params.get('search_query')
            min_price = query_params.get('min_price')
            max_price = query_params.get('max_price')
            availability = query_params.get('availability')

            filters = Q()

            if search_query:
                filters |= Q(name__icontains=search_query) | Q(category__icontains=search_query) | Q(
                    description__icontains=search_query) | Q(preparation_time__icontains=search_query) | Q(tags__name__icontains=search_query)

            if min_price:
                filters &= Q(price__gte=min_price)
            if max_price:
                filters &= Q(price__lte=max_price)
            if availability:
                filters &= Q(availability=availability)

            menu_items_query = menu_items_query.filter(filters).distinct()
            # Create a list to store serialized menu items
            serialized_menu_items = []

            # Iterate through each menu item
            for menu_item in menu_items_query:
                # Fetch associated menu item images
                menu_item_images = MenuItemImage.objects.filter(
                    menu_item=menu_item)

                # Serialize menu item and menu item images
                menu_item_serializer = MenuItemSerializer(menu_item)
                image_serializer = MenuItemImageSerializer(
                    menu_item_images, many=True)

                # Include menu item images in the response data
                menu_item_data = menu_item_serializer.data
                image_data = image_serializer.data
                for image in image_data:
                    image_id = image['id']
                    image['image'] = f"{image['image']}?id={image_id}"

                menu_item_data['images'] = image_data

                # Calculate and add average rating
                menu_item_ratings = Rating.objects.filter(menu_item=menu_item)
                rating_sum = menu_item_ratings.aggregate(Avg('rating'))[
                    'rating__avg']
                menu_item_data["rating"] = rating_sum if rating_sum is not None else 0
                serialized_menu_items.append(menu_item_data)

            return custom_response(status_code=status.HTTP_200_OK, message="Successful", data=serialized_menu_items)
        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()


class GetDiscountedMenuItemsView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a list of menu items that are currently discounted.",
        responses={
            200: openapi.Response(
                description="Successfully retrieved discounted menu items.",
                schema=MenuItemSerializer(many=True)
            ),
            500: openapi.Response(
                description="Internal server error, custom error message."
            ),
        }
    )
    def get(self, request):
        try:
            # Filter queryset to get discounted menu items
            discounted_menu_items = MenuItem.objects.filter(is_discounted=True)
            # Serialize the discounted menu items
            serializer = MenuItemSerializer(discounted_menu_items, many=True)
            return custom_response(status_code=status.HTTP_200_OK, message="Successfully retrieved discounted menu items.", data=serializer.data)
        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()


class GetDrinksMenuItemsView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a list of menu items categorized as drinks.",
        responses={
            200: openapi.Response(
                description="Successfully retrieved drinks menu items.",
                schema=MenuItemSerializer(many=True)
            ),
            500: openapi.Response(
                description="Internal server error, custom error message."
            ),
        }
    )
    def get(self, request):
        try:
            # Filter queryset to get menu items categorized as drinks
            drinks_menu_items = MenuItem.objects.filter(category='Drink')
            # Serialize the drinks menu items
            serializer = MenuItemSerializer(drinks_menu_items, many=True)
            return custom_response(status_code=status.HTTP_200_OK, message="Successfully retrieved drinks menu items.", data=serializer.data)
        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
