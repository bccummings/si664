from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('', views.HorseListView.as_view()),
    path('horses', views.HorseListView.as_view(), name='horses'),
    path('horse/<int:pk>', views.HorseDetailView.as_view(), name='horse_detail'),
    path('horse/create',
        views.HorseCreateView.as_view(success_url=reverse_lazy('horses')), name='horse_create'),
    path('horse/<int:pk>/update',
        views.HorseUpdateView.as_view(success_url=reverse_lazy('horses')), name='horse_update'),
    path('horse/<int:pk>/delete',
        views.HorseDeleteView.as_view(success_url=reverse_lazy('horses')), name='horse_delete'),
    path('horse/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('forums')), name='comment_delete'),
]
