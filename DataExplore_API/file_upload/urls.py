from .views import FileUploadView, SummaryView, VisualizationView
from .views import FileUploadView, DataVisualizationView
from django.urls import path
from . import views
from .views import FileUploadView
from .views import FileUploadView, SummaryView

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('filter', views.filter_data, name='filter_data'),
    path('summary/<int:data_id>/', SummaryView.as_view(), name='summary'),
    path('visualize/', VisualizationView.as_view(), name='visualize'),
    path('data-visualization/', DataVisualizationView.as_view(), name='data-visualization'),
]
