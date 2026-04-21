from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from database.db import Base


class QREvent(Base):
    __tablename__ = "qr_events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    token = Column(String(255), unique=True, index=True)

    start_time_utc = Column(DateTime)
    end_time_utc = Column(DateTime)

    created_by = Column(Integer)  # user_id (RBAC user)
    created_at = Column(DateTime, default=datetime.utcnow)


class QRScan(Base):
    __tablename__ = "qr_scans"

    id = Column(Integer, primary_key=True, index=True)
    qr_id = Column(Integer, ForeignKey("qr_events.id"))

    scanned_at_utc = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(100))
    user_agent = Column(String(255))
    user_name = Column(String(100))