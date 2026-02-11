#!/usr/bin/env python3
"""
Run the Flask application
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    # تاسك 4: إنشاء Admin عند التشغيل
    with app.app_context():
        from app.services.facade import facade
        
        try:
            admin_data = {
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@hbnb.com',
                'password': 'admin123',
                'is_admin': True
            }
            
            existing = facade.get_user_by_email('admin@hbnb.com')
            if not existing:
                admin = facade.create_user(admin_data)
                print(f"✅ Admin created: {admin.email}")
            else:
                print(f"ℹ️  Admin exists: {existing.email}")
        except Exception as e:
            print(f"⚠️  Admin creation error: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
