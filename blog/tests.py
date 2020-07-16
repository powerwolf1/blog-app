from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post
from django.urls import reverse
# Create your tests here.

class BlogTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username = 'testuser',
			email = 'test@email.com',
			password = 'secret'
			)
		self.post = Post.objects.create(
			title = 'Simple Title',
			body = 'Nice body content',
			author = self.user,
			)

	def test_string_representation(self):
		post = Post(title = 'Simple Title')
		self.assertEqual(str(post), post.title)

	def test_post_content(self):
		self.assertEqual(f'{self.post.title}', 'Simple Title')
		self.assertEqual(f'{self.post.body}', 'Nice body content')
		self.assertEqual(f'{self.post.author}', 'testuser')

	def test_post_list_view(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Nice body content')
		self.assertTemplateUsed(response, 'home.html')

	def test_post_detail_view(self):
		response = self.client.get('/post/1/')
		no_response = self.client.get('/post/10000/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(no_response.status_code, 404)
		self.assertContains(response, 'Simple Title')
		self.assertTemplateUsed(response, 'post_detail.html')
