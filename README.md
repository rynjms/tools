# Python CLI Tools Collection

A collection of focused, single-purpose Python command-line tools designed for UNIX pipeline compatibility.

## Development Paradigm

### Core Principles
- **Single Responsibility**: Each tool does ONE specific task well
- **Pipeline Compatible**: Tools work seamlessly in UNIX pipelines
- **Consistent Interface**: Standard argument patterns across all tools
- **Quiet Mode**: Support for silent operation with exit codes only
- **Full Paths**: Always preserve and display full file paths

### Standard Tool Structure

Every tool follows this basic structure:

```python
#!/usr/bin/env python3
"""
Tool Name - Brief description
"""
import argparse
import sys
from typing import Optional, List

def process_files(files: List[str], quiet: bool = False) -> bool:
    """Process files and return success status."""
    # Tool-specific logic here
    pass

def main():
    parser = argparse.ArgumentParser(description="Tool description")
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    parser.add_argument('-a', '--algorithm', help='Algorithm to use')
    parser.add_argument('files', nargs='+', help='Files to process')
    args = parser.parse_args()
    
    success = process_files(args.files, args.quiet)
    
    if args.quiet:
        sys.exit(0 if success else 1)
    
    # Output in 'filename: score' format
    for filename, score in results:
        print(f"{filename}: {score}")

if __name__ == "__main__":
    main()
```

### Required Patterns

#### Command Line Interface
- Use `argparse` for argument parsing
- Support `-q/--quiet` for silent operation
- Support `-a` as shortcut for `--algorithm`
- Accept file arguments (positional or via `-f/--files`)
- Provide `-h/--help` and `--version`

#### Output Format
- Default: `filename: score`
- JSON: `{"filename": "path", "score": value}`
- CSV: `filename,score`
- Quiet: No output, exit code only

#### Exit Codes
- `0`: Success
- `1`: General error
- `2`: Invalid input
- `3`: File not found
- `4`: Permission error

#### Environment
- Always use `.venv/bin/python` interpreter
- Use type hints throughout
- Follow PEP 8 style guidelines
- Include comprehensive docstrings

### File Organization

```
tools/
├── core/           # Shared utilities
├── config/         # Configuration files
├── templates/      # Tool templates
├── tests/          # Test files
├── tool1/          # Individual tool directories
├── tool2/
└── README.md
```

### Development Workflow

1. **Create New Tool**:
   ```bash
   mkdir new-tool
   cp templates/tool_template.py new-tool/main.py
   chmod +x new-tool/main.py
   ```

2. **Run Tool**:
   ```bash
   .venv/bin/python tool/main.py [args]
   ```

3. **Test Pipeline Compatibility**:
   ```bash
   find . -name "*.txt" | .venv/bin/python tool/main.py
   ```

### Examples

#### Basic Usage
```bash
# Process single file
.venv/bin/python tool/main.py file.txt

# Process multiple files
.venv/bin/python tool/main.py file1.txt file2.txt

# Quiet mode
.venv/bin/python tool/main.py -q file.txt

# Pipeline usage
find . -name "*.txt" | .venv/bin/python tool/main.py
```

#### Output Examples
```
# Standard output
/path/to/file.txt: 0.85
/another/path/file.txt: 0.72

# JSON output
{"filename": "/path/to/file.txt", "score": 0.85}

# Quiet mode (no output, exit code only)
echo $?  # 0 for success, 1 for failure
```

## Contributing

When adding new tools:
1. Follow the established paradigm
2. Use the template structure
3. Include comprehensive tests
4. Document any deviations from standard patterns
5. Ensure pipeline compatibility
6. Test quiet mode functionality 