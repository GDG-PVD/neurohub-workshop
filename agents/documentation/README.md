# Documentation Agent

## Purpose

The Documentation Agent generates comprehensive research reports, experiment summaries, and formatted findings for neurotechnology research projects.

**Agent Type:** LlmAgent  
**A2A Port:** 8002  
**Status:** Production

## Capabilities

This agent can:
- Generate structured research reports
- Create experiment documentation
- Format findings for publication
- Export data in various formats (PDF, Markdown, LaTeX)
- Summarize complex analysis results

## Architecture

### Integration Points

- **MCP Tools Used**: 
  - `export_findings` - Save formatted reports
  - `create_analysis_report` - Document analysis results
- **External Services**: None
- **Database Access**: Read-only access to experiments and analyses

## Running the Agent

### Local Development

```bash
cd agents/documentation
uv pip install -r requirements.txt
uv pip install ../a2a_common-0.1.0-py3-none-any.whl

# Run the A2A server
python a2a_server.py
```

The agent will be available at `http://localhost:8002`

### Testing

```bash
# Run the test client
python neurohub_test_client.py

# Test specific documentation task
curl -X POST http://localhost:8002/generate \
  -H "Content-Type: application/json" \
  -d '{"task": "create_experiment_report", "experiment_id": "EXP001"}'
```

## Usage Examples

### Generate Experiment Report

```json
{
  "task": "generate_experiment_report",
  "parameters": {
    "experiment_id": "EXP001",
    "include_sections": ["methodology", "results", "discussion"],
    "format": "markdown"
  }
}
```

### Create Analysis Summary

```json
{
  "task": "summarize_analysis",
  "parameters": {
    "analysis_ids": ["AN001", "AN002"],
    "detail_level": "high",
    "include_visualizations": true
  }
}
```

### Expected Response

```json
{
  "status": "success",
  "result": {
    "document_id": "DOC_20240718_001",
    "format": "markdown",
    "sections": {
      "title": "EEG Analysis of Attention Task",
      "abstract": "This study examined...",
      "methodology": "Participants performed...",
      "results": "Significant changes in alpha band..."
    },
    "export_path": "/exports/EXP001_report.md"
  }
}
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `A2A_PORT` | Port for A2A server | 8002 |
| `MCP_SERVER_URL` | MCP server endpoint | http://localhost:8001 |
| `EXPORT_FORMAT` | Default export format | markdown |
| `TEMPLATE_DIR` | Report templates location | ./templates |

## Document Templates

The agent uses customizable templates for different report types:
- `experiment_report.md` - Full experiment documentation
- `analysis_summary.md` - Concise analysis results
- `publication_draft.md` - Journal-ready format

## Performance Notes

- Generates typical report in 5-10 seconds
- Can process multiple experiments concurrently
- Caches frequently used data

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `ExperimentNotFound` | Invalid experiment ID | Verify ID exists |
| `TemplateError` | Missing template file | Check template directory |
| `ExportFailed` | Permissions issue | Verify write access |

## Best Practices

1. Always specify the desired format explicitly
2. Use `detail_level` to control report length
3. Include metadata for better organization
4. Review generated content before publication

## Related Documentation

- [Documentation Standards](../../docs/documentation-standards.md)
- [Report Templates Guide](../../docs/templates/report-guide.md)
- [Export Formats](../../docs/export-formats.md)