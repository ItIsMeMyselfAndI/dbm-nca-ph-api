import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class ReleaseModel(Base):
    __tablename__ = "release"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    filename = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    page_count = Column(Integer, default=0)
    file_meta_created_at = Column(DateTime(timezone=True), nullable=True)
    file_meta_modified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    records = relationship("RecordModel", back_populates="release")


class RecordModel(Base):
    __tablename__ = "record"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    nca_number = Column(String, unique=True, nullable=False)
    nca_type = Column(String, nullable=False)
    department = Column(String, nullable=False)
    released_date = Column(String, nullable=False)
    purpose = Column(Text, nullable=False)
    release_id = Column(String, ForeignKey("release.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    release = relationship("ReleaseModel", back_populates="records")
    allocations = relationship("AllocationModel", back_populates="record")


class AllocationModel(Base):
    __tablename__ = "allocation"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    operating_unit = Column(String, nullable=False)
    agency = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    nca_number = Column(String, ForeignKey("record.nca_number"), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    record = relationship("RecordModel", back_populates="allocations")
