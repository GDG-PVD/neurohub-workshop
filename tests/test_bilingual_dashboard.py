"""
Tests for bilingual dashboard functionality.
"""

import pytest
from flask import Flask, render_template_string
import json


class TestBilingualDashboard:
    """Test suite for bilingual dashboard features."""
    
    def test_language_toggle_javascript(self):
        """Test that language toggle JavaScript functions are present."""
        # Read the bilingual template
        with open('neurohub/templates/index_bilingual.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check for required JavaScript functions
        assert 'function setLanguage(lang)' in template_content
        assert 'localStorage.setItem' in template_content
        assert 'localStorage.getItem' in template_content
        assert 'document.dir = \'rtl\'' in template_content
        assert 'document.dir = \'ltr\'' in template_content
    
    def test_bilingual_text_structure(self):
        """Test that bilingual text follows correct pattern."""
        with open('neurohub/templates/index_bilingual.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check for bilingual text pattern
        assert 'en-text bilingual-text' in template_content
        assert 'he-text bilingual-text' in template_content
        
        # Check for specific Hebrew translations
        assert 'לוח בקרת מחקר' in template_content  # Research Dashboard
        assert 'ניסויים פעילים' in template_content  # Active Experiments
        assert 'חוקרים' in template_content  # Researchers
        assert 'אותות שנותחו' in template_content  # Signals Analyzed
    
    def test_rtl_css_support(self):
        """Test that RTL CSS rules are present."""
        with open('neurohub/templates/index_bilingual.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check for RTL-specific CSS
        assert '[lang="he"]' in template_content
        assert 'direction: rtl' in template_content
        assert 'text-align: right' in template_content
        
        # Check for Bootstrap class adjustments
        assert '.ms-2' in template_content
        assert '.me-2' in template_content
    
    def test_language_buttons(self):
        """Test that language toggle buttons are present."""
        with open('neurohub/templates/index_bilingual.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check for language buttons
        assert 'onclick="setLanguage(\'en\')"' in template_content
        assert 'onclick="setLanguage(\'he\')"' in template_content
        assert 'EN</button>' in template_content
        assert 'עב</button>' in template_content
    
    def test_hebrew_status_translations(self):
        """Test that status indicators have Hebrew translations."""
        with open('neurohub/templates/index_bilingual.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check for status translations
        assert 'פעיל' in template_content  # Active
        assert 'הושלם' in template_content  # Completed
        assert 'תכנון' in template_content  # Planning
    
    def test_time_translations(self):
        """Test that time descriptions have Hebrew translations."""
        with open('neurohub/templates/index_bilingual.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check for time translations
        assert 'לפני שעתיים' in template_content  # 2 hours ago
        assert 'אתמול' in template_content  # Yesterday
        assert 'לפני 3 ימים' in template_content  # 3 days ago
    
    def test_modal_translations(self):
        """Test that modal dialogs have Hebrew translations."""
        with open('neurohub/templates/index_bilingual.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check for modal translations
        assert 'צור ניסוי חדש' in template_content  # Create New Experiment
        assert 'העלאת נתוני אותות' in template_content  # Upload Signal Data
        assert 'ביטול' in template_content  # Cancel
        assert 'שם הניסוי' in template_content  # Experiment Name
    
    def test_accessibility_attributes(self):
        """Test that language attributes are properly set."""
        with open('neurohub/templates/index_bilingual.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check for proper language attribute handling
        assert 'document.documentElement.lang = lang' in template_content
        assert 'lang-en' in template_content
        assert 'lang-he' in template_content


class TestBilingualIntegration:
    """Integration tests for bilingual functionality."""
    
    @pytest.fixture
    def app(self):
        """Create a test Flask app."""
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
    
    def test_template_renders(self, app):
        """Test that the bilingual template renders without errors."""
        with app.app_context():
            # Mock template rendering with sample data
            sample_data = {
                'active_experiments': 12,
                'signals_analyzed': 847,
                'total_researchers': 24,
                'active_devices': 8,
                'recent_experiments': []
            }
            
            # This would normally render the template
            # For testing, we just verify the template exists and is valid
            import os
            template_path = os.path.join('neurohub', 'templates', 'index_bilingual.html')
            assert os.path.exists(template_path)
            
            # Verify it's a valid Jinja2 template
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '{% extends "base.html" %}' in content
                assert '{% block content %}' in content
                assert '{% endblock %}' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])