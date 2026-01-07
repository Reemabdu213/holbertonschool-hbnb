#!/usr/bin/env python3
"""
BaseModel - الكلاس الأساسي لكل الموديلات
"""
import uuid
from datetime import datetime


class BaseModel:
    """الكلاس الأساسي لكل الموديلات"""
    
    def __init__(self):
        """تهيئة الكائن الأساسي"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def save(self):
        """تحديث updated_at عند الحفظ"""
        self.updated_at = datetime.now()
    
    def update(self, data):
        """
        تحديث attributes من dictionary
        
        Args:
            data: dictionary يحتوي البيانات الجديدة
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
    
    def to_dict(self):
        """تحويل الكائن إلى dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
