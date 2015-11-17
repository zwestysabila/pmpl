from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List

# Create your views here.
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    countList = Item.objects.filter(list_id=list_.id).count()
    if countList == 0 :
        comment = 'yey, waktunya berlibur'
    if (countList < 5) and (countList != 0) :
        comment = 'sibuk tapi santai'
    if countList >= 5 :
        comment = 'oh tidak'
    return render(request, 'list.html', {'list': list_, 'comment':comment})

def home_page(request):
    #if request.method == 'POST':
    #   Item.objects.create(text=request.POST['item_text'])
    #  return redirect('/lists/the-only-list-in-the-world/')
    #return render(request, 'home.html')
    countsItem = Item.objects.count()
    comment = 'yey, waktunya berlibur'   
    return render(request, 'home.html', {'comment':comment})

def list_page(request):
    countsItem = Item.objects.count()
    comment = 'yey, waktunya berlibur'   
    return render(request, 'home.html', {'comment':comment})

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:    
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect('/lists/%d/' % (list_.id,))
