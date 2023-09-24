from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from .models import Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'shop/index.html'
    title = 'Top Shop'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'shop/list.html'
    paginate_by = 3
    title = 'Top Shop - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


