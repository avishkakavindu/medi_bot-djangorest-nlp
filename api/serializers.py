from rest_framework import serializers
from api.models import Doctor, Appointment


class DoctorSerializer(serializers.ModelSerializer):
    """ Serialize the Doctor model """
    class Meta:
        model = Doctor
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    """ Serialize the Appointment model """

    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time']
