# db_neurohub.py - SQL-based data fetchers for NeuroHub

import os
import traceback
from datetime import datetime
import json

from google.cloud import spanner
from google.cloud.spanner_v1 import param_types
from google.api_core import exceptions

# --- Spanner Configuration ---
INSTANCE_ID = os.environ.get("SPANNER_INSTANCE_ID", "neurohub-graph-instance")
DATABASE_ID = os.environ.get("SPANNER_DATABASE_ID", "neurohub-db")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

if not PROJECT_ID:
    print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set.")

# --- Spanner Client Initialization ---
db = None
spanner_client = None
try:
    if PROJECT_ID:
        spanner_client = spanner.Client(project=PROJECT_ID)
        instance = spanner_client.instance(INSTANCE_ID)
        database = instance.database(DATABASE_ID)
        print(f"Attempting to connect to Spanner: {instance.name}/databases/{database.database_id}")

        if not database.exists():
            print(f"Error: Database '{database.database_id}' does not exist in instance '{instance.name}'.")
            db = None
        else:
            print("Spanner database connection check successful.")
            db = database
    else:
        print("Skipping Spanner client initialization due to missing GOOGLE_CLOUD_PROJECT.")

except exceptions.NotFound:
    print(f"Error: Spanner instance '{INSTANCE_ID}' not found in project '{PROJECT_ID}'.")
    db = None
except Exception as e:
    print(f"An unexpected error occurred during Spanner initialization: {e}")
    db = None

# --- Utility Function for SQL Queries ---

def run_sql_query(db_instance, sql, params=None, param_types=None):
    """
    Executes a SQL query on Spanner.

    Args:
        db_instance: The Spanner database object.
        sql (str): The SQL query string.
        params (dict, optional): Dictionary of query parameters.
        param_types (dict, optional): Dictionary mapping param names to Spanner types.

    Returns:
        list[dict]: A list of dictionaries representing the rows, or None on error.
    """
    if not db_instance:
        print("Error: Database connection is not available.")
        return None

    results_list = []
    print(f"--- Executing SQL Query ---")

    try:
        with db_instance.snapshot() as snapshot:
            results = snapshot.execute_sql(
                sql,
                params=params,
                param_types=param_types
            )

            # First consume the result to get metadata
            rows = list(results)
            
            # Get column names from the result set metadata
            if results.metadata and results.metadata.row_type and results.metadata.row_type.fields:
                field_names = [field.name for field in results.metadata.row_type.fields]
                
                # Convert rows to dictionaries
                for row in rows:
                    results_list.append(dict(zip(field_names, row)))
            else:
                # No metadata means no results
                return results_list

    except Exception as e:
        print(f"An error occurred during SQL query execution: {e}")
        traceback.print_exc()
        return None

    return results_list


# --- Data Fetching Functions for NeuroHub ---

def get_all_researchers(db_instance, limit=50):
    """
    Fetches all researchers with their expertise.
    """
    if not db_instance: return None

    sql = """
        SELECT researcher_id, name, email, institution, expertise, years_experience
        FROM Researcher
        ORDER BY name
        LIMIT @limit
    """
    params = {"limit": limit}
    param_types_map = {"limit": param_types.INT64}

    return run_sql_query(db_instance, sql, params=params, param_types=param_types_map)


def get_experiments_by_researcher(db_instance, researcher_id):
    """
    Fetches all experiments led by a specific researcher.
    """
    if not db_instance: return None

    sql = """
        SELECT e.experiment_id, e.name, e.description, e.status, 
               e.start_date, e.end_date, r.name as pi_name
        FROM Experiment e
        JOIN Researcher r ON e.principal_investigator_id = r.researcher_id
        WHERE e.principal_investigator_id = @researcher_id
        ORDER BY e.start_date DESC
    """
    params = {"researcher_id": researcher_id}
    param_types_map = {"researcher_id": param_types.STRING}

    results = run_sql_query(db_instance, sql, params=params, param_types=param_types_map)
    
    # Convert datetime objects to ISO format strings
    if results:
        for exp in results:
            if isinstance(exp.get('start_date'), datetime):
                exp['start_date'] = exp['start_date'].isoformat()
            if isinstance(exp.get('end_date'), datetime):
                exp['end_date'] = exp['end_date'].isoformat()
    
    return results


def get_experiment_details(db_instance, experiment_id):
    """
    Fetches detailed information about an experiment including devices and sessions.
    """
    if not db_instance: return None

    # Get experiment info
    exp_sql = """
        SELECT e.*, r.name as pi_name
        FROM Experiment e
        JOIN Researcher r ON e.principal_investigator_id = r.researcher_id
        WHERE e.experiment_id = @experiment_id
    """
    params = {"experiment_id": experiment_id}
    param_types_map = {"experiment_id": param_types.STRING}
    
    experiments = run_sql_query(db_instance, exp_sql, params=params, param_types=param_types_map)
    if not experiments:
        return None
    
    experiment = experiments[0]
    
    # Get devices used
    devices_sql = """
        SELECT d.device_id, d.name, d.device_type, d.manufacturer, d.model
        FROM Device d
        JOIN ExperimentDevice ed ON d.device_id = ed.device_id
        WHERE ed.experiment_id = @experiment_id
    """
    experiment['devices'] = run_sql_query(db_instance, devices_sql, params=params, param_types=param_types_map)
    
    # Get sessions
    sessions_sql = """
        SELECT s.session_id, s.session_date, s.duration_minutes, r.name as researcher_name
        FROM Session s
        JOIN Researcher r ON s.researcher_id = r.researcher_id
        WHERE s.experiment_id = @experiment_id
        ORDER BY s.session_date DESC
    """
    experiment['sessions'] = run_sql_query(db_instance, sessions_sql, params=params, param_types=param_types_map)
    
    # Convert datetime objects
    if isinstance(experiment.get('start_date'), datetime):
        experiment['start_date'] = experiment['start_date'].isoformat()
    if isinstance(experiment.get('end_date'), datetime):
        experiment['end_date'] = experiment['end_date'].isoformat()
    
    if experiment.get('sessions'):
        for session in experiment['sessions']:
            if isinstance(session.get('session_date'), datetime):
                session['session_date'] = session['session_date'].isoformat()
    
    return experiment


