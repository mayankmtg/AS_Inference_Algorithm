from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

# variables
Base = declarative_base()

class IPPrefix(Base):
    """
    Table containing all the uniqie IP Prefixes and prefix ids
    """
    
    __tablename__ = "ip_prefix"

    id = Column(Integer, primary_key=True)
    prefix = Column(String, unique=True)

    def __repr__(self):
        return "id: {} - prefix: {}".format(self.id, self.prefix)

class BaseAS(Base):
    """
    Table containing all the BaseAS sets
    """
    __tablename__ = "base_as"
    id = Column(Integer, primary_key=True)
    prefix_id = Column(Integer, ForeignKey(IPPrefix.id))
    asn = Column(Integer)

class BGPGaph(Base):
    
    """
    Table containing all the routeview entries in formatted sequence
    prefix - contains the IP prefix from the routeview entry
    path - contains the sequence of autonomous systems (ASes) found in the path to the prefix with each AS separated by '|'
    TODO :: Check if the path is from or to the prefix and mention clearly in the documentation here
    """

    __tablename__ = 'bgp_graph'

    id = Column(Integer, primary_key=True)
    prefix_id = Column(Integer, ForeignKey(IPPrefix.id))
    path = Column(String)

    def __repr__(self):
        return "id: {} - prefix: {} - path: {}".format(self.id, self.prefix_id, self.path)

def get_declarative_base() -> DeclarativeMeta:
    """
    Method to get the declarative base variable that links all models

    Returns:
        DeclarativeMeta: declarative base with defined models
    """
    return Base