from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers, serializers, viewsets

from django.contrib.auth.models import User
from trips.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ('url', 'name', 'license_plate',)

class TripSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trip
        fields = ('url', 'date', 'destination', 'reason', 'distance', 'car',)

class OdometerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Odometer
        fields = ('url', 'date', 'car', 'km',)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

class OdometerViewSet(viewsets.ModelViewSet):
    queryset = Odometer.objects.all()
    serializer_class = OdometerSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cars', CarViewSet)
router.register(r'trips', TripViewSet)
router.register(r'odometers', OdometerViewSet)


#urlpatterns = [
    # Examples:
    # url(r'^$', 'carlog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^', include(router.urls)),
#    url(r'^admin/', include(admin.site.urls)),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'),),
#]


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    ]
