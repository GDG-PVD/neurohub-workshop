import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, render_template, abort, flash, request, jsonify
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types
from google.api_core import exceptions
import humanize 
import uuid
import traceback
from dateutil import parser
from neurohub_routes import neurohub_bp

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "neurohub_secret_key_dev")
app.register_blueprint(neurohub_bp)

load_dotenv()

# --- Spanner Configuration ---
INSTANCE_ID = os.environ.get("SPANNER_INSTANCE_ID", "neurohub-graph-instance")
DATABASE_ID = os.environ.get("SPANNER_DATABASE_ID", "neurohub-db")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = os.environ.get("APP_PORT", "8080")

if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

# --- Spanner Client Initialization ---
db = None
try:
    spanner_client = spanner.Client(project=PROJECT_ID)
    instance = spanner_client.instance(INSTANCE_ID)
    database = instance.database(DATABASE_ID)
    print(f"Attempting to connect to Spanner: {instance.name}/databases/{database.name}")
    
    if not database.exists():
        print(f"Error: Database '{database.name}' does not exist in instance '{instance.name}'.")
    else:
        print("Database connection check successful (database exists).")
        db = database
        
except exceptions.NotFound:
    print(f"Error: Spanner instance '{INSTANCE_ID}' not found in project '{PROJECT_ID}'.")
except Exception as e:
    print(f"An unexpected error occurred during Spanner initialization: {e}")

def run_query(sql, params=None, param_types=None, expected_fields=None):
    """Executes a SQL query against the Spanner database."""
    if not db:
        print("Error: Database connection is not available.")
        raise ConnectionError("Spanner database connection not initialized.")
    
    results_list = []
    print(f"--- Executing SQL ---")
    print(f"SQL: {sql}")
    if params:
        print(f"Params: {params}")
    print("----------------------")
    
    try:
        with db.snapshot() as snapshot:
            results = snapshot.execute_sql(
                sql,
                params=params,
                param_types=param_types
            )
            
            field_names = expected_fields
            if not field_names:
                print("Warning: expected_fields not provided to run_query.")
                try:
                    field_names = [field.name for field in results.fields]
                except AttributeError as e:
                    print(f"Error accessing results.fields: {e}")
                    raise ValueError("Could not determine field names for query results.") from e
            
            print(f"Using field names: {field_names}")
            
            for row in results:
                if len(field_names) != len(row):
                    print(f"Warning: Mismatch between field names and row values")
                    continue
                results_list.append(dict(zip(field_names, row)))
            
            print(f"Query successful, fetched {len(results_list)} rows.")
            
    except (exceptions.NotFound, exceptions.PermissionDenied, exceptions.InvalidArgument) as spanner_err:
        print(f"Spanner Error ({type(spanner_err).__name__}): {spanner_err}")
        flash(f"Database error: {spanner_err}", "danger")
        return []
    except ValueError as e:
        print(f"Query Processing Error: {e}")
        flash("Internal error processing query results.", "danger")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during query execution: {e}")
        traceback.print_exc()
        flash(f"An unexpected server error occurred while fetching data.", "danger")
        raise e
    
    return results_list

# --- Database Query Functions ---

def get_all_experiments_db():
    """Fetch all experiments with their principal investigators."""
    sql = """
        SELECT 
            e.experiment_id, e.name, e.description, e.status,
            e.start_date, e.end_date,
            r.name as pi_name, r.researcher_id as pi_id
        FROM Experiment e
        JOIN Researcher r ON e.principal_investigator_id = r.researcher_id
        ORDER BY e.start_date DESC
        LIMIT 50
    """
    fields = ["experiment_id", "name", "description", "status", 
              "start_date", "end_date", "pi_name", "pi_id"]
    return run_query(sql, expected_fields=fields)

def get_recent_signals_db():
    """Fetch recent signal recordings with quality metrics."""
    sql = """
        SELECT 
            s.signal_id, s.signal_type, s.quality_score,
            s.processing_status, s.duration_seconds,
            e.name as experiment_name,
            d.name as device_name,
            sess.session_date
        FROM SignalData s
        JOIN Experiment e ON s.experiment_id = e.experiment_id
        JOIN Device d ON s.device_id = d.device_id
        JOIN Session sess ON s.session_id = sess.session_id
        ORDER BY sess.session_date DESC
        LIMIT 20
    """
    fields = ["signal_id", "signal_type", "quality_score", "processing_status",
              "duration_seconds", "experiment_name", "device_name", "session_date"]
    return run_query(sql, expected_fields=fields)

