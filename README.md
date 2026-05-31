# AirBnB Clone v2

A second iteration of the AirBnB clone project, adding MySQL database support via SQLAlchemy alongside the existing FileStorage engine.

## Author
- mndekwe-dot (m.ndekwe@alustudent.com)

## Original Authors
- Guillaume Salva
- Julien Barbier

## Features
- Dual storage engines: FileStorage (JSON) and DBStorage (MySQL/SQLAlchemy)
- Switch via `HBNB_TYPE_STORAGE=db` environment variable
- Console with extended `create` command supporting key=value parameters
- Full SQLAlchemy ORM models: User, State, City, Place, Review, Amenity
- Many-to-Many relationship between Place and Amenity

## Setup

### FileStorage (default)
```bash
./console.py
```

### DBStorage
```bash
cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db \
HBNB_TYPE_STORAGE=db ./console.py
```

## Run tests
```bash
python3 -m unittest discover tests
```
