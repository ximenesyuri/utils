import importlib
from utils.err import ModErr

class mod:
    def exists(module):
        try:
            importlib.import_module(module)
            return True
        except:
            return False

    def get(module):
        try:
            return importlib.import_module(module)
        except Exception as e:
            raise ModErr(e)

    def has_object(module, *objects):
        try:
            return all(hasattr(mod.get(module), obj) for obj in objects)
        except Exception as e:
            raise ModErr(e)

    def get_object(module, *objects):
        try:
            existing_objects = []
            for obj in objects:
                if mod.has_object(module, obj):
                    existing_objects.append(getattr(mod.get(module), obj))
            if existing_objects:
                if len(existing_objects) > 1:
                    return existing_objects
                return existing_objects[0]
        except Exception as e:
            raise ModErr(e)
