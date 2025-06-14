from django import template

register = template.Library()

@register.filter
def get_category_bg_class(category):
    # Dictionary mapping categories to Bootstrap background classes
    category_classes = {
        'SIP': 'bg-success',
        'Rent': 'bg-danger',
        'Cash Transaction': 'bg-primary',
        'Online Food Platform': 'bg-warning',
        'Grooming': 'bg-info',
        'Home': 'bg-success',
        'College Fees': 'bg-primary',
        'Insurance': 'bg-warning',
    }
    return category_classes.get(category, 'bg-info')

@register.filter
def get_category_icon_class(category):
    # Dictionary mapping categories to Material Design Icons (MDI)
    category_icons = {
        'SIP': 'mdi-bank',
        'Rent': 'mdi-home',
        'Cash Transaction': 'mdi-cash',
        'Online Food Platform': 'mdi-food',
        'Grooming': 'mdi-face-man',
        'Home': 'mdi-home-variant',
        'College Fees': 'mdi-school',
        'Insurance': 'mdi-hospital',
        'Bills & Recharges': 'mdi-credit-card',
    }
    return category_icons.get(category, 'mdi-help-circle')