import sys
import os
import pandas as pd
import plotly.express as px
import webbrowser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFileDialog, QLabel, QWidget, QLineEdit)
from PyQt6.QtCore import Qt
from tempfile import NamedTemporaryFile


class CurriculumChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Curriculum Chart Generator")
        self.setGeometry(100, 100, 600, 200)

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # File selection layout
        file_layout = QHBoxLayout()
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("Chọn file Excel chương trình đào tạo...")
        self.file_path_input.setReadOnly(True)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(browse_button)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        self.open_chart_button = QPushButton("Open Chart in Browser")
        self.open_chart_button.clicked.connect(self.open_chart_in_browser)
        self.open_chart_button.setEnabled(False)

        self.save_chart_button = QPushButton("Save Chart to HTML File")
        self.save_chart_button.clicked.connect(self.save_chart_to_html)
        self.save_chart_button.setEnabled(False)

        buttons_layout.addWidget(self.open_chart_button)
        buttons_layout.addWidget(self.save_chart_button)

        # Status label
        self.status_label = QLabel("Vui lòng chọn file Excel chương trình đào tạo")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add all layouts to main layout
        main_layout.addLayout(file_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.status_label)

        # Set main widget
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Data storage
        self.excel_data = None
        self.fig = None
        self.temp_html_file = None

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn file Excel", "", "Excel Files (*.xlsx *.xls)"
        )

        if file_path:
            self.file_path_input.setText(file_path)
            self.status_label.setText("Đang xử lý dữ liệu...")
            try:
                self.process_excel_data(file_path)
                self.status_label.setText("Dữ liệu đã được xử lý thành công!")
                self.open_chart_button.setEnabled(True)
                self.save_chart_button.setEnabled(True)
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.status_label.setText(f"Lỗi: {str(e)}")
                self.open_chart_button.setEnabled(False)
                self.save_chart_button.setEnabled(False)

    def process_excel_data(self, file_path):
        try:
            # Đọc file Excel
            print(f"Đang đọc file: {file_path}")
            self.excel_data = pd.read_excel(file_path)
            print(f"Đã đọc file thành công. Số dòng: {len(self.excel_data)}")
            print(f"Các cột trong file: {self.excel_data.columns.tolist()}")

            # Tạo cấu trúc dữ liệu cơ bản nếu thiếu
            if 'Học kỳ' not in self.excel_data.columns:
                print("Không tìm thấy cột 'Học kỳ'. Tạo cột mặc định.")
                # Tìm cột có thể là học kỳ
                semester_cols = [col for col in self.excel_data.columns if
                                 any(kw in str(col).lower() for kw in ['kỳ', 'ky', 'hk', 'semester'])]
                if semester_cols:
                    print(f"Sử dụng cột '{semester_cols[0]}' làm 'Học kỳ'")
                    self.excel_data.rename(columns={semester_cols[0]: 'Học kỳ'}, inplace=True)
                else:
                    # Tạo cột học kỳ mặc định
                    self.excel_data['Học kỳ'] = 1

            if 'Loại' not in self.excel_data.columns:
                print("Không tìm thấy cột 'Loại'. Tạo cột mặc định.")
                # Tìm cột có thể là loại
                type_cols = [col for col in self.excel_data.columns if
                             any(kw in str(col).lower() for kw in ['loại', 'loai', 'type', 'bắt buộc', 'tự chọn'])]
                if type_cols:
                    print(f"Sử dụng cột '{type_cols[0]}' làm 'Loại'")
                    self.excel_data.rename(columns={type_cols[0]: 'Loại'}, inplace=True)
                else:
                    # Tạo cột loại mặc định
                    self.excel_data['Loại'] = 'Bắt buộc'

            if 'Tên môn học' not in self.excel_data.columns:
                print("Không tìm thấy cột 'Tên môn học'. Tìm cột thay thế.")
                # Tìm cột có thể là tên môn học
                name_cols = [col for col in self.excel_data.columns if
                             any(kw in str(col).lower() for kw in ['tên', 'ten', 'môn', 'mon', 'name', 'course'])]
                if name_cols:
                    print(f"Sử dụng cột '{name_cols[0]}' làm 'Tên môn học'")
                    self.excel_data.rename(columns={name_cols[0]: 'Tên môn học'}, inplace=True)
                else:
                    # Tìm cột kiểu chuỗi đầu tiên không phải Loại
                    string_cols = [col for col in self.excel_data.columns if
                                   self.excel_data[col].dtype == 'object' and col != 'Loại']
                    if string_cols:
                        print(f"Sử dụng cột '{string_cols[0]}' làm 'Tên môn học'")
                        self.excel_data.rename(columns={string_cols[0]: 'Tên môn học'}, inplace=True)
                    else:
                        # Tạo cột tên môn học mặc định
                        self.excel_data['Tên môn học'] = [f'Môn học {i + 1}' for i in range(len(self.excel_data))]

            if 'Số tín chỉ' not in self.excel_data.columns:
                print("Không tìm thấy cột 'Số tín chỉ'. Tìm cột thay thế.")
                # Tìm cột có thể là số tín chỉ
                credit_cols = [col for col in self.excel_data.columns if
                               any(kw in str(col).lower() for kw in ['tín', 'tin', 'tc', 'credit'])]
                if credit_cols:
                    print(f"Sử dụng cột '{credit_cols[0]}' làm 'Số tín chỉ'")
                    self.excel_data.rename(columns={credit_cols[0]: 'Số tín chỉ'}, inplace=True)
                else:
                    # Tìm cột số đầu tiên không phải Học kỳ
                    numeric_cols = [col for col in self.excel_data.select_dtypes(include=['number']).columns if
                                    col != 'Học kỳ']
                    if numeric_cols:
                        print(f"Sử dụng cột '{numeric_cols[0]}' làm 'Số tín chỉ'")
                        self.excel_data.rename(columns={numeric_cols[0]: 'Số tín chỉ'}, inplace=True)
                    else:
                        # Tạo cột số tín chỉ mặc định
                        self.excel_data['Số tín chỉ'] = 3

            # Chuyển đổi kiểu dữ liệu
            print("Chuyển đổi kiểu dữ liệu...")
            self.excel_data['Học kỳ'] = pd.to_numeric(self.excel_data['Học kỳ'], errors='coerce').fillna(1).astype(int)
            self.excel_data['Số tín chỉ'] = pd.to_numeric(self.excel_data['Số tín chỉ'], errors='coerce').fillna(
                3).astype(int)

            # Chuẩn hóa cột Loại
            def standardize_type(type_str):
                if pd.isna(type_str):
                    return "Bắt buộc"

                type_lower = str(type_str).lower()
                if any(kw in type_lower for kw in ["bắt buộc", "bat buoc", "bb", "bắt", "bat"]):
                    return "Bắt buộc"
                elif any(kw in type_lower for kw in ["tự chọn", "tu chon", "tc", "tự", "tu", "chọn", "chon"]):
                    return "Tự chọn"
                return "Bắt buộc"  # Mặc định là bắt buộc

            self.excel_data['Loại'] = self.excel_data['Loại'].apply(standardize_type)

            # Hiển thị dữ liệu sau khi xử lý
            print("Dữ liệu sau khi xử lý:")
            print(self.excel_data.head())

            # Tạo biểu đồ đơn giản hơn sử dụng plotly express
            print("Đang tạo biểu đồ...")

            # Chuẩn bị dữ liệu cho biểu đồ
            # Thêm cột path để tạo đường dẫn phân cấp
            self.excel_data['path'] = self.excel_data.apply(
                lambda row: f"Chương trình đào tạo/Học kỳ {row['Học kỳ']}/{row['Loại']}/{row['Tên môn học']}",
                axis=1
            )

            # Tạo biểu đồ sunburst đơn giản
            self.fig = px.sunburst(
                self.excel_data,
                path=['Học kỳ', 'Loại', 'Tên môn học'],
                values='Số tín chỉ',
                title="Chương trình đào tạo Thương Mại Điện Tử",
                width=1000,
                height=1000,
                color='Học kỳ',
                color_continuous_scale='viridis'
            )

            # Cấu hình layout
            self.fig.update_layout(margin=dict(t=30, l=0, r=0, b=0))
            print("Đã tạo biểu đồ thành công!")

        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"Lỗi khi xử lý file Excel: {str(e)}")

    def open_chart_in_browser(self):
        if self.fig:
            try:
                print("Đang mở biểu đồ trong trình duyệt...")
                # Tạo file HTML tạm thời
                if self.temp_html_file:
                    # Xóa file tạm cũ nếu tồn tại
                    try:
                        os.unlink(self.temp_html_file.name)
                    except:
                        pass

                # Tạo file HTML mới
                self.temp_html_file = NamedTemporaryFile(delete=False, suffix='.html')
                temp_path = self.temp_html_file.name
                self.temp_html_file.close()

                # Ghi biểu đồ vào file HTML
                print(f"Đang ghi biểu đồ vào file: {temp_path}")
                self.fig.write_html(temp_path, full_html=True, include_plotlyjs='cdn')

                # Mở file trong trình duyệt
                print(f"Đang mở file trong trình duyệt: {temp_path}")
                webbrowser.open('file://' + temp_path)
                self.status_label.setText("Đã mở biểu đồ trong trình duyệt!")

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.status_label.setText(f"Lỗi khi mở biểu đồ: {str(e)}")

    def save_chart_to_html(self):
        if self.fig:
            try:
                # Mở hộp thoại lưu file
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Lưu biểu đồ", "411_10k.html", "HTML Files (*.html)"
                )

                if file_path:
                    print(f"Đang lưu biểu đồ vào: {file_path}")
                    self.fig.write_html(file_path, full_html=True, include_plotlyjs='cdn')
                    self.status_label.setText(f"Đã lưu biểu đồ vào: {file_path}")

                    # Thử mở file đã lưu
                    print(f"Đang mở file đã lưu: {file_path}")
                    webbrowser.open('file://' + file_path)

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.status_label.setText(f"Lỗi khi lưu biểu đồ: {str(e)}")

    def closeEvent(self, event):
        # Xóa file tạm khi đóng ứng dụng
        if self.temp_html_file:
            try:
                os.unlink(self.temp_html_file.name)
            except:
                pass
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = CurriculumChartApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()