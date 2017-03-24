import logging
import datetime
import uuid

import ckan.model as m
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy import Index

from sqlalchemy.engine.reflection import Inspector
from ckan.model.meta import metadata, mapper, Session
from ckan.model.types import make_uuid
from ckan.model.domain_object import DomainObject
from ckan.lib.munge import munge_title_to_name

log = logging.getLogger(__name__)

__all__ = [
    'ckanextEvent', 'event_table',
]

event_table = None


def setup():
    if event_table is None:
        define_event_tables()
        log.debug('Event table defined in memory')

        if not event_table.exists():
            event_table.create()

    else:
        log.debug('Event table already exist')
        from ckan.model.meta import engine
        inspector = Inspector.from_engine(engine)

        index_names = [index['name'] for index in inspector.get_indexes("ckanext_event")]
        if not "ckanext_event_id_idx" in index_names:
            log.debug('Creating index for ckanext_event')
            Index("ckanext_event_id_idx", event_table.c.ckanext_event_id).create()
            Index("ckanext_event_name_idx", event_table.c.ckanext_event_name).create()


class ckanextEvent(DomainObject):
    '''Convenience methods for searching objects
    '''
    key_attr = 'id'

    @classmethod
    def get(cls, key, default=None, attr=None):
        '''Finds a single entity in the register.'''
        if attr is None:
            attr = cls.key_attr
        kwds = {attr: key}
        o = Session.query(cls).autoflush(False)
        o = o.filter_by(**kwds).first()
        if o:
            return o
        else:
            return default

    @classmethod
    def search(cls, limit, offset=0, order='id', **kwds):
        query = Session.query(cls).autoflush(False)
        query = query.filter_by(**kwds)
        query = query.order_by(order)
        query = query.limit(limit).offset(offset)
        return query.all()

    @classmethod
    def delete(cls, id):
        # Delete single event

        obj = Session.query(cls).filter_by(id=id)
        obj.delete()
        Session.commit()


def define_event_tables():
    global event_table
    event_table = Table('ckanext_event', metadata,
                        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
                        Column('name', types.UnicodeText, nullable=False, unique=True),
                        Column('title', types.UnicodeText, nullable=False),
                        Column('description', types.UnicodeText, default=u''),
                        Column('venue', types.UnicodeText, default=u''),
                        Column('start', types.DateTime, nullable=False),
                        Column('end', types.DateTime, nullable=False),
                        # SQLAlchemy 0.9 doesn't support JSON type
                        Column('meta', types.UnicodeText, default=u'{}'),
                        Column('active', types.Boolean, default=True),
                        Column('creator_id', types.UnicodeText, nullable=False),
                        Column('created_at', types.DateTime, default=datetime.datetime.utcnow),
                        Index('ckanext_event_id_idx', 'id'),
                        Index('ckanext_event_name_idx', 'name'))

    mapper(
        ckanextEvent,
        event_table
    )


def gen_event_name(title):
    name = munge_title_to_name(title).replace('_', '-')
    while '--' in name:
        name = name.replace('--', '-')
    print name
    evt_obj = Session.query(ckanextEvent).filter(ckanextEvent.name == name).first()
    if evt_obj:
        return name + str(uuid.uuid4())[:5]

    return name
