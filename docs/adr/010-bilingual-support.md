# ADR-010: Bilingual Dashboard Support

## Status
Accepted

## Context
The NeuroHub workshop is part of the BGU-Brown Summer School collaboration between Ben-Gurion University (Israel) and Brown University (USA). This international collaboration requires supporting both English and Hebrew languages to ensure accessibility for all participants.

Key considerations:
- Israeli students and researchers may prefer Hebrew interface
- International collaboration benefits from multilingual support
- Technical terms often remain in English even in Hebrew contexts
- RTL (Right-to-Left) support is essential for proper Hebrew display

## Decision
We will implement bilingual (English/Hebrew) support for the NeuroHub dashboard with:
1. Client-side language switching using JavaScript
2. Dual text elements with CSS-based visibility control
3. Proper RTL layout support for Hebrew
4. localStorage for persisting language preferences
5. No server-side changes required (all client-side)

## Implementation Details

### Technical Approach
```html
<!-- Dual language text pattern -->
<span class="en-text bilingual-text">English Text</span>
<span class="he-text bilingual-text">טקסט בעברית</span>
```

### CSS Classes
- `.lang-en` / `.lang-he`: Applied to body element
- `.en-text` / `.he-text`: Language-specific content
- `.bilingual-text`: Hidden by default, shown based on language

### JavaScript Functions
- `setLanguage(lang)`: Switches language and updates direction
- Saves preference to localStorage
- Updates Bootstrap directional classes dynamically

## Consequences

### Positive
- **Inclusive**: All workshop participants can use their preferred language
- **Professional**: Demonstrates commitment to international collaboration
- **Educational**: Helps cross-cultural learning
- **Lightweight**: No backend changes or additional dependencies
- **Extensible**: Pattern can be applied to other pages/components
- **Performance**: No server round-trips for language switching

### Negative
- **Maintenance**: Requires maintaining translations in templates
- **Coverage**: Initial implementation only covers dashboard
- **Static**: Dynamic content from database remains untranslated
- **Complexity**: Developers must remember to add both languages

### Neutral
- Technical terms (EEG, EMG, BCI) remain in English as is standard practice
- Time/date formatting follows browser locale settings
- Agent responses remain in their configured language

## Alternatives Considered

1. **Server-side i18n (Flask-Babel)**
   - Pros: Standard approach, separate translation files
   - Cons: Requires backend changes, more complex setup

2. **Client-side i18n library**
   - Pros: More features, JSON translation files
   - Cons: Additional dependency, overhead for simple use case

3. **Separate Hebrew templates**
   - Pros: Complete separation of concerns
   - Cons: Massive duplication, maintenance nightmare

## Future Enhancements

1. **Extended Coverage**
   - Apply pattern to all templates (researcher.html, experiment.html, etc.)
   - Translate agent responses based on user preference
   - Localize error messages and notifications

2. **Backend Integration**
   - Store language preference in user profile
   - Provide translated content from database
   - API responses in selected language

3. **Additional Languages**
   - Arabic (for broader Middle East inclusion)
   - Spanish (for Latin American collaborations)
   - Chinese (for Asian partnerships)

## Related ADRs
- ADR-001: Technology Stack Selection (Frontend considerations)
- ADR-006: Documentation and Codelab Structure (Multilingual docs)
- ADR-007: NeuroHub Ally Integration (Agent response language)
- ADR-009: Workshop Agent Pattern (Consider bilingual config)

## References
- [BGU-Brown Summer School](https://in.bgu.ac.il/en/summer/Pages/default.aspx)
- [W3C Internationalization Best Practices](https://www.w3.org/International/quicktips/)
- [Bootstrap RTL Documentation](https://getbootstrap.com/docs/5.0/getting-started/rtl/)

## Date
2024-01-23