"""
NeuroHub Signal Processing Tools
Tools for accessing and analyzing biosignal data from the Spanner Graph Database
"""

import os
from datetime import datetime
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types
from typing import Optional, Dict, List

# Database configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
INSTANCE_ID = os.environ.get("SPANNER_INSTANCE_ID", "neurohub-graph-instance")
DATABASE_ID = os.environ.get("SPANNER_DATABASE_ID", "neurohub-db")

# Initialize Spanner client
db_instance = None
try:
    spanner_client = spanner.Client(project=PROJECT_ID)
    instance = spanner_client.instance(INSTANCE_ID)
    db_instance = instance.database(DATABASE_ID)
    print(f"Connected to NeuroHub database: {DATABASE_ID}")
except Exception as e:
    print(f"Error connecting to database: {e}")

def run_query(sql: str, params: dict = None, param_types: dict = None, expected_fields: list = None) -> list:
    """Execute a query against the Spanner database."""
    if not db_instance:
        return None
    
    try:
        with db_instance.snapshot() as snapshot:
            results = snapshot.execute_sql(sql, params=params, param_types=param_types)
            
            field_names = expected_fields
            if not field_names:
                try:
                    field_names = [field.name for field in results.fields]
                except AttributeError:
                    raise ValueError("Could not determine field names for query results.")
            
            result_list = []
            for row in results:
                result_list.append(dict(zip(field_names, row)))
            
            return result_list
    except Exception as e:
        print(f"Query error: {e}")
        return None

def run_graph_query(graph_sql: str, params: dict = None, param_types: dict = None, expected_fields: list = None) -> list:
    """Execute a Graph SQL query."""
    return run_query(graph_sql, params, param_types, expected_fields)

# Tool functions for the Signal Processing Agent

def get_researcher_id_by_name(name: str) -> str:
    """
    Fetches the researcher_id for a given name.
    
    Args:
        name (str): The name of the researcher to search for.
    
    Returns:
        str or None: The researcher_id if found, otherwise None.
    """
    if not db_instance:
        return None
    
    sql = """
        SELECT researcher_id
        FROM Researcher
        WHERE name = @name
        LIMIT 1
    """
    params = {"name": name}
    param_types_map = {"name": param_types.STRING}
    fields = ["researcher_id"]
    
    results = run_query(sql, params=params, param_types=param_types_map, expected_fields=fields)
    
    if results:
        return results[0].get('researcher_id')
    else:
        return None

def get_researcher_experiments(researcher_id: str) -> List[Dict]:
    """
    Fetches all experiments where the researcher is the principal investigator.
    
    Args:
        researcher_id (str): The ID of the researcher.
    
    Returns:
        list[dict] or None: List of experiment dictionaries.
    """
    if not db_instance:
        return None
    
    sql = """
        SELECT 
            e.experiment_id, 
            e.name, 
            e.description, 
            e.status,
            e.start_date,
            e.end_date,
            e.hypothesis
        FROM Experiment e
        WHERE e.principal_investigator_id = @researcher_id
        ORDER BY e.start_date DESC
    """
    params = {"researcher_id": researcher_id}
    param_types_map = {"researcher_id": param_types.STRING}
    fields = ["experiment_id", "name", "description", "status", "start_date", "end_date", "hypothesis"]
    
    results = run_query(sql, params=params, param_types=param_types_map, expected_fields=fields)
    
    # Convert datetime objects to ISO format strings
    if results:
        for exp in results:
            if isinstance(exp.get('start_date'), datetime):
                exp['start_date'] = exp['start_date'].isoformat()
            if isinstance(exp.get('end_date'), datetime):
                exp['end_date'] = exp['end_date'].isoformat()
    
    return results

def get_experiment_sessions(experiment_id: str) -> List[Dict]:
    """
    Fetches all sessions for a specific experiment.
    
    Args:
        experiment_id (str): The ID of the experiment.
    
    Returns:
        list[dict] or None: List of session dictionaries.
    """
    if not db_instance:
        return None
    
    sql = """
        SELECT 
            s.session_id,
            s.session_date,
            s.duration_minutes,
            s.notes,
            r.name as researcher_name
        FROM Session s
        JOIN Researcher r ON s.researcher_id = r.researcher_id
        WHERE s.experiment_id = @experiment_id
        ORDER BY s.session_date DESC
    """
    params = {"experiment_id": experiment_id}
    param_types_map = {"experiment_id": param_types.STRING}
    fields = ["session_id", "session_date", "duration_minutes", "notes", "researcher_name"]
    
    results = run_query(sql, params=params, param_types=param_types_map, expected_fields=fields)
    
    if results:
        for session in results:
            if isinstance(session.get('session_date'), datetime):
                session['session_date'] = session['session_date'].isoformat()
    
    return results

