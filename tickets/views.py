from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework import status ,filters
from rest_framework.views import APIView
from rest_framework import mixins, generics ,viewsets

from rest_framework .authentication import BasicAuthentication, TokenAuthentication
from rest_framework .permissions import IsAuthenticated

from .permissions import IsOwnerOrReadOnly
# Create your views here.

#1 without REST and no model query FBV
def no_rest_no_model(request):
    guests = [
        {
            'id':1,
            "name":"omar",
            "mobile":446545,
        },
        {
            'id':2,
            "name":"hazem",
            "mobile":87498456,
        }
    ]
    return JsonResponse(guests, safe=False)

# 2 model data deflault without rest

def no_rest_form_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)

# 3 function based views

# 3.1 GET POST
@api_view(['GET', 'POST'])
def FBV_List(request):
    #GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = Guestserializer(guests, many=True)
        return Response(serializer.data)
    #POST
    elif request.method == 'POST':
        serializer = Guestserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    

# 3.1 GET PUT DELETE 
@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        serializer = Guestserializer(guest)
        return Response(serializer.data)
    #PUT
    elif request.method == 'PUT':
        serializer = Guestserializer(guest, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #DELETE
    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CBV class based views

# list and create == GET POST
class CBV_list(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = Guestserializer(guests, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = Guestserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# GET PUT DELETE CBV
    
class CBV_pk(APIView):
    
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = Guestserializer(guest)
        return Response(serializer.data)
    def put(self, request, pk):
        guest=self.get_object(pk)
        serializer = Guestserializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
#5- mixins 

# 1 mixins list
class mixins_list(mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
    
# 2 mixins edit get put  delete
class mixins_pk(mixins.DestroyModelMixin,mixins.RetrieveModelMixin,  
                  mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer
    def get(self, request, pk):
        return self.retrieve(request)
    def put(self,request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)

#6 -api Generics

class generics_list(generics.ListAPIView):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    

# 7 viewsets

class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer
    
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = Movieserializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets_reservations(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = Reservationserializer
    
    
# 8 find  movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.data['movie'],   
    )
    serializer = Movieserializer(movies, many=True)
    return Response(serializer.data)
    


# 9 Creat new reservation

@api_view(['POST'])
def newservation(request):
    
    movie = Movie.objects.get(
        hall=request.data['hall'],
        movie = request.data['movie'],
    )
    guest = Guest()
    guest.name= request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()
    
    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    return Response(status= status.HTTP_201_CREATED)


class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = Postserializer
    
class Post_list(generics.ListAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = Postserializer