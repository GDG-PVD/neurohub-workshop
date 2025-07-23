"""
Enhanced database functions for NeuroHub with researcher statistics.
"""

from .db_neurohub import run_sql_query
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def get_all_researchers_with_stats(db_instance, limit=50):
    """
    Fetches all researchers with their expertise and statistics.
    """
    if not db_instance: 
        return None
    
    sql = """
        SELECT 
            r.researcher_id, 
            r.name, 
            r.email, 
            r.institution, 
            r.expertise, 
            r.years_experience,
            -- Count projects where researcher is PI
            (SELECT COUNT(*) 
             FROM Experiment e 
             WHERE e.principal_investigator_id = r.researcher_id) as projects,
            -- Count publications
            (SELECT COUNT(*) 
             FROM Publication p 
             JOIN Experiment e ON p.experiment_id = e.experiment_id
             WHERE e.principal_investigator_id = r.researcher_id) as publications,
            -- Count unique collaborators
            (SELECT COUNT(DISTINCT c.researcher_id_b) 
             FROM Collaboration c 
             WHERE c.researcher_id_a = r.researcher_id
             UNION 
             SELECT COUNT(DISTINCT c.researcher_id_a) 
             FROM Collaboration c 
             WHERE c.researcher_id_b = r.researcher_id) as collaborators
        FROM Researcher r
        ORDER BY r.name
        LIMIT @limit
    """
    
    params = {"limit": limit}
    param_types_map = {"limit": param_types.INT64}
    
    researchers = run_sql_query(db_instance, sql, params=params, param_types=param_types_map)
    
    # Add default bio based on expertise
    if researchers:
        for researcher in researchers:
            if not researcher.get('bio'):
                expertise_str = researcher.get('expertise', 'neurotechnology research')
                if isinstance(expertise_str, str) and expertise_str:
                    researcher['bio'] = f"Research interests include {expertise_str}."
                else:
                    researcher['bio'] = "Research interests in neurotechnology and brain-computer interfaces."
    
    return researchers