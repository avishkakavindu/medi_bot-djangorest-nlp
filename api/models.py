from django.db import models


class Specialty(models.Model):
    """ Holds the specialty details """
    specialty = models.CharField(max_length=50)

    def __str__(self):
        return self.specialty


class Doctor(models.Model):
    """ Holds details of Doctors """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    experience = models.IntegerField()
    telephone = models.TextField(max_length=10)
    specialty = models.ForeignKey(Specialty, on_delete=models.DO_NOTHING)
    link = models.URLField()

    def __str__(self):
        return 'Dr. {} {}'.format(self.first_name, self.last_name)


class Appointment(models.Model):
    """ Holds appointment details """

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def __str__(self):
        return self.id