def get_researcher_db(researcher_id):
    """Fetch a single researcher's details."""
    sql = """
        SELECT researcher_id, name, email, institution, expertise, years_experience
        FROM Researcher
        WHERE researcher_id = @researcher_id
    """
    params = {"researcher_id": researcher_id}
    param_types_map = {"researcher_id": param_types.STRING}
    fields = ["researcher_id", "name", "email", "institution", "expertise", "years_experience"]
    results = run_query(sql, params=params, param_types=param_types_map, expected_fields=fields)
    return results[0] if results else None

def get_researcher_experiments_db(researcher_id):
    """Fetch experiments led by a specific researcher."""
    sql = """
        SELECT 
            e.experiment_id, e.name, e.description, e.status,
            e.start_date, e.end_date
        FROM Experiment e
        WHERE e.principal_investigator_id = @researcher_id
        ORDER BY e.start_date DESC
    """
    params = {"researcher_id": researcher_id}
    param_types_map = {"researcher_id": param_types.STRING}
    fields = ["experiment_id", "name", "description", "status", "start_date", "end_date"]
    return run_query(sql, params=params, param_types=param_types_map, expected_fields=fields)

def get_researcher_collaborations_db(researcher_id):
    """Fetch collaboration network for a researcher."""
    sql = """
        SELECT DISTINCT
            collab.researcher_id, collab.name,
            c.project_name, c.collaboration_type
        FROM Collaboration c
        JOIN Researcher collab ON
            (c.researcher_id_a = @researcher_id AND c.researcher_id_b = collab.researcher_id) OR
            (c.researcher_id_b = @researcher_id AND c.researcher_id_a = collab.researcher_id)
        WHERE c.researcher_id_a = @researcher_id OR c.researcher_id_b = @researcher_id
        ORDER BY collab.name
    """
    params = {"researcher_id": researcher_id}
    param_types_map = {"researcher_id": param_types.STRING}
    fields = ["researcher_id", "name", "project_name", "collaboration_type"]
    return run_query(sql, params=params, param_types=param_types_map, expected_fields=fields)

def get_experiment_details_db(experiment_id):
    """Fetch full experiment details including sessions and devices."""
    if not db:
        raise ConnectionError("Spanner database connection not initialized.")
    
    # Get experiment basic info
    exp_sql = """
        SELECT 
            e.experiment_id, e.name, e.description, e.protocol,
            e.hypothesis, e.status, e.start_date, e.end_date,
            r.name as pi_name, r.researcher_id as pi_id
        FROM Experiment e
        JOIN Researcher r ON e.principal_investigator_id = r.researcher_id
        WHERE e.experiment_id = @experiment_id
    """
    params = {"experiment_id": experiment_id}
    param_types_map = {"experiment_id": param_types.STRING}
    exp_fields = ["experiment_id", "name", "description", "protocol", 
                  "hypothesis", "status", "start_date", "end_date", "pi_name", "pi_id"]
    exp_results = run_query(exp_sql, params=params, param_types=param_types_map, expected_fields=exp_fields)
    
    if not exp_results:
        return None
    
    experiment = exp_results[0]
    
    # Get experiment devices
    devices_sql = """
        SELECT d.device_id, d.name, d.device_type, d.manufacturer, d.model
        FROM Device d
        JOIN ExperimentDevice ed ON d.device_id = ed.device_id
        WHERE ed.experiment_id = @experiment_id
        ORDER BY d.name
    """
    device_fields = ["device_id", "name", "device_type", "manufacturer", "model"]
    experiment["devices"] = run_query(devices_sql, params=params, param_types=param_types_map, expected_fields=device_fields)
    
    # Get experiment sessions
    sessions_sql = """
        SELECT 
            s.session_id, s.session_date, s.duration_minutes,
            r.name as researcher_name,
            COUNT(DISTINCT sig.signal_id) as signal_count
        FROM Session s
        JOIN Researcher r ON s.researcher_id = r.researcher_id
        LEFT JOIN SignalData sig ON s.session_id = sig.session_id
        WHERE s.experiment_id = @experiment_id
        GROUP BY s.session_id, s.session_date, s.duration_minutes, r.name
        ORDER BY s.session_date DESC
    """
    session_fields = ["session_id", "session_date", "duration_minutes", "researcher_name", "signal_count"]
    experiment["sessions"] = run_query(sessions_sql, params=params, param_types=param_types_map, expected_fields=session_fields)
    
    # Convert datetime objects to ISO format
    if isinstance(experiment.get('start_date'), datetime):
        experiment['start_date'] = experiment['start_date'].isoformat()
    if isinstance(experiment.get('end_date'), datetime):
        experiment['end_date'] = experiment['end_date'].isoformat()
    
    for session in experiment.get("sessions", []):
        if isinstance(session.get('session_date'), datetime):
            session['session_date'] = session['session_date'].isoformat()
    
    return experiment

