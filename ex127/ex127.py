import sys
import pandas as pd
import numpy as np
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QMessageBox
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas

CSV_FILE = './data/SampleData2.csv'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pandas DataFrame Manager (PyQt6)")
        self.resize(900, 700)
        # Đọc DataFrame ban đầu từ CSV
        self.df = pd.read_csv(CSV_FILE)
        self.initUI()

    def initUI(self):
        # Tạo widget chính và layout
        widget = QWidget()
        self.setCentralWidget(widget)
        mainLayout = QVBoxLayout()
        widget.setLayout(mainLayout)

        # Tạo QTableWidget để hiển thị DataFrame
        self.table = QTableWidget()
        mainLayout.addWidget(self.table)
        self.updateTable()

        # ---- Các nút chức năng (1)-(4) ----
        controlsLayout = QHBoxLayout()

        # (1) In toàn bộ dữ liệu ra console
        self.printBtn = QPushButton("Print Data")
        self.printBtn.clicked.connect(self.printData)
        controlsLayout.addWidget(self.printBtn)

        # (2) Sắp xếp dữ liệu theo Price tăng dần
        self.sortBtn = QPushButton("Sort by Price")
        self.sortBtn.clicked.connect(self.sortByPrice)
        controlsLayout.addWidget(self.sortBtn)

        # (3) Tìm kiếm Symbol nhập từ bàn phím, nếu tìm thấy thì giảm Price đi 1/2
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Enter Symbol to search")
        controlsLayout.addWidget(self.searchInput)
        self.reducePriceBtn = QPushButton("Reduce Price by 1/2")
        self.reducePriceBtn.clicked.connect(self.reducePrice)
        controlsLayout.addWidget(self.reducePriceBtn)

        # (4) Thêm cột USD với giá trị = Price/23
        self.addUSDBtn = QPushButton("Add USD Column")
        self.addUSDBtn.clicked.connect(self.addUSD)
        controlsLayout.addWidget(self.addUSDBtn)

        mainLayout.addLayout(controlsLayout)

        # ---- (5) Nhập dữ liệu mới và thêm vào cuối DataFrame ----
        addRowLayout = QHBoxLayout()
        self.symbolInput = QLineEdit()
        self.symbolInput.setPlaceholderText("Symbol")
        addRowLayout.addWidget(self.symbolInput)
        self.priceInput = QLineEdit()
        self.priceInput.setPlaceholderText("Price")
        addRowLayout.addWidget(self.priceInput)
        self.peInput = QLineEdit()
        self.peInput.setPlaceholderText("PE")
        addRowLayout.addWidget(self.peInput)
        self.usdInput = QLineEdit()
        self.usdInput.setPlaceholderText("USD")
        addRowLayout.addWidget(self.usdInput)
        self.addRowBtn = QPushButton("Add Row")
        self.addRowBtn.clicked.connect(self.addRow)
        addRowLayout.addWidget(self.addRowBtn)
        mainLayout.addLayout(addRowLayout)

        # ---- (6) Group data theo 'Group' và thống kê, (7) Xóa dòng theo Symbol ----
        statsDeleteLayout = QHBoxLayout()
        self.groupStatsBtn = QPushButton("Group Statistics")
        self.groupStatsBtn.clicked.connect(self.groupStats)
        statsDeleteLayout.addWidget(self.groupStatsBtn)

        self.deleteInput = QLineEdit()
        self.deleteInput.setPlaceholderText("Enter Symbol to delete")
        statsDeleteLayout.addWidget(self.deleteInput)
        self.deleteBtn = QPushButton("Delete Row")
        self.deleteBtn.clicked.connect(self.deleteRow)
        statsDeleteLayout.addWidget(self.deleteBtn)
        mainLayout.addLayout(statsDeleteLayout)

        # ---- (8) Hiển thị biểu đồ tích hợp vào giao diện ----
        self.chartBtn = QPushButton("Show Price Chart")
        self.chartBtn.clicked.connect(self.showChart)
        mainLayout.addWidget(self.chartBtn)

        # Thêm canvas của matplotlib
        self.figureCanvas = FigureCanvas(plt.Figure(figsize=(5, 3)))
        mainLayout.addWidget(self.figureCanvas)

    def updateTable(self):
        """Cập nhật QTableWidget theo dữ liệu của DataFrame hiện tại."""
        df = self.df
        self.table.setRowCount(len(df.index))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns.tolist())
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def printData(self):
        """(1) In toàn bộ dữ liệu ra console."""
        print("Full DataFrame:")
        print(self.df)

    def sortByPrice(self):
        """(2) Sắp xếp DataFrame theo cột Price tăng dần."""
        if 'Price' in self.df.columns:
            self.df = self.df.sort_values(by='Price', ascending=True)
            self.updateTable()
            print("DataFrame sorted by Price:")
            print(self.df)
        else:
            QMessageBox.warning(self, "Error", "No 'Price' column found.")

    def reducePrice(self):
        """(3) Tìm kiếm Symbol và giảm Price đi 1/2 nếu tìm thấy."""
        symbol = self.searchInput.text().strip()
        if symbol == "":
            QMessageBox.warning(self, "Input Error", "Please enter a Symbol.")
            return
        mask = self.df['Symbol'] == symbol
        if mask.any():
            self.df.loc[mask, 'Price'] = self.df.loc[mask, 'Price'] / 2
            self.updateTable()
            print(f"Price for symbol {symbol} reduced by half.")
        else:
            QMessageBox.information(self, "Not Found", f"Symbol '{symbol}' not found.")

    def addUSD(self):
        """(4) Thêm cột USD với giá trị = Price/23."""
        if 'Price' in self.df.columns:
            self.df['USD'] = self.df['Price'] / 23
            self.updateTable()
            print("USD column added.")
        else:
            QMessageBox.warning(self, "Error", "No 'Price' column found.")

    def addRow(self):
        """(5) Thêm dòng mới với dữ liệu nhập từ người dùng."""
        symbol = self.symbolInput.text().strip()
        try:
            price = float(self.priceInput.text().strip())
            pe = float(self.peInput.text().strip())
            usd = float(self.usdInput.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price, PE, and USD must be numeric.")
            return
        newRow = {'Symbol': symbol, 'Price': price, 'PE': pe, 'USD': usd}
        if 'Group' in self.df.columns:
            newRow['Group'] = ""
        self.df = pd.concat([self.df, pd.DataFrame([newRow])], ignore_index=True)
        self.updateTable()
        print("New row added:", newRow)

    def groupStats(self):
        """(6) Group theo 'Group' và tính thống kê (mean, sum, count)."""
        if 'Group' in self.df.columns:
            group_mean = self.df.groupby('Group').mean(numeric_only=True)
            group_sum = self.df.groupby('Group').sum(numeric_only=True)
            group_count = self.df.groupby('Group').count()
            stats = f"Group Mean:\n{group_mean}\n\nGroup Sum:\n{group_sum}\n\nGroup Count:\n{group_count}"
            print(stats)
            QMessageBox.information(self, "Group Statistics", stats)
        else:
            QMessageBox.warning(self, "Error", "No 'Group' column found.")

    def deleteRow(self):
        """(7) Xóa dòng có Symbol nhập từ bàn phím."""
        symbol = self.deleteInput.text().strip()
        if symbol == "":
            QMessageBox.warning(self, "Input Error", "Please enter a Symbol to delete.")
            return
        mask = self.df['Symbol'] == symbol
        if mask.any():
            self.df = self.df[~mask]
            self.updateTable()
            print(f"Rows with symbol '{symbol}' deleted.")
        else:
            QMessageBox.information(self, "Not Found", f"Symbol '{symbol}' not found.")

    def showChart(self):
        """(8) Hiển thị biểu đồ Price theo Symbol sử dụng matplotlib."""
        if 'Price' not in self.df.columns or 'Symbol' not in self.df.columns:
            QMessageBox.warning(self, "Error", "Required columns not found for chart.")
            return
        ax = self.figureCanvas.figure.subplots()
        ax.clear()
        ax.plot(self.df['Symbol'], self.df['Price'], marker='o', linestyle='-')
        ax.set_title("Price Chart")
        ax.set_xlabel("Symbol")
        ax.set_ylabel("Price")
        self.figureCanvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
