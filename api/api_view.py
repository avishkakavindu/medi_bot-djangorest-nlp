from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from medi_bot_api.chatbot import bot, model_train
from medi_bot_api.heart_disease import classifier
from rest_framework import status
from api.models import *
from api.serializers import DoctorSerializer, AppointmentSerializer


class MediBotAPIView(APIView):
    """ Handles the chatbot """

    def get(self, request, *args, **kwargs):
        try:
            model = model_train.ChatBotModel()
        except FileNotFoundError:
            context = {
                'detail': 'Something went wrong on required files configurations! please contact system admin.'
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            model.train()
        except:
            context = {
                'detail': 'Something went wrong! please contact system admin.'
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        context = {
            'detail': 'Model trained successfully!'
        }

        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # get pattern(message) from the post requst
        pattern = request.data.get('pattern')

        # create chatbot model instance
        model = bot.ChatBot()

        # get predictions for pattern
        prediction = model.predict_class(pattern)
        # retrieve tag from the prediction
        tag = prediction[0]['intent']

        # get random response fron tentents.json
        response = model.get_response(prediction, model.intents)

        # print('\n\n\n\n\n', tag)

        if tag == 'heart_disease':
            context = {
                'tag': tag,
                'response': response,
                'followup_questions': [
                    'Age?',
                    'Sex?',
                    'Cp?',
                    'Tresttbps?',
                    'Chol?',
                    'Fbs?',
                    'Restecg?',
                    'Thalach?',
                    'Exang?',
                    'Oldpeak?',
                    'Slope?',
                    'Ca?',
                    'Thal?'
                ]
            }
        else:
            context = {
                'tag': tag,
                'response': response,
                'followup_questions': None
            }

        return Response(context, status=status.HTTP_200_OK)


class HeartDiseaseAPIView(APIView):
    """ Handles operations related to Heart Disease model training """

    def get(self, request, *args, **kwargs):
        try:
            model = classifier.HeartDiseaseClassifier()
        except FileNotFoundError:
            context = {
                'detail': 'Something went wrong on required files configurations! please contact system admin.'
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            model.train()
        except:
            context = {
                'detail': 'Something went wrong on model training! please contact system admin.'
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        context = {
            'detail': 'Model trained successfully!'
        }

        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        age = request.data.get('age')
        sex = request.data.get('sex')
        cp = request.data.get('cp')
        trestbps = request.data.get('tresttbps')
        chol = request.data.get('chol')
        fbs = request.data.get('fbs')
        restecg = request.data.get('restecg')
        thalach = request.data.get('thalach')
        exang = request.data.get('exang')
        oldpeak = request.data.get('oldpeak')
        slope = request.data.get('slope')
        ca = request.data.get('ca')
        thal = request.data.get('thal')
        
        data = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        clf = classifier.HeartDiseaseClassifier()
        try:
            prediction = clf.get_predictions(data)
        except ValueError:
            context = {
                'detail': 'Something went wrong on predicting! please recheck the data.'
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if prediction:
            response = 'You have a heart disease.'
            specialty = Specialty.objects.get(specialty='Heart disease')
            doctors = Doctor.objects.filter(specialty=specialty)

            serializer = DoctorSerializer(doctors, many=True)
            doctors_list = serializer.data

        else:
            response = "You don't have a heart disease"
            doctors_list = None

        context = {
            'tag': 'heart_disease_prediction',
            'response': response,
            'doctors_list': doctors_list
        }
        
        return Response(context, status=status.HTTP_200_OK)


class AppointmentCreateAPIView(generics.CreateAPIView):
    """ Handles appointment creation """

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

