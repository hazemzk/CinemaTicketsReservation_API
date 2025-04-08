from rest_framework import serializers
from tickets.models import Guest, Movie, Reservation, Post

class Movieserializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'
        

class Reservationserializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reservation
        fields = '__all__'
        
class Guestserializer(serializers.ModelSerializer):
    
    class Meta:
        model = Guest
        fields = ['pk', 'reservation', 'name', 'mobile']
        
        
class Postserializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'