from store.models import Product, OrderItem


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
