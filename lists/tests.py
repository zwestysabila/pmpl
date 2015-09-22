from lists.models import Item
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', 
            {'comment':'yey, waktunya berlibur'}
        )
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_displays_comments_zero(self):
        request = HttpRequest()
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 0)
        self.assertIn('yey, waktunya berlibur', response.content.decode())

    def test_home_page_displays_comments_less_five(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertLess(Item.objects.count(), 5)
        self.assertGreater(Item.objects.count(), 0)
        self.assertIn('sibuk tapi santai', response.content.decode())

    def test_home_page_displays_comments_greater_equal_five(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        Item.objects.create(text='itemey 3')
        Item.objects.create(text='itemey 4')
        Item.objects.create(text='itemey 5')

        request = HttpRequest()
        response = home_page(request)

        self.assertGreaterEqual(Item.objects.count(), 5)
        self.assertIn('oh tidak', response.content.decode())

class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        #request = HttpRequest()
        #request.method = 'POST'
        #request.POST['item_text'] = 'A new list item'

        #response = home_page(request)
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)  #1
        new_item = Item.objects.first()  #2
        self.assertEqual(new_item.text, 'A new list item')  #3       
        
    def test_redirects_after_POST(self):
        #request = HttpRequest()
        #request.method = 'POST'
        #request.POST['item_text'] = 'A new list item'

        #response = home_page(request)
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
    
    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
