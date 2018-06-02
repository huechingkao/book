# -*- coding: utf8 -*-
from django.shortcuts import render
from django.views import generic
from .models import Book
from .models import Reader
from .models import Circulation
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

@method_decorator(login_required, name='dispatch')
class BookListView(generic.ListView):
    model = Book
    ordering = ['-id']
    paginate_by = 3 

@method_decorator(login_required, name='dispatch')
class BookDetailView(generic.DetailView):
    model = Book
    
    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['circulations'] = Circulation.objects.filter(book_id=self.kwargs['pk']).order_by("-id")
        return context	
    
@method_decorator(login_required, name='dispatch')
class BookCreate(CreateView):
    model = Book
    fields = "__all__"
    success_url = "/"   
    template_name = 'form.html' 
    
@method_decorator(login_required, name='dispatch') 
class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'   
    success_url = "/"   
    template_name = 'form.html'
    
@method_decorator(login_required, name='dispatch')      
class BookDelete(DeleteView):
    model = Book
    success_url = "/"
    template_name = 'confirm_delete.html'
    
@method_decorator(login_required, name='dispatch')
class ReaderListView(generic.ListView):
    model = Reader
    ordering = ['-id']
    paginate_by = 3 

@method_decorator(login_required, name='dispatch')
class ReaderDetailView(generic.DetailView):
    model = Reader
        
    def get_context_data(self, **kwargs):
        context = super(ReaderDetailView, self).get_context_data(**kwargs)
        context['circulations'] = Circulation.objects.filter(reader_id=self.kwargs['pk']).order_by("-id")
        return context	    
    
@method_decorator(login_required, name='dispatch')
class ReaderCreate(CreateView):
    model = Reader
    fields = "__all__"
    success_url = "/web/reader"   
    template_name = 'form.html' 
    
@method_decorator(login_required, name='dispatch') 
class ReaderUpdate(UpdateView):
    model = Reader
    fields = '__all__'   
    success_url = "/web/reader"   
    template_name = 'form.html'    
    
@method_decorator(login_required, name='dispatch')      
class ReaderDelete(DeleteView):
    model = Reader
    success_url = "/web/reader"
    template_name = 'confirm_delete.html'
    
@method_decorator(login_required, name='dispatch')
class Circulate1ListView(generic.ListView):
    model = Reader
    paginate_by = 3 
    template_name = 'web/circulate1.html'  
    
    def get_queryset(self):
        if self.request.GET.get('keyword'):
            readers = Reader.objects.filter(realname__icontains=self.request.GET.get('keyword')).order_by("-id")
        else :
            readers = Reader.objects.all().order_by("-id")
        return readers
      
    def get_context_data(self, **kwargs):
        context = super(Circulate1ListView, self).get_context_data(**kwargs)
        context['keyword'] = self.request.GET.get('keyword')
        return context	 

@method_decorator(login_required, name='dispatch')
class Circulate2ListView(generic.ListView):
    model = Book
    paginate_by = 3 
    template_name = 'web/circulate2.html'  
    
    def get_queryset(self):
        # 出借中的書籍 id list
        off_shelf_book_ids = [circulation.book_id for circulation in Circulation.objects.filter(date_return=None)]
        # 該使用者借閱中的書籍紀錄
        borrowing = Circulation.objects.filter(reader_id=self.kwargs['reader_id'], date_return=None)
        # 可借書籍清單：所有的書籍排除(exclude)出借中的書籍
        keyword = self.request.POST.get('keyword')
        if keyword != None:
            books = Book.objects.filter(title__icontains=keyword).exclude(id__in=off_shelf_book_ids).order_by('-id')
        else:
            books = Book.objects.exclude(id__in=off_shelf_book_ids).order_by('-id')
        return books
      
    def get_context_data(self, **kwargs):
        context = super(Circulate2ListView, self).get_context_data(**kwargs)
        context['keyword'] = self.request.GET.get('keyword')
        context['reader_id'] = self.kwargs['reader_id']        
        return context	 
      
@method_decorator(login_required, name='dispatch')
class Circulate3DetailView(generic.DetailView):
    model = Circulation
    template_name = 'web/circulate3.html'    
    
    def get_object(self):
        circulation = None
        try:
            is_lent = Circulation.objects.filter(book_id=self.kwargs['book_id'], date_return=None)
            if not is_lent: # 如果這本書還沒被借走才能登錄
                circulation = Circulation(reader_id=self.kwargs['reader_id'], book_id=self.kwargs['book_id'], date_checkout=datetime.now())
                circulation.save()
        except ObjectDoesNotExist:
            pass      
        return circulation
 
    def get_context_data(self, **kwargs):
        context = super(Circulate3DetailView, self).get_context_data(**kwargs)
        context['book'] = Book.objects.get(id=self.kwargs['book_id'])
        context['reader'] = Reader.objects.get(id=self.kwargs['reader_id'])        
        return context	 
      
@method_decorator(login_required, name='dispatch')
class Return1ListView(generic.ListView):
    model = Book
    ordering = ['-id']
    paginate_by = 3 
    template_name = 'web/return1.html'  
    
    def get_queryset(self):
        off_shelf_book_ids = [circulation.book_id for circulation in Circulation.objects.filter(date_return=None)]
        keyword = self.request.POST.get('keyword')
        if keyword != None:
            books = Book.objects.filter(title__icontains=keyword, id__in=off_shelf_book_ids).order_by('-id')
        else:
            books = Book.objects.filter(id__in=off_shelf_book_ids).order_by('-id')
        return books
      
    def get_context_data(self, **kwargs):
        context = super(Return1ListView, self).get_context_data(**kwargs)
        context['keyword'] = self.request.GET.get('keyword')    
        return context	 
      
@method_decorator(login_required, name='dispatch')
class Return2DetailView(generic.DetailView):
    model = Circulation
    template_name = 'web/return2.html'    
    
    def get_object(self):
        circulation = None
        try:
            circulation = Circulation.objects.get(book_id=self.kwargs['book_id'], date_return=None)
            circulation.date_return = datetime.now() # 填上歸還日期表示已還書
            circulation.save()
        except ObjectDoesNotExist:
            pass
        return circulation
 
    def get_context_data(self, **kwargs):
        context = super(Return2DetailView, self).get_context_data(**kwargs)             
        context['book'] = Book.objects.get(id=self.kwargs['book_id'])    
        return context	 
 
    