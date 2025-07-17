import os
import uuid
from datetime import datetime, timedelta, timezone
from dateutil import parser as dateutil_parser
import time
import random

from google.cloud import spanner
from google.api_core import exceptions

# --- Configuration ---
INSTANCE_ID = os.environ.get("SPANNER_INSTANCE_ID", "neurohub-graph-instance")
DATABASE_ID = os.environ.get("SPANNER_DATABASE_ID", "neurohub-db")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

# --- Spanner Client Initialization ---
try:
    spanner_client = spanner.Client(project=PROJECT_ID)
    instance = spanner_client.instance(INSTANCE_ID)
    database = instance.database(DATABASE_ID)
    print(f"Targeting Spanner: {instance.name}/databases/{database.name}")
    if not database.exists():
        print(f"Error: Database '{DATABASE_ID}' does not exist. Please create it first.")
        database = None
    else:
        print("Database connection successful.")
except exceptions.NotFound:
    print(f"Error: Spanner instance '{INSTANCE_ID}' not found or missing permissions.")
    spanner_client = None; instance = None; database = None
except Exception as e:
    print(f"Error initializing Spanner client: {e}")
    spanner_client = None; instance = None; database = None

def run_ddl_statements(db_instance, ddl_list, operation_description):
    """Helper function to run DDL statements and handle potential errors."""
    if not db_instance:
        print(f"Skipping DDL ({operation_description}) - database connection not available.")
        return False
    print(f"\n--- Running DDL: {operation_description} ---")
    print("Statements:")
    # Print statements cleanly
    for i, stmt in enumerate(ddl_list):
        print(f"  [{i+1}] {stmt.strip()}")
    try:
        operation = db_instance.update_ddl(ddl_list)
        print("Waiting for DDL operation to complete...")
        operation.result(360)  # Wait up to 6 minutes
        print(f"DDL operation '{operation_description}' completed successfully.")
        return True
    except (exceptions.FailedPrecondition, exceptions.AlreadyExists) as e:
        print(f"Warning/Info during DDL '{operation_description}': {type(e).__name__} - {e}")
        print("Continuing script execution (schema object might already exist or precondition failed).")
        return True
    except exceptions.InvalidArgument as e:
        print(f"ERROR during DDL '{operation_description}': {type(e).__name__} - {e}")
        print(">>> This indicates a DDL syntax error. The schema was NOT created/updated correctly. Stopping script. <<<")
        return False
    except exceptions.DeadlineExceeded:
        print(f"ERROR during DDL '{operation_description}': DeadlineExceeded - Operation took too long.")
        return False
    except Exception as e:
        print(f"ERROR during DDL '{operation_description}': {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        print("Stopping script due to unexpected DDL error.")
        return False

def setup_base_schema_and_indexes(db_instance):
    """Creates the base relational tables and associated indexes for NeuroHub."""
    ddl_statements = [
        # --- 1. Base Tables for Neurotechnology Research ---
        """
        CREATE TABLE IF NOT EXISTS Researcher (
            researcher_id STRING(36) NOT NULL,
            name STRING(MAX),
            email STRING(MAX),
            institution STRING(MAX),
            expertise STRING(MAX),
            years_experience INT64,
            create_time TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (researcher_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS Experiment (
            experiment_id STRING(36) NOT NULL,
            name STRING(MAX),
            description STRING(MAX),
            protocol STRING(MAX),
            hypothesis STRING(MAX),
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            status STRING(50),  -- planning, active, completed, archived
            principal_investigator_id STRING(36),  -- References Researcher.researcher_id
            create_time TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (experiment_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS Device (
            device_id STRING(36) NOT NULL,
            name STRING(MAX),
            device_type STRING(100),  -- EEG, EMG, ECG, Eye-tracker, etc.
            manufacturer STRING(MAX),
            model STRING(MAX),
            sampling_rate INT64,  -- Hz
            channels INT64,
            specifications STRING(MAX),  -- JSON string with detailed specs
            status STRING(50),  -- available, in_use, maintenance, retired
            create_time TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (device_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS SignalData (
            signal_id STRING(36) NOT NULL,
            experiment_id STRING(36) NOT NULL,  -- References Experiment.experiment_id
            session_id STRING(36) NOT NULL,  -- References Session.session_id
            device_id STRING(36) NOT NULL,  -- References Device.device_id
            signal_type STRING(50),  -- EEG, EMG, ECG, etc.
            duration_seconds FLOAT64,
            sampling_rate INT64,
            channels INT64,
            file_path STRING(MAX),  -- Cloud Storage path
            quality_score FLOAT64,  -- 0-1 signal quality metric
            processing_status STRING(50),  -- raw, filtered, processed, analyzed
            recorded_at TIMESTAMP,
            notes STRING(MAX),
            create_time TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (signal_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS Session (
            session_id STRING(36) NOT NULL,
            experiment_id STRING(36) NOT NULL,  -- References Experiment.experiment_id
            participant_id STRING(36),  -- Could reference a Participant table (simplified here)
            researcher_id STRING(36) NOT NULL,  -- References Researcher.researcher_id
            session_date TIMESTAMP,
            duration_minutes INT64,
            notes STRING(MAX),
            create_time TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (session_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS Analysis (
            analysis_id STRING(36) NOT NULL,
            signal_id STRING(36) NOT NULL,  -- References SignalData.signal_id
            researcher_id STRING(36) NOT NULL,  -- References Researcher.researcher_id
            analysis_type STRING(100),  -- spectral, temporal, connectivity, etc.
            parameters STRING(MAX),  -- JSON string with analysis parameters
            results STRING(MAX),  -- JSON string with analysis results
            findings STRING(MAX),  -- Human-readable findings
            confidence_score FLOAT64,
            analyzed_at TIMESTAMP,
            create_time TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (analysis_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS Collaboration (
            researcher_id_a STRING(36) NOT NULL,  -- References Researcher.researcher_id
            researcher_id_b STRING(36) NOT NULL,  -- References Researcher.researcher_id
            project_name STRING(MAX),
            collaboration_type STRING(50),  -- co-author, advisor, team_member
            start_date TIMESTAMP,
            create_time TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (researcher_id_a, researcher_id_b)
        """,
        """
        CREATE TABLE IF NOT EXISTS ExperimentDevice (
            experiment_id STRING(36) NOT NULL,  -- References Experiment.experiment_id
            device_id STRING(36) NOT NULL,  -- References Device.device_id
            configuration STRING(MAX),  -- JSON string with device-specific settings
            create_time TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp=true),
            CONSTRAINT FK_Experiment FOREIGN KEY (experiment_id) REFERENCES Experiment (experiment_id),
            CONSTRAINT FK_Device FOREIGN KEY (device_id) REFERENCES Device (device_id)
        ) PRIMARY KEY (experiment_id, device_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS Publication (
            publication_id STRING(36) NOT NULL,
            experiment_id STRING(36),  -- References Experiment.experiment_id
            title STRING(MAX),
            authors STRING(MAX),  -- JSON array of author names
            journal STRING(MAX),
            publication_date TIMESTAMP,
            doi STRING(MAX),
            abstract STRING(MAX),
            create_time TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (publication_id)
        """,
        # --- 2. Indexes ---
        "CREATE INDEX IF NOT EXISTS ResearcherByName ON Researcher(name)",
        "CREATE INDEX IF NOT EXISTS ResearcherByInstitution ON Researcher(institution)",
        "CREATE INDEX IF NOT EXISTS ExperimentByStatus ON Experiment(status, start_date DESC)",
        "CREATE INDEX IF NOT EXISTS ExperimentByPI ON Experiment(principal_investigator_id, start_date DESC)",
        "CREATE INDEX IF NOT EXISTS DeviceByType ON Device(device_type, status)",
        "CREATE INDEX IF NOT EXISTS SignalByExperiment ON SignalData(experiment_id, recorded_at DESC)",
        "CREATE INDEX IF NOT EXISTS SignalByDevice ON SignalData(device_id, recorded_at DESC)",
        "CREATE INDEX IF NOT EXISTS SessionByExperiment ON Session(experiment_id, session_date DESC)",
        "CREATE INDEX IF NOT EXISTS AnalysisBySignal ON Analysis(signal_id, analyzed_at DESC)",
        "CREATE INDEX IF NOT EXISTS CollaborationByResearcherB ON Collaboration(researcher_id_b, researcher_id_a)",
    ]
    return run_ddl_statements(db_instance, ddl_statements, "Create Base Tables and Indexes")

def setup_graph_definition(db_instance):
    """Creates the Property Graph definition for research relationships."""
    ddl_statements = [
        """
        CREATE PROPERTY GRAPH IF NOT EXISTS NeuroResearchGraph
          NODE TABLES (
            Researcher KEY (researcher_id),
            Experiment KEY (experiment_id),
            Device KEY (device_id),
            SignalData KEY (signal_id),
            Session KEY (session_id),
            Analysis KEY (analysis_id),
            Publication KEY (publication_id)
          )
          EDGE TABLES (
            Collaboration 
              SOURCE KEY (researcher_id_a) REFERENCES Researcher (researcher_id)
              DESTINATION KEY (researcher_id_b) REFERENCES Researcher (researcher_id),
            
            Experiment AS Leads
              SOURCE KEY (principal_investigator_id) REFERENCES Researcher (researcher_id)
              DESTINATION KEY (experiment_id) REFERENCES Experiment (experiment_id),
            
            Session AS Conducts
              SOURCE KEY (researcher_id) REFERENCES Researcher (researcher_id)
              DESTINATION KEY (session_id) REFERENCES Session (session_id),
            
            Session AS PartOf
              SOURCE KEY (session_id) REFERENCES Session (session_id)
              DESTINATION KEY (experiment_id) REFERENCES Experiment (experiment_id),
            
            SignalData AS RecordedIn
              SOURCE KEY (signal_id) REFERENCES SignalData (signal_id)
              DESTINATION KEY (session_id) REFERENCES Session (session_id),
            
            SignalData AS RecordedWith
              SOURCE KEY (signal_id) REFERENCES SignalData (signal_id)
              DESTINATION KEY (device_id) REFERENCES Device (device_id),
            
            Analysis AS Analyzes
              SOURCE KEY (analysis_id) REFERENCES Analysis (analysis_id)
              DESTINATION KEY (signal_id) REFERENCES SignalData (signal_id),
            
            Analysis AS PerformedBy
              SOURCE KEY (researcher_id) REFERENCES Researcher (researcher_id)
              DESTINATION KEY (analysis_id) REFERENCES Analysis (analysis_id),
            
            ExperimentDevice AS Uses
              SOURCE KEY (experiment_id) REFERENCES Experiment (experiment_id)
              DESTINATION KEY (device_id) REFERENCES Device (device_id),
              
            Publication AS Documents
              SOURCE KEY (publication_id) REFERENCES Publication (publication_id)
              DESTINATION KEY (experiment_id) REFERENCES Experiment (experiment_id)
          )
        """
    ]
    return run_ddl_statements(db_instance, ddl_statements, "Create Property Graph Definition")

# --- Data Generation / Insertion ---
def generate_uuid(): 
    return str(uuid.uuid4())

def insert_neurohub_data(db_instance):
    """Generates and inserts sample neurotechnology research data."""
    if not db_instance: 
        print("Skipping data insertion - db connection unavailable.")
        return False
    
    print("\n--- Generating Sample NeuroHub Data ---")
    
    # Maps for referential integrity
    researcher_map = {}  # name -> id
    experiment_map = {}  # name -> id
    device_map = {}      # name -> id
    session_map = {}     # (experiment_name, session_num) -> id
    signal_map = {}      # signal_id -> signal_info
    
    # Data lists for batch insertion
    researchers_rows = []
    experiments_rows = []
    devices_rows = []
    sessions_rows = []
    signals_rows = []
    analyses_rows = []
    collaborations_rows = []
    experiment_devices_rows = []
    publications_rows = []
    
    now = datetime.now(timezone.utc)
    
    # 1. Prepare Researchers Data
    researchers_data = {
        "Dr. Sarah Chen": {"email": "s.chen@brown.edu", "institution": "Brown University", 
                          "expertise": "EEG, Brain-Computer Interfaces", "years": 12},
        "Dr. Michael Rodriguez": {"email": "m.rodriguez@bgu.ac.il", "institution": "Ben-Gurion University",
                                 "expertise": "Signal Processing, Machine Learning", "years": 8},
        "Prof. Emily Watson": {"email": "e.watson@brown.edu", "institution": "Brown University",
                              "expertise": "Cognitive Neuroscience, fMRI", "years": 20},
        "Dr. David Kim": {"email": "d.kim@bgu.ac.il", "institution": "Ben-Gurion University",
                         "expertise": "Neurofeedback, Real-time Processing", "years": 6},
        "Dr. Lisa Anderson": {"email": "l.anderson@brown.edu", "institution": "Brown University",
                             "expertise": "EMG, Motor Control", "years": 10},
        "Dr. James Liu": {"email": "j.liu@bgu.ac.il", "institution": "Ben-Gurion University",
                         "expertise": "Wearable Sensors, IoT", "years": 5},
        "Prof. Rachel Green": {"email": "r.green@brown.edu", "institution": "Brown University",
                              "expertise": "Clinical Applications, Rehabilitation", "years": 15},
        "Dr. Ahmed Hassan": {"email": "a.hassan@bgu.ac.il", "institution": "Ben-Gurion University",
                            "expertise": "Deep Learning, Pattern Recognition", "years": 7}
    }
    
    print(f"Preparing {len(researchers_data)} researchers.")
    for name, data in researchers_data.items():
        researcher_id = generate_uuid()
        researcher_map[name] = researcher_id
        researchers_rows.append({
            "researcher_id": researcher_id,
            "name": name,
            "email": data["email"],
            "institution": data["institution"],
            "expertise": data["expertise"],
            "years_experience": data["years"],
            "create_time": spanner.COMMIT_TIMESTAMP
        })
    
    # 2. Prepare Devices Data
    devices_data = {
        "OpenBCI Cyton 8": {"type": "EEG", "manufacturer": "OpenBCI", "model": "Cyton", 
                           "sampling_rate": 250, "channels": 8, "status": "available"},
        "Emotiv EPOC X": {"type": "EEG", "manufacturer": "Emotiv", "model": "EPOC X",
                         "sampling_rate": 256, "channels": 14, "status": "available"},
        "Delsys Trigno": {"type": "EMG", "manufacturer": "Delsys", "model": "Trigno Wireless",
                         "sampling_rate": 2000, "channels": 16, "status": "in_use"},
        "Tobii Pro Nano": {"type": "Eye Tracker", "manufacturer": "Tobii", "model": "Pro Nano",
                          "sampling_rate": 60, "channels": 2, "status": "available"},
        "BioSemi ActiveTwo": {"type": "EEG", "manufacturer": "BioSemi", "model": "ActiveTwo",
                             "sampling_rate": 2048, "channels": 64, "status": "available"},
        "Polar H10": {"type": "ECG", "manufacturer": "Polar", "model": "H10",
                     "sampling_rate": 130, "channels": 1, "status": "available"}
    }
    
    print(f"Preparing {len(devices_data)} devices.")
    for name, data in devices_data.items():
        device_id = generate_uuid()
        device_map[name] = device_id
        devices_rows.append({
            "device_id": device_id,
            "name": name,
            "device_type": data["type"],
            "manufacturer": data["manufacturer"],
            "model": data["model"],
            "sampling_rate": data["sampling_rate"],
            "channels": data["channels"],
            "specifications": '{"wireless": true, "battery_life": "8 hours"}',
            "status": data["status"],
            "create_time": spanner.COMMIT_TIMESTAMP
        })
    
    # 3. Prepare Experiments Data
    experiments_data = {
        "Motor Imagery BCI Training": {
            "description": "Developing a brain-computer interface for motor imagery classification using deep learning",
            "protocol": "10 sessions of motor imagery tasks with visual feedback",
            "hypothesis": "CNN-based classifiers will outperform traditional CSP+LDA approaches",
            "pi": "Dr. Sarah Chen",
            "status": "active",
            "devices": ["OpenBCI Cyton 8", "Tobii Pro Nano"],
            "start_days_ago": 30
        },
        "Stress Detection from Multimodal Signals": {
            "description": "Real-time stress detection using combined EEG, ECG, and eye-tracking data",
            "protocol": "Stress-inducing tasks with simultaneous physiological recording",
            "hypothesis": "Multimodal fusion will improve stress detection accuracy by 25%",
            "pi": "Dr. Michael Rodriguez",
            "status": "active",
            "devices": ["Emotiv EPOC X", "Polar H10", "Tobii Pro Nano"],
            "start_days_ago": 45
        },
        "EMG-based Gesture Recognition": {
            "description": "Developing a real-time hand gesture recognition system using surface EMG",
            "protocol": "Recording EMG during 10 different hand gestures",
            "hypothesis": "Temporal convolutional networks will achieve >95% accuracy",
            "pi": "Dr. Lisa Anderson",
            "status": "completed",
            "devices": ["Delsys Trigno"],
            "start_days_ago": 90,
            "end_days_ago": 10
        },
        "Neurofeedback for ADHD": {
            "description": "Clinical trial of EEG neurofeedback training for ADHD symptom reduction",
            "protocol": "20 sessions of theta/beta ratio training with clinical assessments",
            "hypothesis": "Neurofeedback will reduce ADHD symptoms by 30% on standard scales",
            "pi": "Prof. Rachel Green",
            "status": "planning",
            "devices": ["BioSemi ActiveTwo"],
            "start_days_ago": -10  # Future start
        }
    }
    
    print(f"Preparing {len(experiments_data)} experiments.")
    for name, data in experiments_data.items():
        experiment_id = generate_uuid()
        experiment_map[name] = experiment_id
        
        start_date = now - timedelta(days=data["start_days_ago"])
        end_date = None
        if data["status"] == "completed" and "end_days_ago" in data:
            end_date = now - timedelta(days=data["end_days_ago"])
        
        experiments_rows.append({
            "experiment_id": experiment_id,
            "name": name,
            "description": data["description"],
            "protocol": data["protocol"],
            "hypothesis": data["hypothesis"],
            "start_date": start_date,
            "end_date": end_date,
            "status": data["status"],
            "principal_investigator_id": researcher_map[data["pi"]],
            "create_time": spanner.COMMIT_TIMESTAMP
        })
        
        # Link devices to experiments
        for device_name in data["devices"]:
            if device_name in device_map:
                experiment_devices_rows.append({
                    "experiment_id": experiment_id,
                    "device_id": device_map[device_name],
                    "configuration": '{"gain": 24, "notch_filter": "60Hz"}',
                    "create_time": spanner.COMMIT_TIMESTAMP
                })
    
    # 4. Prepare Sessions and Signals Data
    active_experiments = ["Motor Imagery BCI Training", "Stress Detection from Multimodal Signals"]
    
    for exp_name in active_experiments:
        if exp_name not in experiment_map:
            continue
            
        exp_id = experiment_map[exp_name]
        exp_data = experiments_data[exp_name]
        
        # Create 5 sessions per active experiment
        for session_num in range(1, 6):
            session_id = generate_uuid()
            session_key = (exp_name, session_num)
            session_map[session_key] = session_id
            
            # Randomly assign a researcher
            researcher_name = random.choice(list(researcher_map.keys()))
            
            session_date = now - timedelta(days=random.randint(1, 20))
            
            sessions_rows.append({
                "session_id": session_id,
                "experiment_id": exp_id,
                "participant_id": generate_uuid(),  # Anonymous participant
                "researcher_id": researcher_map[researcher_name],
                "session_date": session_date,
                "duration_minutes": random.randint(30, 90),
                "notes": f"Session {session_num} - participant performed well",
                "create_time": spanner.COMMIT_TIMESTAMP
            })
            
            # Create signals for each device in the experiment
            for device_name in exp_data["devices"]:
                if device_name in device_map:
                    signal_id = generate_uuid()
                    device = devices_data[device_name]
                    
                    signals_rows.append({
                        "signal_id": signal_id,
                        "experiment_id": exp_id,
                        "session_id": session_id,
                        "device_id": device_map[device_name],
                        "signal_type": device["type"],
                        "duration_seconds": random.uniform(300, 1800),
                        "sampling_rate": device["sampling_rate"],
                        "channels": device["channels"],
                        "file_path": f"gs://neurohub-data/{exp_name}/{session_num}/{device_name}.edf",
                        "quality_score": random.uniform(0.7, 1.0),
                        "processing_status": random.choice(["raw", "filtered", "processed"]),
                        "recorded_at": session_date,
                        "notes": "Good signal quality",
                        "create_time": spanner.COMMIT_TIMESTAMP
                    })
                    
                    # Create analyses for some signals
                    if random.random() > 0.5:
                        analysis_id = generate_uuid()
                        analyst = random.choice(list(researcher_map.keys()))
                        
                        analyses_rows.append({
                            "analysis_id": analysis_id,
                            "signal_id": signal_id,
                            "researcher_id": researcher_map[analyst],
                            "analysis_type": random.choice(["spectral", "temporal", "connectivity"]),
                            "parameters": '{"window": "hann", "overlap": 0.5}',
                            "results": '{"dominant_frequency": 10.5, "power_ratio": 0.75}',
                            "findings": "Strong alpha activity observed in occipital channels",
                            "confidence_score": random.uniform(0.8, 0.95),
                            "analyzed_at": session_date + timedelta(days=random.randint(1, 5)),
                            "create_time": spanner.COMMIT_TIMESTAMP
                        })
    
    # 5. Prepare Collaborations Data
    collaborations_data = [
        ("Dr. Sarah Chen", "Dr. Michael Rodriguez", "BCI-ML Integration", "co-author"),
        ("Prof. Emily Watson", "Dr. David Kim", "Real-time fMRI Analysis", "advisor"),
        ("Dr. Lisa Anderson", "Dr. James Liu", "Wearable EMG Systems", "team_member"),
        ("Prof. Rachel Green", "Dr. Sarah Chen", "Clinical BCI Applications", "co-author"),
        ("Dr. Michael Rodriguez", "Dr. Ahmed Hassan", "Deep Learning for EEG", "team_member"),
        ("Dr. David Kim", "Dr. James Liu", "IoT Neurofeedback Platform", "co-author")
    ]
    
    print(f"Preparing {len(collaborations_data)} collaborations.")
    for r1_name, r2_name, project, collab_type in collaborations_data:
        if r1_name in researcher_map and r2_name in researcher_map:
            id1, id2 = researcher_map[r1_name], researcher_map[r2_name]
            # Ensure consistent ordering for primary key
            researcher_id_a, researcher_id_b = tuple(sorted((id1, id2)))
            
            collaborations_rows.append({
                "researcher_id_a": researcher_id_a,
                "researcher_id_b": researcher_id_b,
                "project_name": project,
                "collaboration_type": collab_type,
                "start_date": now - timedelta(days=random.randint(30, 365)),
                "create_time": spanner.COMMIT_TIMESTAMP
            })
    
    # 6. Prepare Publications Data
    publications_data = [
        {
            "experiment": "EMG-based Gesture Recognition",
            "title": "Real-time Hand Gesture Recognition Using Temporal Convolutional Networks and Surface EMG",
            "authors": ["Dr. Lisa Anderson", "Dr. James Liu", "Dr. Ahmed Hassan"],
            "journal": "IEEE Transactions on Neural Systems and Rehabilitation Engineering",
            "doi": "10.1109/TNSRE.2024.1234567"
        }
    ]
    
    for pub_data in publications_data:
        if pub_data["experiment"] in experiment_map:
            publications_rows.append({
                "publication_id": generate_uuid(),
                "experiment_id": experiment_map[pub_data["experiment"]],
                "title": pub_data["title"],
                "authors": str(pub_data["authors"]),  # Convert list to string
                "journal": pub_data["journal"],
                "publication_date": now - timedelta(days=random.randint(1, 30)),
                "doi": pub_data["doi"],
                "abstract": "We present a novel approach to real-time hand gesture recognition...",
                "create_time": spanner.COMMIT_TIMESTAMP
            })
    
    print(f"Prepared: {len(researchers_rows)} researchers, {len(experiments_rows)} experiments, "
          f"{len(devices_rows)} devices, {len(sessions_rows)} sessions, {len(signals_rows)} signals, "
          f"{len(analyses_rows)} analyses")
    
    # --- Insert Data into Spanner using a Transaction ---
    print("\n--- Inserting Data into NeuroHub Tables ---")
    inserted_counts = {}
    
    def insert_data_txn(transaction):
        total_rows_attempted = 0
        table_map = {
            "Researcher": (["researcher_id", "name", "email", "institution", "expertise", 
                           "years_experience", "create_time"], researchers_rows),
            "Device": (["device_id", "name", "device_type", "manufacturer", "model", 
                       "sampling_rate", "channels", "specifications", "status", "create_time"], devices_rows),
            "Experiment": (["experiment_id", "name", "description", "protocol", "hypothesis", 
                           "start_date", "end_date", "status", "principal_investigator_id", 
                           "create_time"], experiments_rows),
            "Session": (["session_id", "experiment_id", "participant_id", "researcher_id", 
                        "session_date", "duration_minutes", "notes", "create_time"], sessions_rows),
            "SignalData": (["signal_id", "experiment_id", "session_id", "device_id", "signal_type",
                           "duration_seconds", "sampling_rate", "channels", "file_path", 
                           "quality_score", "processing_status", "recorded_at", "notes", 
                           "create_time"], signals_rows),
            "Analysis": (["analysis_id", "signal_id", "researcher_id", "analysis_type", 
                         "parameters", "results", "findings", "confidence_score", 
                         "analyzed_at", "create_time"], analyses_rows),
            "Collaboration": (["researcher_id_a", "researcher_id_b", "project_name", 
                              "collaboration_type", "start_date", "create_time"], collaborations_rows),
            "ExperimentDevice": (["experiment_id", "device_id", "configuration", 
                                 "create_time"], experiment_devices_rows),
            "Publication": (["publication_id", "experiment_id", "title", "authors", "journal",
                            "publication_date", "doi", "abstract", "create_time"], publications_rows)
        }
        
        for table_name, (cols, rows_dict_list) in table_map.items():
            if rows_dict_list:
                print(f"Inserting {len(rows_dict_list)} rows into {table_name}...")
                values_list = []
                for row_dict in rows_dict_list:
                    try:
                        values_tuple = tuple(row_dict.get(c) for c in cols)
                        values_list.append(values_tuple)
                    except Exception as e:
                        print(f"Error preparing row for {table_name}: {e} - Row: {row_dict}")
                
                if values_list:
                    transaction.insert(
                        table=table_name,
                        columns=cols,
                        values=values_list
                    )
                    inserted_counts[table_name] = len(values_list)
                    total_rows_attempted += len(values_list)
                else:
                    inserted_counts[table_name] = 0
            else:
                inserted_counts[table_name] = 0
        print(f"Transaction attempting to insert {total_rows_attempted} rows across all tables.")
    
    # Execute the transaction
    try:
        print("Executing data insertion transaction...")
        all_data_lists = [
            researchers_rows, experiments_rows, devices_rows, sessions_rows,
            signals_rows, analyses_rows, collaborations_rows, experiment_devices_rows,
            publications_rows
        ]
        if any(len(data_list) > 0 for data_list in all_data_lists):
            db_instance.run_in_transaction(insert_data_txn)
            print("Transaction committed successfully.")
            for table, count in inserted_counts.items():
                if count > 0: 
                    print(f"  -> Inserted {count} rows into {table}.")
            return True
        else:
            print("No data prepared for insertion.")
        return True
    except exceptions.Aborted as e:
        print(f"ERROR: Data insertion transaction aborted: {e}. Consider retrying.")
        return False
    except Exception as e:
        print(f"ERROR during data insertion transaction: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        print("Data insertion failed. Database schema might exist but data is missing/incomplete.")
        return False

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting NeuroHub Database Setup Script...")
    print("This creates a neurotechnology research platform schema.")
    print("Adapted from InstaVibe by Christina Lin")
    print("-" * 50)
    start_time = time.time()
    
    if not database:
        print("\nCritical Error: Spanner database connection not established. Aborting.")
        exit(1)
    
    # Step 1: Create schema
    if not setup_base_schema_and_indexes(database):
        print("\nAborting script due to errors during base schema/index creation.")
        exit(1)
    
    # Step 2: Create graph definition
    if not setup_graph_definition(database):
        print("\nAborting script due to errors during graph definition creation.")
        exit(1)
    
    # Step 3: Insert sample data
    if not insert_neurohub_data(database):
        print("\nScript finished with errors during data insertion.")
        exit(1)
    
    end_time = time.time()
    print("\n" + "=" * 50)
    print("NeuroHub setup completed successfully!")
    print(f"Database '{DATABASE_ID}' on instance '{INSTANCE_ID}' is ready.")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print("=" * 50)