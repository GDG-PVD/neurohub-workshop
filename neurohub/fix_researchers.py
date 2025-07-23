"""
Script to fix researcher data in the database.
"""

import uuid
from datetime import datetime, timezone
from google.cloud import spanner
from db_neurohub import db, run_sql_query

def clear_researchers():
    """Clear existing researcher data (careful - this affects relationships!)."""
    if not db:
        print("Database connection not available.")
        return False
    
    print("WARNING: This will delete all researchers and related data!")
    confirm = input("Type 'YES' to continue: ")
    if confirm != 'YES':
        print("Aborted.")
        return False
    
    def delete_txn(transaction):
        # Delete in reverse dependency order
        tables = [
            "Publication",
            "Analysis", 
            "SignalData",
            "Session",
            "ExperimentDevice",
            "Collaboration",
            "Experiment",
            "Researcher"
        ]
        
        for table in tables:
            print(f"Clearing {table}...")
            transaction.execute_update(f"DELETE FROM {table} WHERE TRUE")
    
    try:
        db.run_in_transaction(delete_txn)
        print("All data cleared successfully.")
        return True
    except Exception as e:
        print(f"Error clearing data: {e}")
        return False

def insert_diverse_researchers():
    """Insert properly diverse researcher data."""
    if not db:
        print("Database connection not available.")
        return False
    
    researchers_data = [
        {
            "name": "Dr. Sarah Chen",
            "email": "s.chen@brown.edu",
            "institution": "Brown University",
            "expertise": "EEG, Brain-Computer Interfaces, Deep Learning",
            "years": 12
        },
        {
            "name": "Dr. Michael Rodriguez",
            "email": "m.rodriguez@bgu.ac.il",
            "institution": "Ben-Gurion University",
            "expertise": "Signal Processing, Machine Learning, Real-time Systems",
            "years": 8
        },
        {
            "name": "Prof. Emily Watson",
            "email": "e.watson@brown.edu",
            "institution": "Brown University",
            "expertise": "Cognitive Neuroscience, fMRI, Memory Studies",
            "years": 20
        },
        {
            "name": "Dr. David Kim",
            "email": "d.kim@bgu.ac.il",
            "institution": "Ben-Gurion University",
            "expertise": "Neurofeedback, Real-time Processing, Clinical Applications",
            "years": 6
        },
        {
            "name": "Dr. Lisa Anderson",
            "email": "l.anderson@brown.edu",
            "institution": "Brown University",
            "expertise": "EMG, Motor Control, Rehabilitation Engineering",
            "years": 10
        },
        {
            "name": "Dr. James Liu",
            "email": "j.liu@bgu.ac.il",
            "institution": "Ben-Gurion University",
            "expertise": "Wearable Sensors, IoT, Embedded Systems",
            "years": 5
        },
        {
            "name": "Prof. Rachel Green",
            "email": "r.green@brown.edu",
            "institution": "Brown University",
            "expertise": "Clinical Applications, Rehabilitation, Neuroplasticity",
            "years": 15
        },
        {
            "name": "Dr. Ahmed Hassan",
            "email": "a.hassan@bgu.ac.il",
            "institution": "Ben-Gurion University",
            "expertise": "Deep Learning, Pattern Recognition, Computer Vision",
            "years": 7
        },
        {
            "name": "Dr. Maria Gonzalez",
            "email": "m.gonzalez@brown.edu",
            "institution": "Brown University",
            "expertise": "Sleep Research, Polysomnography, Circadian Rhythms",
            "years": 9
        },
        {
            "name": "Dr. Yuki Tanaka",
            "email": "y.tanaka@bgu.ac.il",
            "institution": "Ben-Gurion University",
            "expertise": "Multimodal Integration, Sensor Fusion, HCI",
            "years": 4
        }
    ]
    
    def insert_txn(transaction):
        rows = []
        for data in researchers_data:
            rows.append((
                str(uuid.uuid4()),
                data["name"],
                data["email"],
                data["institution"],
                data["expertise"],
                data["years"],
                spanner.COMMIT_TIMESTAMP
            ))
        
        transaction.insert(
            table="Researcher",
            columns=["researcher_id", "name", "email", "institution", 
                    "expertise", "years_experience", "create_time"],
            values=rows
        )
        print(f"Inserted {len(rows)} researchers.")
    
    try:
        db.run_in_transaction(insert_txn)
        print("Researchers inserted successfully!")
        return True
    except Exception as e:
        print(f"Error inserting researchers: {e}")
        return False

def main():
    print("NeuroHub Researcher Data Fix Script")
    print("-" * 40)
    
    # First check current state
    from check_researchers import check_researchers
    print("\nCurrent database state:")
    check_researchers()
    
    print("\n" + "-" * 40)
    print("\nOptions:")
    print("1. Insert diverse researchers (adds to existing)")
    print("2. Clear ALL data and re-run setup.py")
    print("3. Exit without changes")
    
    choice = input("\nSelect option (1-3): ")
    
    if choice == "1":
        print("\nInserting diverse researchers...")
        if insert_diverse_researchers():
            print("\nNew database state:")
            check_researchers()
    elif choice == "2":
        print("\nThis will clear ALL data. You'll need to run setup.py again.")
        if clear_researchers():
            print("\nDatabase cleared. Now run: python setup.py")
    else:
        print("No changes made.")

if __name__ == "__main__":
    main()