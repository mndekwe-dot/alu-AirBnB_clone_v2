#!/usr/bin/python3
"""FileStorage module"""
import json


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects, optionally filtered by class"""
        if cls is None:
            return self.__objects
        return {k: v for k, v in self.__objects.items()
                if type(v) is cls or type(v).__name__ == cls}

    def new(self, obj):
        """Sets obj in __objects with key <class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        json_objects = {}
        for key, obj in self.__objects.items():
            json_objects[key] = obj.to_dict()
        with open(self.__file_path, "w") as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
        try:
            with open(self.__file_path, "r") as f:
                json_objects = json.load(f)
            for key, value in json_objects.items():
                cls_name = value.get("__class__")
                if cls_name in classes:
                    self.__objects[key] = classes[cls_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it exists"""
        if obj is None:
            return
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects.pop(key, None)

    def close(self):
        """Calls reload() for deserializing the JSON file"""
        self.reload()
