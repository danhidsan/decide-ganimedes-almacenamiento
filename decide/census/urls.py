from django.urls import path, include
from census.views import add_custom_census, export_csv, import_csv
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('addAllRegistered/', views.addAllRegistered, name='addAllRegistered'),
    path('addAllInCity/', views.addAllInCity, name='addAllInCity'),
    path('addAllBySex/', views.addAllBySex, name='addAllBySex'),
    path('addCustomCensus', add_custom_census, name='addCustomCensus'),
    path('exportCensus', export_csv, name='exportCSV'),
    path('importCensus', import_csv, name='importCSV')
]