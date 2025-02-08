#!/usr/bin/python3
"""DB storage class for AirBnB clone"""

from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class_mapping = {
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "User": User,
    "Place": Place,
    "Review": Review
}

class DBStorage:
    """Handles MySQL database interactions"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DB engine and create tables"""

        db_uri = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')
        )

        self.__engine = create_engine(db_uri, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

        self.reload()

    def all(self, cls=None):
        """Return a dictionary of all objects"""

        entities = {}

        if isinstance(cls, str):
            cls = class_mapping.get(cls, None)

        if cls:
            return self.get_data_from_table(cls, entities)

        for entity in class_mapping.values():
            entities = self.get_data_from_table(entity, entities)

        return entities

    def new(self, obj):
        """Add obj to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and start a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def get_data_from_table(self, cls, structure):
        """Retrieve all rows from a table"""
        if isinstance(structure, dict):
            query = self.__session.query(cls).all()
            for _row in query:
                key = "{}.{}".format(cls.__name__, _row.id)
                structure[key] = _row
        return structure

    def close(self):
        """Close the session"""
        self.__session.close()

