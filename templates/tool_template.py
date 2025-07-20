#!/usr/bin/env python3
"""
Tool Template - Replace with actual tool name and description

This template follows the established paradigm for CLI tools in this collection.
"""
import argparse
import sys
from typing import List, Optional, Tuple
from pathlib import Path


def process_file(file_path: str) -> float:
    """
    Process a single file and return a score.
    
    Args:
        file_path: Path to the file to process
        
    Returns:
        float: Score for the file (0.0 to 1.0)
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If the file can't be read
    """
    # TODO: Implement your tool-specific logic here
    # This is where you'd add your actual processing code
    
    # Example placeholder logic
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")
    
    # Placeholder: return a dummy score based on file size
    size = path.stat().st_size
    return min(1.0, size / 1000.0)  # Score based on file size


def process_files(files: List[str], quiet: bool = False) -> List[Tuple[str, float]]:
    """
    Process multiple files and return results.
    
    Args:
        files: List of file paths to process
        quiet: If True, suppress output
        
    Returns:
        List of (filename, score) tuples
    """
    results = []
    
    for file_path in files:
        try:
            score = process_file(file_path)
            results.append((file_path, score))
            
            if not quiet:
                print(f"{file_path}: {score:.3f}")
                
        except (FileNotFoundError, PermissionError) as e:
            if not quiet:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)
            continue
        except Exception as e:
            if not quiet:
                print(f"Unexpected error processing {file_path}: {e}", file=sys.stderr)
            continue
    
    return results


def main():
    """Main entry point for the tool."""
    parser = argparse.ArgumentParser(
        description="Tool Template - Replace with actual description",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file.txt
  %(prog)s file1.txt file2.txt
  %(prog)s -q file.txt  # Quiet mode
  find . -name "*.txt" | %(prog)s  # Pipeline usage
        """
    )
    
    # Standard arguments
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode - output only exit code'
    )
    parser.add_argument(
        '-a', '--algorithm',
        help='Algorithm to use (tool-specific)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0'
    )
    
    # File arguments
    parser.add_argument(
        'files',
        nargs='+',
        help='Files to process'
    )
    
    args = parser.parse_args()
    
    # Process files
    try:
        results = process_files(args.files, args.quiet)
        
        # Exit with appropriate code
        if args.quiet:
            # In quiet mode, exit 0 if any files processed successfully
            sys.exit(0 if results else 1)
        else:
            # In normal mode, exit 0 if all files processed
            sys.exit(0 if len(results) == len(args.files) else 1)
            
    except KeyboardInterrupt:
        if not args.quiet:
            print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        if not args.quiet:
            print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 