def lazyproperty(func):
    """
    A decorator for lazy evaluation of properties
    Source: http://code.activestate.com/recipes/576720-lazy-property/
    """
    cache = {}
    def _get(self):
        try:
            return cache[self]
        except KeyError:
            cache[self] = value = func(self)
            return value
        
    return property(_get)
