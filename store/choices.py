class Status:
    ORDERED = 'ordered'
    CANCELED = 'canceled'

    ITEMS = [
        ORDERED,
        CANCELED,
    ]

    CHOICES = (
        (ORDERED, 'Заказано'),
        (CANCELED, 'Отменено'),
    )
