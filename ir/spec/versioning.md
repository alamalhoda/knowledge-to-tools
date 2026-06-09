# Aegis IR Specification v1 — Versioning

## IR Version Policy

### Version Format

IR versions use semantic versioning: `MAJOR.MINOR`

- **MAJOR**: Structural changes that break backward compatibility.
- **MINOR**: Additive changes that maintain backward compatibility.

### Current Version

```
IR_VERSION = "2.0"
SUPPORTED_VERSIONS = ["1.0", "2.0"]
```

### Version Metadata

Every IR artifact includes:

```json
{
  "version": "2.0",
  "generated_at": "2026-06-09T23:11:26Z",
  "source_hash": "sha256:..."
}
```

### Compatibility Rules

1. Compilers must support all versions in `SUPPORTED_VERSIONS`.
2. Emitters must declare the minimum IR version they support.
3. When an unsupported version is encountered:
   - Compiler: raise `UnsupportedIRVersionError`
   - Emitter: raise `UnsupportedIRVersionError`
   - Pipeline: skip the artifact and log a warning

### Migration Policy

1. **Minor version increments** (e.g., 2.0 → 2.1):
   - New optional fields may be added.
   - New node types may be added.
   - Existing fields must not be removed or redefined.

2. **Major version increments** (e.g., 2.0 → 3.0):
   - Require migration documentation.
   - Require compatibility assessment.
   - May remove or redefine existing fields.
   - Require new emitter contracts.

### Stability Commitment

- Once an IR version is released, its core structure is frozen.
- Bug fixes may add new optional fields but cannot change required fields.
- Deprecated fields are marked with `deprecated: true` and removed only in the next major version.

### Version Checking

```python
from .version import IR_VERSION, SUPPORTED_VERSIONS, check_version

def check_version(version: str) -> bool:
    """Check if an IR version is supported."""
    return version in SUPPORTED_VERSIONS
```
