from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from database.database import Database
from services.schedule_service import ScheduleService
from schemas import ScheduleCreate, ScheduleResponse, AssignmentCreate, AssignmentResponse, AssignmentStatusUpdate

router = APIRouter(prefix="/api/schedules", tags=["Schedules"])

@router.post("/", response_model=ScheduleResponse, status_code=201)
def create_schedule(schedule_data: ScheduleCreate, db: Session = Depends(Database.get_session)):
    """
    Create a new schedule.
    
    Args:
        schedule_data: Schedule creation data
        db: Database session (injected)
        
    Returns:
        Created schedule
    """
    service = ScheduleService(db)
    schedule = service.create_schedule(
        schedule_date=schedule_data.schedule_date,
        shift_type=schedule_data.shift_type,
        created_by=schedule_data.created_by
    )
    return schedule.to_dict()

@router.get("/", response_model=List[ScheduleResponse])
def get_schedules(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(Database.get_session)
):
    """
    Get schedules within a date range.
    
    Args:
        start_date: Start date filter
        end_date: End date filter
        db: Database session (injected)
        
    Returns:
        List of schedules
    """
    service = ScheduleService(db)
    schedules = service.get_schedules(start_date=start_date, end_date=end_date)
    
    # Explicitly build response with assignments
    result = []
    for s in schedules:
        schedule_dict = {
            'id': s.id,
            'schedule_date': s.schedule_date.isoformat() if s.schedule_date else None,
            'shift_type': s.shift_type,
            'created_at': s.created_at.isoformat() if s.created_at else None,
            'created_by': s.created_by,
            'assignments_count': len(s.get_assignments()),
            'assignments': [
                {
                    'id': a.id,
                    'staff_id': a.staff_id,
                    'staff': {
                        'id': a.staff.id,
                        'name': a.staff.name,
                        'position': a.staff.position
                    } if a.staff else None,
                    'status': a.status,
                    'notes': a.notes
                }
                for a in s.get_assignments()
            ]
        }
        result.append(schedule_dict)
    
    return result

@router.get("/{schedule_id}")
def get_schedule_details(schedule_id: int, db: Session = Depends(Database.get_session)):
    """
    Get schedule with assignments.
    
    Args:
        schedule_id: Schedule ID
        db: Database session (injected)
        
    Returns:
        Schedule with assignments
        
    Raises:
        HTTPException: If schedule not found
    """
    service = ScheduleService(db)
    schedule_data = service.get_schedule_with_assignments(schedule_id)
    if not schedule_data:
        raise HTTPException(status_code=404, detail=f"Schedule with ID {schedule_id} not found")
    return schedule_data

@router.post("/assign", response_model=List[AssignmentResponse], status_code=201)
def assign_staff_to_schedule(assignment_data: AssignmentCreate, db: Session = Depends(Database.get_session)):
    """
    Assign staff members to a schedule.
    
    Args:
        assignment_data: Assignment data
        db: Database session (injected)
        
    Returns:
        List of created assignments
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        service = ScheduleService(db)
        assignments = service.assign_staff(
            schedule_id=assignment_data.schedule_id,
            staff_ids=assignment_data.staff_ids,
            notes=assignment_data.notes
        )
        return [a.to_dict() for a in assignments]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/staff/{staff_id}/schedule", response_model=List[AssignmentResponse])
def get_staff_schedule(
    staff_id: int,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(Database.get_session)
):
    """
    Get schedule for a specific staff member.
    
    Args:
        staff_id: Staff ID
        start_date: Start date filter
        end_date: End date filter
        db: Database session (injected)
        
    Returns:
        List of assignments for the staff
    """
    service = ScheduleService(db)
    assignments = service.get_staff_schedule(staff_id=staff_id, start_date=start_date, end_date=end_date)
    return [a.to_dict() for a in assignments]

@router.patch("/assignment/{assignment_id}/status")
def update_assignment_status(
    assignment_id: int,
    status_data: AssignmentStatusUpdate,
    db: Session = Depends(Database.get_session)
):
    """
    Update assignment status.
    
    Args:
        assignment_id: Assignment ID
        status_data: New status
        db: Database session (injected)
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If assignment not found
    """
    service = ScheduleService(db)
    success = service.update_assignment_status(assignment_id, status_data.status)
    if not success:
        raise HTTPException(status_code=404, detail=f"Assignment with ID {assignment_id} not found")
    return {"message": "Assignment status updated successfully"}
