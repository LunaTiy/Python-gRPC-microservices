from sqlalchemy import Column, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='categories_pkey'),
    )

    id = Column(Integer)
    category_name = Column(String(255), nullable=False)

    books = relationship('Books', back_populates='category')


class Books(Base):
    __tablename__ = 'books'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.id'], name='books_category_id_fkey'),
        PrimaryKeyConstraint('id', name='books_pkey')
    )

    id = Column(Integer)
    book_name = Column(String(255), nullable=False)
    category_id = Column(Integer, nullable=False)

    category = relationship('Categories', back_populates='books')
