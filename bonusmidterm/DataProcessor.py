import os
import pandas as pd
import plotly.express as px
from datetime import datetime
import webbrowser


class DataProcessor:
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.output_file = f"411_10k_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    def read_excel_data(self):
        try:
            df = pd.read_excel(self.excel_file_path, engine='openpyxl')

            # Đổi tên cột "Học Kỳ" thành "Học Kỳ X"
            if "Học Kỳ" in df.columns:
                df["Học Kỳ"] = df["Học Kỳ"].apply(lambda x: f"Học Kỳ {int(x)}" if pd.notna(x) else "Không xác định")

            print("Danh sách cột sau khi đổi tên:", df.columns.tolist())  # Kiểm tra lại danh sách cột
            return df
        except Exception as e:
            raise Exception(f"Không thể đọc tập tin Excel: {e}")

    def process_data_for_visualization(self, df):
        # Kiểm tra các cột cần thiết
        required_columns = ['Học Kỳ', 'Bắt buộc/tự chọn', 'Tên học phần', 'Tín Chỉ']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise Exception(f"Thiếu cột: {', '.join(missing_columns)}")

        # Chuyển cột tín chỉ thành kiểu số
        df['Tín Chỉ'] = pd.to_numeric(df['Tín Chỉ'], errors='coerce').fillna(1)

        # Sắp xếp dữ liệu theo học kỳ và tên môn học
        df = df.sort_values(by=['Học Kỳ', 'Tên học phần'])

        return df

    def create_sunburst_chart(self, processed_data):
        # Tạo biểu đồ sunburst
        processed_data['Tín Chỉ'] = pd.to_numeric(processed_data['Tín Chỉ'], errors='coerce').fillna(1)
        fig = px.sunburst(
            processed_data, path=['Học Kỳ', 'Bắt buộc/tự chọn', 'Tên học phần'], values='Tín Chỉ',
            title='Chương trình đào tạo ngành 411', width=1000, height=800, color='Học Kỳ',
            color_discrete_sequence=px.colors.qualitative.Pastel)
        return fig

    def generate_chart(self):
        try:
            # Đọc dữ liệu
            df = self.read_excel_data()
            # Xử lý dữ liệu
            processed_data = self.process_data_for_visualization(df)
            # Tạo biểu đồ
            fig = self.create_sunburst_chart(processed_data)

            # Tạo nội dung HTML cho biểu đồ
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Chương trình đào tạo</title>
</head>
<body>
    <h1>Chương trình đào tạo ngành 411</h1>
    {fig.to_html(full_html=False, include_plotlyjs='cdn')}
</body>
</html>"""

            # Lưu biểu đồ vào file HTML
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            return os.path.abspath(self.output_file)
        except Exception as e:
            raise Exception(f"Lỗi khi tạo biểu đồ: {str(e)}")

    def open_chart_in_browser(self):
        # Mở file HTML trong trình duyệt
        webbrowser.open(f"file://{os.path.abspath(self.output_file)}")
