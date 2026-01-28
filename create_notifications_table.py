"""
Migration script to create the notifications table.
Run with: pipenv run python create_notifications_table.py
"""
from database import engine
from models.notification import NotificationModel
from models.base import BaseModel

BaseModel.metadata.create_all(bind=engine)

print("OK Notifications table created successfully!")