def get_recent_analyses(db_instance, limit=20):
    """
    Fetches recent analyses with researcher and signal information.
    """
    if not db_instance: return None

    sql = """
        SELECT 
            a.analysis_id, 
            a.analysis_type, 
            a.findings,
            a.confidence_score,
            a.analyzed_at,
            r.name as researcher_name,
            s.signal_type,
            s.duration_seconds,
            e.name as experiment_name
        FROM Analysis a
        JOIN Researcher r ON a.researcher_id = r.researcher_id
        JOIN SignalData s ON a.signal_id = s.signal_id
        JOIN Session sess ON s.session_id = sess.session_id
        JOIN Experiment e ON sess.experiment_id = e.experiment_id
        ORDER BY a.analyzed_at DESC
        LIMIT @limit
    """
    params = {"limit": limit}
    param_types_map = {"limit": param_types.INT64}

    results = run_sql_query(db_instance, sql, params=params, param_types=param_types_map)
    
    # Convert datetime objects
    if results:
        for analysis in results:
            if isinstance(analysis.get('analyzed_at'), datetime):
                analysis['analyzed_at'] = analysis['analyzed_at'].isoformat()
    
    return results


def get_researcher_collaborations(db_instance, researcher_id):
    """
    Fetches all collaborations for a specific researcher.
    """
    if not db_instance: return None

    sql = """
        SELECT 
            CASE 
                WHEN c.researcher_id_a = @researcher_id THEN r2.researcher_id
                ELSE r1.researcher_id
            END as collaborator_id,
            CASE 
                WHEN c.researcher_id_a = @researcher_id THEN r2.name
                ELSE r1.name
            END as collaborator_name,
            c.project_name,
            c.collaboration_type,
            c.start_date
        FROM Collaboration c
        JOIN Researcher r1 ON c.researcher_id_a = r1.researcher_id
        JOIN Researcher r2 ON c.researcher_id_b = r2.researcher_id
        WHERE c.researcher_id_a = @researcher_id OR c.researcher_id_b = @researcher_id
        ORDER BY c.start_date DESC
    """
    params = {"researcher_id": researcher_id}
    param_types_map = {"researcher_id": param_types.STRING}

    results = run_sql_query(db_instance, sql, params=params, param_types=param_types_map)
    
    # Convert datetime objects
    if results:
        for collab in results:
            if isinstance(collab.get('start_date'), datetime):
                collab['start_date'] = collab['start_date'].isoformat()
    
    return results


def get_signal_data_by_experiment(db_instance, experiment_id):
    """
    Fetches all signal data recorded for an experiment.
    """
    if not db_instance: return None

    sql = """
        SELECT 
            s.signal_id,
            s.signal_type,
            s.duration_seconds,
            s.sampling_rate,
            s.channels,
            s.quality_score,
            s.processing_status,
            s.recorded_at,
            d.name as device_name,
            sess.session_date
        FROM SignalData s
        JOIN Device d ON s.device_id = d.device_id
        JOIN Session sess ON s.session_id = sess.session_id
        WHERE s.experiment_id = @experiment_id
        ORDER BY s.recorded_at DESC
    """
    params = {"experiment_id": experiment_id}
    param_types_map = {"experiment_id": param_types.STRING}

    results = run_sql_query(db_instance, sql, params=params, param_types=param_types_map)
    
    # Convert datetime objects
    if results:
        for signal in results:
            if isinstance(signal.get('recorded_at'), datetime):
                signal['recorded_at'] = signal['recorded_at'].isoformat()
            if isinstance(signal.get('session_date'), datetime):
                signal['session_date'] = signal['session_date'].isoformat()
    
    return results


# --- Example Usage (if run directly) ---
if __name__ == "__main__":
    if db:
        print("\n--- Testing NeuroHub Data Fetching Functions ---")

        print("\n1. Fetching all researchers")
        researchers = get_all_researchers(db, limit=5)
        if researchers:
            print(json.dumps(researchers, indent=2))

        if researchers and len(researchers) > 0:
            test_researcher_id = researchers[0]['researcher_id']
            
            print(f"\n2. Fetching experiments by researcher: {test_researcher_id}")
            experiments = get_experiments_by_researcher(db, test_researcher_id)
            if experiments:
                print(json.dumps(experiments, indent=2))
                
                if len(experiments) > 0:
                    test_experiment_id = experiments[0]['experiment_id']
                    
                    print(f"\n3. Fetching experiment details: {test_experiment_id}")
                    exp_details = get_experiment_details(db, test_experiment_id)
                    if exp_details:
                        print(json.dumps(exp_details, indent=2))

        print("\n4. Fetching recent analyses")
        analyses = get_recent_analyses(db, limit=5)
        if analyses:
            print(json.dumps(analyses, indent=2))

    else:
        print("\nCannot run examples: Spanner database connection not established.")