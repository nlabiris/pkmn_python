# coding: utf-8
import json
import base64
from decimal import Decimal
from datetime import date, time, datetime
from sqlalchemy import Column, ForeignKey, Index, LargeBinary, String, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy, _AssociationList

Base = declarative_base()


def new_alchemy_encoder():
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj): # pylint: disable=method-hidden
            if isinstance(obj.__class__, DeclarativeMeta) or isinstance(obj.__class__, datetime) or not isinstance(obj.__class__, _AssociationList):
                # don't re-visit self unless it is specified otherwise
                if obj not in _visited_objs:
                    _visited_objs.append(obj)
                else:
                    if type(obj).__name__ not in models_to_expand():
                        return None

                # an SQLAlchemy class
                fields = {}
                attributes = obj.__json__() if hasattr(obj, '__json__') else dir(obj)
                for field in [x for x in attributes if not x.startswith('_') and x not in ['metadata', 'query', 'query_class']]:
                    value = obj.__getattribute__(field)
                    if isinstance(value, bytes):
                        fields[field] = base64.b64encode(value).decode().replace("\n", "")
                    elif isinstance(value, date):
                        fields[field] = value.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        fields[field] = value
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


def models_to_expand():
    return ["EvSpread", "IvSpread", "ContestEffect", "ContestType", "GrowthRate", "ItemFlingEffect",
            "ItemPocket", "MoveDamageClass", "MoveEffect", "MoveTarget", "PokemonColor", "PokemonHabitat",
            "PokemonShape", "Region", "SuperContestEffect", "Generation", "ItemCategory", "Stat",
            "Ability", "Item", "Nature", "Type", "EvolutionChain", "Move", "PokemonSpecy"]

class ContestEffect(Base):
    __tablename__ = 'contest_effects'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    appeal = Column(SMALLINT(6), nullable=False)
    jam = Column(SMALLINT(6), nullable=False)


class ContestType(Base):
    __tablename__ = 'contest_types'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)


class GrowthRate(Base):
    __tablename__ = 'growth_rates'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    formula = Column(Text(collation='utf8_unicode_ci'), nullable=False)


class ItemFlingEffect(Base):
    __tablename__ = 'item_fling_effects'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)


class ItemPocket(Base):
    __tablename__ = 'item_pockets'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)


class MoveDamageClass(Base):
    __tablename__ = 'move_damage_classes'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)


class MoveEffect(Base):
    __tablename__ = 'move_effects'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)


class MoveTarget(Base):
    __tablename__ = 'move_targets'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)


class PokemonColor(Base):
    __tablename__ = 'pokemon_colors'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)


class PokemonHabitat(Base):
    __tablename__ = 'pokemon_habitats'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    image = Column(LargeBinary)


class PokemonShape(Base):
    __tablename__ = 'pokemon_shapes'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    image = Column(LargeBinary)


class Region(Base):
    __tablename__ = 'regions'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)


class SuperContestEffect(Base):
    __tablename__ = 'super_contest_effects'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    appeal = Column(SMALLINT(6), nullable=False)


class Generation(Base):
    __tablename__ = 'generations'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    main_region_id = Column(ForeignKey('pkmn.regions.id'),
                            nullable=False, index=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)

    main_region = relationship('Region')


class ItemCategory(Base):
    __tablename__ = 'item_categories'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    pocket_id = Column(ForeignKey('pkmn.item_pockets.id'),
                       nullable=False, index=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)

    pocket = relationship('ItemPocket')


