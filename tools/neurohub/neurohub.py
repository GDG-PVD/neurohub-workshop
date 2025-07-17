"""
NeuroHub MCP Tools
Functions for creating experiments, analyses, and documentation in the NeuroHub platform
"""

import os
import uuid
import requests
import json
from datetime import datetime, timezone
from typing import List, Dict, Optional

# Base URL for NeuroHub API (will be set via environment variable)
BASE_URL = os.environ.get("NEUROHUB_BASE_URL", "http://localhost:8080/api")

def create_experiment(
    experiment_name: str, 
    description: str, 
    protocol: str,
    hypothesis: str,
    principal_investigator_name: str,
    start_date: str,
    status: str = "planning",
    base_url: str = BASE_URL
) -> Dict:
    """
    Creates a new experiment in the NeuroHub system.
    
    Args:
        experiment_name (str): Name of the experiment
        description (str): Detailed description of the experiment
        protocol (str): Experimental protocol details
        hypothesis (str): Research hypothesis
        principal_investigator_name (str): Name of the PI (must exist in system)
        start_date (str): Start date in ISO format (YYYY-MM-DDTHH:MM:SSZ)
        status (str): Experiment status (planning, active, completed, archived)
        base_url (str): Base URL of the API
    
    Returns:
        dict: The JSON response from the API if successful, None if error
    """
    url = f"{base_url}/experiments"
    headers = {"Content-Type": "application/json"}
    payload = {
        "experiment_name": experiment_name,
        "description": description,
        "protocol": protocol,
        "hypothesis": hypothesis,
        "principal_investigator_name": principal_investigator_name,
        "start_date": start_date,
        "status": status
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Successfully created experiment. Status Code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating experiment: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from {url}. Response text: {response.text}")
        return None

def create_analysis_report(
    signal_id: str,
    researcher_name: str,
    analysis_type: str,
    parameters: Dict,
    results: Dict,
    findings: str,
    confidence_score: float,
    base_url: str = BASE_URL
) -> Dict:
    """
    Creates an analysis report for a biosignal.
    
    Args:
        signal_id (str): ID of the signal being analyzed
        researcher_name (str): Name of the researcher performing analysis
        analysis_type (str): Type of analysis (spectral, temporal, connectivity, etc.)
        parameters (dict): Analysis parameters used
        results (dict): Quantitative results
        findings (str): Human-readable findings and interpretation
        confidence_score (float): Confidence score (0-1)
        base_url (str): Base URL of the API
    
    Returns:
        dict: The JSON response from the API if successful, None if error
    """
    url = f"{base_url}/analyses"
    headers = {"Content-Type": "application/json"}
    payload = {
        "signal_id": signal_id,
        "researcher_name": researcher_name,
        "analysis_type": analysis_type,
        "parameters": json.dumps(parameters),  # Convert dict to JSON string
        "results": json.dumps(results),        # Convert dict to JSON string
        "findings": findings,
        "confidence_score": confidence_score,
        "analyzed_at": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Successfully created analysis report. Status Code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating analysis report: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from {url}. Response text: {response.text}")
        return None

def create_session_log(
    experiment_id: str,
    researcher_name: str,
    participant_id: str,
    session_date: str,
    duration_minutes: int,
    notes: str,
    signals_recorded: List[Dict],
    base_url: str = BASE_URL
) -> Dict:
    """
    Creates a session log entry with recorded signals.
    
    Args:
        experiment_id (str): ID of the experiment
        researcher_name (str): Name of the researcher conducting session
        participant_id (str): Anonymous participant identifier
        session_date (str): Session date in ISO format
        duration_minutes (int): Session duration in minutes
        notes (str): Session notes
        signals_recorded (list): List of signal recordings with device info
        base_url (str): Base URL of the API
    
    Returns:
        dict: The JSON response from the API if successful, None if error
    """
    url = f"{base_url}/sessions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "experiment_id": experiment_id,
        "researcher_name": researcher_name,
        "participant_id": participant_id,
        "session_date": session_date,
        "duration_minutes": duration_minutes,
        "notes": notes,
        "signals": signals_recorded
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Successfully created session log. Status Code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating session log: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from {url}. Response text: {response.text}")
        return None

def export_findings(
    experiment_id: str,
    format: str = "markdown",
    include_raw_data: bool = False,
    base_url: str = BASE_URL
) -> Dict:
    """
    Exports experiment findings in a publication-ready format.
    
    Args:
        experiment_id (str): ID of the experiment to export
        format (str): Export format (markdown, latex, json)
        include_raw_data (bool): Whether to include raw data references
        base_url (str): Base URL of the API
    
    Returns:
        dict: Export data including formatted content and metadata
    """
    url = f"{base_url}/experiments/{experiment_id}/export"
    headers = {"Content-Type": "application/json"}
    params = {
        "format": format,
        "include_raw_data": include_raw_data
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        print(f"Successfully exported findings. Status Code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error exporting findings: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from {url}. Response text: {response.text}")
        return None

def register_device(
    device_name: str,
    device_type: str,
    manufacturer: str,
    model: str,
    sampling_rate: int,
    channels: int,
    specifications: Dict,
    base_url: str = BASE_URL
) -> Dict:
    """
    Registers a new device in the NeuroHub system.
    
    Args:
        device_name (str): Friendly name for the device
        device_type (str): Type of device (EEG, EMG, ECG, etc.)
        manufacturer (str): Device manufacturer
        model (str): Device model
        sampling_rate (int): Sampling rate in Hz
        channels (int): Number of channels
        specifications (dict): Additional technical specifications
        base_url (str): Base URL of the API
    
    Returns:
        dict: The JSON response from the API if successful, None if error
    """
    url = f"{base_url}/devices"
    headers = {"Content-Type": "application/json"}
    payload = {
        "name": device_name,
        "device_type": device_type,
        "manufacturer": manufacturer,
        "model": model,
        "sampling_rate": sampling_rate,
        "channels": channels,
        "specifications": json.dumps(specifications),
        "status": "available"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Successfully registered device. Status Code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error registering device: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from {url}. Response text: {response.text}")
        return None
