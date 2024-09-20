from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sample/', views.sample_view, name='sample'),
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
    path('filter/', views.DataFilterView.as_view(), name='data-filter'),
    path('api/summary/<str:data_id>/', views.DataSummaryView.as_view(), name='data-summary'),
    path('api/visualize/', views.DataVisualizationView.as_view(), name='data-visualization'),
     path('api/visualize/', views.visualize, name='visualize'),
]
