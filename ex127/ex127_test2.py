import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit,
                             QLabel, QGroupBox, QFormLayout, QComboBox, QMessageBox,
                             QTabWidget, QSplitter, QFrame, QStatusBar, QHeaderView,
                             QFileDialog, QMenu, QToolBar, QSizePolicy, QSpinBox,
                             QDoubleSpinBox, QTextEdit, QDialog, QDialogButtonBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QColor, QPalette, QPixmap, QAction


class StockAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Market Analysis")
        self.setGeometry(100, 100, 1200, 800)

        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
            QTableWidget {
                gridline-color: #d9d9d9;
                selection-background-color: #4a86e8;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #e6e6e6;
                padding: 4px;
                border: 1px solid #d9d9d9;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e6e6e6;
                border: 1px solid #cccccc;
                border-bottom-color: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 6px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
            }
        """)

        # Load data
        self.file_path = "./data/SampleData2.csv"
        self.load_data()

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Create top section with controls and table
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        # Create control panel
        control_panel = self.create_control_panel()
        top_layout.addWidget(control_panel)

        # Create table widget
        self.table = QTableWidget()
        self.update_table()
        top_layout.addWidget(self.table)

        # Create bottom section with charts
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        # Create chart tabs
        chart_tabs = QTabWidget()

        # Tab 1: Price by Symbol
        price_tab = QWidget()
        price_layout = QVBoxLayout(price_tab)
        self.price_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        price_layout.addWidget(self.price_canvas)
        chart_tabs.addTab(price_tab, "Price by Symbol")

        # Tab 2: PE Ratio
        pe_tab = QWidget()
        pe_layout = QVBoxLayout(pe_tab)
        self.pe_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        pe_layout.addWidget(self.pe_canvas)
        chart_tabs.addTab(pe_tab, "PE Ratio")

        # Tab 3: Group Analysis
        group_tab = QWidget()
        group_layout = QVBoxLayout(group_tab)
        self.group_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        group_layout.addWidget(self.group_canvas)
        chart_tabs.addTab(group_tab, "Group Analysis")

        # Tab 4: Scatter Plot
        scatter_tab = QWidget()
        scatter_layout = QVBoxLayout(scatter_tab)
        self.scatter_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        scatter_layout.addWidget(self.scatter_canvas)
        chart_tabs.addTab(scatter_tab, "Price vs PE")

        bottom_layout.addWidget(chart_tabs)

        # Add widgets to splitter
        splitter.addWidget(top_widget)
        splitter.addWidget(bottom_widget)
        splitter.setSizes([400, 400])  # Initial sizes

        # Add splitter to main layout
        main_layout.addWidget(splitter)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Create menu bar
        self.create_menu_bar()

        # Create toolbar
        self.create_toolbar()

        # Update charts
        self.update_charts()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            # Add USD column if it doesn't exist
            if 'USD' not in self.df.columns:
                self.df['USD'] = self.df['Price'] / 23
            self.status_bar.showMessage(f"Data loaded from {self.file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
            self.df = pd.DataFrame(columns=['Symbol', 'Price', 'PE', 'Group', 'USD'])

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")

        add_row_action = QAction("Add Row", self)
        add_row_action.triggered.connect(self.show_add_dialog)
        edit_menu.addAction(add_row_action)

        delete_row_action = QAction("Delete Row", self)
        delete_row_action.triggered.connect(self.show_delete_dialog)
        edit_menu.addAction(delete_row_action)

        # View menu
        view_menu = menu_bar.addMenu("View")

        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_all)
        view_menu.addAction(refresh_action)

        # Analysis menu
        analysis_menu = menu_bar.addMenu("Analysis")

        group_stats_action = QAction("Group Statistics", self)
        group_stats_action.triggered.connect(self.show_group_statistics)
        analysis_menu.addAction(group_stats_action)

        # Help menu
        help_menu = menu_bar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_all)
        toolbar.addAction(refresh_action)

        toolbar.addSeparator()

        add_action = QAction("Add Row", self)
        add_action.triggered.connect(self.show_add_dialog)
        toolbar.addAction(add_action)

        delete_action = QAction("Delete Row", self)
        delete_action.triggered.connect(self.show_delete_dialog)
        toolbar.addAction(delete_action)

        toolbar.addSeparator()

        stats_action = QAction("Statistics", self)
        stats_action.triggered.connect(self.show_group_statistics)
        toolbar.addAction(stats_action)

    def create_control_panel(self):
        control_panel = QGroupBox("Control Panel")
        control_layout = QHBoxLayout()

        # Search and modify section
        search_group = QGroupBox("Search and Modify")
        search_layout = QFormLayout()
        self.search_input = QLineEdit()
        search_button = QPushButton("Search & Halve Price")
        search_button.clicked.connect(self.search_and_modify)
        search_layout.addRow(QLabel("Symbol:"), self.search_input)
        search_layout.addRow(search_button)
        search_group.setLayout(search_layout)

        # Add new row section
        add_group = QGroupBox("Add New Row")
        add_layout = QFormLayout()
        self.new_symbol = QLineEdit()
        self.new_price = QDoubleSpinBox()
        self.new_price.setRange(0, 10000)
        self.new_price.setDecimals(2)
        self.new_pe = QDoubleSpinBox()
        self.new_pe.setRange(0, 1000)
        self.new_pe.setDecimals(2)
        self.new_group = QComboBox()

        # Get unique groups from data
        if not self.df.empty and 'Group' in self.df.columns:
            unique_groups = self.df['Group'].unique()
            self.new_group.addItems(unique_groups)
            self.new_group.setEditable(True)

        add_button = QPushButton("Add Row")
        add_button.clicked.connect(self.add_row)
        add_layout.addRow(QLabel("Symbol:"), self.new_symbol)
        add_layout.addRow(QLabel("Price:"), self.new_price)
        add_layout.addRow(QLabel("PE:"), self.new_pe)
        add_layout.addRow(QLabel("Group:"), self.new_group)
        add_layout.addRow(add_button)
        add_group.setLayout(add_layout)

        # Delete row section
        delete_group = QGroupBox("Delete Row")
        delete_layout = QFormLayout()
        self.delete_input = QLineEdit()
        delete_button = QPushButton("Delete Row")
        delete_button.clicked.connect(self.delete_row)
        delete_layout.addRow(QLabel("Symbol:"), self.delete_input)
        delete_layout.addRow(delete_button)
        delete_group.setLayout(delete_layout)

        # Sort section
        sort_group = QGroupBox("Sort Data")
        sort_layout = QFormLayout()
        self.sort_column = QComboBox()

        # Add column names to sort combo
        if not self.df.empty:
            self.sort_column.addItems(self.df.columns)

        self.sort_order = QComboBox()
        self.sort_order.addItems(["Ascending", "Descending"])
        sort_button = QPushButton("Sort")
        sort_button.clicked.connect(self.sort_data)
        sort_layout.addRow(QLabel("Column:"), self.sort_column)
        sort_layout.addRow(QLabel("Order:"), self.sort_order)
        sort_layout.addRow(sort_button)
        sort_group.setLayout(sort_layout)

        # Add all control groups to control panel
        control_layout.addWidget(search_group)
        control_layout.addWidget(add_group)
        control_layout.addWidget(delete_group)
        control_layout.addWidget(sort_group)
        control_panel.setLayout(control_layout)

        return control_panel

    def update_table(self):
        # Update the table with current DataFrame data
        self.table.setRowCount(len(self.df))
        self.table.setColumnCount(len(self.df.columns))
        self.table.setHorizontalHeaderLabels(self.df.columns)

        # Populate table with data
        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                value = self.df.iloc[i, j]
                # Format numeric values
                if isinstance(value, (int, float)):
                    item = QTableWidgetItem(f"{value:.2f}" if isinstance(value, float) else str(value))
                    item.setTextAlignment(int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter))
                else:
                    item = QTableWidgetItem(str(value))

                # Set item as non-editable
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, j, item)

        # Resize columns to content
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Enable sorting
        self.table.setSortingEnabled(True)

        # Update status bar
        self.status_bar.showMessage(f"Displaying {len(self.df)} records")

    def update_charts(self):
        if self.df.empty:
            return

        # Chart 1: Price by Symbol
        ax1 = self.price_canvas.figure.subplots()
        ax1.clear()
        self.df.sort_values('Price', ascending=False).plot(
            kind='bar',
            x='Symbol',
            y='Price',
            ax=ax1,
            color='#4a86e8'
        )
        ax1.set_title('Price by Symbol')
        ax1.set_xlabel('Symbol')
        ax1.set_ylabel('Price')
        ax1.tick_params(axis='x', rotation=45)
        self.price_canvas.figure.tight_layout()
        self.price_canvas.draw()

        # Chart 2: PE Ratio
        ax2 = self.pe_canvas.figure.subplots()
        ax2.clear()
        self.df.sort_values('PE', ascending=False).plot(
            kind='bar',
            x='Symbol',
            y='PE',
            ax=ax2,
            color='#6aa84f'
        )
        ax2.set_title('PE Ratio by Symbol')
        ax2.set_xlabel('Symbol')
        ax2.set_ylabel('PE Ratio')
        ax2.tick_params(axis='x', rotation=45)
        self.pe_canvas.figure.tight_layout()
        self.pe_canvas.draw()

        # Chart 3: Group Analysis
        ax3 = self.group_canvas.figure.subplots()
        ax3.clear()

        # Group by Group and calculate mean
        group_stats = self.df.groupby('Group').mean()

        # Create bar chart
        group_stats.plot(kind='bar', y=['Price', 'PE'], ax=ax3)
        ax3.set_title('Average Price and PE by Group')
        ax3.set_xlabel('Group')
        ax3.set_ylabel('Value')
        ax3.tick_params(axis='x', rotation=45)
        ax3.legend(['Price', 'PE'])
        self.group_canvas.figure.tight_layout()
        self.group_canvas.draw()

        # Chart 4: Scatter Plot
        ax4 = self.scatter_canvas.figure.subplots()
        ax4.clear()

        # Create scatter plot with different colors for each group
        groups = self.df['Group'].unique()
        colors = plt.cm.tab10(np.linspace(0, 1, len(groups)))

        for i, group in enumerate(groups):
            group_data = self.df[self.df['Group'] == group]
            ax4.scatter(
                group_data['Price'],
                group_data['PE'],
                label=group,
                color=colors[i],
                alpha=0.7,
                s=100
            )

            # Add annotations for each point
            for _, row in group_data.iterrows():
                ax4.annotate(
                    row['Symbol'],
                    (row['Price'], row['PE']),
                    xytext=(5, 5),
                    textcoords='offset points'
                )

        ax4.set_title('Price vs PE Ratio')
        ax4.set_xlabel('Price')
        ax4.set_ylabel('PE Ratio')
        ax4.grid(True, linestyle='--', alpha=0.7)
        ax4.legend()
        self.scatter_canvas.figure.tight_layout()
        self.scatter_canvas.draw()

    def search_and_modify(self):
        symbol = self.search_input.text().strip()
        if not symbol:
            QMessageBox.warning(self, "Input Error", "Please enter a symbol to search.")
            return

        if symbol in self.df['Symbol'].values:
            # Reduce price by half
            self.df.loc[self.df['Symbol'] == symbol, 'Price'] /= 2
            # Update USD value
            self.df.loc[self.df['Symbol'] == symbol, 'USD'] = self.df.loc[self.df['Symbol'] == symbol, 'Price'] / 23

            self.update_table()
            self.update_charts()
            self.status_bar.showMessage(f"Symbol {symbol} found! Price reduced by half.")
            QMessageBox.information(self, "Success", f"Symbol {symbol} found! Price reduced by half.")
        else:
            self.status_bar.showMessage(f"Symbol {symbol} not found.")
            QMessageBox.warning(self, "Not Found", f"Symbol {symbol} not found in the dataset.")

    def add_row(self):
        symbol = self.new_symbol.text().strip()
        price = self.new_price.value()
        pe = self.new_pe.value()
        group = self.new_group.currentText()

        if not symbol:
            QMessageBox.warning(self, "Input Error", "Symbol cannot be empty.")
            return

        # Calculate USD
        usd = price / 23

        # Create new row
        new_row = pd.DataFrame({
            'Symbol': [symbol],
            'Price': [price],
            'PE': [pe],
            'Group': [group],
            'USD': [usd]
        })

        # Add to DataFrame
        self.df = pd.concat([self.df, new_row], ignore_index=True)

        # Update UI
        self.update_table()
        self.update_charts()

        # Clear input fields
        self.new_symbol.clear()
        self.new_price.setValue(0)
        self.new_pe.setValue(0)

        self.status_bar.showMessage(f"New row added: {symbol}")
        QMessageBox.information(self, "Success", "New row added successfully!")

    def delete_row(self):
        symbol = self.delete_input.text().strip()
        if not symbol:
            QMessageBox.warning(self, "Input Error", "Please enter a symbol to delete.")
            return

        if symbol in self.df['Symbol'].values:
            # Remove rows with matching symbol
            self.df = self.df[self.df['Symbol'] != symbol]

            # Update UI
            self.update_table()
            self.update_charts()

            self.status_bar.showMessage(f"Row with Symbol {symbol} deleted.")
            QMessageBox.information(self, "Success", f"Row with Symbol {symbol} deleted.")
        else:
            self.status_bar.showMessage(f"Symbol {symbol} not found.")
            QMessageBox.warning(self, "Not Found", f"Symbol {symbol} not found in the dataset.")

    def sort_data(self):
        column = self.sort_column.currentText()
        order = self.sort_order.currentText()

        if column in self.df.columns:
            ascending = order == "Ascending"
            self.df = self.df.sort_values(by=column, ascending=ascending)

            # Update UI
            self.update_table()

            self.status_bar.showMessage(f"Data sorted by {column} ({order}).")
        else:
            QMessageBox.warning(self, "Error", f"Column {column} not found.")

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                # Add USD column if it doesn't exist
                if 'USD' not in self.df.columns:
                    self.df['USD'] = self.df['Price'] / 23

                self.file_path = file_path
                self.update_table()
                self.update_charts()

                # Update group combobox
                if 'Group' in self.df.columns:
                    self.new_group.clear()
                    unique_groups = self.df['Group'].unique()
                    self.new_group.addItems(unique_groups)

                # Update sort column combobox
                self.sort_column.clear()
                self.sort_column.addItems(self.df.columns)

                self.status_bar.showMessage(f"File loaded: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:
            try:
                self.df.to_csv(file_path, index=False)
                self.status_bar.showMessage(f"File saved: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

    def show_add_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Row")
        dialog.setMinimumWidth(300)

        layout = QFormLayout()

        symbol_input = QLineEdit()
        price_input = QDoubleSpinBox()
        price_input.setRange(0, 10000)
        price_input.setDecimals(2)
        pe_input = QDoubleSpinBox()
        pe_input.setRange(0, 1000)
        pe_input.setDecimals(2)
        group_input = QComboBox()

        # Get unique groups from data
        if not self.df.empty and 'Group' in self.df.columns:
            unique_groups = self.df['Group'].unique()
            group_input.addItems(unique_groups)
            group_input.setEditable(True)

        layout.addRow(QLabel("Symbol:"), symbol_input)
        layout.addRow(QLabel("Price:"), price_input)
        layout.addRow(QLabel("PE:"), pe_input)
        layout.addRow(QLabel("Group:"), group_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addRow(buttons)
        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            symbol = symbol_input.text().strip()
            price = price_input.value()
            pe = pe_input.value()
            group = group_input.currentText()

            if not symbol:
                QMessageBox.warning(self, "Input Error", "Symbol cannot be empty.")
                return

            # Calculate USD
            usd = price / 23

            # Create new row
            new_row = pd.DataFrame({
                'Symbol': [symbol],
                'Price': [price],
                'PE': [pe],
                'Group': [group],
                'USD': [usd]
            })

            # Add to DataFrame
            self.df = pd.concat([self.df, new_row], ignore_index=True)

            # Update UI
            self.update_table()
            self.update_charts()

            self.status_bar.showMessage(f"New row added: {symbol}")

    def show_delete_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Delete Row")
        dialog.setMinimumWidth(300)

        layout = QFormLayout()

        symbol_input = QComboBox()
        if not self.df.empty and 'Symbol' in self.df.columns:
            symbol_input.addItems(self.df['Symbol'].unique())
            symbol_input.setEditable(True)

        layout.addRow(QLabel("Symbol to delete:"), symbol_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addRow(buttons)
        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            symbol = symbol_input.currentText().strip()

            if not symbol:
                QMessageBox.warning(self, "Input Error", "Please select a symbol to delete.")
                return

            if symbol in self.df['Symbol'].values:
                # Remove rows with matching symbol
                self.df = self.df[self.df['Symbol'] != symbol]

                # Update UI
                self.update_table()
                self.update_charts()

                self.status_bar.showMessage(f"Row with Symbol {symbol} deleted.")
            else:
                self.status_bar.showMessage(f"Symbol {symbol} not found.")
                QMessageBox.warning(self, "Not Found", f"Symbol {symbol} not found in the dataset.")

    def show_group_statistics(self):
        if self.df.empty:
            QMessageBox.warning(self, "No Data", "No data available for analysis.")
            return

        # Group by Group column
        grouped = self.df.groupby('Group')

        # Calculate statistics
        stats = {
            'Count': grouped.size(),
            'Mean Price': grouped['Price'].mean(),
            'Mean PE': grouped['PE'].mean(),
            'Sum Price': grouped['Price'].sum(),
            'Min Price': grouped['Price'].min(),
            'Max Price': grouped['Price'].max(),
            'Price StdDev': grouped['Price'].std()
        }

        # Convert to DataFrame
        stats_df = pd.DataFrame(stats).round(2)

        # Create dialog to display statistics
        dialog = QDialog(self)
        dialog.setWindowTitle("Group Statistics")
        dialog.setMinimumSize(800, 600)

        layout = QVBoxLayout()

        # Create tabs for different views
        tabs = QTabWidget()

        # Tab 1: Table View
        table_tab = QWidget()
        table_layout = QVBoxLayout(table_tab)

        # Create table for statistics
        stats_table = QTableWidget()
        stats_table.setRowCount(len(stats_df))
        stats_table.setColumnCount(len(stats_df.columns) + 1)  # +1 for group names

        # Set headers
        headers = ['Group'] + list(stats_df.columns)
        stats_table.setHorizontalHeaderLabels(headers)

        # Populate table
        for i, (group, row) in enumerate(stats_df.iterrows()):
            # Group name
            stats_table.setItem(i, 0, QTableWidgetItem(group))

            # Statistics
            for j, value in enumerate(row):
                item = QTableWidgetItem(f"{value:.2f}" if isinstance(value, float) else str(value))
                item.setTextAlignment(int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter))
                stats_table.setItem(i, j + 1, item)

        stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(stats_table)
        tabs.addTab(table_tab, "Table View")

        # Tab 2: Chart View
        chart_tab = QWidget()
        chart_layout = QVBoxLayout(chart_tab)

        # Create chart
        chart_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        chart_ax = chart_canvas.figure.subplots()

        # Create bar chart of mean prices by group
        stats_df['Mean Price'].plot(kind='bar', ax=chart_ax, color='#4a86e8')
        chart_ax.set_title('Average Price by Group')
        chart_ax.set_xlabel('Group')
        chart_ax.set_ylabel('Average Price')
        chart_ax.tick_params(axis='x', rotation=45)

        # Add value labels on top of bars
        for i, v in enumerate(stats_df['Mean Price']):
            chart_ax.text(i, v + 1, f"{v:.2f}", ha='center')

        chart_canvas.figure.tight_layout()
        chart_layout.addWidget(chart_canvas)

        # Add combo box to select different statistics to view
        stat_selector = QComboBox()
        stat_selector.addItems(stats_df.columns)
        stat_selector.setCurrentText('Mean Price')
        chart_layout.addWidget(stat_selector)

        # Connect combo box to update chart
        def update_stat_chart():
            selected_stat = stat_selector.currentText()
            chart_ax.clear()
            stats_df[selected_stat].plot(kind='bar', ax=chart_ax, color='#4a86e8')
            chart_ax.set_title(f'{selected_stat} by Group')
            chart_ax.set_xlabel('Group')
            chart_ax.set_ylabel(selected_stat)
            chart_ax.tick_params(axis='x', rotation=45)

            # Add value labels
            for i, v in enumerate(stats_df[selected_stat]):
                chart_ax.text(i, v + (v * 0.05), f"{v:.2f}", ha='center')

            chart_canvas.figure.tight_layout()
            chart_canvas.draw()

        stat_selector.currentIndexChanged.connect(update_stat_chart)

        tabs.addTab(chart_tab, "Chart View")

        # Tab 3: Pie Chart View
        pie_tab = QWidget()
        pie_layout = QVBoxLayout(pie_tab)

        pie_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        pie_ax = pie_canvas.figure.subplots()

        # Create pie chart of market share
        group_sums = grouped['Price'].sum()
        pie_ax.pie(group_sums, labels=group_sums.index, autopct='%1.1f%%',
                   startangle=90, shadow=True, explode=[0.05] * len(group_sums))
        pie_ax.set_title('Market Share by Group')
        pie_ax.axis('equal')

        pie_canvas.figure.tight_layout()
        pie_layout.addWidget(pie_canvas)
        tabs.addTab(pie_tab, "Pie Chart")

        # Add tabs to layout
        layout.addWidget(tabs)

        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec()

    def show_about(self):
        QMessageBox.about(
            self,
            "About Stock Market Analysis",
            """<h1>Stock Market Analysis</h1>
            <p>Version 1.0</p>
            <p>A comprehensive application for analyzing stock market data.</p>
            <p>Features:</p>
            <ul>
                <li>Display and sort stock data</li>
                <li>Search and modify prices</li>
                <li>Add and delete records</li>
                <li>Group statistics and analysis</li>
                <li>Interactive charts and visualizations</li>
            </ul>
            """
        )

    def refresh_all(self):
        self.update_table()
        self.update_charts()
        self.status_bar.showMessage("Data refreshed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockAnalysisApp()
    window.show()
    sys.exit(app.exec())