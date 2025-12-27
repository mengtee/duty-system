from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

class Staff(Base):
    '''
    Staff entity class.
    
    Attributes:
        id: PK,
        name: Staff member's name
        age: Staff member's age
        position: Job position/ title
        is_active: Solf delete flag
        created_at: creation timestamp
        updated_at: update timestamp
    '''
    
    __tablename__ = 'staff'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    position = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to schedule assignments
    assignments = relationship('ScheduleAssignment', back_populates='staff', lazy='dynamic')
    
    def __init__(self, name: str, age: int, position: str):
        """
        Initialize a new Staff member.
        
        Args:
            name: Staff member's name
            age: Staff member's age
            position: Job position
        """
        self.name = name
        self.age = age
        self.position = position
        self.validate()
    
    def validate(self):
        """
        Validate staff data.
        
        Raises:
            ValueError: If validation fails
        """
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        if self.age < 18 or self.age > 60:
            raise ValueError("Age must be between 18 and 60")
        if not self.position or len(self.position.strip()) == 0:
            raise ValueError("Position cannot be empty")
    
    def to_dict(self) -> dict:
        """
        Convert staff object to dictionary.
        
        Returns:
            Dictionary representation of staff
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'position': self.position,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def soft_delete(self):
        """Soft delete the staff member by setting is_active to False."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        """String representation of Staff object."""
        return f'<Staff {self.name} - {self.position}>'
