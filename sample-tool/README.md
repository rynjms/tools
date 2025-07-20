# Sample Tool

A sample CLI tool that demonstrates the tool development paradigm for the Python CLI tools collection.

## Description

This tool processes files and outputs scores in the format `filename: score`. It serves as a template and example for creating new tools that follow the established paradigm.

## Installation

```bash
# Install in development mode
uv sync
uv run -m pip install -e .

# Or install directly
uv run -m pip install .
```

## Usage

### Basic Usage

```bash
# Process a single file
sample-tool file.txt

# Process multiple files
sample-tool file1.txt file2.txt file3.txt

# Pipeline usage
find . -name "*.txt" | sample-tool
```

### Command Line Options

- `-q, --quiet`: Quiet mode - output only exit code
- `-a, --algorithm`: Algorithm to use (default: size-based)
- `-v, --verbose`: Verbose output
- `-h, --help`: Show help message
- `--version`: Show version information

### Examples

```bash
# Standard output
$ sample-tool test.txt
/Users/rmoon/tools/sample-tool/test.txt: 0.125

# Quiet mode
$ sample-tool -q test.txt
$ echo $?
0

# Pipeline with find
$ find . -name "*.txt" | sample-tool
./file1.txt: 0.250
./file2.txt: 0.500
./file3.txt: 0.750

# Verbose mode
$ sample-tool -v test.txt
Processing: /Users/rmoon/tools/sample-tool/test.txt
File size: 125 bytes
Calculated score: 0.125
/Users/rmoon/tools/sample-tool/test.txt: 0.125
```

## Development

### Setup

```bash
# Create virtual environment
uv venv

# Install dependencies
uv sync

# Install in development mode
uv run -m pip install -e .
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=sample_tool

# Run specific test
uv run pytest tests/test_sample_tool.py::test_process_file
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Type checking
uv run mypy src/

# Linting
uv run flake8 src/ tests/
```

### Building

```bash
# Build package
uv build

# Install from build
uv run -m pip install dist/*.whl
```

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid input
- `3`: File not found
- `4`: Permission error

## Architecture

This tool follows the established paradigm:

- **Single Responsibility**: Processes files and outputs scores
- **Pipeline Compatible**: Works with stdin/stdout
- **Consistent Interface**: Standard argument patterns
- **Quiet Mode**: Supports silent operation
- **Full Paths**: Always displays complete file paths

## Contributing

When modifying this tool:

1. Follow the established paradigm
2. Maintain backward compatibility
3. Add tests for new features
4. Update documentation
5. Ensure pipeline compatibility
6. Test quiet mode functionality 