from json import JSONEncoder
from datetime import datetime
from django.db.models import QuerySet


class DateEncoder(JSONEncoder):
    def default(self, o):
        # if o is an instance of datetime
        #    return o.isoformat()
        if isinstance(o, datetime):
            return o.isoformat()
        # otherwise
        #    return super().default(o)
        else:
            return super().default(o)


class QuerySetEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        else:
            return super().default(o)


class ModelEncoder(DateEncoder, QuerySetEncoder, JSONEncoder):
    encoders = {}

    def default(self, o):
        #   if the object to decode is the same class as what's in the
        #   model property, then
        #     * create an empty dictionary that will hold the property names
        #       as keys and the property values as values
        if isinstance(o, self.model):
            d = {}
            # if o has the attribute get_api_url
            #    then add its return value to the dictionary
            #    with the key "href"
            if hasattr(o, "get_api_url"):
                d["href"] = o.get_api_url()
            #     * for each name in the properties list
            #         * get the value of that property from the model instance
            #           given just the property name
            #         * put it into the dictionary with that property name as
            #           the key
            #     * return the dictionary
            for property in self.properties:
                value = getattr(o, property)
                if property in self.encoders:
                    encoder = self.encoders[property]
                    value = encoder.default(value)
                d[property] = value
            d.update(self.get_extra_data(o))
            return d
        #   otherwise,
        #       return super().default(o)  # From the documentation
        else:
            return super().default(o)

    def get_extra_data(self, o):
        return {}
