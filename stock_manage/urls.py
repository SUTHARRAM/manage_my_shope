from django.urls import path
from .views import (home, list_item, add_items, 
                    temp_view, update_items, stock_detail,
                    issue_items, receive_items, reorder_level, list_history,
                    add_category)

urlpatterns = [
    path('', home, name='home'), 
    path('list_items/', list_item, name='list_item'),
    path('add_items/', add_items, name='add_items'), 
    path('update_items/<str:pk>/', update_items, name='update_items'),  
    path('stock_detail/<str:pk>/', stock_detail, name='stock_detail'), 
    path('issue_items/<str:pk>/', issue_items, name='issue_items'),
    path('receive_items/<str:pk>/', receive_items, name='receive_items'), 
    path('reorder_level/<str:pk>/', reorder_level, name="reorder_level"), 
    path('list_history/', list_history, name='list_history'), 
    path('add_category/', add_category, name='add_category'), 
  #  path('temp/', temp_view, name='temp_view'), 
]