#!/usr/bin/python3
"""Tests for BaseModel"""
import unittest
import os
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel"""

    def test_instance(self):
        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)

    def test_id_is_string(self):
        obj = BaseModel()
        self.assertIsInstance(obj.id, str)

    def test_created_at_is_datetime(self):
        obj = BaseModel()
        self.assertIsInstance(obj.created_at, datetime)

    def test_updated_at_is_datetime(self):
        obj = BaseModel()
        self.assertIsInstance(obj.updated_at, datetime)

    def test_to_dict_contains_class(self):
        obj = BaseModel()
        d = obj.to_dict()
        self.assertEqual(d["__class__"], "BaseModel")

    def test_to_dict_no_sa_instance(self):
        obj = BaseModel()
        d = obj.to_dict()
        self.assertNotIn("_sa_instance_state", d)

    def test_str_contains_class_name(self):
        obj = BaseModel()
        self.assertIn("BaseModel", str(obj))

    def test_kwargs_init(self):
        obj = BaseModel(name="test", number=42)
        self.assertEqual(obj.name, "test")
        self.assertEqual(obj.number, 42)


if __name__ == "__main__":
    unittest.main()
