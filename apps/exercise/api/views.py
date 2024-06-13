from rest_framework import viewsets # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

from apps.exercise.models import Exercise
from apps.exercise.api.serializers import ExerciseSerializer

class ExerciseApiViewset(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer