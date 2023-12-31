from django.shortcuts import get_object_or_404, render
# Create your views here.
from rest_framework.generics import GenericAPIView
from Booking.models import Service_domain, providerSchedule, ReservationInfo, Notification, service_Info, Service_category
from my_users.models import provider, Recipient, CustomUser
from .serializer import (Rating_Serializer, Service_Info_Serializer, Reservation_Serializer,
                         TimeSlotSerializer, NotificationSerializer, category_serializers, domain_serializers)
from rest_framework.response import Response
from rest_framework import status
from . import serializer
from django.utils import timezone
import datetime


class ProviderBookedServices(GenericAPIView):

    def get(self, request):
        provider_id = request.query_params.get('provider')
        #provider_id = request.data['provider']
        if not provider_id:
            return Response({'error': 'provider ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        all_services = service_Info.objects.filter(provider=provider_id)
        reservations = []
        for service in all_services:
            reservations.extend(ReservationInfo.objects.filter(service_Info=service))

        filtered_reservations = []
        for reservation in reservations:
            if reservation.start_time < timezone.now():
                filtered_reservations.append(reservation)
        serializer = Reservation_Serializer(filtered_reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class providerFutureServices(GenericAPIView):
    def get(self, request):
        provider_id = request.query_params.get('provider')
        #provider_id = request.data['provider']
        if not provider_id:
            return Response({'error': 'provider ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        all_services = service_Info.objects.filter(provider=provider_id)
        reservations = []
        for service in all_services:
            reservations.extend(ReservationInfo.objects.filter(service_Info=service))

        filtered_reservations = []
        for reservation in reservations:
            if reservation.start_time > timezone.now():
                filtered_reservations.append(reservation)
        serializer = Reservation_Serializer(filtered_reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteServiceInfo(GenericAPIView):

    def post(self, request):

        service_Info_id = request.data['service_Info']
        # service_Info_id=request.query_params.get('service_Info')
        service_Info_instance = service_Info.objects.get(pk=service_Info_id)
        service_Info_instance.is_deleted = True
        service_Info_instance.save()
        return Response(status=status.HTTP_200_OK)


class SearchInServiceInfo (GenericAPIView):
    def get(self, request):
        data = request.data
        category = request.query_params.get('category')
        title = request.query_params.get('title')
        # category =  request.data['category']
        # title=request.data['title']
        try:
            all_sevices = service_Info.objects.filter(
                category=category, title__icontains=title, is_deleted=False)
        except:
            try:
                all_sevices = service_Info.objects.filter(
                    title__icontains=title, is_deleted=False)
            except:
                raise KeyError
        serializer = Service_Info_Serializer(all_sevices, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class allcategory (GenericAPIView):
    def get(self, request):
        all_category = Service_category.objects.all()
        serializer = category_serializers(all_category, many=True)
        pairs = [(item["id"], item["category"]) for item in serializer.data]
        return Response(pairs, status=status.HTTP_200_OK)


class ServicesByCategory (GenericAPIView):
    def get(self, request):
        data = request.data
        # categoryserializer = serializer.category_serializers(data=data)
        # category =  request.data['category']
        category = request.query_params.get('category')
        try:
            all_sevices = service_Info.objects.filter(
                category=category, is_deleted=False)
            serializer = Service_Info_Serializer(all_sevices, many=True)
        except:
            all_sevices = service_Info.objects.filter(is_deleted=False)
            serializer = Service_Info_Serializer(all_sevices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationViewSet(GenericAPIView):
    serializer_class = NotificationSerializer

    def get(self, request):
        data = request.data
        user_id = request.query_params.get('user')
        if not user_id:
            raise IndexError("Wrong ID. Please provide a valid user ID.")
        user = CustomUser.objects.get(pk=user_id)
        queryset = Notification.objects.filter(user=user)
        if not queryset:
            return Response(' empty ', status=status.HTTP_200_OK)
        serializer = self.serializer_class(queryset, many=True)
        response_data = serializer.data
        response = Response(response_data, status=status.HTTP_200_OK)
        queryset.update(is_read=True)
        return response


class ServiceRating(GenericAPIView):
    serializer_class = Rating_Serializer

    def post(self, request):
        data = request.data
        recipient_id = request.data['recipient']
        reservation_id = request.data['reservation']
        score = request.data['score']
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class RecipientBookedServices(GenericAPIView):
    def get(self, request):
        data = request.data
        #Recipient_id = request.query_params.get('recipient')
        Recipient_id = request.data['recipient']
        if not Recipient_id:
            return Response({'error': 'Recipient ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        resipient_instence = Recipient.objects.get(pk=Recipient_id)
        reservations = ReservationInfo.objects.filter(
            recipient=resipient_instence)
        filtered_reservations = []

        for reservation in reservations:
            if reservation.start_time < timezone.now():
                filtered_reservations.append(reservation)
        serializer = Reservation_Serializer(filtered_reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipientFutureServices(GenericAPIView):
    def get(self, request):
        data = request.data
        Recipient_id = request.query_params.get('recipient')
        # Recipient_id = request.data['recipient']
        if not Recipient_id:
            return Response({'error': 'Recipient ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        resipient_instence = Recipient.objects.get(pk=Recipient_id)
        reservations = ReservationInfo.objects.filter(
            recipient=resipient_instence)
        filtered_reservations = []
        for reservation in reservations:
            if reservation.start_time > timezone.now():
                filtered_reservations.append(reservation)
        serializer = Reservation_Serializer(filtered_reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListNewService(GenericAPIView):
    serializer_class = Service_Info_Serializer

    def post(self, request):
        data = request.data

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class ListNewReservation(GenericAPIView):
    serializer_class = Reservation_Serializer

    def post(self, request):
        data = request.data

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    """
        """


class View_Provider_Booked_times(GenericAPIView):

    def get(self, request):
        data = request.data
        # serializer = provider_Schedule_Serializer(data=data)
        # provider_id = request.data['provider']
        provider_id = request.query_params.get('provider')
        if not provider_id:
            return Response({'error': 'provider ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # serializer VS request
        provider_instance = provider.objects.get(pk=provider_id)
        provider_schedule_instance = get_object_or_404(
            providerSchedule, provider=provider_instance)

        time_slots = provider_schedule_instance.TimeSlot.all()
        serializer = TimeSlotSerializer(time_slots, many=True)
        # time_slots = self.get_queryset(provider_instance)
        # serializer = self.get_serializer(time_slots, many=True)
        booked_times = provider_schedule_instance.TimeSlot.all()
        iterator = iter(serializer.data)
        l = []

        while True:
            try:
                time_slot = next(iterator)
                l.append(time_slot)
            except StopIteration:
                break

        return Response(serializer.data, status=status.HTTP_200_OK)


class alldomain (GenericAPIView):
    def get(self, request):
        all_domain = Service_domain.objects.all()
        serializer = domain_serializers(all_domain, many=True)
        pairs = {item["id"]: item["domain"] for item in serializer.data}
        return Response(pairs, status=status.HTTP_200_OK)


class ServicesProviderByCategory (GenericAPIView):
    def get(self, request):
        data = request.data
        # category =  request.data['category']
        # provider_id=request.data['provider']
        category = request.query_params.get('category')
        provider_id = request.query_params.get('provider')
        provider_instance = provider.objects.get(pk=provider_id)

        try:
            all_sevices = service_Info.objects.filter(
                provider=provider_instance, is_deleted=False)
        except:
            raise KeyError
        try:
            all_sevices = all_sevices.filter(
                category=category, is_deleted=False)
        except:
            pass
        serializer = Service_Info_Serializer(all_sevices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    """
class providerutureServices(GenericAPIView):

    def get(self, request):
        data = request.data
            # provider_id = request.query_params.get('provider')
        provider_id = request.data['provider']
        if not provider_id:
            return Response({'error': 'provider ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        all_sevices = service_Info.objects.filter(provider=provider_id)
        reservations = []
        for service in all_sevices:
            reservations.append(
                ReservationInfo.objects.get(service_Info=service.id))
            
        filtered_reservations = []
        for reservation in reservations:
            if reservation.start_time > timezone.now():
                filtered_reservations.append(reservation)
        serializer = Reservation_Serializer(filtered_reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""