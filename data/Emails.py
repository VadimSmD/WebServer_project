import sqlalchemy
from db.db_session import SqlAlchemyBase


class Email(SqlAlchemyBase):
    __tablename__ = 'emails'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    reciever_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    thema = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
