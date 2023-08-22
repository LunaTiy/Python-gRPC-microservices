from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from services.recommendations.models import Books

engine = create_engine("postgresql+psycopg2://postgres:qwerty123@localhost:5432/marketplace", echo=False)
session_maker = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def session_scope() -> Iterator[Session]:
    session: Session = session_maker()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    with session_scope() as s:
        book = s.query(Books).filter(Books.category_id == 1).all()
        pass
