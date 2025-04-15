from django import template

register = template.Library()

@register.filter
def filter_status(tasks, status):
    return [task for task in tasks if task.status == status] 