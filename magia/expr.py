# -*- coding: utf-8 -*-

from .database import Database


class Expr(object):
    def __init__(self, model, kwargs):
        self.model = model
        self.params = kwargs.values()
        self.where_expr = ''
        for field in kwargs.keys():
            self._append_field_to_where_expr(field)

    def update(self, **kwargs):
        _keys = []
        _params = []
        for key, val in kwargs.iteritems():
            if val is None or key not in self.model.fields:
                continue
            _keys.append(key)
            _params.append(val)
        _params.extend(self.params)

        sql = 'update {table} set {fields} {where};'.format(
            table=self.model.db_table,
            fields=', '.join([key + ' = %s' for key in _keys]),
            where=self.where_expr,
        )
        return Database.execute(sql, _params)

    def all(self):
        sql = 'select {fields} from {table} {where};'.format(
            fields=', '.join(self.model.fields.keys()),
            table=self.model.db_table,
            where=self.where_expr
        )

        cursor = Database.execute(sql, self.params)
        for row in cursor.fetchall():
            yield self._make_instance_with_descriptor(
                self._get_desciptor(cursor), row
            )

    def first(self):
        sql = 'select {fields} from {table} {where};'.format(
            fields=', '.join(self.model.fields.keys()),
            table=self.model.db_table,
            where=self.where_expr
        )

        cursor = Database.execute(sql, self.params)
        row = cursor.fetchone()
        if not row:
            return None
        return self._make_instance_with_descriptor(
            self._get_desciptor(cursor), row
        )

    def count(self):
        sql = 'select count(*) from {table} {where};'.format(
            table=self.model.db_table,
            where=self.where_expr,
        )
        (row_cnt, ) = Database.execute(sql, self.params).fetchone()
        return row_cnt

    def limit(self, limit):
        self._append_condition_to_where_expr('limit', limit)
        return self

    def offset(self, offset):
        self._append_condition_to_where_expr('offset', offset)
        return self

    def _make_instance(self, row):
        instance = self.model()
        for idx, value in enumerate(row):
            field = instance.fields.keys()[idx]
            setattr(instance, field, value)
        return instance

    def _make_instance_with_descriptor(self, descriptor, row):
        try:
            return self.model(**dict(zip(descriptor, row)))
        except TypeError:
            return None

    def _append_field_to_where_expr(self, field):
        sub_expr = '{} = %s'.format(field)
        if not self.where_expr:
            self.where_expr = 'where {}'.format(sub_expr)
        else:
            self.where_expr += ' and {}'.format(sub_expr)

    def _append_condition_to_where_expr(self, condition, value):
        self.where_expr += ' {} {}'.format(condition, value)

    @classmethod
    def _get_desciptor(cls, cursor):
        return list(i[0] for i in cursor.description)
