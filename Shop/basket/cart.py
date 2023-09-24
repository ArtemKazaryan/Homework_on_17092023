from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Basket(object):
    """
    Инициализация корзины
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get[settings.CART_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        Args:
            product: Экземпляр Product для добавления или обновления в корзине
            quantity: Необязательное целое число для количества продукта. По умолчанию используется значение 1
            update_quantity: Это логическое значение, которое указывает, требуется ли обновление количества с заданным количеством (True), или же новое количество должно быть добавлено к существующему количеству (False)

        """

        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0,
                                       'price': str(product.price)}
        if update_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Сохранение корзины
        """
        self.session[settings.CART_SESSION_ID] = self.basket
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def __iter__(self):
        """
            Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.basket[str(product.id)]['product'] = product

        for item in self.basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price'] * item['quantity'] for item in self.basket.values()))

    def clear(self):
        """
        Удаление корзины из сессии
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
