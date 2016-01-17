# -*- coding: utf-8 -*-

from magia import (
    IntField,
    MongoModel,
)


class UniteParticipateRecord(MongoModel):
    __tablename__ = 'unite_participate_record'

    user_id = IntField(default=0)
    gift_id = IntField(default=0)
    code = IntField(default=0)
    user_gift_id = IntField(default=0)
