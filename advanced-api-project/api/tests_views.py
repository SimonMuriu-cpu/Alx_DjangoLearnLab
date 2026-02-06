"""
Unit tests for the Book API endpoints.
Tests CRUD operations, filtering, searching, ordering, and permissions.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(TestCase):
    """Test case for Book API endpoints."""
    
    def setUp(self):
        """
        Set up test data and client for each test.
        This runs before every test method.
        """
        # Create test client
        self.client = APIClient()
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="Test Author One")
        self.author2 = Author.objects.create(name="Test Author Two")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Python Programming",
            publication_year=2020,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Django Web Development",
            publication_year=2021,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="Advanced Django",
            publication_year=2022,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title="Python Cookbook",
            publication_year=2020,
            author=self.author2
        )
    
    # Helper methods
    def authenticate_user(self):
        """Authenticate as regular user."""
        self.client.force_authenticate(user=self.user)
    
    def authenticate_admin(self):
        """Authenticate as admin user."""
        self.client.force_authenticate(user=self.admin_user)
    
    def logout(self):
        """Remove authentication."""
        self.client.force_authenticate(user=None)
    
    # Test 1: List Books Endpoint
    def test_list_books_unauthenticated(self):
        """Test GET /api/books/ without authentication (should work)."""
        self.logout()
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Should return all 4 books
    
    def test_list_books_authenticated(self):
        """Test GET /api/books/ with authentication (should also work)."""
        self.authenticate_user()
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    # Test 2: Filtering functionality
    def test_filter_by_publication_year(self):
        """Test filtering books by publication_year."""
        response = self.client.get('/api/books/?publication_year=2020')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 books published in 2020
        
        # Check that all returned books have publication_year=2020
        for book in response.data:
            self.assertEqual(book['publication_year'], 2020)
    
    def test_filter_by_author(self):
        """Test filtering books by author."""
        response = self.client.get(f'/api/books/?author={self.author1.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 books by author1
        
        # Check that all returned books are by author1
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)
    
    # Test 3: Searching functionality
    def test_search_by_title(self):
        """Test searching books by title."""
        response = self.client.get('/api/books/?search=Python')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 books with "Python" in title
        
        titles = [book['title'] for book in response.data]
        self.assertIn("Python Programming", titles)
        self.assertIn("Python Cookbook", titles)
    
    def test_search_by_author_name(self):
        """Test searching books by author name."""
        response = self.client.get('/api/books/?search=Two')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 books by "Test Author Two"
    
    # Test 4: Ordering functionality
    def test_ordering_by_title_ascending(self):
        """Test ordering books by title (A-Z)."""
        response = self.client.get('/api/books/?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check titles are in alphabetical order
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_title_descending(self):
        """Test ordering books by title (Z-A)."""
        response = self.client.get('/api/books/?ordering=-title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check titles are in reverse alphabetical order
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_ordering_by_publication_year_descending(self):
        """Test ordering books by publication_year (newest first)."""
        response = self.client.get('/api/books/?ordering=-publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check books are ordered by publication_year descending
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
    
    # Test 5: Combined features
    def test_combined_filter_search_order(self):
        """Test combining filtering, searching, and ordering."""
        response = self.client.get(
            f'/api/books/?author={self.author1.id}&search=Programming&ordering=-publication_year'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book matches
        
        book = response.data[0]
        self.assertEqual(book['title'], "Python Programming")
        self.assertEqual(book['publication_year'], 2020)
        self.assertEqual(book['author'], self.author1.id)
    
    # Test 6: Retrieve Single Book
    def test_retrieve_book_unauthenticated(self):
        """Test GET /api/books/<id>/ without authentication (should work)."""
        self.logout()
        response = self.client.get(f'/api/books/{self.book1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.book1.author.id)
    
    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist."""
        response = self.client.get('/api/books/999/')  # Non-existent ID
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # Test 7: Create Book (Authentication required)
    def test_create_book_unauthenticated(self):
        """Test POST /api/books/create/ without authentication (should fail)."""
        self.logout()
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """Test POST /api/books/create/ with authentication (should succeed)."""
        self.authenticate_user()
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['publication_year'], data['publication_year'])
        self.assertEqual(response.data['author'], data['author'])
        
        # Verify book was actually created in database
        book_count = Book.objects.filter(title='New Test Book').count()
        self.assertEqual(book_count, 1)
    
    def test_create_book_validation_future_year(self):
        """Test creating book with future publication year (should fail validation)."""
        self.authenticate_user()
        from django.utils import timezone
        current_year = timezone.now().year
        future_year = current_year + 1
        
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    # Test 8: Update Book (Authentication required)
    def test_update_book_unauthenticated(self):
        """Test PUT /api/books/<id>/update/ without authentication (should fail)."""
        self.logout()
        data = {
            'title': 'Updated Title',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.put(
            f'/api/books/{self.book1.id}/update/', 
            data, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_book_authenticated(self):
        """Test PUT /api/books/<id>/update/ with authentication (should succeed)."""
        self.authenticate_user()
        data = {
            'title': 'Updated Python Programming',
            'publication_year': 2023,
            'author': self.author2.id  # Change author
        }
        response = self.client.put(
            f'/api/books/{self.book1.id}/update/', 
            data, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['publication_year'], data['publication_year'])
        self.assertEqual(response.data['author'], data['author'])
        
        # Verify book was actually updated in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, data['title'])
        self.assertEqual(self.book1.author.id, data['author'])
    
    # Test 9: Delete Book (Authentication required)
    def test_delete_book_unauthenticated(self):
        """Test DELETE /api/books/<id>/delete/ without authentication (should fail)."""
        self.logout()
        response = self.client.delete(f'/api/books/{self.book1.id}/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify book still exists
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_book_authenticated(self):
        """Test DELETE /api/books/<id>/delete/ with authentication (should succeed)."""
        self.authenticate_user()
        book_id = self.book1.id
        response = self.client.delete(f'/api/books/{book_id}/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book was actually deleted from database
        self.assertFalse(Book.objects.filter(id=book_id).exists())
    
    def test_delete_nonexistent_book(self):
        """Test deleting a book that doesn't exist."""
        self.authenticate_user()
        response = self.client.delete('/api/books/999/delete/')  # Non-existent ID
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PermissionTests(TestCase):
    """Additional tests specifically for permission scenarios."""
    
    def setUp(self):
        """Set up for permission tests."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
    
    def test_permissions_summary(self):
        """Test that permissions are correctly enforced across all endpoints."""
        endpoints_permissions = {
            '/api/books/': {'method': 'GET', 'auth_required': False},
            '/api/books/1/': {'method': 'GET', 'auth_required': False},
            '/api/books/create/': {'method': 'POST', 'auth_required': True},
            '/api/books/1/update/': {'method': 'PUT', 'auth_required': True},
            '/api/books/1/delete/': {'method': 'DELETE', 'auth_required': True},
        }
        
        for endpoint, info in endpoints_permissions.items():
            # Test without authentication
            self.client.force_authenticate(user=None)
            if info['method'] == 'GET':
                response = self.client.get(endpoint)
            elif info['method'] == 'POST':
                response = self.client.post(endpoint, {})
            elif info['method'] == 'PUT':
                response = self.client.put(endpoint, {})
            elif info['method'] == 'DELETE':
                response = self.client.delete(endpoint)
            
            if info['auth_required']:
                self.assertIn(
                    response.status_code, 
                    [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
                    f"{endpoint} should require authentication"
                )
            else:
                self.assertNotEqual(
                    response.status_code, 
                    status.HTTP_401_UNAUTHORIZED,
                    f"{endpoint} should not require authentication"
                )