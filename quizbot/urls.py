from django.contrib import admin
from django.urls import path
from .quiz.views import RandomQuestionView
from .score.views import UpdateScore , Leaderboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/random',RandomQuestionView.as_view() , name='random'),
    path('api/score/update',UpdateScore.as_view(),name='score_update'),
    path('api/score/leaderboard', Leaderboard.as_view(), name='leaderboard')

]
