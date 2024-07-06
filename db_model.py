import sqlalchemy
from db_session import SqlAlchemyBase

class Vacancy(SqlAlchemyBase):
    __tablename__ = 'vacancy'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    experience = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    salary = sqlalchemy.Column(sqlalchemy.String, nullable=True)




