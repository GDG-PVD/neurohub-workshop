# Bilingual Dashboard Implementation Guide

## Overview

I've created a bilingual (English/Hebrew) version of the NeuroHub dashboard that's perfect for the BGU-Brown collaboration. The implementation is designed to be:
- Easy to toggle between languages
- Properly handle RTL (Right-to-Left) text for Hebrew
- Maintain all functionality in both languages
- Remember user's language preference

## Key Features

### 1. Language Toggle
- Simple EN/עב buttons in the top-right corner
- Instant switching without page reload
- Saves preference to localStorage

### 2. Dual Text Support
```html
<span class="en-text bilingual-text">English Text</span>
<span class="he-text bilingual-text">טקסט בעברית</span>
```

### 3. RTL Support
- Automatic direction switching
- Bootstrap class adjustments (ms-2 ↔ me-2)
- Proper alignment for all elements

### 4. Translated Elements
- Headers and titles
- Button labels
- Table columns
- Status indicators
- Time descriptions (e.g., "2 hours ago" → "לפני שעתיים")
- Modal dialogs

## Implementation Steps

### 1. Update Routes
To use the bilingual template, update your Flask route:

```python
# In neurohub_routes.py
@app.route('/')
def index():
    return render_template('index_bilingual.html', 
                         active_experiments=12,
                         signals_analyzed=847,
                         total_researchers=24,
                         active_devices=8)
```

### 2. Enable in Production
Simply rename or copy:
```bash
cd neurohub/templates
cp index_bilingual.html index.html
```

### 3. Extend to Other Pages
The same pattern can be applied to other templates:
- researcher.html
- experiment.html
- neurohub_ally.html

## Technical Implementation

### CSS Classes
- `.lang-en` / `.lang-he`: Applied to body for language-specific styling
- `.en-text` / `.he-text`: Show/hide based on selected language
- `.bilingual-text`: Hidden by default, shown based on language

### JavaScript Functions
- `setLanguage(lang)`: Switches language and updates direction
- Saves preference to localStorage
- Updates Bootstrap directional classes

### RTL Considerations
- Hebrew text automatically gets `direction: rtl`
- Margin and padding classes are swapped
- Float directions are reversed
- Text alignment is adjusted

## Benefits for BGU-Brown Workshop

1. **Inclusivity**: Israeli students can use their native language
2. **Learning**: English speakers can see Hebrew translations
3. **Professional**: Shows attention to international collaboration
4. **Practical**: Useful for presenting to Hebrew-speaking stakeholders

## Future Enhancements

1. **Backend Integration**
   - Store language preference in user profile
   - Translate dynamic content from database
   - API responses in selected language

2. **Extended Coverage**
   - Agent responses in both languages
   - Error messages and notifications
   - Help documentation

3. **Additional Languages**
   - Easy to extend pattern for more languages
   - Could add Arabic, Spanish, etc.

## Usage Example

```javascript
// Check current language
const currentLang = document.documentElement.lang;

// Programmatically change language
setLanguage('he'); // Switch to Hebrew
setLanguage('en'); // Switch to English

// Get saved preference
const userLang = localStorage.getItem('preferred-language') || 'en';
```

## Notes

- Hebrew translations are contextually appropriate for neurotechnology
- Technical terms (EEG, EMG, etc.) remain in English as is standard
- Time formats follow local conventions
- The implementation is lightweight and doesn't require additional libraries

This bilingual support demonstrates the international nature of the workshop and makes the platform more accessible to all participants!