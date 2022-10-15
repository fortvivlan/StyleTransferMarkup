import PyQt5.QtWidgets as qtwidgets
import PyQt5.QtGui as qtgui
import PyQt5.QtCore as qtcore


class Stats(qtwidgets.QWidget):
    def __init__(self, data):
        super().__init__()
        
        self.setWindowTitle('Time statistics')
        self.resize(500, 300)
        self.setWindowIcon(qtgui.QIcon('markup/style/stats.png'))
        self.data = data 

        self.createTable()

        self.layout = qtwidgets.QVBoxLayout()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def createTable(self):
        self.table = qtwidgets.QTableWidget(4, 2)
        self.table.setHorizontalHeaderLabels(['Metric', 'Seconds/Sents'])
        self.table.setItem(0, 0, qtwidgets.QTableWidgetItem('Mean'))
        self.table.setItem(0, 1, qtwidgets.QTableWidgetItem(str(self.data[0])))
        self.table.setItem(1, 0, qtwidgets.QTableWidgetItem('Median'))
        self.table.setItem(1, 1, qtwidgets.QTableWidgetItem(str(self.data[1])))
        self.table.setItem(2, 0, qtwidgets.QTableWidgetItem('St. dev.'))
        self.table.setItem(2, 1, qtwidgets.QTableWidgetItem(str(self.data[2])))
        self.table.setItem(3, 0, qtwidgets.QTableWidgetItem('Labelled'))
        self.table.setItem(3, 1, qtwidgets.QTableWidgetItem(str(self.data[3])))

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            qtwidgets.QHeaderView.Stretch)

