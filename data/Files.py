import sqlalchemy
from db.db_session import SqlAlchemyBase


class File(SqlAlchemyBase):
    __tablename__ = 'files'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    reciever_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    ext = sqlalchemy.Column(sqlalchemy.String, nullable=True)
