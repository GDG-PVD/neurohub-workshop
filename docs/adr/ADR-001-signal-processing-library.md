# ADR-001: Use SciPy for Biosignal Processing

**Date:** 2024-07-01

**Status:** Accepted

**Deciders:** Workshop instructors, with input from neuroscience researchers

**Tags:** architecture, signal-processing, dependencies

## Context

The NeuroHub platform needs to process various biosignals (EEG, EMG, ECG) for research purposes. We need reliable algorithms for:
- Signal filtering (bandpass, notch filters)
- Feature extraction (power spectral density, peak detection)
- Artifact detection and removal
- Time-frequency analysis

The decision impacts the signal_processor agent and any future analysis capabilities.

## Decision

We will use SciPy (specifically scipy.signal) as our primary signal processing library, supplemented by NumPy for array operations.

## Considered Options

1. **SciPy + NumPy**: Established scientific computing libraries
   - Pros: 
     - Well-tested, peer-reviewed implementations
     - Extensive documentation and community support
     - Integrates well with other scientific Python tools
     - No licensing costs
   - Cons: 
     - Additional dependency (180MB)
     - May be overkill for simple operations

2. **Custom implementations**: Build our own signal processing functions
   - Pros: 
     - No external dependencies
     - Tailored exactly to our needs
     - Full control over algorithms
   - Cons: 
     - Time-consuming to implement correctly
     - Risk of bugs in critical algorithms
     - Need to maintain and test extensively
     - Reinventing well-solved problems

3. **MNE-Python**: Specialized neuroscience toolbox
   - Pros: 
     - Purpose-built for EEG/MEG analysis
     - High-level functions for neuroscience
   - Cons: 
     - Much larger dependency (>1GB)
     - May be too specialized for our educational focus
     - Steeper learning curve for students

## Consequences

### Positive
- Students learn industry-standard tools
- Reliable, tested algorithms for critical analysis
- Rich ecosystem of compatible tools
- Good documentation for self-learning

### Negative
- Increases project dependencies
- Students must learn SciPy API
- Potential version compatibility issues

### Neutral
- Commits us to Python's scientific stack
- May influence choice of other libraries

## Implementation Notes

Standard imports for signal processing modules:

```python
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from scipy.signal import butter, filtfilt, find_peaks

# Example: Bandpass filter for EEG
def bandpass_filter(data, lowcut=0.5, highcut=50.0, fs=256, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)
```

## References

- [SciPy Signal Processing Tutorial](https://docs.scipy.org/doc/scipy/tutorial/signal.html)
- [ADR-002: Python Version Requirements](ADR-002-python-version.md)
- Research paper: "Best Practices in EEG Processing" (example reference)

## Notes

This decision was made with AI assistance to evaluate the trade-offs between different libraries. The final decision was validated by reviewing actual implementation requirements in the workshop.