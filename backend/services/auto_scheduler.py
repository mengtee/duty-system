"""
Auto-Scheduler Service - Intelligent automatic shift scheduling.
Demonstrates Algorithm Design and Fair Distribution Logic.
"""
from typing import List, Dict
from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.staff import Staff
from models.schedule import Schedule
from models.schedule_assignment import ScheduleAssignment
from collections import defaultdict
import random

class AutoScheduler:
    """
    Service class for automatic schedule generation.
    Implements fair workload distribution algorithm.
    """
    
    SHIFT_WEIGHTS = {
        'morning': 1,
        'afternoon': 1,
        'night': 1
    }
    
    def __init__(self, db: Session):
        """
        Initialize AutoScheduler with database session.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def generate_schedule(
        self,
        start_date: date,
        end_date: date,
        shift_types: List[str],
        staff_per_shift: int = 2,
        created_by: str = 'auto-scheduler'
    ) -> Dict:
        """
        Generate automatic schedule with fair distribution.
        
        Algorithm:
        1. Calculate total shifts needed
        2. Get all active staff
        3. Distribute shifts fairly using round-robin with randomization
        4. Balance workload to ensure no staff is overworked
        
        Args:
            start_date: Start date of schedule period
            end_date: End date of schedule period
            shift_types: List of shift types to create
            staff_per_shift: Number of staff per shift
            created_by: Creator identifier
            
        Returns:
            Dictionary with created schedules and assignments
        """
        # Get all active staff
        staff_list = self.db.query(Staff).filter(Staff.is_active == True).all()
        
        if len(staff_list) == 0:
            raise ValueError("No active staff available for scheduling")
        
        if len(staff_list) < staff_per_shift:
            raise ValueError(f"Need at least {staff_per_shift} staff members, only {len(staff_list)} available")
        
        # Initialize workload tracker
        workload = defaultdict(int)
        for staff in staff_list:
            workload[staff.id] = 0
        
        created_schedules = []
        created_assignments = []
        
        # Iterate through date range
        current_date = start_date
        shift_day_index = 0
        
        while current_date <= end_date:
            # For each shift type
            for shift_type in shift_types:
                # Create schedule
                schedule = Schedule(
                    schedule_date=current_date,
                    shift_type=shift_type,
                    created_by=created_by
                )
                self.db.add(schedule)
                self.db.flush()  # Get the schedule ID
                
                # Select staff for this shift using simple fair distribution
                selected_staff = self._select_staff_simple(
                    staff_list=staff_list,
                    workload=workload,
                    count=staff_per_shift,
                    shift_day_index=shift_day_index
                )
                
                # Create assignments
                for staff in selected_staff:
                    assignment = ScheduleAssignment(
                        staff_id=staff.id,
                        schedule_id=schedule.id,
                        duty_date=current_date,
                        shift_type=shift_type,
                        notes="自动排班生成"
                    )
                    self.db.add(assignment)
                    
                    # Update workload (simple increment)
                    workload[staff.id] += 1
                    
                    created_assignments.append({
                        'staff_name': staff.name,
                        'date': current_date.isoformat(),
                        'shift_type': shift_type
                    })
                
                created_schedules.append({
                    'date': current_date.isoformat(),
                    'shift_type': shift_type,
                    'staff_count': len(selected_staff)
                })
                
                shift_day_index += 1
            
            current_date += timedelta(days=1)
        
        # Commit all changes
        self.db.commit()
        
        # Calculate final workload distribution
        workload_stats = {
            staff.name: workload[staff.id]
            for staff in staff_list
        }
        
        return {
            'summary': {
                'total_schedules': len(created_schedules),
                'total_assignments': len(created_assignments),
                'date_range': f"{start_date.isoformat()} to {end_date.isoformat()}",
                'staff_count': len(staff_list)
            },
            'workload_distribution': workload_stats,
            'schedules': created_schedules[:10],  # Return first 10 as sample
            'assignments': created_assignments[:20]  # Return first 20 as sample
        }
    
    def _select_staff_simple(
        self,
        staff_list: List[Staff],
        workload: Dict[int, int],
        count: int,
        shift_day_index: int
    ) -> List[Staff]:
        """
        Select staff members using simple fair distribution algorithm.
        
        Algorithm:
        1. Sort staff by current workload (ascending)
        2. Add rotation to avoid predictable patterns
        3. Select the least-worked staff members
        
        Args:
            staff_list: List of all available staff
            workload: Current workload per staff
            count: Number of staff to select
            shift_day_index: Index of current shift for rotation
            
        Returns:
            List of selected Staff objects
        """
        # Create list of (staff, workload) tuples
        staff_workload = [(staff, workload[staff.id]) for staff in staff_list]
        
        # Sort by workload (ascending) - least worked first
        staff_workload.sort(key=lambda x: x[1])
        
        # Take the staff with lowest workload
        selected = [staff for staff, _ in staff_workload[:count]]
        
        # Add rotation to avoid always picking same people
        # If multiple staff have the same workload, rotate through them
        min_workload = staff_workload[0][1]
        staff_with_min = [s for s, w in staff_workload if w == min_workload]
        
        if len(staff_with_min) > count:
            # More staff with minimum workload than needed
            # Rotate selection based on shift index
            rotation_offset = shift_day_index % len(staff_with_min)
            rotated = staff_with_min[rotation_offset:] + staff_with_min[:rotation_offset]
            selected = rotated[:count]
        
        return selected
    
    def get_recommended_distribution(self, days: int, shift_types: List[str]) -> Dict:
        """
        Get recommendations for staff distribution.
        
        Args:
            days: Number of days to schedule
            shift_types: List of shift types
            
        Returns:
            Dictionary with recommendations
        """
        staff_count = self.db.query(Staff).filter(Staff.is_active == True).count()
        
        total_shifts = days * len(shift_types)
        
        recommendations = {
            'staff_count': staff_count,
            'total_days': days,
            'shift_types_per_day': len(shift_types),
            'total_shifts': total_shifts,
            'recommended_staff_per_shift': 2 if staff_count >= 4 else 1,
            'total_assignments_needed': total_shifts * 2,
            'avg_shifts_per_person': (total_shifts * 2) / staff_count if staff_count > 0 else 0
        }
        
        if staff_count < 2:
            recommendations['warning'] = "建议至少需要2名员工才能进行合理排班"
        elif staff_count < 4:
            recommendations['warning'] = "员工数量较少，建议增加人员以实现更好的轮换"
        
        return recommendations
