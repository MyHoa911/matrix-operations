import os
import pandas as pd
import plotly.express as px
from datetime import datetime
import webbrowser


class CurriculumVisualizer:
    """Class for visualizing curriculum data from Excel files using Plotly."""

    def __init__(self, excel_path):
        """Initialize with the path to an Excel file containing curriculum data."""
        self.excel_path = excel_path
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.html_output_path = f"curriculum_chart_{timestamp}.html"

    def extract_data(self):
        """Extract and preprocess data from the Excel file."""
        try:
            # Load the Excel file
            data = pd.read_excel(self.excel_path, engine='openpyxl')

            # Format semester column if it exists
            if "Học Kỳ" in data.columns:
                data["Học Kỳ"] = data["Học Kỳ"].apply(
                    lambda x: f"Học Kỳ {int(x)}" if pd.notna(x) else "Không xác định"
                )

            print(f"Columns after preprocessing: {data.columns.tolist()}")
            return data
        except Exception as e:
            raise Exception(f"Failed to read Excel file: {str(e)}")

    def validate_and_prepare_data(self, data):
        """Validate and prepare data for visualization."""
        # Check for required columns
        essential_columns = ['Học Kỳ', 'Bắt buộc/tự chọn', 'Tên học phần', 'Tín Chỉ']
        missing = [col for col in essential_columns if col not in data.columns]

        if missing:
            raise Exception(f"Missing required columns: {', '.join(missing)}")

        # Convert credits to numeric values
        data['Tín Chỉ'] = pd.to_numeric(data['Tín Chỉ'], errors='coerce').fillna(1)

        # Sort data for better visualization
        return data.sort_values(by=['Học Kỳ', 'Tên học phần'])

    def generate_sunburst_chart(self, data):
        """Create a sunburst chart from the prepared data."""
        # Ensure credits are numeric
        data['Tín Chỉ'] = pd.to_numeric(data['Tín Chỉ'], errors='coerce').fillna(1)

        # Create the sunburst chart
        figure = px.sunburst(
            data,
            path=['Học Kỳ', 'Bắt buộc/tự chọn', 'Tên học phần'],
            values='Tín Chỉ',
            title='Chương trình đào tạo ngành 411',
            width=1000,
            height=800,
            color='Học Kỳ',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        return figure

    def save_chart_to_html(self, figure):
        """Save the chart to an HTML file."""
        # Create HTML content with the chart
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Chương trình đào tạo</title>
</head>
<body>
    <h1>Chương trình đào tạo ngành 411</h1>
    {figure.to_html(full_html=False, include_plotlyjs='cdn')}
</body>
</html>"""

        # Write to file
        with open(self.html_output_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        return os.path.abspath(self.html_output_path)

    def display_in_browser(self):
        """Open the generated chart in the default web browser."""
        webbrowser.open(f"file://{os.path.abspath(self.html_output_path)}")

    def visualize_curriculum(self):
        """Complete process to visualize curriculum data."""
        try:
            # Extract data from Excel
            raw_data = self.extract_data()

            # Validate and prepare data
            prepared_data = self.validate_and_prepare_data(raw_data)

            # Generate chart
            chart = self.generate_sunburst_chart(prepared_data)

            # Save chart to HTML
            html_path = self.save_chart_to_html(chart)

            # Display in browser
            self.display_in_browser()

            return html_path
        except Exception as e:
            raise Exception(f"Error visualizing curriculum: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Replace with your Excel file path
    excel_file = "curriculum_data.xlsx"

    visualizer = CurriculumVisualizer(excel_file)
    output_file = visualizer.visualize_curriculum()

    print(f"Chart generated and saved to: {output_file}")