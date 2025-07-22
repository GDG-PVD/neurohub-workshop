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
from neurohub_routes import ally_bp
from db_neurohub import (
    db,
    get_all_researchers,
    get_experiments_by_researcher,
    get_experiment_details,
    get_recent_analyses,
    get_researcher_collaborations,
    get_signal_data_by_experiment
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "a_default_secret_key_for_dev") 
app.register_blueprint(ally_bp)

load_dotenv()

# --- Configuration ---
INSTANCE_ID = os.environ.get("SPANNER_INSTANCE_ID", "neurohub-graph-instance")
DATABASE_ID = os.environ.get("SPANNER_DATABASE_ID", "neurohub-db")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = os.environ.get("APP_PORT", "8080")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
GOOGLE_MAPS_MAP_KEY = os.environ.get('GOOGLE_MAPS_MAP_ID')

if not PROJECT_ID:
    print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set.")

# --- Custom Jinja Filter ---
@app.template_filter('humanize_datetime')
def humanize_datetime(dt):
    """Convert datetime to human-readable format like '2 hours ago'."""
    if dt is None:
        return "Unknown time"
    if isinstance(dt, str):
        try:
            dt = parser.parse(dt)
        except:
            return dt
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return humanize.naturaltime(dt)

# --- Routes ---
@app.route('/')
def home():
    """Home page: Dashboard showing experiment statistics and recent activity."""
    # TODO: Add database queries to fetch:
    # - Recent experiments
    # - Active researchers
    # - Recent analyses
    # - Signal data stats
    return render_template('index.html')

@app.route('/experiments')
def experiments():
    """List all experiments."""
    # TODO: Fetch experiments from database
    return render_template('experiments.html')

@app.route('/experiment/<int:experiment_id>')
def experiment_detail(experiment_id):
    """Show experiment details."""
    if not db:
        flash("Database connection not available.", "danger")
        abort(503)
    
    try:
        # Get experiment details
        experiment = get_experiment_details(db, experiment_id)
        if not experiment:
            abort(404)
        
        # Get signal data for this experiment
        signal_data = get_signal_data_by_experiment(db, experiment_id)
        
        return render_template(
            'experiment.html',
            experiment=experiment,
            signal_data=signal_data or []
        )
        
    except Exception as e:
        flash(f"Failed to load experiment: {e}", "danger")
        return render_template('experiment.html', error=True)

@app.route('/researchers')
def researchers():
    """List all researchers."""
    if not db:
        flash("Database connection not available.", "danger")
        return render_template('researchers.html', researchers=[])
    
    try:
        researchers_list = get_all_researchers(db, limit=100)
        return render_template('researchers.html', researchers=researchers_list or [])
    except Exception as e:
        flash(f"Failed to load researchers: {e}", "danger")
        return render_template('researchers.html', researchers=[])

@app.route('/researcher/<int:researcher_id>')
def researcher_profile(researcher_id):
    """Show researcher profile with experiments, collaborations, and activity."""
    if not db:
        flash("Database connection not available.", "danger")
        abort(503)
    
    try:
        # Get researcher details (TODO: Add get_researcher_by_id function to db_neurohub)
        # For now, create a dummy researcher object
        researcher = {
            'researcher_id': researcher_id,
            'name': f'Researcher {researcher_id}',
            'email': f'researcher{researcher_id}@neurohub.org',
            'institution': 'NeuroHub Research Institute',
            'expertise': 'EEG, Signal Processing, Machine Learning',
            'bio': 'Leading researcher in neurotechnology'
        }
        
        # Get researcher's experiments
        experiments = get_experiments_by_researcher(db, researcher_id)
        
        # Get collaborations
        collaborators = get_researcher_collaborations(db, researcher_id)
        
        # Calculate stats
        total_sessions = 0  # TODO: Add function to calculate this
        publications = []  # TODO: Add publications table/function
        recent_activity = []  # TODO: Add activity tracking function
        
        return render_template(
            'researcher.html',
            researcher=researcher,
            experiments=experiments or [],
            collaborators=collaborators or [],
            publications=publications,
            total_sessions=total_sessions,
            recent_activity=recent_activity,
            error=False
        )
        
    except Exception as e:
        flash(f"Failed to load researcher profile: {e}", "danger")
        return render_template('researcher.html', error=True)

@app.route('/signals')
def signals():
    """Signal analysis dashboard."""
    # TODO: Fetch signal data and analyses
    return render_template('signals.html')

@app.route('/devices')
def devices():
    """Device management page."""
    # TODO: Fetch devices from database
    return render_template('devices.html')

# --- API Routes for NeuroHub ---
@app.route('/api/experiments', methods=['POST'])
def create_experiment():
    """
    API endpoint to create a new experiment.
    Expects JSON body with experiment details.
    """
    if not db:
        return jsonify({"error": "Database connection not available"}), 503
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    # TODO: Implement experiment creation
    return jsonify({"message": "Experiment creation endpoint - to be implemented"}), 501

@app.route('/api/analyses', methods=['POST'])
def create_analysis():
    """
    API endpoint to create a new analysis report.
    Expects JSON body with analysis details.
    """
    if not db:
        return jsonify({"error": "Database connection not available"}), 503
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    # TODO: Implement analysis creation
    return jsonify({"message": "Analysis creation endpoint - to be implemented"}), 501

@app.route('/api/sessions', methods=['POST'])
def create_session():
    """
    API endpoint to create a new experimental session.
    Expects JSON body with session details.
    """
    if not db:
        return jsonify({"error": "Database connection not available"}), 503
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    # TODO: Implement session creation
    return jsonify({"message": "Session creation endpoint - to be implemented"}), 501

# --- Error Handlers ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(503)
def service_unavailable(e):
    return render_template('503.html'), 503

if __name__ == '__main__':
    print(f"Starting NeuroHub app on {APP_HOST}:{APP_PORT}")
    app.run(host=APP_HOST, port=int(APP_PORT), debug=True)