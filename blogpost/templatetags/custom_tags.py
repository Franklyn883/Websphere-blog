from django import template

register = template.Library()

@register.filter
def has_liked(comment, user):
    return comment.likes.filter(user=user).exists()