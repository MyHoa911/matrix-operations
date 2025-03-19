import sys
from PyQt6.QtWidgets import QApplication

from Bonus.bonus import CurriculumChartApp


def main():
    app = QApplication(sys.argv)
    window = CurriculumChartApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()