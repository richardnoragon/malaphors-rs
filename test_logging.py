import pytest
from unittest.mock import MagicMock, patch
import sys
import os
import unittest
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from log_manager import LogManager, QtHandler, log_message
import logging

@pytest.mark.logging
class TestLogManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up Qt application for all tests."""
        # Create a QApplication instance if it doesn't exist
        cls.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.log_manager = LogManager()
        self.log_manager.show()  # Need to show for Qt tests
        QTest.qWaitForWindowExposed(self.log_manager)

    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self, 'log_manager'):
            self.log_manager.close()
            self.log_manager.deleteLater()
        QTest.qWait(0)  # Process any pending events

    def test_log_message_info(self):
        """Test logging of info messages."""
        test_message = "Test info message"
        initial_text = self.log_manager.logTextEdit.toPlainText()
        log_message(test_message, logging.INFO)
        QTest.qWait(100)  # Wait for message to be processed
        final_text = self.log_manager.logTextEdit.toPlainText()
        self.assertGreater(len(final_text), len(initial_text))
        self.assertIn(test_message, final_text)

    def test_log_message_warning(self):
        """Test logging of warning messages."""
        test_message = "Test warning message"
        initial_text = self.log_manager.logTextEdit.toPlainText()
        log_message(test_message, logging.WARNING)
        QTest.qWait(100)
        final_text = self.log_manager.logTextEdit.toPlainText()
        self.assertGreater(len(final_text), len(initial_text))
        self.assertIn(test_message, final_text)

    def test_log_message_error(self):
        """Test logging of error messages."""
        test_message = "Test error message"
        initial_text = self.log_manager.logTextEdit.toPlainText()
        log_message(test_message, logging.ERROR)
        QTest.qWait(100)
        final_text = self.log_manager.logTextEdit.toPlainText()
        self.assertGreater(len(final_text), len(initial_text))
        self.assertIn(test_message, final_text)

    def test_clear_logs(self):
        """Test clearing of logs."""
        log_message("Test message before clear")
        QTest.qWait(100)
        self.assertNotEqual("", self.log_manager.logTextEdit.toPlainText())
        
        # Click clear button
        QTest.mouseClick(self.log_manager.clearButton, Qt.MouseButton.LeftButton)
        QTest.qWait(100)
        self.assertEqual("", self.log_manager.logTextEdit.toPlainText())

    def test_qt_handler(self):
        """Test the Qt logging handler."""
        test_record = logging.LogRecord(
            "test", logging.INFO, "", 0, "Test message", (), None
        )
        initial_text = self.log_manager.logTextEdit.toPlainText()
        self.log_manager.qt_handler.emit(test_record)
        QTest.qWait(100)
        final_text = self.log_manager.logTextEdit.toPlainText()
        self.assertGreater(len(final_text), len(initial_text))

    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName')
    def test_export_logs(self, mock_file_dialog):
        """Test exporting logs to a file."""
        test_file = "test_export.log"
        mock_file_dialog.return_value = (test_file, "")
        
        # Add some logs to export
        log_message("Test export message")
        QTest.qWait(100)
        
        # Click export button
        QTest.mouseClick(self.log_manager.exportButton, Qt.MouseButton.LeftButton)
        QTest.qWait(100)
        
        # Verify file was written
        self.assertTrue(os.path.exists(test_file))
        with open(test_file, 'r') as f:
            content = f.read()
        self.assertIn("Test export message", content)
        
        # Clean up
        try:
            os.remove(test_file)
        except:
            pass

    def test_log_message_formatting(self):
        """Test log message formatting."""
        test_message = "Test formatting"
        initial_text = self.log_manager.logTextEdit.toPlainText()
        log_message(test_message, logging.INFO)
        QTest.qWait(100)
        final_text = self.log_manager.logTextEdit.toPlainText()
        self.assertGreater(len(final_text), len(initial_text))
        self.assertIn(test_message, final_text)
        self.assertIn("[INFO]", final_text)

    @classmethod
    def tearDownClass(cls):
        """Clean up Qt application."""
        QTest.qWait(100)  # Final event processing

if __name__ == '__main__':
    unittest.main()