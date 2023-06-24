from django.shortcuts import get_object_or_404, render

# Create your views here.
from rest_framework.generics import GenericAPIView
from Booking.models import Service_domain, providerSchedule,ReservationInfo,Notification,service_Info,Service_category
from my_users.models import provider,Recipient,CustomUser
from .serializer import Rating_Serializer, Service_Info_Serializer, Reservation_Serializer,TimeSlotSerializer ,NotificationSerializer,category_serializers, domain_serializers
from rest_framework.response import Response
from rest_framework import status
from . import serializer

class allcategory (GenericAPIView):
    def get (self,request):
        all_category = Service_category.objects.all()
        serializer = category_serializers(all_category,many=True)
        return Response(serializer.data,status= status.HTTP_200_OK)

class ServicesByCategory (GenericAPIView):
    def get (self, request):
        data=request.data
        #categoryserializer = serializer.category_serializers(data=data)
        category =  request.data['category']
        try:
            all_sevices = service_Info.objects.filter(category=category)
            serializer = Service_Info_Serializer(all_sevices, many=True)
        except: 
            all_sevices = service_Info.objects.all()
            serializer = Service_Info_Serializer(all_sevices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NotificationViewSet(GenericAPIView):
    serializer_class = NotificationSerializer
    def get(self, request):
        data=request.data
        user_id = data.get("user")
        if not user_id:
            raise IndexError("Wrong ID. Please provide a valid user ID.")
        user=CustomUser.objects.get(pk=user_id)       
        queryset = Notification.objects.filter(user=user)
        if not queryset:
            raise IndexError("user dont have any notification message.")
        serializer = self.serializer_class(queryset, many=True)
        response_data = serializer.data
        response = Response(response_data, status=status.HTTP_200_OK)
        queryset.update(is_read=True)
        return response

class ServiceRating(GenericAPIView):
    serializer_class = Rating_Serializer
    def post(self , request):
        data=request.data
        recipient_id=request.data['recipient']
        reservation_id=request.data['reservation']
        score=request.data['score']
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,status=status.HTTP_400_BAD_REQUEST
        )

class RecipientBookedServices(GenericAPIView):
    def get (self,request):
        data = request.data
        Recipient_id = request.data['recipient']
        if not Recipient_id:
            return Response({'error': 'Recipient ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        resipient_instence = Recipient.objects.get(pk=Recipient_id)
        reservations =  ReservationInfo.objects.filter( recipient=resipient_instence)
        serializer = Reservation_Serializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListNewService(GenericAPIView):
    serializer_class = Service_Info_Serializer

    def post (self , request ):
        data = request.data 
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,status=status.HTTP_400_BAD_REQUEST
        )
    
class ListNewReservation(GenericAPIView):
    serializer_class = Reservation_Serializer

    def post(self , request ):
        data = request.data

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,status=status.HTTP_400_BAD_REQUEST
        )
    

    
    """
        """
    
class View_Provider_Booked_times(GenericAPIView):
    
    
    def get(self , request):
        data = request.data
        #serializer = provider_Schedule_Serializer(data=data)
        provider_id = request.data['provider']
        if not provider_id:
            return Response({'error': 'provider ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        #serializer VS request
        provider_instance = provider.objects.get(pk=provider_id)
        provider_schedule_instance = get_object_or_404(providerSchedule, provider=provider_instance)

        time_slots = provider_schedule_instance.TimeSlot.all()
        serializer = TimeSlotSerializer(time_slots, many=True)
        #time_slots = self.get_queryset(provider_instance)
        #serializer = self.get_serializer(time_slots, many=True)
        booked_times = provider_schedule_instance.TimeSlot.all()
        iterator = iter(serializer.data)
        l=[]
        

        while True:
            try:
                time_slot = next(iterator)
                l.append(time_slot)
            except StopIteration:
                break

        return Response(serializer.data, status=status.HTTP_200_OK)

class alldomain (GenericAPIView):
    def get (self,request):
        all_domain = Service_domain.objects.all()
        serializer = domain_serializers(all_domain,many=True)
        return Response(serializer.data,status= status.HTTP_200_OK)
    
class ServicesProviderByCategory (GenericAPIView):
    def get (self, request):
        data=request.data
        category =  request.data['category']
        provider_id=request.data['provider']
        provider_instance=provider.objects.get(pk=provider_id)

        try:
            all_sevices = service_Info.objects.filter(provider=provider_instance)
        except: raise   KeyError
        try:
            all_sevices = all_sevices.filter(category=category)
        except :
            pass
        serializer = Service_Info_Serializer(all_sevices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    