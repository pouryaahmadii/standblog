from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from .models import Article, Category, Comment , Contact
from .forms import ContactForm


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/post_list.html'
    context_object_name = 'articles'
    paginate_by = 1


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/post_details.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            login_url = 'account/login'
            return redirect(f"{login_url}?next={request.path}")
        body = request.POST.get('body')
        parent_id = request.POST.get('parent_id')

        if body:
            Comment.objects.create(user=request.user, article=self.object, body=body, parent_id=parent_id)
        return redirect('blog:detail', slug=self.kwargs['slug'])

class CategoryDetailView(ListView):
    model = Article
    template_name = 'blog/post_list.html'
    context_object_name = 'articles'

    category: Category
    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        self.category = get_object_or_404(Category, pk=category_id)
        queryset = super().get_queryset().filter(category=self.category)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ArticleSearchView(ListView):
    model = Article
    template_name = 'blog/post_list.html'
    context_object_name = 'articles'
    paginate_by = 1

    def get_queryset(self):
        queryset = self.request.GET.get('q')
        if queryset:
            return Article.objects.filter(Q(title__icontains=queryset)|Q(category__title__icontains=queryset)).distinct()
        return Article.objects.all()

class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'blog/contact_us.html'
    success_url = reverse_lazy('home_app:main')

    def form_valid(self, form):
        form_data = form.cleaned_data
        Contact.objects.create(**form_data)
        return super().form_valid(form)