def get_session_signals(session_id: str) -> List[Dict]:
    """
    Fetches all recorded signals for a specific session.
    
    Args:
        session_id (str): The ID of the session.
    
    Returns:
        list[dict] or None: List of signal dictionaries.
    """
    if not db_instance:
        return None
    
    sql = """
        SELECT 
            s.signal_id,
            s.signal_type,
            s.duration_seconds,
            s.sampling_rate,
            s.channels,
            s.quality_score,
            s.processing_status,
            s.file_path,
            s.notes,
            d.name as device_name,
            d.device_type
        FROM SignalData s
        JOIN Device d ON s.device_id = d.device_id
        WHERE s.session_id = @session_id
        ORDER BY s.recorded_at DESC
    """
    params = {"session_id": session_id}
    param_types_map = {"session_id": param_types.STRING}
    fields = ["signal_id", "signal_type", "duration_seconds", "sampling_rate", 
              "channels", "quality_score", "processing_status", "file_path", 
              "notes", "device_name", "device_type"]
    
    return run_query(sql, params=params, param_types=param_types_map, expected_fields=fields)

def get_signal_analyses(signal_id: str) -> List[Dict]:
    """
    Fetches all analyses performed on a specific signal.
    
    Args:
        signal_id (str): The ID of the signal.
    
    Returns:
        list[dict] or None: List of analysis dictionaries.
    """
    if not db_instance:
        return None
    
    sql = """
        SELECT 
            a.analysis_id,
            a.analysis_type,
            a.findings,
            a.confidence_score,
            a.analyzed_at,
            r.name as analyst_name
        FROM Analysis a
        JOIN Researcher r ON a.researcher_id = r.researcher_id
        WHERE a.signal_id = @signal_id
        ORDER BY a.analyzed_at DESC
    """
    params = {"signal_id": signal_id}
    param_types_map = {"signal_id": param_types.STRING}
    fields = ["analysis_id", "analysis_type", "findings", "confidence_score", 
              "analyzed_at", "analyst_name"]
    
    results = run_query(sql, params=params, param_types=param_types_map, expected_fields=fields)
    
    if results:
        for analysis in results:
            if isinstance(analysis.get('analyzed_at'), datetime):
                analysis['analyzed_at'] = analysis['analyzed_at'].isoformat()
    
    return results

def get_device_specifications(device_id: str) -> Dict:
    """
    Fetches specifications for a specific device.
    
    Args:
        device_id (str): The ID of the device.
    
    Returns:
        dict or None: Device specifications.
    """
    if not db_instance:
        return None
    
    sql = """
        SELECT 
            device_id,
            name,
            device_type,
            manufacturer,
            model,
            sampling_rate,
            channels,
            specifications,
            status
        FROM Device
        WHERE device_id = @device_id
    """
    params = {"device_id": device_id}
    param_types_map = {"device_id": param_types.STRING}
    fields = ["device_id", "name", "device_type", "manufacturer", "model", 
              "sampling_rate", "channels", "specifications", "status"]
    
    results = run_query(sql, params=params, param_types=param_types_map, expected_fields=fields)
    
    return results[0] if results else None

# Graph-based queries for relationship analysis

def get_researcher_collaborations(researcher_id: str) -> List[Dict]:
    """
    Fetches collaboration network for a researcher using Graph Query.
    
    Args:
        researcher_id (str): The ID of the researcher.
    
    Returns:
        list[dict] or None: List of collaboration relationships.
    """
    if not db_instance:
        return None
    
    graph_sql = """
        Graph NeuroResearchGraph
        MATCH (r:Researcher {researcher_id: @researcher_id})-[c:Collaboration]-(collaborator:Researcher)
        RETURN DISTINCT 
            collaborator.researcher_id, 
            collaborator.name,
            c.project_name,
            c.collaboration_type
        ORDER BY collaborator.name
    """
    params = {"researcher_id": researcher_id}
    param_types_map = {"researcher_id": param_types.STRING}
    fields = ["researcher_id", "name", "project_name", "collaboration_type"]
    
    return run_graph_query(graph_sql, params=params, param_types=param_types_map, expected_fields=fields)

def get_experiment_data_lineage(experiment_id: str) -> List[Dict]:
    """
    Traces the complete data lineage for an experiment using Graph Query.
    Shows: Experiment -> Sessions -> Signals -> Analyses
    
    Args:
        experiment_id (str): The ID of the experiment.
    
    Returns:
        list[dict] or None: Data lineage information.
    """
    if not db_instance:
        return None
    
    graph_sql = """
        Graph NeuroResearchGraph
        MATCH path = (e:Experiment {experiment_id: @experiment_id})<-[:PartOf]-(s:Session)<-[:RecordedIn]-(sig:SignalData)<-[:Analyzes]-(a:Analysis)
        RETURN 
            e.name as experiment_name,
            s.session_id,
            s.session_date,
            sig.signal_id,
            sig.signal_type,
            sig.quality_score,
            a.analysis_type,
            a.confidence_score
        ORDER BY s.session_date, sig.signal_type
    """
    params = {"experiment_id": experiment_id}
    param_types_map = {"experiment_id": param_types.STRING}
    fields = ["experiment_name", "session_id", "session_date", "signal_id", 
              "signal_type", "quality_score", "analysis_type", "confidence_score"]
    
    results = run_graph_query(graph_sql, params=params, param_types=param_types_map, expected_fields=fields)
    
    if results:
        for item in results:
            if isinstance(item.get('session_date'), datetime):
                item['session_date'] = item['session_date'].isoformat()
    
    return results