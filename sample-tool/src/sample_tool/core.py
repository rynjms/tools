"""
Core processing logic for the sample tool.
"""
import sys
from pathlib import Path
from typing import List, Tuple


def process_file(file_path: str, algorithm: str = "size") -> float:
    """
    Process a single file and return a score.
    
    Args:
        file_path: Path to the file to process
        algorithm: Algorithm to use for scoring (default: "size")
        
    Returns:
        float: Score for the file (0.0 to 1.0)
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If the file can't be read
        ValueError: If the algorithm is not supported
    """
    path = Path(file_path)
    
    # Validate file exists and is readable
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")
    
    if not path.is_readable():
        raise PermissionError(f"Cannot read file: {file_path}")
    
    # Process based on algorithm
    if algorithm == "size":
        return _score_by_size(path)
    elif algorithm == "lines":
        return _score_by_lines(path)
    elif algorithm == "words":
        return _score_by_words(path)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def process_files(
    files: List[str], 
    quiet: bool = False, 
    algorithm: str = "size",
    verbose: bool = False
) -> List[Tuple[str, float]]:
    """
    Process multiple files and return results.
    
    Args:
        files: List of file paths to process
        quiet: If True, suppress output
        algorithm: Algorithm to use for scoring
        verbose: If True, show detailed processing info
        
    Returns:
        List of (filename, score) tuples
    """
    results = []
    
    for file_path in files:
        try:
            if verbose and not quiet:
                print(f"Processing: {file_path}", file=sys.stderr)
            
            score = process_file(file_path, algorithm)
            results.append((file_path, score))
            
            if not quiet:
                print(f"{file_path}: {score:.3f}")
                
        except (FileNotFoundError, PermissionError, ValueError) as e:
            if not quiet:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)
            continue
        except Exception as e:
            if not quiet:
                print(f"Unexpected error processing {file_path}: {e}", file=sys.stderr)
            continue
    
    return results


def _score_by_size(path: Path) -> float:
    """Score file based on size (0.0 to 1.0)."""
    size = path.stat().st_size
    # Normalize to 0-1 range (1KB = 1.0)
    return min(1.0, size / 1024.0)


def _score_by_lines(path: Path) -> float:
    """Score file based on number of lines (0.0 to 1.0)."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        # Normalize to 0-1 range (100 lines = 1.0)
        return min(1.0, line_count / 100.0)
    except UnicodeDecodeError:
        # If file is binary, fall back to size-based scoring
        return _score_by_size(path)


def _score_by_words(path: Path) -> float:
    """Score file based on number of words (0.0 to 1.0)."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            word_count = len(content.split())
        # Normalize to 0-1 range (500 words = 1.0)
        return min(1.0, word_count / 500.0)
    except UnicodeDecodeError:
        # If file is binary, fall back to size-based scoring
        return _score_by_size(path) 