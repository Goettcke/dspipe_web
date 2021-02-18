import  os
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Knn_ldp(Base):
    __tablename__ = "knn_ldp"
    id = Column(Integer, primary_key=True)
    dataset = Column(String)
    number_of_samples = Column(Integer)
    percent_labelled = Column(Float)
    n_neighbors = Column(Integer)
    quality_measure = Column(String)
    evaluation_method = Column(String)
    result = Column(String)

class Lp_knn(Base):
    __tablename__ = "lp_knn"
    id = Column(Integer, primary_key=True)
    dataset = Column(String)
    number_of_samples = Column(Integer)
    percent_labelled = Column(Float)
    n_neighbors = Column(Integer)
    quality_measure = Column(String)
    evaluation_method = Column(String)
    result = Column(String)

class Lp_rbf(Base):
    __tablename__ = "lp_rbf"
    id = Column(Integer, primary_key=True)
    dataset = Column(String)
    number_of_samples = Column(Integer)
    percent_labelled = Column(Float)
    gamma = Column(Float)
    quality_measure = Column(String)
    evaluation_method = Column(String)
    result = Column(String)


class Ls_knn(Base):
    __tablename__ = "ls_knn"
    id = Column(Integer, primary_key=True)
    dataset = Column(String)
    number_of_samples = Column(Integer)
    percent_labelled = Column(Float)
    n_neighbors = Column(Integer)
    quality_measure = Column(String)
    evaluation_method = Column(String)
    result = Column(String)

class Ls_rbf(Base):
    __tablename__ = "ls_rbf"
    id = Column(Integer, primary_key=True)
    dataset = Column(String)
    number_of_samples = Column(Integer)
    percent_labelled = Column(Float)
    gamma = Column(Float)
    alpha = Column(Float)
    quality_measure = Column(String)
    evaluation_method = Column(String)
    result = Column(String)


if not os.path.isfile("db.sqlite"):
    engine = sqlalchemy.create_engine("sqlite:///db.sqlite",echo=True)
    Base.metadata.create_all(engine)

