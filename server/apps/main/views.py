from datetime import datetime

from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet

from server.apps.main.models import Poll, Question, History
from server.apps.main.serializers import PollSerializer, AdminPollSerializer, AdminQuestionSerializer, \
    PassedPollSerializer


# better to wrap in ModelViewSet


class PollListView(ListAPIView):
    serializer_class = PollSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Poll.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now())


class AdminPollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = AdminPollSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)


class QuestionViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    serializer_class = AdminQuestionSerializer
    queryset = Question.objects.all()


class PassPollApi(CreateAPIView):
    serializer_class = PassedPollSerializer
    permission_classes = (permissions.AllowAny,)


class HistoryApi(APIView):

    def get(self, request, pk=None):
        hist = History.objects.get_or_create(user_id=pk)[0]
        data = PassedPollSerializer(instance=hist, many=True, context='pk').data
        return Response(data)