def get_researcher_by_name_db(name):
    """Fetch a researcher's ID by their name."""
    if not db:
        raise ConnectionError("Spanner database connection not initialized.")
    
    sql = "SELECT researcher_id FROM Researcher WHERE name = @name LIMIT 1"
    params = {"name": name}
    param_types_map = {"name": param_types.STRING}
    fields = ["researcher_id"]
    
    try:
        results = run_query(sql, params=params, param_types=param_types_map, expected_fields=fields)
        return results[0]['researcher_id'] if results else None
    except Exception as e:
        print(f"Error fetching researcher by name '{name}': {e}")
        raise e

def add_experiment_db(experiment_id, name, description, protocol, hypothesis, 
                     principal_investigator_id, start_date, status="planning"):
    """Inserts a new experiment into the database."""
    if not db:
        raise ConnectionError("Database connection not initialized.")
    
    def _insert_experiment(transaction):
        transaction.insert(
            table="Experiment",
            columns=[
                "experiment_id", "name", "description", "protocol",
                "hypothesis", "start_date", "end_date", "status",
                "principal_investigator_id", "create_time"
            ],
            values=[(
                experiment_id, name, description, protocol,
                hypothesis, start_date, None, status,
                principal_investigator_id, spanner.COMMIT_TIMESTAMP
            )]
        )
        print(f"Transaction attempting to insert experiment_id: {experiment_id}")
    
    try:
        db.run_in_transaction(_insert_experiment)
        print(f"Successfully inserted experiment_id: {experiment_id}")
        return True
    except Exception as e:
        print(f"Error inserting experiment (id: {experiment_id}): {e}")
        return False

def add_analysis_db(analysis_id, signal_id, researcher_id, analysis_type,
                   parameters, results, findings, confidence_score):
    """Inserts a new analysis record."""
    if not db:
        raise ConnectionError("Database connection not initialized.")
    
    def _insert_analysis(transaction):
        transaction.insert(
            table="Analysis",
            columns=[
                "analysis_id", "signal_id", "researcher_id", "analysis_type",
                "parameters", "results", "findings", "confidence_score",
                "analyzed_at", "create_time"
            ],
            values=[(
                analysis_id, signal_id, researcher_id, analysis_type,
                parameters, results, findings, confidence_score,
                datetime.now(timezone.utc), spanner.COMMIT_TIMESTAMP
            )]
        )
    
    try:
        db.run_in_transaction(_insert_analysis)
        return True
    except Exception as e:
        print(f"Error inserting analysis: {e}")
        return False

# --- Custom Jinja Filter ---
@app.template_filter('humanize_datetime')
def _jinja2_filter_humanize_datetime(value, default="just now"):
    """Convert a datetime object to a human-readable relative time string."""
    if not value:
        return default
    
    dt_object = None
    if isinstance(value, str):
        try:
            dt_object = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            try:
                dt_object = parser.parse(value)
            except (parser.ParserError, TypeError, ValueError) as e:
                app.logger.warning(f"Could not parse date string '{value}': {e}")
                return str(value)
    elif isinstance(value, datetime):
        dt_object = value
    else:
        return str(value)
    
    if dt_object is None:
        return str(value)
    
    now = datetime.now(timezone.utc)
    if dt_object.tzinfo is None or dt_object.tzinfo.utcoffset(dt_object) is None:
        dt_object = dt_object.replace(tzinfo=timezone.utc)
    else:
        dt_object = dt_object.astimezone(timezone.utc)
    
    try:
        return humanize.naturaltime(now - dt_object)
    except TypeError:
        return dt_object.strftime("%Y-%m-%d %H:%M")

# --- Routes ---
@app.route('/')
def home():
    """Home page: Shows experiments and recent signals."""
    experiments = []
    recent_signals = []
    
    if not db:
        flash("Database connection not available. Cannot load page data.", "danger")
    else:
        try:
            experiments = get_all_experiments_db()
            recent_signals = get_recent_signals_db()
        except Exception as e:
            flash(f"Failed to load page data: {e}", "danger")
            experiments = []
            recent_signals = []
    
    return render_template(
        'index.html',
        experiments=experiments,
        recent_signals=recent_signals
    )

