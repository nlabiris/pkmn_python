# coding: utf-8
import datetime
import json
from json import JSONEncoder
from sqlalchemy import Column, ForeignKey, Integer, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base = declarative_base()
metadata = Base.metadata


class AlchemyEncoder(JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other classes
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)


# class GenericJSONEncoder(JSONEncoder):
#     def default(self, obj): # pylint: disable=E0202
#         try:
#             return super().default(obj)
#         except TypeError:
#             pass
#         cls = type(obj)
#         result = {
#             '__custom__': True,
#             '__module__': cls.__module__,
#             '__name__': cls.__name__,
#             'data': obj.__json_encode__ if not hasattr(cls, '__json_encode__') else obj.__json_encode__
#         }
#         return result

# class DictMixIn:
#     """Provides a to_dict method to a SQLAlchemy database model."""

#     def to_dict(self):
#         """Returns a JSON serializable dictionary from a SQLAlchemy database model."""
#         a = {
#             column.name: getattr(self, column.name)
#             if not isinstance(
#                 getattr(self, column.name), (datetime.datetime, datetime.date)
#             )
#             else getattr(self, column.name).isoformat()
#             for column in self.__table__.columns
#         }
#         return a


class Ability(Base):
    __tablename__ = 'ability'

    id = Column(Integer, primary_key=True)
    name = Column(Text)


class EvSpread(Base):
    __tablename__ = 'ev_spread'

    id = Column(Integer, primary_key=True)
    hp = Column(Integer)
    atk = Column(Integer)
    _def = Column('def', Integer)
    spatk = Column(Integer)
    spdef = Column(Integer)
    spe = Column(Integer)
    sum = Column(Integer)


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(Text)


class IvSpread(Base):
    __tablename__ = 'iv_spread'

    id = Column(Integer, primary_key=True)
    hp = Column(Integer)
    atk = Column(Integer)
    _def = Column('def', Integer)
    spatk = Column(Integer)
    spdef = Column(Integer)
    spe = Column(Integer)
    sum = Column(Integer)


class Move(Base):
    __tablename__ = 'move'

    id = Column(Integer, primary_key=True)
    name = Column(Integer)

class Pokemon(Base):
    __tablename__ = 'pokemon'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    breeding_priority = Column(Integer)
    training_priority = Column(Integer)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class Stat(Base):
    __tablename__ = 'stat'

    id = Column(Integer, primary_key=True)
    name = Column(Integer)


class Nature(Base):
    __tablename__ = 'nature'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    increased_stat_id = Column(ForeignKey('stat.id'))
    decreased_stat_id = Column(ForeignKey('stat.id'))

    decreased_stat = relationship('Stat', primaryjoin='Nature.decreased_stat_id == Stat.id')
    increased_stat = relationship('Stat', primaryjoin='Nature.increased_stat_id == Stat.id')


class PokemonAbility(Base):
    __tablename__ = 'pokemon_abilities'

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(ForeignKey('pokemon.id'))
    ability_id = Column(ForeignKey('ability.id'))
    hidden_ability = Column(Integer)

    ability = relationship('Ability')
    pokemon = relationship('Pokemon')


class PokemonEvSpread(Base):
    __tablename__ = 'pokemon_ev_spreads'

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(ForeignKey('pokemon.id'))
    ev_spread_id = Column(ForeignKey('ev_spread.id'))

    ev_spread = relationship('EvSpread')
    pokemon = relationship('Pokemon')


class PokemonItem(Base):
    __tablename__ = 'pokemon_items'

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(ForeignKey('pokemon.id'))
    item_id = Column(ForeignKey('item.id'))

    item = relationship('Item')
    pokemon = relationship('Pokemon')


class PokemonIvSpread(Base):
    __tablename__ = 'pokemon_iv_spreads'

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(ForeignKey('pokemon.id'))
    iv_spread_id = Column(ForeignKey('iv_spread.id'))

    iv_spread = relationship('IvSpread')
    pokemon = relationship('Pokemon')


class PokemonMove(Base):
    __tablename__ = 'pokemon_moves'

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(ForeignKey('pokemon.id'))
    move_id = Column(ForeignKey('move.id'))

    move = relationship('Move')
    pokemon = relationship('Pokemon')


class PokemonNature(Base):
    __tablename__ = 'pokemon_natures'

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(ForeignKey('pokemon.id'))
    nature_id = Column(ForeignKey('nature.id'))

    nature = relationship('Nature')
    pokemon = relationship('Pokemon')
