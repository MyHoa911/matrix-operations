import sys
import os
import pandas as pd
import plotly.express as px
import webbrowser
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from tempfile import NamedTemporaryFile
from MainWindow import Ui_MainWindow


class CurriculumChartApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButtonbrowser.clicked.connect(self.browse_file)
        self.pushButtonopen.clicked.connect(self.open_chart_in_browser)
        self.pushButtonsave.clicked.connect(self.save_chart_to_html)
        self.pushButtonopen.setEnabled(False)
        self.pushButtonsave.setEnabled(False)

        self.excel_data = None
        self.fig = None
        self.temp_html_file = None

        self.lineEdit.setPlaceholderText("Chọn file Excel chương trình đào tạo...")
        self.lineEdit.setReadOnly(True)
        self.statusbar.showMessage("Vui lòng chọn file Excel chương trình đào tạo")

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn file Excel", "", "Excel Files (*.xlsx *.xls)"
        )

        if file_path:
            self.lineEdit.setText(file_path)
            self.statusbar.showMessage("Đang xử lý dữ liệu...")
            try:
                self.process_excel_data(file_path)
                self.statusbar.showMessage("Dữ liệu đã được xử lý thành công!")
                self.pushButtonopen.setEnabled(True)
                self.pushButtonsave.setEnabled(True)
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.statusbar.showMessage(f"Lỗi: {str(e)}")
                self.pushButtonopen.setEnabled(False)
                self.pushButtonsave.setEnabled(False)

    def process_excel_data(self, file_path):
        try:
            print(f"Đang đọc file: {file_path}")
            self.excel_data = pd.read_excel(file_path)
            print(f"Đã đọc file thành công. Số dòng: {len(self.excel_data)}")
            print(f"Các cột trong file: {self.excel_data.columns.tolist()}")

            if 'Học kỳ' not in self.excel_data.columns and 'Học Kỳ' not in self.excel_data.columns:
                print("Không tìm thấy cột 'Học kỳ'. Tạo cột mặc định.")
                semester_cols = [col for col in self.excel_data.columns if
                                 any(kw in str(col).lower() for kw in ['kỳ', 'ky', 'hk', 'semester'])]
                if semester_cols:
                    print(f"Sử dụng cột '{semester_cols[0]}' làm 'Học kỳ'")
                    self.excel_data.rename(columns={semester_cols[0]: 'Học kỳ'}, inplace=True)
                else:
                    self.excel_data['Học kỳ'] = 1
            elif 'Học Kỳ' in self.excel_data.columns:

                self.excel_data.rename(columns={'Học Kỳ': 'Học kỳ'}, inplace=True)

            if 'Loại' not in self.excel_data.columns and 'Bắt buộc/tự chọn' not in self.excel_data.columns:
                print("Không tìm thấy cột 'Loại'. Tạo cột mặc định.")
                # Tìm cột có thể là loại
                type_cols = [col for col in self.excel_data.columns if
                             any(kw in str(col).lower() for kw in
                                 ['loại', 'loai', 'type', 'bắt buộc', 'tự chọn', 'buoc', 'chon'])]
                if type_cols:
                    print(f"Sử dụng cột '{type_cols[0]}' làm 'Loại'")
                    self.excel_data.rename(columns={type_cols[0]: 'Loại'}, inplace=True)
                else:
                    self.excel_data['Loại'] = 'Bắt buộc'
            elif 'Bắt buộc/tự chọn' in self.excel_data.columns:
                self.excel_data.rename(columns={'Bắt buộc/tự chọn': 'Loại'}, inplace=True)

            if 'Tên môn học' not in self.excel_data.columns and 'Tên học phần' not in self.excel_data.columns:
                print("Không tìm thấy cột 'Tên môn học'. Tìm cột thay thế.")
                name_cols = [col for col in self.excel_data.columns if
                             any(kw in str(col).lower() for kw in
                                 ['tên', 'ten', 'môn', 'mon', 'name', 'course', 'học phần', 'hoc phan'])]
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
                        self.excel_data['Tên môn học'] = [f'Môn học {i + 1}' for i in range(len(self.excel_data))]
            elif 'Tên học phần' in self.excel_data.columns:
                self.excel_data.rename(columns={'Tên học phần': 'Tên môn học'}, inplace=True)
            if 'Số tín chỉ' not in self.excel_data.columns and 'Tín Chỉ' not in self.excel_data.columns:
                print("Không tìm thấy cột 'Số tín chỉ'. Tìm cột thay thế.")
                credit_cols = [col for col in self.excel_data.columns if
                               any(kw in str(col).lower() for kw in ['tín', 'tin', 'tc', 'credit'])]
                if credit_cols:
                    print(f"Sử dụng cột '{credit_cols[0]}' làm 'Số tín chỉ'")
                    self.excel_data.rename(columns={credit_cols[0]: 'Số tín chỉ'}, inplace=True)
                else:
                    numeric_cols = [col for col in self.excel_data.select_dtypes(include=['number']).columns if
                                    col != 'Học kỳ']
                    if numeric_cols:
                        print(f"Sử dụng cột '{numeric_cols[0]}' làm 'Số tín chỉ'")
                        self.excel_data.rename(columns={numeric_cols[0]: 'Số tín chỉ'}, inplace=True)
                    else:
                        self.excel_data['Số tín chỉ'] = 3
            elif 'Tín Chỉ' in self.excel_data.columns:
                self.excel_data.rename(columns={'Tín Chỉ': 'Số tín chỉ'}, inplace=True)

            print("Chuyển đổi kiểu dữ liệu...")
            self.excel_data['Học kỳ'] = pd.to_numeric(self.excel_data['Học kỳ'], errors='coerce').fillna(1).astype(int)
            self.excel_data['Số tín chỉ'] = pd.to_numeric(self.excel_data['Số tín chỉ'], errors='coerce').fillna(
                3).astype(int)


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

            print("Dữ liệu sau khi xử lý:")
            print(self.excel_data.head())

            print("Đang tạo biểu đồ...")

            self.fig = px.sunburst(
                self.excel_data,
                path=['Học kỳ', 'Loại', 'Tên môn học'],
                values='Số tín chỉ',
                title="Chương trình đào tạo ngành 411",
                width=1000,
                height=1000,
                color='Học kỳ',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            self.fig.update_layout(margin=dict(t=30, l=0, r=0, b=0))
            print("Đã tạo biểu đồ thành công!")

        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"Lỗi khi xử lý file Excel: {str(e)}")

    def open_chart_in_browser(self):
        if self.fig:
            try:
                if self.temp_html_file:

                    try:
                        os.unlink(self.temp_html_file.name)
                    except:
                        pass


                self.temp_html_file = NamedTemporaryFile(delete=False, suffix='.html')
                temp_path = self.temp_html_file.name
                self.temp_html_file.close()

                html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Chương trình đào tạo</title>
