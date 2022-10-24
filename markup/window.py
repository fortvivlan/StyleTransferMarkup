import os
import pickle
import PyQt5.QtWidgets as qtwidgets
import PyQt5.QtGui as qtgui
import PyQt5.QtCore as qtcore
from time import time
from markup.handler import Handler
from markup.statwindow import Stats


class Window(qtwidgets.QMainWindow):
    """
    Main window class for the program, handles GUI
    """
    def __init__(self, parent = None):
        super().__init__(parent)
        self.restore = self._getsaved()
        self.handler = Handler(self.restore['result'], self.restore['index'], self.restore['path'])
        self.path = self.restore['path']
        self.InitUI()

    def InitUI(self):
        self.settings = qtcore.QSettings('ABBYY', 'Style Transfer Markup')
        self.resize(self.settings.value("size", qtcore.QSize(1250, 600)))
        self.move(self.settings.value("pos", qtcore.QPoint(50, 50)))
        wid = qtwidgets.QWidget(self)
        self.setCentralWidget(wid)
        grid = qtwidgets.QVBoxLayout()
        wid.setLayout(grid)

        self.setWindowTitle('Style Transfer Markup')
        self.setWindowIcon(qtgui.QIcon('markup/style/mainico.png'))

        self._createActions()
        self._createMenuBar()
        self._createToolBars()

        # I want my favourite font!
        fontId = qtgui.QFontDatabase.addApplicationFont("markup/style/maiola.ttf")
        if fontId < 0:
            print('font not loaded')
        families = qtgui.QFontDatabase.applicationFontFamilies(fontId)
        
        # donor for raw text, recipient for rewritten text
        self.donor = qtwidgets.QPlainTextEdit(self)
        self.donor.setReadOnly(True)
        self.recipient = qtwidgets.QPlainTextEdit(self)
        grid.addWidget(self.donor)
        grid.addWidget(self.recipient)
        f = qtgui.QFont(families[0], 14)
        self.donor.setFont(f)
        self.recipient.setFont(f)
        # If there has been some labelled text
        if self.handler.result:
            self.donor.insertPlainText(self.handler.result[self.handler.index].original)
            self.recipient.insertPlainText(self.handler.result[self.handler.index].rewritten)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)

    def _createToolBars(self):
        toolbar = self.addToolBar('Next')
        toolbar.addAction(self.backAction)
        toolbar.addAction(self.nextAction)
        toolbar.addAction(self.timerAction)
        toolbar.addAction(self.statsAction)
        # to display number of text
        self.counter = qtwidgets.QLineEdit()
        self.counter.setFixedWidth(60)
        self.counter.setReadOnly(True)
        self.counter.setText(str(self.handler.index + 1))
        toolbar.addWidget(self.counter)
        # to display total count
        self.total = qtwidgets.QLineEdit()
        self.total.setFixedWidth(60)
        self.total.setReadOnly(True)
        self.total.setText(str(len(self.handler.result)))
        toolbar.addWidget(self.total)

    def _createActions(self):
        self.openAction = qtwidgets.QAction('&Open')
        self.openAction.setText('&Open')
        self.openAction.setShortcut(qtgui.QKeySequence.Open)
        self.openAction.triggered.connect(self.openFile)

        self.saveAction = qtwidgets.QAction('&Save')
        self.saveAction.setText('&Save')
        self.saveAction.setShortcut(qtgui.QKeySequence.Save)
        self.saveAction.triggered.connect(self.handler.save)

        self.nextAction = qtwidgets.QAction(qtgui.QIcon('markup/style/next.png'), '&Next')
        self.nextAction.setText('&Next')
        self.nextAction.setShortcut(qtcore.Qt.Key_Right)
        self.nextAction.triggered.connect(self.nextSent)

        self.backAction = qtwidgets.QAction(qtgui.QIcon('markup/style/back.png'), '&Back')
        self.backAction.setText('&Back')
        self.backAction.setShortcut(qtcore.Qt.Key_Left)
        self.backAction.triggered.connect(self.prevSent)

        self.timerAction = qtwidgets.QAction(qtgui.QIcon('markup/style/timergray.png'), '&Timer')
        self.timerAction.setText('&Timer')
        self.timerAction.setShortcut(qtgui.QKeySequence('Ctrl+T'))
        self.timerAction.triggered.connect(self.timerswitch)

        self.statsAction = qtwidgets.QAction(qtgui.QIcon('markup/style/stats.png'), '&Statistics')
        self.statsAction.setText('&Statistics')
        self.statsAction.triggered.connect(self.stats)

    def openFile(self):
        text = self.handler.open()
        if text == 'not txt':
            qtwidgets.QMessageBox.about(self, 'Error', 'Your encoding should be UTF-8')
        elif not text:
            qtwidgets.QMessageBox.about(self, 'Error', 'Open .txt file')
        else:
            self.donor.clear()
            self.recipient.clear()
            self.counter.setText(str(self.handler.index + 1))
            self.donor.insertPlainText(text) 
            self.total.setText(str(len(self.handler.result)))

    def timerswitch(self):
        """timer on|off"""
        if not self.handler.result:
            qtwidgets.QMessageBox.about(self, 'Warning', 'Open .txt file')
            return
        if self.handler.timecheck: 
            self.timerAction.setIcon(qtgui.QIcon('markup/style/timergray.png'))
            self.handler.result[self.handler.index].time += time() - self.handler.timesave
            self.handler.timecheck = False 
        else:
            self.timerAction.setIcon(qtgui.QIcon('markup/style/timer.png'))
            self.handler.timecheck = True
            self.handler.timesave = time()

    def stats(self):
        """count time statistics"""
        data = self.handler.statscount()
        if data:
            self.statwin = Stats(data)
            self.statwin.show()
        else:
            qtwidgets.QMessageBox.about(self, 'Warning', 'No texts labelled')

    def nextSent(self):
        text = self.handler.roll(self.recipient.toPlainText())
        self.counter.setText(str(self.handler.index + 1))
        self.setOriginal(text)

    def prevSent(self):
        text = self.handler.roll(self.recipient.toPlainText(), False)
        self.counter.setText(str(self.handler.index + 1))
        self.setOriginal(text)

    def _getsaved(self):
        if not os.path.exists('settings.bin'):
            return {'result': [], 'index': 0, 'path': None}
        return pickle.load(open('settings.bin', 'rb'))    

    def setOriginal(self, text):
        """load text into gui"""
        if text:
            self.donor.clear()
            self.donor.insertPlainText(text[0])
            self.recipient.clear()
            self.recipient.insertPlainText(text[1])
        else:
            qtwidgets.QMessageBox.about(self, 'Warning', 'End of list')
        
    def closeEvent(self, e):
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.restore['index'] = self.handler.index
        self.restore['result'] = self.handler.result
        self.restore['path'] = self.handler.file
        pickle.dump(self.restore, open('settings.bin', 'wb'))