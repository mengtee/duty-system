from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from database.database import Database
from services.export_service import ExportService
import os

router = APIRouter(prefix="/api/export", tags=["Export"])

@router.get("/excel")
def export_to_excel(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(Database.get_session)
):
    """
    Export schedules to Excel file.
    
    Args:
        start_date: Start date filter (optional)
        end_date: End date filter (optional)
        db: Database session (injected)
        
    Returns:
        Excel file download
    """
    service = ExportService(db)
    filepath = service.export_to_excel(start_date=start_date, end_date=end_date)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=500, detail="Failed to generate Excel file")
    
    return FileResponse(
        path=filepath,
        filename=os.path.basename(filepath),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
