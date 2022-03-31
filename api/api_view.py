from rest_framework.views import APIView
from rest_framework.response import Response
from medi_bot_api.chatbot import bot, model_train
from rest_framework import status


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
                    'q1',
                    'q2'
                ]
            }
        else:
            context = {
                'tag': tag,
                'response': response
            }

        return Response(context, status=status.HTTP_200_OK)
