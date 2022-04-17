class Status:
    ORDERED = 'ordered'
    CANSELED = 'canseled'

    ITEMS = [
        ORDERED,
        CANSELED,
    ]

    CHOICES = (
        (ORDERED, 'Заказано'),
        (CANSELED, 'Отменено'),
    )
