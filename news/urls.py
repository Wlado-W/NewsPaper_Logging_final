from django.urls import path
from .views import NewsList, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostSearchView
from .views import subscribe_to_category, unsubscribe_from_category
from .views import AppointmentView
from django.views.decorators.cache import cache_page
from .views import PostCategoryView



# импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем статьям у нас останется пустым, позже станет ясно почему
    path('', NewsList.as_view()),  # т.к. сам по себе это класс, то нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view
    path('<int:pk>/', cache_page(10*5) (PostDetailView.as_view()), name='post_detail'),  # Ссылка на детали статьи
    path('add/', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание статьи
    path('edit/<int:pk>', PostUpdateView.as_view(), name='post_update'),  # Ссылка на редактирование статьи
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),  # Ссылка на удаление статьи
    path('search/', PostSearchView.as_view(), name='post_search'),  # Ссылка на поиск статьи
    path('make_app/', AppointmentView.as_view(), name='make_app'),
    path('category/<int:pk>', PostCategoryView.as_view(), name='category'), # Ссылка на категории
    path('subscribe/<int:pk>', subscribe_to_category, name='subscribe'), # Ссылка на подписчиков
    path('unsubscribe/<int:pk>', unsubscribe_from_category, name='unsubscribe'), # Ссылка на отписку

]