from django.urls import path
from . import views

app_name = 'textengines'

urlpatterns = [
    path('', views.engine, name='text'),
    path('lstm_test/', views.text_classification, name="lstm_test"),
    path('tensorflow_analyze/', views.LstmRunAPIView.as_view(), name="lstm_test"),
    path('sklearn_analyze/', views.SklearnAPIView.as_view(), name="test3"),
    path('movie_set/', views.return_data, name="movie_data"),
    path('sklearn_result_analyze/', views.sklearn_result_analyze, name="sklearn_result_analyze"),
    path('base_analyze/', views.base_analyze, name="base_analyze"),
]