@app.route('/researcher/<string:researcher_id>')
def researcher_profile(researcher_id):
    """Researcher profile page."""
    if not db:
        flash("Database connection not available.", "danger")
        abort(503)
    
    try:
        researcher = get_researcher_db(researcher_id)
        if not researcher:
            abort(404)
        
        experiments = get_researcher_experiments_db(researcher_id)
        collaborations = get_researcher_collaborations_db(researcher_id)
        
    except Exception as e:
        flash(f"Failed to load researcher data: {e}", "danger")
        return render_template('researcher.html', researcher=researcher, 
                             experiments=[], collaborations=[], error=True)
    
    return render_template(
        'researcher.html',
        researcher=researcher,
        experiments=experiments,
        collaborations=collaborations
    )

@app.route('/experiment/<string:experiment_id>')
def experiment_detail(experiment_id):
    """Experiment detail page."""
    if not db:
        flash("Database connection not available.", "danger")
        abort(503)
    
    try:
        experiment = get_experiment_details_db(experiment_id)
        if not experiment:
            abort(404)
    except Exception as e:
        flash(f"Failed to load experiment data: {e}", "danger")
        print(f"Error fetching experiment {experiment_id}: {e}")
        traceback.print_exc()
        return render_template('experiment.html', experiment=None, error=True)
    
    return render_template('experiment.html', experiment=experiment)

# --- API Routes ---
@app.route('/api/experiments', methods=['POST'])
def add_experiment_api():
    """API endpoint to create a new experiment."""
    if not db:
        return jsonify({"error": "Database connection not available"}), 503
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    required_fields = ["experiment_name", "description", "protocol", 
                      "hypothesis", "principal_investigator_name", "start_date"]
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    try:
        # Find PI by name
        pi_id = get_researcher_by_name_db(data['principal_investigator_name'])
        if not pi_id:
            return jsonify({"error": f"Principal investigator '{data['principal_investigator_name']}' not found"}), 404
        
        # Parse start date
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=timezone.utc)
        else:
            start_date = start_date.astimezone(timezone.utc)
        
        # Create experiment
        experiment_id = str(uuid.uuid4())
        success = add_experiment_db(
            experiment_id=experiment_id,
            name=data['experiment_name'],
            description=data['description'],
            protocol=data['protocol'],
            hypothesis=data['hypothesis'],
            principal_investigator_id=pi_id,
            start_date=start_date,
            status=data.get('status', 'planning')
        )
        
        if success:
            return jsonify({
                "message": "Experiment created successfully",
                "experiment_id": experiment_id,
                "name": data['experiment_name'],
                "principal_investigator": data['principal_investigator_name']
            }), 201
        else:
            return jsonify({"error": "Failed to save experiment to database"}), 500
            
    except Exception as e:
        print(f"Error creating experiment: {e}")
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/api/analyses', methods=['POST'])
def add_analysis_api():
    """API endpoint to create a new analysis report."""
    if not db:
        return jsonify({"error": "Database connection not available"}), 503
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    required_fields = ["signal_id", "researcher_name", "analysis_type",
                      "parameters", "results", "findings", "confidence_score"]
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    try:
        # Find researcher by name
        researcher_id = get_researcher_by_name_db(data['researcher_name'])
        if not researcher_id:
            return jsonify({"error": f"Researcher '{data['researcher_name']}' not found"}), 404
        
        # Create analysis
        analysis_id = str(uuid.uuid4())
        success = add_analysis_db(
            analysis_id=analysis_id,
            signal_id=data['signal_id'],
            researcher_id=researcher_id,
            analysis_type=data['analysis_type'],
            parameters=data['parameters'],  # Already JSON string from MCP
            results=data['results'],        # Already JSON string from MCP
            findings=data['findings'],
            confidence_score=float(data['confidence_score'])
        )
        
        if success:
            return jsonify({
                "message": "Analysis report created successfully",
                "analysis_id": analysis_id,
                "signal_id": data['signal_id'],
                "researcher": data['researcher_name']
            }), 201
        else:
            return jsonify({"error": "Failed to save analysis to database"}), 500
            
    except Exception as e:
        print(f"Error creating analysis: {e}")
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred"}), 500

# --- Error Handlers ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    print(f"Internal Server Error: {e}")
    return render_template('500.html'), 500

@app.errorhandler(503)
def service_unavailable(e):
    print(f"Service Unavailable Error: {e}")
    return render_template('503.html'), 503

if __name__ == '__main__':
    if not db:
        print("\n--- Cannot start Flask app: Spanner database connection failed. ---")
        print("--- Please check GCP project, instance ID, database ID, and permissions. ---")
    else:
        print("\n--- Starting NeuroHub Development Server ---")
        print("--- Adapted from InstaVibe by Christina Lin ---")
        app.run(debug=True, host=APP_HOST, port=APP_PORT)