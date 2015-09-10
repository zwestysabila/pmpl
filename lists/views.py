from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title><head>Zwesty Tria Sabila<br></head><body>1206208403</body></html>')
