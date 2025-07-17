from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()



class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    service = Column(String, nullable=False)
    category = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    invoice_number = Column(String, nullable=False, unique=False)