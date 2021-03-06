# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'posconv.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PosConv(object):
    def setupUi(self, PosConv):
        PosConv.setObjectName("PosConv")
        PosConv.resize(708, 431)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(PosConv)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.paramLayout = QtWidgets.QVBoxLayout()
        self.paramLayout.setObjectName("paramLayout")
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        self.calculateButton = QtWidgets.QRadioButton(PosConv)
        self.calculateButton.setChecked(True)
        self.calculateButton.setObjectName("calculateButton")
        self.buttonLayout.addWidget(self.calculateButton)
        self.simulateButton = QtWidgets.QRadioButton(PosConv)
        self.simulateButton.setObjectName("simulateButton")
        self.buttonLayout.addWidget(self.simulateButton)
        self.paramLayout.addLayout(self.buttonLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pulsesPerRotationLabel = QtWidgets.QLabel(PosConv)
        self.pulsesPerRotationLabel.setObjectName("pulsesPerRotationLabel")
        self.horizontalLayout_3.addWidget(self.pulsesPerRotationLabel)
        self.pulsesPerRotationBox = QtWidgets.QSpinBox(PosConv)
        self.pulsesPerRotationBox.setMinimum(1)
        self.pulsesPerRotationBox.setMaximum(9999)
        self.pulsesPerRotationBox.setObjectName("pulsesPerRotationBox")
        self.horizontalLayout_3.addWidget(self.pulsesPerRotationBox)
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rpmLabel = QtWidgets.QLabel(PosConv)
        self.rpmLabel.setEnabled(False)
        self.rpmLabel.setObjectName("rpmLabel")
        self.horizontalLayout_2.addWidget(self.rpmLabel)
        self.rpmBox = QtWidgets.QSpinBox(PosConv)
        self.rpmBox.setEnabled(False)
        self.rpmBox.setMinimum(1)
        self.rpmBox.setMaximum(9999)
        self.rpmBox.setObjectName("rpmBox")
        self.horizontalLayout_2.addWidget(self.rpmBox)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.paramLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(PosConv)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.directionComboBox = QtWidgets.QComboBox(PosConv)
        self.directionComboBox.setObjectName("directionComboBox")
        self.directionComboBox.addItem("")
        self.directionComboBox.addItem("")
        self.horizontalLayout_4.addWidget(self.directionComboBox)
        self.paramLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.paramLayout)
        self.fileLayout = QtWidgets.QHBoxLayout()
        self.fileLayout.setObjectName("fileLayout")
        self.fileList = QtWidgets.QListWidget(PosConv)
        self.fileList.setObjectName("fileList")
        item = QtWidgets.QListWidgetItem()
        self.fileList.addItem(item)
        self.fileLayout.addWidget(self.fileList)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addDirButton = QtWidgets.QPushButton(PosConv)
        self.addDirButton.setObjectName("addDirButton")
        self.verticalLayout.addWidget(self.addDirButton)
        self.addButton = QtWidgets.QPushButton(PosConv)
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton)
        self.line = QtWidgets.QFrame(PosConv)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.removeButton = QtWidgets.QPushButton(PosConv)
        self.removeButton.setObjectName("removeButton")
        self.verticalLayout.addWidget(self.removeButton)
        self.clearButton = QtWidgets.QPushButton(PosConv)
        self.clearButton.setObjectName("clearButton")
        self.verticalLayout.addWidget(self.clearButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.processButton = QtWidgets.QPushButton(PosConv)
        self.processButton.setEnabled(False)
        self.processButton.setObjectName("processButton")
        self.verticalLayout.addWidget(self.processButton)
        self.fileLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.fileLayout)

        self.retranslateUi(PosConv)
        QtCore.QMetaObject.connectSlotsByName(PosConv)

    def retranslateUi(self, PosConv):
        _translate = QtCore.QCoreApplication.translate
        PosConv.setWindowTitle(_translate("PosConv", "POSCONV - Position Log Converter"))
        self.calculateButton.setText(_translate("PosConv", "Ca&lculate arena frame"))
        self.simulateButton.setText(_translate("PosConv", "Sim&ulate arena frame"))
        self.pulsesPerRotationLabel.setText(_translate("PosConv", "Pulses per rotation"))
        self.rpmLabel.setText(_translate("PosConv", "Seconds per revolution"))
        self.label.setText(_translate("PosConv", "Arena rotation direction"))
        self.directionComboBox.setItemText(0, _translate("PosConv", "CW"))
        self.directionComboBox.setItemText(1, _translate("PosConv", "CCW"))
        __sortingEnabled = self.fileList.isSortingEnabled()
        self.fileList.setSortingEnabled(False)
        item = self.fileList.item(0)
        item.setText(_translate("PosConv", "Add files..."))
        self.fileList.setSortingEnabled(__sortingEnabled)
        self.addDirButton.setText(_translate("PosConv", "Add directory"))
        self.addButton.setText(_translate("PosConv", "Add files"))
        self.removeButton.setText(_translate("PosConv", "Remove files"))
        self.clearButton.setText(_translate("PosConv", "Clear list"))
        self.processButton.setText(_translate("PosConv", "Process"))

