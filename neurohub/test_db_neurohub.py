#!/usr/bin/env python3
"""
Test script for SQL-based NeuroHub database queries.
Run this to verify database connectivity and query functionality.
"""

import os
import sys
import json
from datetime import datetime

# Import our database module
from db_neurohub import (
    db,
    get_all_researchers,
    get_experiments_by_researcher,
    get_experiment_details,
    get_recent_analyses,
    get_researcher_collaborations,
    get_signal_data_by_experiment
)

def test_database_connection():
    """Test 1: Database Connection"""
    print("=" * 60)
    print("TEST 1: Database Connection")
    print("=" * 60)
    
    if db:
        print("✅ Database connection established")
        print(f"   Instance: {os.environ.get('SPANNER_INSTANCE_ID', 'Not set')}")
        print(f"   Database: {os.environ.get('SPANNER_DATABASE_ID', 'Not set')}")
        print(f"   Project: {os.environ.get('GOOGLE_CLOUD_PROJECT', 'Not set')}")
        return True
    else:
        print("❌ Database connection failed")
        return False

def test_get_all_researchers():
    """Test 2: Fetch All Researchers"""
    print("\n" + "=" * 60)
    print("TEST 2: Fetch All Researchers")
    print("=" * 60)
    
    try:
        researchers = get_all_researchers(db, limit=3)
        if researchers:
            print(f"✅ Found {len(researchers)} researchers")
            for r in researchers:
                print(f"   - {r['name']} ({r['institution']}) - {r['expertise']}")
            return researchers[0]['researcher_id'] if researchers else None
        else:
            print("❌ No researchers found")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_experiments_by_researcher(researcher_id):
    """Test 3: Fetch Experiments by Researcher"""
    print("\n" + "=" * 60)
    print("TEST 3: Fetch Experiments by Researcher")
    print("=" * 60)
    
    if not researcher_id:
        print("⚠️  Skipping - no researcher ID available")
        return None
    
    try:
        experiments = get_experiments_by_researcher(db, researcher_id)
        if experiments:
            print(f"✅ Found {len(experiments)} experiments")
            for e in experiments:
                print(f"   - {e['name']} (Status: {e['status']})")
            return experiments[0]['experiment_id'] if experiments else None
        else:
            print("⚠️  No experiments found for this researcher")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_experiment_details(experiment_id):
    """Test 4: Get Experiment Details"""
    print("\n" + "=" * 60)
    print("TEST 4: Get Experiment Details")
    print("=" * 60)
    
    if not experiment_id:
        print("⚠️  Skipping - no experiment ID available")
        return
    
    try:
        details = get_experiment_details(db, experiment_id)
        if details:
            print(f"✅ Retrieved experiment details")
            print(f"   Name: {details['name']}")
            print(f"   PI: {details['pi_name']}")
            print(f"   Devices: {len(details.get('devices', []))}")
            print(f"   Sessions: {len(details.get('sessions', []))}")
        else:
            print("❌ No details found")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_recent_analyses():
    """Test 5: Get Recent Analyses"""
    print("\n" + "=" * 60)
    print("TEST 5: Get Recent Analyses")
    print("=" * 60)
    
    try:
        analyses = get_recent_analyses(db, limit=5)
        if analyses:
            print(f"✅ Found {len(analyses)} recent analyses")
            for a in analyses:
                print(f"   - {a['analysis_type']} on {a['signal_type']} "
                      f"(Confidence: {a['confidence_score']:.2f})")
        else:
            print("⚠️  No analyses found")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_collaborations(researcher_id):
    """Test 6: Get Researcher Collaborations"""
    print("\n" + "=" * 60)
    print("TEST 6: Get Researcher Collaborations")
    print("=" * 60)
    
    if not researcher_id:
        print("⚠️  Skipping - no researcher ID available")
        return
    
    try:
        collabs = get_researcher_collaborations(db, researcher_id)
        if collabs:
            print(f"✅ Found {len(collabs)} collaborations")
            for c in collabs:
                print(f"   - With {c['collaborator_name']} "
                      f"({c['collaboration_type']})")
        else:
            print("⚠️  No collaborations found")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_signal_data(experiment_id):
    """Test 7: Get Signal Data by Experiment"""
    print("\n" + "=" * 60)
    print("TEST 7: Get Signal Data by Experiment")
    print("=" * 60)
    
    if not experiment_id:
        print("⚠️  Skipping - no experiment ID available")
        return
    
    try:
        signals = get_signal_data_by_experiment(db, experiment_id)
        if signals:
            print(f"✅ Found {len(signals)} signal recordings")
            for s in signals:
                print(f"   - {s['signal_type']} from {s['device_name']} "
                      f"({s['duration_seconds']:.1f}s)")
        else:
            print("⚠️  No signals found")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_all_tests():
    """Run all database tests"""
    print("\n🧪 NEUROHUB DATABASE TEST SUITE")
    print("Testing SQL-based queries on Spanner Standard Edition")
    
    # Test 1: Connection
    if not test_database_connection():
        print("\n❌ Stopping tests - database connection required")
        return
    
    # Test 2: Get researchers
    researcher_id = test_get_all_researchers()
    
    # Test 3: Get experiments
    experiment_id = test_get_experiments_by_researcher(researcher_id)
    
    # Test 4: Get experiment details
    test_get_experiment_details(experiment_id)
    
    # Test 5: Get recent analyses
    test_get_recent_analyses()
    
    # Test 6: Get collaborations
    test_get_collaborations(researcher_id)
    
    # Test 7: Get signal data
    test_get_signal_data(experiment_id)
    
    print("\n" + "=" * 60)
    print("✅ TEST SUITE COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    # Ensure environment is set up
    if not os.environ.get('GOOGLE_CLOUD_PROJECT'):
        print("⚠️  WARNING: GOOGLE_CLOUD_PROJECT not set")
        print("Run: source set_env.sh")
    
    run_all_tests()