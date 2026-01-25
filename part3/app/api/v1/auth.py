import pytest
from app import create_app
from app.models.user import User

@pytest.fixture
def client():
    """إنشاء Flask test client"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_user(client):
    """إنشاء مستخدم للاختبار"""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password123"
    }
    # أضف المستخدم للنظام
    response = client.post('/api/v1/users/', json=user_data)
    return user_data

def test_login_success(client, sample_user):
    """اختبار تسجيل الدخول الناجح"""
    response = client.post('/api/v1/auth/login', json={
        'email': sample_user['email'],
        'password': sample_user['password']
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_credentials(client):
    """اختبار تسجيل دخول بمعلومات خاطئة"""
    response = client.post('/api/v1/auth/login', json={
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    assert 'error' in response.json

def test_protected_endpoint_without_token(client):
    """اختبار الوصول لـ endpoint محمي بدون token"""
    response = client.get('/api/v1/protected')
    
    assert response.status_code == 401

def test_protected_endpoint_with_token(client, sample_user):
    """اختبار الوصول لـ endpoint محمي مع token صحيح"""
    # الحصول على token
    login_response = client.post('/api/v1/auth/login', json={
        'email': sample_user['email'],
        'password': sample_user['password']
    })
    
    token = login_response.json['access_token']
    
    # استخدام الـ token
    response = client.get('/api/v1/protected', 
                          headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert 'message' in response.json

def test_token_contains_claims(client, sample_user):
    """اختبار أن الـ token يحتوي على الـ claims الصحيحة"""
    from flask_jwt_extended import decode_token
    
    login_response = client.post('/api/v1/auth/login', json={
        'email': sample_user['email'],
        'password': sample_user['password']
    })
    
    token = login_response.json['access_token']
    decoded = decode_token(token)
    
    assert 'sub' in decoded  # identity
    assert 'is_admin' in decoded
