#!/usr/bin/python3
"""Console module for AirBnB clone"""
import cmd
import shlex
import models
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


class HBnBCommand(cmd.Cmd):
    """HBnB command interpreter"""
    prompt = "(hbnb) "

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Does nothing on empty input"""
        pass

    def do_create(self, arg):
        """Creates a new instance with given parameters.
        Usage: create <Class name> [<key>=<value> ...]
        """
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        class_name = args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return

        obj = classes[class_name]()
        for param in args[1:]:
            if "=" not in param:
                continue
            key, _, raw_value = param.partition("=")
            if not key or not raw_value:
                continue
            # String value
            if raw_value.startswith('"'):
                if not raw_value.endswith('"') or len(raw_value) < 2:
                    continue
                value = raw_value[1:-1]
                # Validate: no unescaped quotes inside
                if '"' in value.replace('\\"', ''):
                    continue
                value = value.replace('\\"', '"').replace("_", " ")
                setattr(obj, key, value)
            else:
                # Float
                if "." in raw_value:
                    try:
                        value = float(raw_value)
                        setattr(obj, key, value)
                    except ValueError:
                        continue
                else:
                    # Integer
                    try:
                        value = int(raw_value)
                        setattr(obj, key, value)
                    except ValueError:
                        continue

        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """Shows an instance based on class name and id.
        Usage: show <Class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = models.storage.all().get(key)
        if obj is None:
            print("** no instance found **")
        else:
            print(obj)

    def do_destroy(self, arg):
        """Deletes an instance based on class name and id.
        Usage: destroy <Class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = models.storage.all().get(key)
        if obj is None:
            print("** no instance found **")
        else:
            models.storage.delete(obj)
            models.storage.save()

    def do_all(self, arg):
        """Shows all instances, optionally filtered by class name.
        Usage: all [Class name]
        """
        if arg and arg not in classes:
            print("** class doesn't exist **")
            return
        if arg:
            objs = models.storage.all(classes[arg])
        else:
            objs = models.storage.all()
        print([str(v) for v in objs.values()])

    def do_update(self, arg):
        """Updates an instance based on class name and id.
        Usage: update <Class name> <id> <attribute name> "<attribute value>"
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = models.storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        setattr(obj, args[2], args[3])
        obj.save()

    def default(self, arg):
        """Handles <class name>.<command>(<args>) syntax"""
        methods = {
            "all": self.do_all,
            "count": self._count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        if "." not in arg:
            print("*** Unknown syntax: {}".format(arg))
            return
        parts = arg.split(".", 1)
        cls_name = parts[0]
        rest = parts[1]
        if "(" not in rest or not rest.endswith(")"):
            print("*** Unknown syntax: {}".format(arg))
            return
        method_name = rest[:rest.index("(")]
        inner = rest[rest.index("(") + 1:-1]
        if method_name not in methods:
            print("*** Unknown syntax: {}".format(arg))
            return
        methods[method_name]("{} {}".format(cls_name, inner).strip())

    def _count(self, arg):
        """Counts instances of a class"""
        args = arg.split()
        if not args or args[0] not in classes:
            print(0)
            return
        print(len(models.storage.all(classes[args[0]])))


if __name__ == "__main__":
    HBnBCommand().cmdloop()
