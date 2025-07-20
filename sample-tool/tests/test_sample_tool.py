"""
Tests for the sample tool.
"""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sample_tool.core import process_file, process_files


class TestProcessFile(unittest.TestCase):
    """Test the process_file function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"
        
        # Create a test file with known content
        with open(self.test_file, 'w') as f:
            f.write("This is a test file.\nIt has multiple lines.\nAnd some words.")
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_process_file_size_algorithm(self):
        """Test processing file with size algorithm."""
        score = process_file(str(self.test_file), "size")
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_process_file_lines_algorithm(self):
        """Test processing file with lines algorithm."""
        score = process_file(str(self.test_file), "lines")
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_process_file_words_algorithm(self):
        """Test processing file with words algorithm."""
        score = process_file(str(self.test_file), "words")
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_process_file_invalid_algorithm(self):
        """Test processing file with invalid algorithm."""
        with self.assertRaises(ValueError):
            process_file(str(self.test_file), "invalid")
    
    def test_process_file_not_found(self):
        """Test processing non-existent file."""
        with self.assertRaises(FileNotFoundError):
            process_file("nonexistent.txt")
    
    def test_process_file_directory(self):
        """Test processing a directory."""
        with self.assertRaises(ValueError):
            process_file(self.temp_dir)
    
    def test_process_file_binary_fallback(self):
        """Test processing binary file falls back to size algorithm."""
        binary_file = Path(self.temp_dir) / "binary.bin"
        with open(binary_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03')
        
        # Should not raise UnicodeDecodeError
        score = process_file(str(binary_file), "lines")
        self.assertIsInstance(score, float)


class TestProcessFiles(unittest.TestCase):
    """Test the process_files function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_files = []
        
        # Create multiple test files
        for i in range(3):
            test_file = Path(self.temp_dir) / f"test{i}.txt"
            with open(test_file, 'w') as f:
                f.write(f"This is test file {i}.\n" * (i + 1))
            self.test_files.append(str(test_file))
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_process_files_success(self):
        """Test processing multiple files successfully."""
        results = process_files(self.test_files)
        self.assertEqual(len(results), 3)
        
        for filename, score in results:
            self.assertIsInstance(filename, str)
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
    
    def test_process_files_quiet_mode(self):
        """Test processing files in quiet mode."""
        with patch('sys.stdout') as mock_stdout:
            results = process_files(self.test_files, quiet=True)
            mock_stdout.write.assert_not_called()
        
        self.assertEqual(len(results), 3)
    
    def test_process_files_verbose_mode(self):
        """Test processing files in verbose mode."""
        with patch('sys.stderr') as mock_stderr:
            results = process_files(self.test_files, verbose=True)
            # Should have called stderr for each file
            self.assertGreater(mock_stderr.write.call_count, 0)
        
        self.assertEqual(len(results), 3)
    
    def test_process_files_with_errors(self):
        """Test processing files with some errors."""
        files_with_errors = self.test_files + ["nonexistent.txt"]
        results = process_files(files_with_errors)
        
        # Should process valid files and skip invalid ones
        self.assertEqual(len(results), 3)
    
    def test_process_files_all_errors(self):
        """Test processing files with all errors."""
        results = process_files(["nonexistent1.txt", "nonexistent2.txt"])
        self.assertEqual(len(results), 0)
    
    def test_process_files_different_algorithms(self):
        """Test processing files with different algorithms."""
        algorithms = ["size", "lines", "words"]
        
        for algorithm in algorithms:
            results = process_files(self.test_files, algorithm=algorithm)
            self.assertEqual(len(results), 3)
            
            for filename, score in results:
                self.assertIsInstance(score, float)
                self.assertGreaterEqual(score, 0.0)
                self.assertLessEqual(score, 1.0)


class TestCLI(unittest.TestCase):
    """Test the command-line interface."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"
        
        with open(self.test_file, 'w') as f:
            f.write("This is a test file.")
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @patch('sys.argv', ['sample-tool', '--help'])
    def test_cli_help(self):
        """Test CLI help output."""
        from sample_tool.cli import main
        
        with patch('sys.stdout') as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)
    
    @patch('sys.argv', ['sample-tool', '--version'])
    def test_cli_version(self):
        """Test CLI version output."""
        from sample_tool.cli import main
        
        with patch('sys.stdout') as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)
    
    @patch('sys.argv', ['sample-tool', 'nonexistent.txt'])
    def test_cli_file_not_found(self):
        """Test CLI with non-existent file."""
        from sample_tool.cli import main
        
        with patch('sys.stderr') as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main() 