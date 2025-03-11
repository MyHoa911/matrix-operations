import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, \
    QLabel, QHBoxLayout
import sys

# Load dataset
dataset_url = "https://tranduythanh.com/datasets/TCB_2018_2020.csv"
df = pd.read_csv(dataset_url, index_col=0)


class TCBViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TCB Data Viewer")
        self.setGeometry(100, 100, 900, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Input fields for filtering data
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.filter_button = QPushButton("Filter Data")
        self.filter_button.clicked.connect(self.filter_data)

        # Input field for date search
        self.date_input = QLineEdit()
        self.search_button = QPushButton("Search Date")
        self.search_button.clicked.connect(self.search_date)

        # Table widget to display data
        self.tableWidget = QTableWidget()
        self.load_data()

        # Layouts for inputs
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Min Close:"))
        input_layout.addWidget(self.x_input)
        input_layout.addWidget(QLabel("Max Close:"))
        input_layout.addWidget(self.y_input)
        input_layout.addWidget(self.filter_button)

        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Date (YYYY-MM-DD):"))
        date_layout.addWidget(self.date_input)
        date_layout.addWidget(self.search_button)

        layout.addLayout(input_layout)
        layout.addLayout(date_layout)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def load_data(self):
        num_rows, num_cols = df.shape
        self.tableWidget.setRowCount(num_rows)
        self.tableWidget.setColumnCount(num_cols)
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        for row in range(num_rows):
            for col in range(num_cols):
                item = QTableWidgetItem(str(df.iloc[row, col]))
                self.tableWidget.setItem(row, col, item)

    def filter_data(self):
        x = float(self.x_input.text())
        y = float(self.y_input.text())
        filtered_df = df[(df['Close'] > x) & (df['Close'] < y)]
        self.update_table(filtered_df)

    def search_date(self):
        date = self.date_input.text()
        if date in df.index:
            result_df = df.loc[[date]]
            self.update_table(result_df)
        else:
            self.update_table(pd.DataFrame())

    def update_table(self, new_df):
        self.tableWidget.setRowCount(new_df.shape[0])
        self.tableWidget.setColumnCount(new_df.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(new_df.columns)
        for row in range(new_df.shape[0]):
            for col in range(new_df.shape[1]):
                item = QTableWidgetItem(str(new_df.iloc[row, col]))
                self.tableWidget.setItem(row, col, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = TCBViewer()
    viewer.show()
    sys.exit(app.exec())
