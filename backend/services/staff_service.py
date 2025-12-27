from typing import List, Optional
from sqlalchemy.orm import Session
from models.staff import Staff

class StaffService:
    def __init__(self, db: Session):
        """
        Initialize StaffService with database session.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def add_staff(self, name: str, age: int, position: str) -> Staff:
        """
        Add a new staff member.
        
        Args:
            name: Staff member's name
            age: Staff member's age
            position: Job position
            
        Returns:
            Created Staff object
            
        Raises:
            ValueError: If validation fails
        """
        staff = Staff(name=name, age=age, position=position)
        self.db.add(staff)
        self.db.commit()
        self.db.refresh(staff)
        return staff
    
    def delete_staff(self, staff_id: int) -> bool:
        """
        Delete (soft delete) a staff member.
        
        Args:
            staff_id: ID of staff to delete
            
        Returns:
            True if deleted, False if not found
        """
        staff = self.get_staff_by_id(staff_id)
        if staff:
            staff.soft_delete()
            self.db.commit()
            return True
        return False
    
    def get_all_staff(self, include_inactive: bool = False) -> List[Staff]:
        """
        Get all staff members.
        
        Args:
            include_inactive: Whether to include soft-deleted staff
            
        Returns:
            List of Staff objects
        """
        query = self.db.query(Staff)
        if not include_inactive:
            query = query.filter(Staff.is_active == True)
        return query.all()
    
    def get_staff_by_id(self, staff_id: int) -> Optional[Staff]:
        """
        Get staff by ID.
        
        Args:
            staff_id: Staff ID
            
        Returns:
            Staff object or None if not found
        """
        return self.db.query(Staff).filter(Staff.id == staff_id).first()
    
    def get_staff_statistics(self) -> dict:
        """
        Get statistics about staff.
        
        Returns:
            Dictionary with staff statistics
        """
        total = self.db.query(Staff).filter(Staff.is_active == True).count()
        
        # Count by position
        positions = self.db.query(Staff.position, self.db.func.count(Staff.id))\
            .filter(Staff.is_active == True)\
            .group_by(Staff.position)\
            .all()
        
        position_dist = {pos: count for pos, count in positions}
        
        return {
            'total_staff': total,
            'position_distribution': position_dist
        }
