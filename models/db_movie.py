from sqlalchemy import Column, Float, Integer, String

from config.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)

    class Config:
        orm_mode = True