class Stat(Base):
    __tablename__ = 'stats'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    damage_class_id = Column(ForeignKey(
        'pkmn.move_damage_classes.id'), index=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    is_battle_only = Column(TINYINT(1), nullable=False)
    game_index = Column(INTEGER(11))

    damage_class = relationship('MoveDamageClass')


class Ability(Base):
    __tablename__ = 'abilities'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    generation_id = Column(ForeignKey(
        'pkmn.generations.id'), nullable=False, index=True)
    is_main_series = Column(TINYINT(1), nullable=False, index=True)

    generation = relationship('Generation')


class Item(Base):
    __tablename__ = 'items'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    category_id = Column(ForeignKey(
        'pkmn.item_categories.id'), nullable=False, index=True)
    cost = Column(INTEGER(11), nullable=False)
    fling_power = Column(INTEGER(11))
    fling_effect_id = Column(ForeignKey(
        'pkmn.item_fling_effects.id'), index=True)

    category = relationship('ItemCategory')
    fling_effect = relationship('ItemFlingEffect')


class Nature(Base):
    __tablename__ = 'natures'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    decreased_stat_id = Column(ForeignKey(
        'pkmn.stats.id'), nullable=False, index=True)
    increased_stat_id = Column(ForeignKey(
        'pkmn.stats.id'), nullable=False, index=True)
    hates_flavor_id = Column(ForeignKey(
        'pkmn.contest_types.id'), nullable=False, index=True)
    likes_flavor_id = Column(ForeignKey(
        'pkmn.contest_types.id'), nullable=False, index=True)
    game_index = Column(INTEGER(11), nullable=False, unique=True)

    decreased_stat = relationship(
        'Stat', primaryjoin='Nature.decreased_stat_id == Stat.id')
    hates_flavor = relationship(
        'ContestType', primaryjoin='Nature.hates_flavor_id == ContestType.id')
    increased_stat = relationship(
        'Stat', primaryjoin='Nature.increased_stat_id == Stat.id')
    likes_flavor = relationship(
        'ContestType', primaryjoin='Nature.likes_flavor_id == ContestType.id')


class Type(Base):
    __tablename__ = 'types'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    generation_id = Column(ForeignKey(
        'pkmn.generations.id'), nullable=False, index=True)
    damage_class_id = Column(ForeignKey(
        'pkmn.move_damage_classes.id'), index=True)
    image = Column(LargeBinary)
    color = Column(String(10, 'utf8_unicode_ci'), nullable=False)

    damage_class = relationship('MoveDamageClass')
    generation = relationship('Generation')


class EvolutionChain(Base):
    __tablename__ = 'evolution_chains'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    baby_trigger_item_id = Column(ForeignKey('pkmn.items.id'), index=True)

    baby_trigger_item = relationship('Item')


class Move(Base):
    __tablename__ = 'moves'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    generation_id = Column(ForeignKey(
        'pkmn.generations.id'), nullable=False, index=True)
    type_id = Column(ForeignKey('pkmn.types.id'), nullable=False, index=True)
    power = Column(SMALLINT(6))
    pp = Column(SMALLINT(6))
    accuracy = Column(SMALLINT(6))
    priority = Column(SMALLINT(6), nullable=False)
    target_id = Column(ForeignKey('pkmn.move_targets.id'),
                       nullable=False, index=True)
    damage_class_id = Column(ForeignKey(
        'pkmn.move_damage_classes.id'), nullable=False, index=True)
    effect_id = Column(ForeignKey('pkmn.move_effects.id'),
                       nullable=False, index=True)
    effect_chance = Column(INTEGER(11))
    contest_type_id = Column(ForeignKey('pkmn.contest_types.id'), index=True)
    contest_effect_id = Column(ForeignKey(
        'pkmn.contest_effects.id'), index=True)
    super_contest_effect_id = Column(ForeignKey(
        'pkmn.super_contest_effects.id'), index=True)

    contest_effect = relationship('ContestEffect')
    contest_type = relationship('ContestType')
    damage_class = relationship('MoveDamageClass')
    effect = relationship('MoveEffect')
    generation = relationship('Generation')
    super_contest_effect = relationship('SuperContestEffect')
    target = relationship('MoveTarget')
    type = relationship('Type')


class PokemonSpecy(Base):
    __tablename__ = 'pokemon_species'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    generation_id = Column(ForeignKey('pkmn.generations.id'), index=True)
    evolves_from_species_id = Column(INTEGER(11), index=True)
    evolution_chain_id = Column(ForeignKey(
        'pkmn.evolution_chains.id'), index=True)
    color_id = Column(ForeignKey('pkmn.pokemon_colors.id'),
                      nullable=False, index=True)
    shape_id = Column(ForeignKey('pkmn.pokemon_shapes.id'),
                      nullable=False, index=True)
    habitat_id = Column(ForeignKey('pkmn.pokemon_habitats.id'), index=True)
    gender_rate = Column(INTEGER(11), nullable=False)
    capture_rate = Column(INTEGER(11), nullable=False)
    base_happiness = Column(INTEGER(11), nullable=False)
    is_baby = Column(TINYINT(1), nullable=False)
    hatch_counter = Column(INTEGER(11), nullable=False)
    has_gender_differences = Column(TINYINT(1), nullable=False)
    growth_rate_id = Column(ForeignKey(
        'pkmn.growth_rates.id'), nullable=False, index=True)
    forms_switchable = Column(TINYINT(1), nullable=False)
    order = Column(INTEGER(11), nullable=False, index=True)
    conquest_order = Column(INTEGER(11), index=True)
    footprint = Column(LargeBinary)

    color = relationship('PokemonColor')
    evolution_chain = relationship('EvolutionChain')
    generation = relationship('Generation')
    growth_rate = relationship('GrowthRate')
    habitat = relationship('PokemonHabitat')
    shape = relationship('PokemonShape')


class Pokemon(Base):
    __tablename__ = 'pokemon'
    __table_args__ = {'schema': 'pkmn'}

    id = Column(INTEGER(11), primary_key=True)
    identifier = Column(String(79, 'utf8_unicode_ci'), nullable=False)
    species_id = Column(ForeignKey('pkmn.pokemon_species.id'), index=True)
    height = Column(INTEGER(11), nullable=False)
    weight = Column(INTEGER(11), nullable=False)
    base_experience = Column(INTEGER(11), nullable=False)
    order = Column(INTEGER(11), nullable=False, index=True)
    is_default = Column(TINYINT(1), nullable=False, index=True)

    species = relationship('PokemonSpecy')


class Candidate(Base):
    __tablename__ = 'candidate'

    id = Column(INTEGER(11), primary_key=True)
    pokemon_id = Column(ForeignKey('pkmn.pokemon.id'),
                        nullable=False, index=True)
    breeding_priority = Column(TINYINT(3))
    training_priority = Column(TINYINT(3))
    updated = Column(TIMESTAMP, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created = Column(TIMESTAMP, nullable=False,
                     server_default=text("CURRENT_TIMESTAMP"))

    pokemon = relationship('Pokemon')
    candidate_abilities = relationship('CandidateAbility', backref="candidate", cascade="all, delete",)
    candidate_ev_spreads = relationship('CandidateEvSpread', backref="candidate", cascade="all, delete",)
    candidate_items = relationship('CandidateItem', backref="candidate", cascade="all, delete",)
    candidate_iv_spreads = relationship('CandidateIvSpread', backref="candidate", cascade="all, delete",)
    candidate_moves = relationship('CandidateMove', backref="candidate", cascade="all, delete",)
    candidate_natures = relationship('CandidateNature', backref="candidate", cascade="all, delete",)

    abilities = association_proxy("candidate_abilities", "ability")
    items = association_proxy("candidate_items", "item")
    moves = association_proxy("candidate_moves", "move")
    natures = association_proxy("candidate_natures", "nature")

    def __json__(self):
        return ["id", "breeding_priority", "training_priority", "updated", "created",
                "pokemon", "candidate_abilities", "candidate_ev_spreads",
                "candidate_items", "candidate_iv_spreads", "candidate_moves",
                "candidate_natures"]


class CandidateAbility(Base):
    __tablename__ = 'candidate_abilities'

    id = Column(INTEGER(11), primary_key=True)
    candidate_id = Column(ForeignKey('candidate.id'),
                          nullable=False, index=True)
    ability_id = Column(ForeignKey('pkmn.abilities.id'),
                        nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created = Column(TIMESTAMP, nullable=False,
                     server_default=text("CURRENT_TIMESTAMP"))

    ability = relationship('Ability')

    def __json__(self):
        return ["id", "candidate_id", "ability_id", "updated", "created", "ability"]

    def __init__(self, ability):
        self.ability = ability


class CandidateEvSpread(Base):
    __tablename__ = 'candidate_ev_spreads'

    id = Column(INTEGER(11), primary_key=True)
    candidate_id = Column(ForeignKey('candidate.id'),
                          nullable=False, index=True)
    hp = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    atk = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    _def = Column('def', TINYINT(3), nullable=False,
                  server_default=text("'0'"))
    spatk = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    spdef = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    spe = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    sum = Column(SMALLINT(5), nullable=False, server_default=text("'0'"))
    updated = Column(TIMESTAMP, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created = Column(TIMESTAMP, nullable=False,
                     server_default=text("CURRENT_TIMESTAMP"))


class CandidateItem(Base):
    __tablename__ = 'candidate_items'

    id = Column(INTEGER(11), primary_key=True)
    candidate_id = Column(ForeignKey('candidate.id'),
                          nullable=False, index=True)
    item_id = Column(ForeignKey('pkmn.items.id'), nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created = Column(TIMESTAMP, nullable=False,
                     server_default=text("CURRENT_TIMESTAMP"))

    item = relationship('Item')

    def __json__(self):
        return ["id", "candidate_id", "item_id", "updated", "created", "item"]

    def __init__(self, item):
        self.item = item


class CandidateIvSpread(Base):
    __tablename__ = 'candidate_iv_spreads'

    id = Column(INTEGER(11), primary_key=True)
    candidate_id = Column(ForeignKey('candidate.id'),
                          nullable=False, index=True)
    hp = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    atk = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    _def = Column('def', TINYINT(3), nullable=False,
                  server_default=text("'0'"))
    spatk = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    spdef = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    spe = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    updated = Column(TIMESTAMP, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created = Column(TIMESTAMP, nullable=False,
                     server_default=text("CURRENT_TIMESTAMP"))


class CandidateMove(Base):
    __tablename__ = 'candidate_moves'

    id = Column(INTEGER(11), primary_key=True)
    candidate_id = Column(ForeignKey('candidate.id'),
                          nullable=False, index=True)
    move_id = Column(ForeignKey('pkmn.moves.id'), nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created = Column(TIMESTAMP, nullable=False,
                     server_default=text("CURRENT_TIMESTAMP"))

    move = relationship('Move')

    def __json__(self):
        return ["id", "candidate_id", "move_id", "updated", "created", "move"]

    def __init__(self, move):
        self.move = move


class CandidateNature(Base):
    __tablename__ = 'candidate_natures'

    id = Column(INTEGER(11), primary_key=True)
    candidate_id = Column(ForeignKey('candidate.id'),
                          nullable=False, index=True)
    nature_id = Column(ForeignKey('pkmn.natures.id'),
                       nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created = Column(TIMESTAMP, nullable=False,
                     server_default=text("CURRENT_TIMESTAMP"))

    nature = relationship('Nature')

    def __json__(self):
        return ["id", "candidate_id", "nature_id", "updated", "created", "nature"]

    def __init__(self, nature):
        self.nature = nature
