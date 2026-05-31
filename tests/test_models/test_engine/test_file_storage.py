#!/usr/bin/python3
"""Tests for FileStorage"""
import unittest
import os
from unittest import skipIf
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.state import State

STORAGE_TYPE = os.getenv("HBNB_TYPE_STORAGE")


@skipIf(STORAGE_TYPE == "db", "FileStorage tests only")
class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage"""

    def setUp(self):
        self.storage = FileStorage()

    def test_all_returns_dict(self):
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_all_with_class_filter(self):
        state = State()
        state.name = "TestState"
        self.storage.new(state)
        result = self.storage.all(State)
        self.assertIsInstance(result, dict)
        for k in result.keys():
            self.assertTrue(k.startswith("State."))

    def test_new_adds_object(self):
        obj = BaseModel()
        self.storage.new(obj)
        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, self.storage.all())

    def test_delete_removes_object(self):
        obj = BaseModel()
        self.storage.new(obj)
        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, self.storage.all())
        self.storage.delete(obj)
        self.assertNotIn(key, self.storage.all())

    def test_delete_none_does_nothing(self):
        """Calling delete with None should not raise"""
        self.storage.delete(None)

    def test_all_no_filter_returns_all(self):
        obj1 = BaseModel()
        obj2 = State()
        obj2.name = "Nevada"
        self.storage.new(obj1)
        self.storage.new(obj2)
        result = self.storage.all()
        self.assertIn("BaseModel.{}".format(obj1.id), result)
        self.assertIn("State.{}".format(obj2.id), result)


@skipIf(STORAGE_TYPE != "db", "DBStorage tests only")
class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage"""

    def test_all_returns_dict(self):
        from models import storage
        result = storage.all()
        self.assertIsInstance(result, dict)

    def test_new_and_save_state(self):
        from models import storage
        initial = len(storage.all(State))
        state = State(name="TestDB_State")
        storage.new(state)
        storage.save()
        final = len(storage.all(State))
        self.assertEqual(final, initial + 1)
        storage.delete(state)
        storage.save()


if __name__ == "__main__":
    unittest.main()
