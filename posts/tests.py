from django.test import TestCase, Client
from posts.models import Post, User

class ProfileTest(TestCase):
    def setUp(self):
        # TODO translate all comments into English
        # создание тестового клиента — подходящая задача для функции setUp()
        self.client = Client()
        # создаём пользователя
        self.user = User.objects.create_user(
            username='sarah', email='connor.s@skynet.com', password='12345'
        )
        # создаём пост от имени пользователя
        self.post = Post.objects.create(text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!", author=self.user)

    def test_profile(self):
        # формируем GET-запрос к странице сайта
        response = self.client.get('/sarah/')

        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

        # проверяем, что при отрисовке страницы был получен список из 1 записи
        self.assertEqual(len(response.context['page']), 1)

        # проверяем, что объект пользователя, переданный в шаблон, 
        # соответствует пользователю, которого мы создали
        self.assertIsInstance(response.context['profile'], User)
        self.assertEqual(response.context['profile'].username, self.user.username)
    
    def test_add_post_authenticated(self):
        # test that authenticated user can add new posts
        if self.client.login(username='sarah', password='12345'):
            response = self.client.get('/new/')
            self.assertEqual(response.status_code, 200, 'Authenticated user must be able to add posts')
        else:
            self.assertTrue(False, 'Failed to authenticate test user')

    def test_add_post_anonymous(self):
        # test that anonymous user cannot add new posts and is redirected to home page
        self.client.logout()
        response = self.client.get('/new/')
        self.assertRedirects(response, '/auth/login/?next=/new/')
    
    def test_post_added(self):
        """ test that after adding a post it appears on home page, 
         on author's profile page on on single post view page """
        
        # TODO split into separate tests and user self.post instead of new_post
        # TODO perhaps move this to a separate class, because it has nothing to do with the profile

        # create test post
        new_post = Post.objects.create(text="The unknown future rolls toward us. " + 
            "I face it, for the first time, with a sense of hope. " + 
            "Because if a machine, a Terminator, can learn the value " + 
            "of human life, maybe we can too.", author=self.user)
        
        # test home page
        response_index = self.client.get('/')
        self.assertIn(new_post, 
            response_index.context['page'], 
            'new post must appear on the home page')

        # test profile
        response_profile = self.client.get('/sarah/')
        self.assertIn(new_post, 
            response_profile.context['page'], 
            "new post must appear on the author's profile page")
        
        # test post view page
        response_post = self.client.get('/sarah/' + str(new_post.id) + '/')
        self.assertEqual(new_post, 
            response_post.context['post'], 
            "new post must appear on post view page")
