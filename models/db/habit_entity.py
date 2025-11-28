import uuid
from datetime import date, datetime
from sqlalchemy import String, Boolean, Date, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.db_session import Base


class HabitEntity(Base):
    __tablename__ = "habits"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=True)  # روزانه، هفتگی، ماهانه، سالانه
    goal_type: Mapped[str] = mapped_column(String(20), nullable=False, default="boolean")  # count / boolean / time
    daily_goal: Mapped[int] = mapped_column(Integer, nullable=True, default=1)  # مثلاً ۱۰ صفحه، ۳۰ دقیقه
    start_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Relationships
    logs: Mapped[list["HabitLogEntity"]] = relationship(back_populates="habit", cascade="all, delete-orphan")
    stats: Mapped[list["HabitStatsEntity"]] = relationship(back_populates="habit", cascade="all, delete-orphan")


class HabitLogEntity(Base):
    __tablename__ = "habit_logs"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    habit_id: Mapped[str] = mapped_column(String(50), ForeignKey("habits.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)  # کلید اصلی برای تحلیل
    value: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # مثلاً ۵ صفحه یا ۲۰ دقیقه یا ۱ برای انجام شد
    note: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationship
    habit: Mapped["HabitEntity"] = relationship(back_populates="logs")


class HabitStatsEntity(Base):
    __tablename__ = "habit_stats"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    habit_id: Mapped[str] = mapped_column(String(50), ForeignKey("habits.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=True)  # NULL برای آمار سالانه
    week: Mapped[int] = mapped_column(Integer, nullable=True)  # NULL برای آمار ماهانه/سالانه
    total_value: Mapped[int] = mapped_column(Integer, default=0)
    percent_success: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.utcnow())
    
    # Relationship
    habit: Mapped["HabitEntity"] = relationship(back_populates="stats")

