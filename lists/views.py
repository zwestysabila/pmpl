from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List


# Create your views here.
def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def view_list(request, list_id):
   list_ = List.objects.get(id=list_id)
   return render(request, 'list.html', {'list': list_})

def home_page(request):
   #Items = Item.objects.all()
   countsItem = Item.objects.count()
   comment = 'yey, waktunya berlibur'
   
   if countsItem > 0:
       comment = 'sibuk tapi santai'
   if countsItem >= 5:
       comment = 'oh tidak'
   return render(request, 'home.html', {'comment' : comment})

def new_list(request):
   list_ = List.objects.create()
   Item.objects.create(text=request.POST['item_text'], list=list_)    
   return redirect('/lists/%d/' % (list_.id,))
