import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

factory: None | orm.session.sessionmaker = None

def global_init(db_file):
    global factory

    if factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Укажите файл базы данных")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    engine = sa.create_engine(conn_str, echo=False)
    factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    return factory()

