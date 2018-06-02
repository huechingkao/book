from django import template
from web.models import Book, Reader

register = template.Library()

@register.filter
def reader_realname(reader_id):
    return Reader.objects.get(id=reader_id).realname
  
@register.filter
def book_title(book_id):
    return Book.objects.get(id=book_id).title