from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='home'), 
    path('addtransaction/', views.addTransaction, name='add_transaction'),
    path('usepoint/', views.spendPoints, name='spend_points'),
    path('points/detail/', views.pointsReport, name='points_report'),
    path('points/balance/', views.totalBalance, name='total_balance'),
    path('points/agg/', views.pointsAggReport, name='agg_report'),
    path('redemedpoints/summary', views.redemedPoints, name='redemed_points')
]