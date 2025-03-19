import os
import webbrowser

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from MidtermBonus.DataProcessor import DataProcessor
from MidtermBonus.MainWindow import Ui_MainWindow


class MainWindowEx(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.excel_file_path = None
        self.output_html_path = None

        self.setup_connections()
        self.ui.statusbar.showMessage("Sẵn sàng. Vui lòng chọn tập tin Excel.")

    def setup_connections(self):
        # Liên kết các nút
        self.ui.pushButton_2.clicked.connect(self.select_excel_file)
        self.ui.pushButton_3.clicked.connect(self.open_chart_in_browser)
        self.ui.pushButton_4.clicked.connect(self.save_chart_to_html)
        self.ui.lineEdit.textChanged.connect(self.update_button_state)

    def update_button_state(self):
        has_text = bool(self.ui.lineEdit.text().strip())
        self.ui.pushButton_4.setEnabled(has_text)

    def select_excel_file(self):
        # Chọn file Excel
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Chọn Tập Tin Excel", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.excel_file_path = file_path
            self.ui.lineEdit.setText(file_path)  # Hiển thị đường dẫn file
            self.ui.statusbar.showMessage(f"Đã chọn tập tin: {os.path.basename(file_path)}")

    def open_chart_in_browser(self):
        # Mở biểu đồ trong trình duyệt
        try:
            if not self.excel_file_path:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn tập tin Excel hợp lệ!")
                return

            processor = DataProcessor(self.excel_file_path)
            self.output_html_path = processor.generate_chart()

            # Mở file HTML trong trình duyệt
            webbrowser.open(f"file://{os.path.abspath(self.output_html_path)}")

        except Exception as e:
            self.ui.statusbar.showMessage(f"Lỗi: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo biểu đồ: {str(e)}")

    def save_chart_to_html(self):
        # Lưu biểu đồ dưới dạng HTML
        try:
            if not self.excel_file_path:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn tập tin Excel hợp lệ!")
                return

            processor = DataProcessor(self.excel_file_path)
            self.output_html_path = processor.generate_chart()

            self.ui.statusbar.showMessage(f"Đã lưu biểu đồ tại: {os.path.basename(self.output_html_path)}")

        except Exception as e:
            self.ui.statusbar.showMessage(f"Lỗi: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu biểu đồ: {str(e)}")
