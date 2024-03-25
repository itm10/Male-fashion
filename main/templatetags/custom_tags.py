from django import template

register = template.Library()

@register.simple_tag
def calculate_total(count, price):
    try:
        count_int = int(count)
        price_int = int(price)
        return count_int * price_int
    except (ValueError, TypeError):
        return 0