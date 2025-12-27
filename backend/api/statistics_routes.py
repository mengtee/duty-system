from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from database.database import Database
from services.statistics_service import StatisticsService

router = APIRouter(prefix="/api/statistics", tags=["Statistics"])

@router.get("/duty")
def get_duty_statistics(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(Database.get_session)
):
    """
    Get overall duty statistics.
    
    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        db: Database session (injected)
        
    Returns:
        Duty statistics
    """
    service = StatisticsService(db)
    return service.get_duty_statistics(start_date=start_date, end_date=end_date)

@router.get("/workload")
def get_staff_workload(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(Database.get_session)
):
    """
    Get workload distribution per staff.
    
    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        db: Database session (injected)
        
    Returns:
        Staff workload statistics
    """
    service = StatisticsService(db)
    return service.get_staff_workload(start_date=start_date, end_date=end_date)

@router.get("/shifts")
def get_shift_distribution(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(Database.get_session)
):
    """
    Get shift type distribution.
    
    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        db: Database session (injected)
        
    Returns:
        Shift distribution statistics
    """
    service = StatisticsService(db)
    return service.get_shift_distribution(start_date=start_date, end_date=end_date)

@router.get("/comprehensive")
def get_comprehensive_report(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(Database.get_session)
):
    """
    Get comprehensive statistics report.
    
    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        db: Database session (injected)
        
    Returns:
        Comprehensive statistics
    """
    service = StatisticsService(db)
    return service.get_comprehensive_report(start_date=start_date, end_date=end_date)
