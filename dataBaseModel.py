from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TCNK_Table(Base):
    __tablename__ = 'tcnk'
    id = Column(Integer, primary_key=True, server_default='autoincrement()')
    publication_date = Column(String)
    views_summary = Column(String)
    views_pdf = Column(String)
    doi_link = Column(String)
    link_title = Column(String)
    header_title = Column(String)
    author_text = Column(String)
    affiliation_text = Column(String)


class TMH_Table(Base):
    __tablename__ = 'tmh'
    id = Column(Integer, primary_key=True, server_default='autoincrement()')
    publication_date = Column(String)
    views_summary = Column(String)
    views_pdf = Column(String)
    link_title = Column(String)
    header_title = Column(String)
    author_text = Column(String)
    affiliation_text = Column(String)


class YHTHVB_Table(Base):
    __tablename__ = 'yhthvb'
    id = Column(Integer, primary_key=True, server_default='autoincrement()')
    publication_date = Column(String)
    views_summary = Column(String)
    views_pdf = Column(String)
    doi_link = Column(String)
    link_title = Column(String)
    header_title = Column(String)
    author_text = Column(String)
    affiliation_text = Column(String)


class DDVTP_Table(Base):
    __tablename__ = 'ddvtp'
    id = Column(Integer, primary_key=True, server_default='autoincrement()')
    publication_date = Column(String)
    views_summary = Column(String)
    views_pdf = Column(String)
    doi_link = Column(String)
    link_title = Column(String)
    header_title = Column(String)
    author_text = Column(String)
    affiliation_text = Column(String)


class YHN_Table(Base):
    __tablename__ = 'yhn'
    id = Column(Integer, primary_key=True, server_default='autoincrement()')
    publication_date = Column(String)
    views_summary = Column(String)
    views_pdf = Column(String)
    doi_link = Column(String)
    link_title = Column(String)
    header_title = Column(String)
    author_text = Column(String)
    affiliation_text = Column(String)
