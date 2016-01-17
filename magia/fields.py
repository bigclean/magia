# -*- coding: utf-8 -*-


class Field(object):

    def __init__(self, default=None):
        self.default = default


class IntField(Field):

    pass


class StringField(Field):

    pass


class PrimaryKeyField(IntField):

    pass
