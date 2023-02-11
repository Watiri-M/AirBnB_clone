#!/usr/bin/python3
'''Module contains 'FileStorage' class definition.
'''
import json


class FileStorage:
    '''class FileStorage.
    Handles persitence for the application by saving objects to the file
    'file.json'
    '''
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        '''Returns the contents of the '__objects' dictionary
        '''
        # Deferred Imports
        from models.amenity import Amenity
        from models.base_model import BaseModel
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        class_names = ('BaseModel', 'User', 'Place', 'City', 'State',
                       'Amenity', 'Review')
        objs_dict = {}
        for obj_id in FileStorage.__objects.keys():
            args = obj_id.split('.')
            class_name = args[0].strip()
            if class_name in class_names:
                temp = FileStorage.__objects[obj_id]
                objs_dict[obj_id] = eval(class_name)(**temp)
        return objs_dict

    def new(self, obj):
        '''Adds the object 'obj' to the collection of objects in the
        '__objects' dictionary.
        '''
        key = '{}.{}'.format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj.to_dict()

    def save(self):
        '''Saves the contents of the '__objects' dictionary to the json file
        specified in the '__file_path' class attribute.
        '''
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as fp:
            json.dump(FileStorage.__objects, fp)

    def reload(self):
        '''Sets the '__objects' dictionary with the collection of objects
        retrieved for the file.json file.
        '''
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as fp:
                FileStorage.__objects = json.load(fp)
        except NameError:
            pass
        except IOError:
            pass

    def delete(self, key):
        '''deletes an entry from the __objects class attribute and updates the
        file
        '''
        if key in FileStorage.__objects.keys():
            del FileStorage.__objects[key]
            with open(FileStorage.__file_path, 'w', encoding='utf-8') as fp:
                json.dump(FileStorage.__objects, fp)
