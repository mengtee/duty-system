from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import date
from database.database import Database
from services.auto_scheduler import AutoScheduler

router = APIRouter(prefix="/api/auto-schedule", tags=["Auto-Schedule"])

class AutoScheduleRequest(BaseModel):
    """Schema for auto-schedule request."""
    start_date: date
    end_date: date
    shift_types: List[str]
    staff_per_shift: int = 2

@router.post("/generate")
def generate_auto_schedule(
    request: AutoScheduleRequest,
    db: Session = Depends(Database.get_session)
):
    """
    Generate automatic schedule with fair distribution.
    
    Args:
        request: Auto-schedule parameters
        db: Database session (injected)
        
    Returns:
        Summary of generated schedules and assignments
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        service = AutoScheduler(db)
        result = service.generate_schedule(
            start_date=request.start_date,
            end_date=request.end_date,
            shift_types=request.shift_types,
            staff_per_shift=request.staff_per_shift
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auto-schedule generation failed: {str(e)}")

@router.get("/recommendations")
def get_recommendations(
    days: int,
    shift_types_count: int = 1,
    db: Session = Depends(Database.get_session)
):
    """
    Get recommendations for auto-scheduling.
    
    Args:
        days: Number of days to schedule
        shift_types_count: Number of shift types per day
        db: Database session (injected)
        
    Returns:
        Recommendations and statistics
    """
    service = AutoScheduler(db)
    # Create dummy shift types for calculation
    shift_types = ['shift'] * shift_types_count
    return service.get_recommended_distribution(days=days, shift_types=shift_types)
