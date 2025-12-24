from django import template
from blog.models import Article, Category  # دسترسی به مدل‌های blog
register = template.Library()

@register.inclusion_tag('includes/sidebar.html', takes_context=True)
def sidebar(context, posts_count=5, show_categories=True):
    """
    Sidebar شامل ریسنت پست‌ها و دسته‌ها از اپ blog
    """
    recent = Article.objects.order_by('-updated')[:posts_count]
    categories = Category.objects.all() if show_categories else []
    return {
        'recent': recent,
        'categories': categories
    }
