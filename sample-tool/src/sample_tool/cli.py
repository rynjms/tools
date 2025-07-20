"""
Command-line interface for the sample tool.
"""
import sys
from typing import List

from .core import process_files


def main() -> None:
    """
    Main entry point for the sample tool CLI.
    
    Processes files and outputs scores in the format 'filename: score'.
    Supports quiet mode, verbose output, and different algorithms.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Sample Tool - Process files and output scores",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file.txt
  %(prog)s file1.txt file2.txt
  %(prog)s -q file.txt  # Quiet mode
  %(prog)s -a lines file.txt  # Use lines algorithm
  find . -name "*.txt" | %(prog)s  # Pipeline usage
        """
    )
    
    # Standard arguments following the paradigm
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode - output only exit code'
    )
    parser.add_argument(
        '-a', '--algorithm',
        choices=['size', 'lines', 'words'],
        default='size',
        help='Algorithm to use for scoring (default: size)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    # File arguments
    parser.add_argument(
        'files',
        nargs='*',
        help='Files to process (if none provided, read from stdin)'
    )
    
    args = parser.parse_args()
    
    # Get files to process
    files = _get_files_to_process(args.files)
    
    if not files:
        if not args.quiet:
            print("No files to process", file=sys.stderr)
        sys.exit(1)
    
    # Process files
    try:
        results = process_files(
            files=files,
            quiet=args.quiet,
            algorithm=args.algorithm,
            verbose=args.verbose
        )
        
        # Determine exit code
        if args.quiet:
            # In quiet mode, exit 0 if any files processed successfully
            sys.exit(0 if results else 1)
        else:
            # In normal mode, exit 0 if all files processed
            sys.exit(0 if len(results) == len(files) else 1)
            
    except KeyboardInterrupt:
        if not args.quiet:
            print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        if not args.quiet:
            print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def _get_files_to_process(files: List[str]) -> List[str]:
    """
    Get list of files to process from arguments or stdin.
    
    Args:
        files: List of files from command line arguments
        
    Returns:
        List of file paths to process
    """
    if files:
        return files
    
    # Read from stdin if no files provided
    if not sys.stdin.isatty():
        return [line.strip() for line in sys.stdin if line.strip()]
    
    return []


if __name__ == "__main__":
    main() 