</head>
<body>
    <h1>Chương trình đào tạo ngành 411</h1>
    {self.fig.to_html(full_html=False, include_plotlyjs='cdn')}
</body>
</html>"""

                # Ghi biểu đồ vào file HTML
                print(f"Đang ghi biểu đồ vào file: {temp_path}")
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                # Mở file trong trình duyệt
                print(f"Đang mở file trong trình duyệt: {temp_path}")
                webbrowser.open('file://' + temp_path)
                self.statusbar.showMessage("Đã mở biểu đồ trong trình duyệt!")

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.statusbar.showMessage(f"Lỗi khi mở biểu đồ: {str(e)}")

    def save_chart_to_html(self):
        if self.fig:
            try:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Lưu biểu đồ", "411_10k.html", "HTML Files (*.html)"
                )

                if file_path:
                    print(f"Đang lưu biểu đồ vào: {file_path}")

                    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Chương trình đào tạo</title>
</head>
<body>
    <h1>Chương trình đào tạo ngành 411</h1>
    {self.fig.to_html(full_html=False, include_plotlyjs='cdn')}
</body>
</html>"""

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)

                    self.statusbar.showMessage(f"Đã lưu biểu đồ vào: {file_path}")

                    print(f"Đang mở file đã lưu: {file_path}")
                    webbrowser.open('file://' + file_path)

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.statusbar.showMessage(f"Lỗi khi lưu biểu đồ: {str(e)}")

    def closeEvent(self, event):
        if self.temp_html_file:
            try:
                os.unlink(self.temp_html_file.name)
            except:
                pass
        event.accept()


