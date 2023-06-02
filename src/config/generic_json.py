import json


class GenericJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        """Implement this method in a subclass such that it returns"""

        # a serializable object for ``obj`` if possible,
        # otherwise call the base implementation (to raise a TypeError).
        try:
            return super().default(obj)
        except TypeError:
            pass

        # use __json_encode__ method if available
        if hasattr(obj, '__json_encode__'):
            return obj.__json_encode__()

        # convert obj to custom dict
        cls = type(obj)
        result = {
            '__custom__': True,
            '__module__': cls.__module__,
            '__name__': cls.__name__,
        }

        # use the object's dict attribute
        if hasattr(obj, '__dict__'):
            data = {k: self.default(v) for k, v in obj.__dict__.items()}
            result['data'] = data
            return result

        # convert iterables
        if hasattr(obj, '__iter__'):
            data = [self.default(v) for v in obj]
            result['data'] = data
            return result

        # convert anything else
        return obj


class GenericJSONDecoder(json.JSONDecoder):
    def decode(self, obj):
        """Implement this method in a subclass such that it returns"""

        # use __json_decode__ method if available
        if hasattr(obj, '__json_decode__'):
            return obj.__json_decode__()

        # convert dict to object
        if isinstance(obj, dict):
            # check if this is a custom encoded object
            if '__custom__' not in obj:
                return {k: self.decode(v) for k, v in obj.items()}

            # convert custom encoded object
            module = obj['__module__']
            name = obj['__name__']
            data = obj['data']

            # import module if not already imported
            import sys
            if not module in sys.modules:
                __import__(module)
            cls = getattr(sys.modules[module], name)
            obj = cls.__new__(cls)

            # set all attributes
            if hasattr(obj, '__dict__'):
                for k, v in data.items():
                    setattr(obj, k, self.decode(v))
                return obj

            # set all items
            if hasattr(obj, '__iter__'):
                if isinstance(obj, tuple):
                    return tuple(self.decode(v) for v in data)
                for k, v in enumerate(data):
                    obj.__setitem__(k, self.decode(v))
                return obj

        # a serializable object for ``obj`` if possible,
        # otherwise call the base implementation (to raise a TypeError).
        if isinstance(obj, str):
            try:
                obj = super().decode(obj)
                return self.decode(obj)
            except ValueError:
                pass

        # convert anything else
        return obj
