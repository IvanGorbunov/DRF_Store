from store.models import Product


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
