"""
Script to check and display researchers in the database.
"""

from db_neurohub import db, run_sql_query
from google.cloud.spanner_v1 import param_types

def check_researchers():
    """Check what researchers are actually in the database."""
    if not db:
        print("Database connection not available.")
        return
    
    # First, count total researchers
    count_sql = "SELECT COUNT(*) as total FROM Researcher"
    count_result = run_sql_query(db, count_sql)
    if count_result:
        print(f"Total researchers in database: {count_result[0]['total']}")
    
    # Get all researchers
    sql = """
        SELECT researcher_id, name, email, institution, expertise, years_experience
        FROM Researcher
        ORDER BY name
    """
    
    researchers = run_sql_query(db, sql)
    
    if not researchers:
        print("No researchers found in database.")
        return
    
    print(f"\nFound {len(researchers)} researchers:")
    print("-" * 80)
    
    # Check for duplicates
    names_seen = {}
    for i, r in enumerate(researchers):
        name = r.get('name', 'Unknown')
        if name in names_seen:
            names_seen[name] += 1
        else:
            names_seen[name] = 1
            
        print(f"{i+1}. {name}")
        print(f"   Email: {r.get('email')}")
        print(f"   Institution: {r.get('institution')}")
        print(f"   Expertise: {r.get('expertise')}")
        print(f"   Years: {r.get('years_experience')}")
        print(f"   ID: {r.get('researcher_id')}")
        print()
    
    # Report duplicates
    print("\nDuplicate Analysis:")
    print("-" * 40)
    for name, count in names_seen.items():
        if count > 1:
            print(f"'{name}' appears {count} times")
    
    if all(count == 1 for count in names_seen.values()):
        print("No duplicate names found.")

if __name__ == "__main__":
    print("Checking researchers in NeuroHub database...\n")
    check_researchers()