from flask import _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()
Session = sessionmaker()

class Database:
    def create_engine(self, uri):
        self.engine = create_engine(uri)

    def bind_engine(self):
        Base.metadata.bind = self.engine
        Session.configure(autocommit=False, autoflush=False, bind=self.engine)

    def create_session(self):
        self.session = scoped_session(Session, scopefunc=_app_ctx_stack.__ident_func__)

    def get_session(self):
        return self.session
