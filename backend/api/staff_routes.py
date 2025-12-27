from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import Database
from services.staff_service import StaffService
from schemas import StaffCreate, StaffResponse

router = APIRouter(prefix="/api/staff", tags=["Staff"])

@router.post("/", response_model=StaffResponse, status_code=201)
def create_staff(staff_data: StaffCreate, db: Session = Depends(Database.get_session)):
    """
    Add a new staff member.
    
    Args:
        staff_data: Staff creation data
        db: Database session (injected)
        
    Returns:
        Created staff member
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        service = StaffService(db)
        staff = service.add_staff(
            name=staff_data.name,
            age=staff_data.age,
            position=staff_data.position
        )
        return staff
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[StaffResponse])
def get_all_staff(include_inactive: bool = False, db: Session = Depends(Database.get_session)):
    """
    Get all staff members.
    
    Args:
        include_inactive: Include soft-deleted staff
        db: Database session (injected)
        
    Returns:
        List of staff members
    """
    service = StaffService(db)
    staff_list = service.get_all_staff(include_inactive=include_inactive)
    return staff_list

@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(Database.get_session)):
    """
    Get staff by ID.
    
    Args:
        staff_id: Staff ID
        db: Database session (injected)
        
    Returns:
        Staff member
        
    Raises:
        HTTPException: If staff not found
    """
    service = StaffService(db)
    staff = service.get_staff_by_id(staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail=f"Staff with ID {staff_id} not found")
    return staff

@router.delete("/{staff_id}", status_code=200)
def delete_staff(staff_id: int, db: Session = Depends(Database.get_session)):
    """
    Delete (soft delete) a staff member.
    
    Args:
        staff_id: Staff ID
        db: Database session (injected)
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If staff not found
    """
    service = StaffService(db)
    success = service.delete_staff(staff_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Staff with ID {staff_id} not found")
    return {"message": "Staff deleted successfully"}

@router.get("/statistics/summary")
def get_staff_statistics(db: Session = Depends(Database.get_session)):
    """
    Get staff statistics.
    
    Args:
        db: Database session (injected)
        
    Returns:
        Staff statistics
    """
    service = StaffService(db)
    return service.get_staff_statistics()
