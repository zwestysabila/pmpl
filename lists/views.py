from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item


# Create your views here.
def view_list(request):
   items = Item.objects.all()
   return render(request, 'list.html', {'items': items})

def home_page(request):
   
   countsItem = Item.objects.count()
   comment = 'yey, waktunya berlibur'
   
   if countsItem > 0:
       comment = 'sibuk tapi santai'
   if countsItem >= 5:
       comment = 'oh tidak'
   return render(request, 'home.html', {'comment' : comment})

def new_list(request):
   Item.objects.create(text=request.POST['item_text'])    
   return redirect('/lists/the-only-list-in-the-world/')
