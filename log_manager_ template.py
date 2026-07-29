import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from log_config import setup_logger

logger = setup_logger(__name__)


class LogManagerUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(LogManagerUI, self).__init__()
        
        # Load UI
        uic.loadUi('log_manager.ui', self)
        
        # Connect signals
        self.refreshButton.clicked.connect(self.refresh_logs)
        self.exportButton.clicked.connect(self.export_log)
        self.clearButton.clicked.connect(self.clear_log)
        self.logFileComboBox.currentIndexChanged.connect(self.load_log_content)
        self.filterLevelComboBox.currentTextChanged.connect(self.apply_filters)
        self.searchEdit.textChanged.connect(self.apply_filters)
        
        # Initialize
        self.refresh_logs()
        self.show()
    
    def refresh_logs(self):
        """Refresh the list of available log files"""
        try:
            self.logFileComboBox.clear()
            
            if not os.path.exists('logs'):
                os.makedirs('logs')
            
            log_files = [f for f in os.listdir('logs') if f.endswith('.log')]
            log_files.sort(reverse=True)  # Most recent first
            
            self.logFileComboBox.addItems(log_files)
            
            if log_files:
                self.load_log_content()
            
            logger.debug("Log files list refreshed")
            
        except Exception as e:
            logger.error("Failed to refresh log files: %s", str(e))
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to refresh log files: {str(e)}"
            )
    
    def load_log_content(self):
        """Load the content of the selected log file"""
        try:
            current_file = self.logFileComboBox.currentText()
            if not current_file:
                return
            
            file_path = os.path.join('logs', current_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                self.full_content = f.readlines()
            
            self.apply_filters()
            logger.debug("Log file content loaded: %s", current_file)
            
        except Exception as e:
            logger.error("Failed to load log content: %s", str(e))
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load log content: {str(e)}"
            )
    
    def apply_filters(self):
        """Apply level and search filters to log content"""
        try:
            if not hasattr(self, 'full_content'):
                return
            
            level_filter = self.filterLevelComboBox.currentText()
            search_text = self.searchEdit.text().lower()
            
            filtered_content = []
            for line in self.full_content:
                # Apply level filter
                if level_filter != "All" and level_filter not in line:
                    continue
                
                # Apply search filter
                if search_text and search_text not in line.lower():
                    continue
                
                filtered_content.append(line)
            
            self.logTextEdit.setPlainText(''.join(filtered_content))
            
        except Exception as e:
            logger.error("Failed to apply filters: %s", str(e))
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to apply filters: {str(e)}"
            )
    
    def export_log(self):
        """Export the current log file"""
        try:
            current_file = self.logFileComboBox.currentText()
            if not current_file:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "No log file selected"
                )
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Log",
                current_file,
                "Log Files (*.log);;All Files (*)"
            )
            
            if file_path:
                source_path = os.path.join('logs', current_file)
                with open(source_path, 'r', encoding='utf-8') as source:
                    content = source.read()
                    
                with open(file_path, 'w', encoding='utf-8') as target:
                    target.write(content)
                
                QMessageBox.information(
                    self,
                    "Success",
                    "Log file exported successfully"
                )
                logger.info("Log file exported to %s", file_path)
            
        except Exception as e:
            logger.error("Failed to export log: %s", str(e))
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to export log: {str(e)}"
            )
    
    def clear_log(self):
        """Clear the current log file"""
        try:
            current_file = self.logFileComboBox.currentText()
            if not current_file:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "No log file selected"
                )
                return
            
            reply = QMessageBox.question(
                self,
                "Confirm Clear",
                f"Are you sure you want to clear {current_file}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                file_path = os.path.join('logs', current_file)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('')
                
                self.load_log_content()
                QMessageBox.information(
                    self,
                    "Success",
                    "Log file cleared successfully"
                )
                logger.info("Log file cleared: %s", current_file)
            
        except Exception as e:
            logger.error("Failed to clear log: %s", str(e))
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to clear log: {str(e)}"
            )

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication([])
        window = LogManagerUI()
        app.exec_()
    except Exception as e:
        logger.critical("Failed to start Log Manager: %s", str(e))
        QMessageBox.critical(None, "Fatal Error", f"Failed to start Log Manager: {str(e)}")
        sys.exit(1)
