#!/usr/bin/python3
"""BaseModel module"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models

time_format = "%Y-%m-%dT%H:%M:%S.%f"
Base = declarative_base()


class BaseModel:
    """BaseModel class - base for all models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiation of BaseModel"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" in kwargs:
                self.created_at = datetime.strptime(
                    kwargs["created_at"], time_format)
            else:
                self.created_at = datetime.utcnow()
            if "updated_at" in kwargs:
                self.updated_at = datetime.strptime(
                    kwargs["updated_at"], time_format)
            else:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def to_dict(self):
        """Returns a dictionary representation of the instance"""
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = type(self).__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        new_dict.pop("_sa_instance_state", None)
        return new_dict

    def save(self):
        """Saves the instance to storage"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Deletes the current instance from storage"""
        models.storage.delete(self)
