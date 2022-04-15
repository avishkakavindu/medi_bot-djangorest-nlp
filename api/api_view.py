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
                    'Sex?(male/ female)',
                    'Chest pain type()?',
                    'Resting blood pressure?',
                    'Serum cholesterol in mg/dl?',
                    'Fast blood sugar > 120mg/dl (yes/no)?',
                    'Resting electrocardiographic results(0, 1, 2)?',
                    'Maximum heart rate achieved?',
                    'Exercise induced angina?',
                    'Oldpeak(ST depression induced by exercise relative to rest)?',
                    'The slope of the peak exercise ST segment',
                    'Number of major vessels (0-3) colored by flourosopy?',
                    'Thal? (thal: 0 = normal; 1 = fixed defect; 2 = reversable defect)'
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
        # print(request.data)
        data = request.data.get('payload')
        import json
        try:
            data = json.loads(data)
        except:
            data = eval(data)
        # print('\n\n\n\n', request.data, 'lol', type(data), '\n\n\n')

        if data[1] == 'male' or 'Male' or 1:
            data[1] = 1
        else:
            data[1] = 0

        if data[5] == 'yes' or 'Yes':
            data[5] = 1
        else:
            data[5] = 0

        
        data = [float(i) for i in data]
        
        clf = classifier.HeartDiseaseClassifier()
        try:
            prediction = clf.get_predictions(data)
        except ValueError:
            context = {
                'detail': 'Something went wrong on predicting! please recheck the data.'
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if prediction:
            response = 'You have a heart disease.<i class="fa fa-frown-o" aria-hidden="true"></i> Do you want to put ' \
                       'an appointment? '
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

