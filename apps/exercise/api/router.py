from apps.exercise.api.views import ExerciseApiViewset

from rest_framework import routers # type: ignore

router = routers.DefaultRouter()
router.register(r'exercises', ExerciseApiViewset, basename='exercises')