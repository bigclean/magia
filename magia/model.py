# -*- coding: utf-8 -*-

from .database import Database
from .expr import Expr
from .fields import Field


class MetaMongoModel(type):

    def __new__(cls, name, bases, attrs):
        cls = super(MetaMongoModel, cls).__new__(cls, name, bases, attrs)

        if '__tablename__' in cls.__dict__.keys():
            setattr(cls, 'db_table', cls.__dict__['__tablename__'])
        else:
            setattr(cls, 'db_table', cls.__name__.lower())

        fields = {}
        for name, attr in cls.__dict__.iteritems():
            if isinstance(attr, Field):
                attr.name = name
                fields[name] = attr
        setattr(cls, 'fields', fields)

        return cls


class MongoModel(object):
    __metaclass__ = MetaMongoModel

    def __init__(self, **kwargs):
        for key, val in kwargs.iteritems():
            setattr(self, key, val)

    @property
    def values(self):
        values = {}
        for name, attr in self.fields.iteritems():
            if name in self.__dict__:
                values[name] = self.__dict__[name]
            else:
                values[name] = attr.default
        return values

    def save(self):
        insert = 'insert ignore into {table} ({fields}) values ({vals});'.format(
            table=self.db_table,
            fields=', '.join(self.fields.keys()),
            vals=', '.join(['%s'] * len(self.fields))
        )
        return Database.execute(insert, self.values.values())

    @classmethod
    def where(cls, **kwargs):
        return Expr(cls, kwargs)
