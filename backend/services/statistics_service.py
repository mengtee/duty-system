from typing import Dict, List
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.schedule_assignment import ScheduleAssignment
from models.staff import Staff

class StatisticsService:
    """
    Service class for statistics and analytics.
    Provides insights into duty schedules and workload.
    """
    
    def __init__(self, db: Session):
        """
        Initialize StatisticsService with database session.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def get_duty_statistics(self, start_date: date = None, end_date: date = None) -> Dict:
        """
        Get overall duty statistics.
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            Dictionary with duty statistics
        """
        query = self.db.query(ScheduleAssignment)
        
        if start_date:
            query = query.filter(ScheduleAssignment.duty_date >= start_date)
        if end_date:
            query = query.filter(ScheduleAssignment.duty_date <= end_date)
        
        total_assignments = query.count()
        
        # Count by status
        status_counts = query.with_entities(
            ScheduleAssignment.status,
            func.count(ScheduleAssignment.id)
        ).group_by(ScheduleAssignment.status).all()
        
        status_dist = {status: count for status, count in status_counts}
        
        return {
            'total_assignments': total_assignments,
            'status_distribution': status_dist,
            'date_range': {
                'start': start_date.isoformat() if start_date else None,
                'end': end_date.isoformat() if end_date else None
            }
        }
    
    def get_staff_workload(self, start_date: date = None, end_date: date = None) -> List[Dict]:
        """
        Get workload distribution per staff member.
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            List of dictionaries with staff workload info
        """
        query = self.db.query(
            Staff.id,
            Staff.name,
            Staff.position,
            func.count(ScheduleAssignment.id).label('shift_count')
        ).join(
            ScheduleAssignment, Staff.id == ScheduleAssignment.staff_id
        ).filter(
            Staff.is_active == True
        )
        
        if start_date:
            query = query.filter(ScheduleAssignment.duty_date >= start_date)
        if end_date:
            query = query.filter(ScheduleAssignment.duty_date <= end_date)
        
        workload = query.group_by(Staff.id, Staff.name, Staff.position).all()
        
        return [
            {
                'staff_id': staff_id,
                'name': name,
                'position': position,
                'shift_count': shift_count
            }
            for staff_id, name, position, shift_count in workload
        ]
    
    def get_shift_distribution(self, start_date: date = None, end_date: date = None) -> Dict:
        """
        Get distribution of shifts by type.
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            Dictionary with shift type distribution
        """
        query = self.db.query(
            ScheduleAssignment.shift_type,
            func.count(ScheduleAssignment.id)
        )
        
        if start_date:
            query = query.filter(ScheduleAssignment.duty_date >= start_date)
        if end_date:
            query = query.filter(ScheduleAssignment.duty_date <= end_date)
        
        shift_counts = query.group_by(ScheduleAssignment.shift_type).all()
        
        return {
            shift_type: count for shift_type, count in shift_counts
        }
    
    def get_comprehensive_report(self, start_date: date = None, end_date: date = None) -> Dict:
        """
        Get comprehensive statistics report.
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            Dictionary with comprehensive statistics
        """
        return {
            'duty_statistics': self.get_duty_statistics(start_date, end_date),
            'staff_workload': self.get_staff_workload(start_date, end_date),
            'shift_distribution': self.get_shift_distribution(start_date, end_date)
        }
