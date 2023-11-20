from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, Float,
    ForeignKey, UniqueConstraint
)

from sqlalchemy.orm import scoped_session

from sqlalchemy.orm import mapper, relationship, synonym

from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wish

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
)

games_table = Table(
    'games', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('publisher_name', ForeignKey('publishers.name')),
    Column('price', Float, nullable=True),
    Column('release_date', Date, nullable=True),
    Column('description', String(2000), nullable=True),
    Column('image_url', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
)

genres_table = Table(
    'genres', metadata,
    Column('name', String(255), primary_key=True, unique=True, nullable=False),
)

publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True, nullable=False),
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('game_id', ForeignKey('games.id')),
    Column('rating', Integer, nullable=False),
    Column('comment', String(2000), nullable=False),
    UniqueConstraint('user_id', 'game_id', 'comment', name='user_game_comment_unique')
)

wish_table = Table(
    'wish', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('game_id', ForeignKey('games.id')),
    Column('date_added', DateTime, nullable=True),
    UniqueConstraint('user_id', 'game_id', name='user_game_unique')
)

game_genre_relationship_table = Table(
    'game_genre_relationship', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.id')),
    Column('genre_name', ForeignKey('genres.name')),
)

def map_model_to_tables():
    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.name
    })

    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.id,
        '_Game__game_title': games_table.c.title,
        '_Game__price': games_table.c.price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.description,
        '_Game__image_url': games_table.c.image_url,
        '_Game__website_url': games_table.c.website_url,
        '_Game__publisher': relationship(Publisher),
        '_Game__genres': relationship(Genre, secondary=game_genre_relationship_table),
        '_Game__reviews': relationship(Review, backref='_Review__game', cascade_backrefs=False)
    })

    mapper(Review, reviews_table, properties={
        '_Review__rating': reviews_table.c.rating,
        '_Review__comment': reviews_table.c.comment,
        '_Review__user': relationship(User, backref='_User__reviews', cascade_backrefs=False),
    })

    mapper(User, users_table, properties={
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
    })

    mapper(Wish, wish_table, properties={
        '_Wish__game': relationship(Game, backref='_Game__wish'),
        '_Wish__user': relationship(User, backref='_User__wish'),
        '_Wish__wish_time': wish_table.c.date_added,
    })
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()