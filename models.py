from database import Base
from sqlalchemy import Column, Integer, String


class person(Base):
    __tablename__ = "Potential Supervisor"

    uid = Column("UID", Integer, primary_key=True)
    uni = Column("University", String)
    dept = Column("Department", String)
    name = Column("Name", String)
    ra = Column("ResearchArea", String)
    pub = Column("Publications", String)
    email = Column("E-Mail", String)
