#!/usr/bin/env python3
"""
Reset Database - Fresh Start
Deletes all data and recreates tables.

Usage:
    python reset_database.py           # Reset only
    python reset_database.py --seed    # Reset + add sample data
"""
import os
import sys
from database.database import Database, Base, engine
from models.staff import Staff
from models.schedule import Schedule
from models.schedule_assignment import ScheduleAssignment
from datetime import date, timedelta

def reset_database():
    """Delete database file and recreate all tables."""
    print("=" * 50)
    print("🗑️  RESETTING DATABASE")
    print("=" * 50)
    
    # Delete SQLite database file
    db_file = "shift_management.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"✅ Deleted {db_file}")
    else:
        print(f"ℹ️  No existing database found")
    
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Recreated all tables")
    print("")

def seed_sample_data():
    """Add sample data for testing."""
    print("=" * 50)
    print("🌱 SEEDING SAMPLE DATA")
    print("=" * 50)
    
    db = Database.SessionLocal()
    
    try:
        # Create sample staff
        staff_data = [
            Staff(name="张三", age=28, position="工程师"),
            Staff(name="李四", age=32, position="经理"),
            Staff(name="王五", age=25, position="助理"),
            Staff(name="赵六", age=30, position="主管"),
        ]
        
        for staff in staff_data:
            db.add(staff)
        
        db.commit()
        print(f"✅ Created {len(staff_data)} staff members")
        
        # Create sample schedules
        today = date.today()
        shift_types = ["morning", "afternoon", "night", "全天"]
        
        schedules = []
        for i in range(7):
            schedule = Schedule(
                schedule_date=today + timedelta(days=i),
                shift_type=shift_types[i % len(shift_types)],
                created_by="seed_script"
            )
            db.add(schedule)
            schedules.append(schedule)
        
        db.commit()
        print(f"✅ Created {len(schedules)} schedules")
        
        # Create sample assignments
        # Assign first 2 staff to each schedule
        assignments = []
        for schedule in schedules:
            for staff in staff_data[:2]:
                assignment = ScheduleAssignment(
                    staff_id=staff.id,
                    schedule_id=schedule.id,
                    duty_date=schedule.schedule_date,
                    shift_type=schedule.shift_type,
                    notes="Sample assignment"
                )
                db.add(assignment)
                assignments.append(assignment)
        
        db.commit()
        print(f"✅ Created {len(assignments)} assignments")
        
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("")

def main():
    """Main execution."""
    # Check for --seed flag
    should_seed = "--seed" in sys.argv
    
    # Always reset
    reset_database()
    
    # Optionally seed
    if should_seed:
        seed_sample_data()
    
    print("=" * 50)
    print("✅ DATABASE RESET COMPLETE")
    print("=" * 50)
    
    if should_seed:
        print("\n📊 Sample data:")
        print("   - 4 staff members")
        print("   - 7 schedules")
        print("   - 14 assignments")
    else:
        print("\nℹ️  Database is empty (no sample data)")
        print("   To add sample data, run:")
        print("   python reset_database.py --seed")
    
    print("\n🚀 Start your server:")
    print("   python app.py")
    print("")

if __name__ == "__main__":
    main()
