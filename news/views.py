from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
# импоритируем необходимые дженерики
# импортируем класс ListView, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
# импортируем класс DetailView получения деталей объекта
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .models import Post, Category, Subscription, Author, PostCategory  # Дополнительно импортируем категорию, чтобы пользователь мог её выбрать
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .forms import PostForm  # импортируем нашу форму
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from datetime import datetime
from .models import Appointment
from django.urls import reverse_lazy, resolve
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator






DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL



class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML,
    # в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = [
        '-dateCreation']  # сортировка по дате публикации, сначала более новые /  queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10  # поставим постраничный вывод в один элемент


# дженерик для получения деталей о товаре
@method_decorator(cache_page(60*15), name='dispatch')
class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'news_app/post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните.
# Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_app/post_create.html'
    form_class = PostForm
    success_url = '/news/'
    permission_required = ('news.add_post',)


# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news_app/post_create.html'
    form_class = PostForm
    success_url = '/news/'
    permission_required = ('news.change_post',)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления поста
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news_app/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post',)


# дженерик для поиска поста
class PostSearchView(ListView):
    model = Post
    template_name = 'news_app/post_search.html'
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = [
        '-dateCreation']  # сортировка по дате публикации, сначала более новые /  queryset = Post.objects.order_by('-dateCreation')

    def get_context_data(self, **kwargs):
        # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostCategoryView(ListView):
    model = Post
    template_name = 'news_app/category.html'
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-dateCreation']  # сортировка
    paginate_by = 10  # поставим постраничный вывод в один элемент

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(postCategory=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['category'] = category


        return context

class AllCategoriesView(ListView):
    model = Category
    template_name = 'news_app/all_categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()




@login_required
def subscribe_to_category(request, pk):  # подписка на категорию
    user = request.user
    category = Category.objects.get(id=pk)


    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribed.html',
            {
                'category': category,
                'user': user,
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'Подписка на {category} на сайте News Paper',
            body='',
            from_email=DEFAULT_FROM_EMAIL,  # в settings.py
            to=[email, ],  # список получателей
        )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect(request.META.get('HTTP_REFERER'))
        # return redirect('news_list')
    return redirect(request.META.get('HTTP_REFERER'))  # возвращает на страницу, с кот-й поступил запрос


@login_required
def unsubscribe_from_category(request, pk):  # отписка от категории
    user = request.user
    c = Category.objects.get(id=pk)

    if c.subscribers.filter(id=user.id).exists():  # проверяем есть ли у нас такой подписчик
        c.subscribers.remove(user)  # то удаляем нашего пользователя
    # return redirect('http://127.0.0.1:8000/')
    return redirect(request.META.get('HTTP_REFERER'))


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news_app/make_app.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        return redirect('news:make_app')
