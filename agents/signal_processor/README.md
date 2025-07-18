# Signal Processor Agent

## Purpose

The Signal Processor Agent analyzes biosignal data (EEG, EMG, ECG) to extract meaningful features, detect artifacts, and assess signal quality for neurotechnology research.

**Agent Type:** LoopAgent with sub-agents  
**A2A Port:** 8003  
**Status:** Production

## Capabilities

This agent can:
- Analyze EEG signals for frequency bands (alpha, beta, gamma)
- Detect and mark artifacts in biosignals
- Calculate signal quality metrics (SNR, impedance)
- Extract features for BCI applications
- Process multi-channel recordings

## Architecture

### Sub-Agents

1. **Quality Checker**: Validates signal integrity
2. **Artifact Detector**: Identifies noise and artifacts
3. **Feature Extractor**: Computes relevant signal features

### Integration Points

- **MCP Tools Used**: 
  - `create_analysis_report` - Store analysis results
  - `create_session_log` - Log processing sessions
- **External Services**: None
- **Dependencies**: SciPy for signal processing (see ADR-001)

## Running the Agent

### Local Development

```bash
cd agents/signal_processor
uv pip install -r requirements.txt
uv pip install ../a2a_common-0.1.0-py3-none-any.whl

# Run the A2A server
python a2a_server.py
```

The agent will be available at `http://localhost:8003`

### Testing

```bash
# Create test signal data
python -c "import numpy as np; np.save('test_eeg.npy', np.random.randn(256*10))"

# Test via curl
curl -X POST http://localhost:8003/process \
  -H "Content-Type: application/json" \
  -d '{"signal_file": "test_eeg.npy", "sampling_rate": 256}'
```

## Usage Examples

### Analyzing EEG Data

```json
{
  "task": "analyze_biosignal",
  "parameters": {
    "signal_type": "EEG",
    "sampling_rate": 256,
    "channels": ["Fp1", "Fp2", "C3", "C4"],
    "analysis_window": 10
  }
}
```

### Expected Response

```json
{
  "status": "success",
  "result": {
    "quality_score": 85,
    "artifacts_detected": ["eye_blink", "muscle"],
    "frequency_bands": {
      "alpha": {"power": 45.2, "peak_freq": 10.5},
      "beta": {"power": 32.1, "peak_freq": 18.2}
    },
    "recommendations": ["Remove eye blink artifacts", "Good for BCI"]
  }
}
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `A2A_PORT` | Port for A2A server | 8003 |
| `MCP_SERVER_URL` | MCP server endpoint | http://localhost:8001 |
| `MAX_SIGNAL_LENGTH` | Maximum samples to process | 1000000 |
| `LOG_LEVEL` | Logging verbosity | INFO |

## Performance Notes

- Processes 10 seconds of 256Hz EEG in ~2 seconds
- Memory usage scales with signal length
- Supports batch processing for multiple channels

## Troubleshooting

### "Signal too noisy" error
- Check electrode impedance
- Verify sampling rate is correct
- Ensure proper grounding

### Memory errors with large files
- Process in chunks using the `analysis_window` parameter
- Reduce number of simultaneous channels

## Related Documentation

- [ADR-001: SciPy for Signal Processing](../../docs/adr/ADR-001-signal-processing-library.md)
- [Signal Processing Best Practices](../../docs/signal-processing-guide.md)