import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from utils import logger


engine = sqlalchemy.create_engine("sqlite:///book.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class BookModel(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    genre = Column(String(80))
    count = Column(Integer)

    def __init__(self, title, genre, count):
        self.title = title
        self.genre = genre
        self.count = count

    @classmethod
    def fynd_by_id(cls, id):
        logger.info(f"Find book by id {id}")
        return session.query(BookModel).filter_by(id=id).first()

    @classmethod
    def find_by_genre(cls, genre):
        logger.info(f"Find book by genre {genre}")
        return session.query(BookModel).filter_by(genre=genre).all()

    @classmethod
    def find_by_title(cls, title):
        logger.info(f"Find book by title {title}")
        return session.query(BookModel).filter_by(title=title).first()

    def save_to_db(self):
        logger.info(f"Save Book {self} to db")
        session.add(self)
        session.commit()

    def update_count(self, count):
        logger.info(f"Update book {self} count to {count}")
        self.count = count
        session.commit()

    def __repr__(self):
        return f"Book: title {self.title}, genre: {self.genre}, count {self.count}, id {self.id}"


Base.metadata.create_all(engine)