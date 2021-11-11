from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QComboBox, QMainWindow, QApplication, QFileDialog, QMessageBox
import sys

from SLtool import SLtool

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("main.ui", self)
        self.setWindowTitle("SL tool")
        self.setStyleSheet('''QMainWindow{background-color:rgb(255,255,255)}''')
        self.setFixedSize(600, 200)
        self.show()

        self.SLtool = SLtool()
        self.fileRoot = self.SLtool.fileRoot
        self.SaveRoot = self.SLtool.targetRoot
        self.fileList = self.SLtool.fileList
        self.currIdx = self.SLtool.currIdx

        self.comboBox.setMaxVisibleItems(5)
        self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self._updateRoot()
        self._updateComboBox()
        
        self.comboBox.currentTextChanged.connect(self.slotChangeIdx)
        self.pushButtonChangeRoot.clicked.connect(self.slotChangeRoot)
        self.pushButtonSave.clicked.connect(self.slotSave)
        self.pushButtonLoad.clicked.connect(self.slotLoad)

    def _updateInfo(self):
        self.fileRoot = self.SLtool.fileRoot
        self.SaveRoot = self.SLtool.targetRoot
        self.fileList = self.SLtool.fileList
        self.currIdx = self.SLtool.currIdx

    def slotChangeRoot(self):
        fileRoot = QFileDialog.getExistingDirectory()
        if fileRoot != '':
            self.fileRoot = fileRoot
            self.SLtool.changeFileRoot(fileRoot)
            self._updateRoot()
    
    def slotChangeIdx(self, text):
        if text in self.fileList:
            self.currIdx = self.fileList.index(text)
            self.SLtool.changeIdx(self.currIdx)
            self.labelNotice.setText("默认存档更改为 " + text)
    
    def slotSave(self):
        if not self.SLtool.copyFile():
            QMessageBox.warning(self, "Error!", "备份失败!", QMessageBox.Ok)
        else:
            self._updateInfo()
            self.labelNotice.setText("备份成功 " + self.fileList[self.currIdx])
            self._updateComboBox()

    def slotLoad(self):
        if not self.SLtool.loadFile():
            QMessageBox.warning(self, "Error!", "读档失败!", QMessageBox.Ok)
        else:
            self._updateInfo()
            self.labelNotice.setText("读档成功 " + self.fileList[self.currIdx])

    def _updateRoot(self):
        self.labelFileRoot.setText(self.fileRoot)

    def _updateComboBox(self):
        self.comboBox.clear()
        self.comboBox.addItems(self.fileList)
        if len(self.fileList):
            self.comboBox.setCurrentText(self.fileList[self.currIdx])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())