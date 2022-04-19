from django.db.models import F

from store.choices import Status
from store.models import Product, OrderItem
from store.utils import find_by_key


def check_rest_products(products):
    if products is None:
        result = {
            'enough_products': False,
            'context': 'Не заполнен список товаров',
        }
        return result
    ids = [item['product'] for item in products]
    result = {
        'enough_products': False,
        'message': 'Нет в остатках на складе',
        'products': [],
    }
    objects = list(Product.objects.filter(pk__in=ids).values(
        'id',
        'title',
        'amount',
    ))
    enough = True
    for product in products:
        found = False
        for current_object in objects:
            if product['product'] == current_object['id']:
                found = True
                if product['quantity'] > current_object['amount']:
                    enough = False
                    p = dict(
                        title=current_object['title'],
                        quantity=product['quantity'] - current_object['amount']
                    )
                    result['products'].append(p)
            if found:
                break
    result['enough_products'] = enough
    return result


def write_off_of_products(order, products):
    ids = []
    for product in products:
        product_id = product['product'].id
        instance, _ = OrderItem.objects.update_or_create(
            order=order,
            product=product['product'],
            quantity=product['quantity'],
            price=product['price'],
        )
        ids.append(instance.id)
        # TODO: реализовать расчет себестоимости
        # уменьшим на количество купленного
        amount = Product.objects.filter(pk=product_id).values('amount')[0]['amount']
        amount -= product['quantity']
        Product.objects.filter(pk=product_id).update(amount=amount)

    OrderItem.objects.filter(order=order).exclude(pk__in=ids).delete()


def return_of_products(products):
    for product in products:
        product_id = product['id']
        # TODO: реализовать расчет себестоимости
        # увеличим остаток на количество купленного
        amount = Product.objects.filter(pk=product_id).values('amount')[0]['amount']
        amount += product['quantity']
        Product.objects.filter(pk=product_id).update(amount=amount)


def get_report(queryset):
    products = []
    # заказнные продукты
    ordered_orders = queryset.filter(status=Status.ORDERED).all()
    ordered_products = OrderItem.objects.filter(order__in=ordered_orders)
    ordered_products = ordered_products.annotate(product_title=F('product__title'))
    ordered_products = ordered_products.annotate(cost_price=F('product__cost_price')).all()
    if ordered_products:
        for item in ordered_products:
            revenue = item.quantity * item.price
            found_row = find_by_key(products, 'product_id', item.product.id)
            if found_row:
                found_row[1]['revenue'] += revenue
                found_row[1]['profit'] += revenue - item.cost_price * item.quantity
                found_row[1]['sale_item'] += item.quantity
            else:
                row = {
                    'product_id': item.product.id,
                    'product': item.product_title,
                    'revenue': revenue,
                    'profit': revenue - item.cost_price * item.quantity,
                    'sale_item': item.quantity,
                    'returns': 0,
                }
                products.append(row)

    # отмененные продукты
    canceled_orders = queryset.filter(status=Status.CANCELED).all()
    canceled_products = OrderItem.objects.filter(order__in=canceled_orders)
    canceled_products = canceled_products.annotate(product_title=F('product__title')).all()
    if canceled_products:
        for item in canceled_products:
            found_row = find_by_key(products, 'product_id', item.product.id)
            if found_row:
                found_row[1]['returns'] += item.quantity
            else:
                row = {
                    'product_id': item.product.id,
                    'product': item.product_title,
                    'revenue': 0,
                    'profit': 0,
                    'sale_item': 0,
                    'returns': item.quantity,
                }
                products.append(row)

    return products
