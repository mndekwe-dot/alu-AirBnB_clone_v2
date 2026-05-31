#!/usr/bin/python3
"""DBStorage module"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """Database storage engine using SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes DBStorage"""
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        db = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True
        )
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects, optionally filtered by class"""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        all_classes = [User, State, City, Amenity, Place, Review]
        objects = {}
        if cls:
            query = self.__session.query(cls).all()
        else:
            query = []
            for c in all_classes:
                query.extend(self.__session.query(c).all())
        for obj in query:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            objects[key] = obj
        return objects

    def new(self, obj):
        """Adds obj to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        try:
            self.__session.commit()
        except Exception:
            self.__session.rollback()
            raise

    def delete(self, obj=None):
        """Deletes obj from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables and initializes the session"""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the current session"""
        self.__session.close()
