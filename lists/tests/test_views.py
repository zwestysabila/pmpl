from django.utils.html import escape
from lists.models import Item, List
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

#    def test_home_page_displays_comments_zero(self):
#       response = home_page(request)
#
#        self.assertEqual(Item.objects.count(), 0)
#        self.assertIn('yey, waktunya berlibur', response.content.decode())

#    def test_home_page_displays_comments_less_five(self):
#        list_ = List.objects.create()
#        Item.objects.create(text='itemey 1', list=list_)
#        Item.objects.create(text='itemey 2', list=list_)

#        request = HttpRequest()
#        response = home_page(request)

#        self.assertLess(Item.objects.count(), 5)
#        self.assertGreater(Item.objects.count(), 0)
#        self.assertIn('sibuk tapi santai', response.content.decode())

#    def test_home_page_displays_comments_greater_equal_five(self):
#        list_ = List.objects.create()
#        Item.objects.create(text='itemey 1', list=list_)
#        Item.objects.create(text='itemey 2', list=list_)
#        Item.objects.create(text='itemey 3', list=list_)
#        Item.objects.create(text='itemey 4', list=list_)
#        Item.objects.create(text='itemey 5', list=list_)

#        request = HttpRequest()
#        response = home_page(request)

#        self.assertGreaterEqual(Item.objects.count(), 5)
#        self.assertIn('oh tidak', response.content.decode())

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
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')
    
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
        
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)
