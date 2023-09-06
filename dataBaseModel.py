from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, server_default='autoincrement()')
    publication_date = Column(String)
    views_summary = Column(String)
    views_pdf = Column(String)
    doi_link = Column(String)
    link_title = Column(String)
    header_title = Column(String)
    author_text = Column(String)
    affiliation_text = Column(String)

    def __repr__(self):
        return f"<Article(id={self.id}, header_title='{self.header_title}')>"
