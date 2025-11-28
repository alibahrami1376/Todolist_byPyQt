from typing import List, Optional, Dict
from datetime import date, datetime
from sqlalchemy import select, func, and_, update, delete, case
from sqlalchemy.orm import Session
from services.db_session import get_session, Base, engine
from models.db.habit_entity import HabitEntity, HabitLogEntity, HabitStatsEntity


class HabitService:
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def create_habit(
        self,
        title: str,
        category: str,
        goal_type: str = "boolean",
        daily_goal: int = 1,
        start_date: Optional[date] = None,
        description: Optional[str] = None
    ) -> str:
        """ایجاد عادت جدید با SQLAlchemy"""
        if start_date is None:
            start_date = date.today()
        
        with get_session() as db:
            habit = HabitEntity(
                title=title,
                category=category,
                goal_type=goal_type,
                daily_goal=daily_goal,
                start_date=start_date,
                description=description,
                is_active=True
            )
            db.add(habit)
            db.commit()
            db.refresh(habit)
            return habit.id

    def get_all_habits(self, active_only: bool = True) -> List[HabitEntity]:
        """دریافت همه عادت‌ها با SQLAlchemy select"""
        with get_session() as db:
            stmt = select(HabitEntity)
            if active_only:
                stmt = stmt.where(HabitEntity.is_active == True)
            stmt = stmt.order_by(HabitEntity.created_at.desc())
            result = db.execute(stmt)
            return list(result.scalars().all())

    def get_habit_by_id(self, habit_id: str) -> Optional[HabitEntity]:
        """دریافت عادت بر اساس ID با SQLAlchemy"""
        with get_session() as db:
            stmt = select(HabitEntity).where(HabitEntity.id == habit_id)
            result = db.execute(stmt)
            return result.scalar_one_or_none()

    def update_habit(
        self,
        habit_id: str,
        title: Optional[str] = None,
        category: Optional[str] = None,
        goal_type: Optional[str] = None,
        daily_goal: Optional[int] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> bool:
        """به‌روزرسانی عادت با SQLAlchemy update statement"""
        with get_session() as db:
            # ساخت دیکشنری برای فیلدهای به‌روزرسانی
            update_data = {}
            if title is not None:
                update_data['title'] = title
            if category is not None:
                update_data['category'] = category
            if goal_type is not None:
                update_data['goal_type'] = goal_type
            if daily_goal is not None:
                update_data['daily_goal'] = daily_goal
            if description is not None:
                update_data['description'] = description
            if is_active is not None:
                update_data['is_active'] = is_active
            
            if not update_data:
                return False
            
            # استفاده از update statement برای بهینه‌سازی
            stmt = (
                update(HabitEntity)
                .where(HabitEntity.id == habit_id)
                .values(**update_data)
            )
            result = db.execute(stmt)
            db.commit()
            return result.rowcount > 0

    def delete_habit(self, habit_id: str) -> bool:
        """حذف عادت با SQLAlchemy delete statement"""
        with get_session() as db:
            # استفاده از delete statement
            stmt = delete(HabitEntity).where(HabitEntity.id == habit_id)
            result = db.execute(stmt)
            db.commit()
            return result.rowcount > 0

    def log_habit(
        self,
        habit_id: str,
        log_date: date,
        value: int = 1,
        note: Optional[str] = None
    ) -> Optional[str]:
        """ثبت لاگ برای عادت با SQLAlchemy - استفاده از upsert pattern"""
        with get_session() as db:
            # بررسی وجود لاگ برای این تاریخ
            stmt = select(HabitLogEntity).where(
                and_(
                    HabitLogEntity.habit_id == habit_id,
                    HabitLogEntity.date == log_date
                )
            )
            existing_log = db.execute(stmt).scalar_one_or_none()
            
            if existing_log:
                # به‌روزرسانی لاگ موجود
                update_stmt = (
                    update(HabitLogEntity)
                    .where(HabitLogEntity.id == existing_log.id)
                    .values(value=value, note=note if note is not None else existing_log.note)
                )
                db.execute(update_stmt)
                db.commit()
                return existing_log.id
            else:
                # ایجاد لاگ جدید
                log = HabitLogEntity(
                    habit_id=habit_id,
                    date=log_date,
                    value=value,
                    note=note
                )
                db.add(log)
                db.commit()
                db.refresh(log)
                return log.id

    def remove_habit_log(self, habit_id: str, log_date: date) -> bool:
        """حذف لاگ عادت برای تاریخ مشخص با SQLAlchemy delete"""
        with get_session() as db:
            stmt = delete(HabitLogEntity).where(
                and_(
                    HabitLogEntity.habit_id == habit_id,
                    HabitLogEntity.date == log_date
                )
            )
            result = db.execute(stmt)
            db.commit()
            return result.rowcount > 0

    def get_habit_logs(
        self,
        habit_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[HabitLogEntity]:
        """دریافت لاگ‌های عادت با SQLAlchemy select و فیلترهای پویا"""
        with get_session() as db:
            stmt = select(HabitLogEntity).where(HabitLogEntity.habit_id == habit_id)
            
            if start_date:
                stmt = stmt.where(HabitLogEntity.date >= start_date)
            if end_date:
                stmt = stmt.where(HabitLogEntity.date <= end_date)
            
            stmt = stmt.order_by(HabitLogEntity.date.desc())
            result = db.execute(stmt)
            return list(result.scalars().all())

    def is_habit_completed_on_date(self, habit_id: str, check_date: date) -> bool:
        """بررسی تکمیل عادت در تاریخ مشخص با SQLAlchemy exists"""
        with get_session() as db:
            stmt = select(func.count(HabitLogEntity.id)).where(
                and_(
                    HabitLogEntity.habit_id == habit_id,
                    HabitLogEntity.date == check_date,
                    HabitLogEntity.value > 0
                )
            )
            result = db.execute(stmt).scalar()
            return result > 0

    def get_habits_by_category(self, category: str) -> List[HabitEntity]:
        """دریافت عادت‌ها بر اساس دسته‌بندی با SQLAlchemy"""
        with get_session() as db:
            stmt = (
                select(HabitEntity)
                .where(
                    and_(
                        HabitEntity.category == category,
                        HabitEntity.is_active == True
                    )
                )
                .order_by(HabitEntity.created_at.desc())
            )
            result = db.execute(stmt)
            return list(result.scalars().all())

    def get_habit_statistics(
        self,
        habit_id: str,
        start_date: date,
        end_date: date
    ) -> Dict:
        """دریافت آمار عادت با SQLAlchemy aggregate functions"""
        with get_session() as db:
            # استفاده از aggregate functions برای محاسبه آمار
            stmt = select(
                func.count(HabitLogEntity.id).label('total_logs'),
                func.sum(HabitLogEntity.value).label('total_value'),
                func.sum(
                    case((HabitLogEntity.value > 0, 1), else_=0)
                ).label('completed_days'),
                func.avg(HabitLogEntity.value).label('average_value')
            ).where(
                and_(
                    HabitLogEntity.habit_id == habit_id,
                    HabitLogEntity.date >= start_date,
                    HabitLogEntity.date <= end_date
                )
            )
            
            result = db.execute(stmt).first()
            
            total_days = (end_date - start_date).days + 1
            completed_days = result.completed_days or 0
            total_value = result.total_value or 0
            average_value = float(result.average_value) if result.average_value else 0.0
            success_rate = (completed_days / total_days * 100) if total_days > 0 else 0.0
            
            return {
                "total_days": total_days,
                "completed_days": int(completed_days),
                "total_value": int(total_value),
                "success_rate": round(success_rate, 2),
                "average_value": round(average_value, 2)
            }

    def get_habits_with_logs_count(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict]:
        """دریافت عادت‌ها همراه با تعداد لاگ‌هایشان با SQLAlchemy join"""
        with get_session() as db:
            # ساخت شرط‌های فیلتر برای لاگ‌ها
            log_conditions = []
            if start_date:
                log_conditions.append(HabitLogEntity.date >= start_date)
            if end_date:
                log_conditions.append(HabitLogEntity.date <= end_date)
            
            # استفاده از join و group_by
            join_condition = HabitEntity.id == HabitLogEntity.habit_id
            if log_conditions:
                join_condition = and_(
                    HabitEntity.id == HabitLogEntity.habit_id,
                    *log_conditions
                )
            
            stmt = (
                select(
                    HabitEntity,
                    func.count(HabitLogEntity.id).label('logs_count'),
                    func.sum(HabitLogEntity.value).label('total_value')
                )
                .outerjoin(
                    HabitLogEntity,
                    join_condition
                )
                .where(HabitEntity.is_active == True)
                .group_by(HabitEntity.id)
            )
            
            result = db.execute(stmt).all()
            
            return [
                {
                    "habit": row[0],
                    "logs_count": row[1] or 0,
                    "total_value": row[2] or 0
                }
                for row in result
            ]

    def bulk_update_habits_status(
        self,
        habit_ids: List[str],
        is_active: bool
    ) -> int:
        """به‌روزرسانی دسته‌ای وضعیت عادت‌ها با SQLAlchemy"""
        with get_session() as db:
            stmt = (
                update(HabitEntity)
                .where(HabitEntity.id.in_(habit_ids))
                .values(is_active=is_active)
            )
            result = db.execute(stmt)
            db.commit()
            return result.rowcount

    def get_habits_completion_rate(
        self,
        habit_id: str,
        days: int = 30
    ) -> float:
        """محاسبه نرخ تکمیل عادت در N روز گذشته با SQLAlchemy"""
        end_date = date.today()
        start_date = date.fromordinal(end_date.toordinal() - days)
        
        with get_session() as db:
            # تعداد روزهای تکمیل شده
            completed_stmt = select(func.count(HabitLogEntity.id)).where(
                and_(
                    HabitLogEntity.habit_id == habit_id,
                    HabitLogEntity.date >= start_date,
                    HabitLogEntity.date <= end_date,
                    HabitLogEntity.value > 0
                )
            )
            completed_days = db.execute(completed_stmt).scalar() or 0
            
            return round((completed_days / days) * 100, 2) if days > 0 else 0.0
