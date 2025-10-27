from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.PcbTypeListView.as_view(), name='pcb_type_list'),
    path('create/', views.PcbTypeCreateView.as_view(), name='pcb_type_create'),
    path('update/<int:pk>/', views.PcbTypeUpdateView.as_view(), name='pcb_type_update'),
    path('delete/<int:pk>/', views.PcbTypeDeleteView.as_view(), name='pcb_type_delete'),
    path('view/<int:pk>/', views.PcbTypeDetailView.as_view(), name='pcb_type_view'),
]
