# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/tool_ps_toolbar.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ToolPSToolBar(object):
    def setupUi(self, ToolPSToolBar):
        ToolPSToolBar.setObjectName("ToolPSToolBar")
        ToolPSToolBar.resize(905, 131)
        ToolPSToolBar.setWindowTitle("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(ToolPSToolBar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(ToolPSToolBar)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        self.minDateEdit = QtWidgets.QDateEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minDateEdit.sizePolicy().hasHeightForWidth())
        self.minDateEdit.setSizePolicy(sizePolicy)
        self.minDateEdit.setCalendarPopup(True)
        self.minDateEdit.setObjectName("minDateEdit")
        self.gridLayout_4.addWidget(self.minDateEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.maxDateEdit = QtWidgets.QDateEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxDateEdit.sizePolicy().hasHeightForWidth())
        self.maxDateEdit.setSizePolicy(sizePolicy)
        self.maxDateEdit.setCalendarPopup(True)
        self.maxDateEdit.setObjectName("maxDateEdit")
        self.gridLayout_4.addWidget(self.maxDateEdit, 1, 1, 1, 1)
        self.refreshScaleButton = QtWidgets.QToolButton(self.groupBox)
        self.refreshScaleButton.setObjectName("refreshScaleButton")
        self.gridLayout_4.addWidget(self.refreshScaleButton, 1, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.minYEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minYEdit.sizePolicy().hasHeightForWidth())
        self.minYEdit.setSizePolicy(sizePolicy)
        self.minYEdit.setObjectName("minYEdit")
        self.horizontalLayout_2.addWidget(self.minYEdit)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setIndent(4)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.maxYEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxYEdit.sizePolicy().hasHeightForWidth())
        self.maxYEdit.setSizePolicy(sizePolicy)
        self.maxYEdit.setObjectName("maxYEdit")
        self.horizontalLayout_2.addWidget(self.maxYEdit)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 2, 0, 1, 3)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(ToolPSToolBar)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.replicaUpCheck = QtWidgets.QCheckBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replicaUpCheck.sizePolicy().hasHeightForWidth())
        self.replicaUpCheck.setSizePolicy(sizePolicy)
        self.replicaUpCheck.setObjectName("replicaUpCheck")
        self.gridLayout_5.addWidget(self.replicaUpCheck, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.replicaDistEdit = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replicaDistEdit.sizePolicy().hasHeightForWidth())
        self.replicaDistEdit.setSizePolicy(sizePolicy)
        self.replicaDistEdit.setText("28")
        self.replicaDistEdit.setObjectName("replicaDistEdit")
        self.horizontalLayout_3.addWidget(self.replicaDistEdit)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.replicaDownCheck = QtWidgets.QCheckBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replicaDownCheck.sizePolicy().hasHeightForWidth())
        self.replicaDownCheck.setSizePolicy(sizePolicy)
        self.replicaDownCheck.setObjectName("replicaDownCheck")
        self.gridLayout_5.addWidget(self.replicaDownCheck, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(ToolPSToolBar)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.hGridCheck = QtWidgets.QCheckBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hGridCheck.sizePolicy().hasHeightForWidth())
        self.hGridCheck.setSizePolicy(sizePolicy)
        self.hGridCheck.setObjectName("hGridCheck")
        self.gridLayout_3.addWidget(self.hGridCheck, 0, 0, 1, 1)
        self.vGridCheck = QtWidgets.QCheckBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vGridCheck.sizePolicy().hasHeightForWidth())
        self.vGridCheck.setSizePolicy(sizePolicy)
        self.vGridCheck.setObjectName("vGridCheck")
        self.gridLayout_3.addWidget(self.vGridCheck, 1, 0, 1, 1)
        self.linesCheck = QtWidgets.QCheckBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linesCheck.sizePolicy().hasHeightForWidth())
        self.linesCheck.setSizePolicy(sizePolicy)
        self.linesCheck.setObjectName("linesCheck")
        self.gridLayout_3.addWidget(self.linesCheck, 2, 0, 1, 1)
        self.linRegrCheck = QtWidgets.QCheckBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linRegrCheck.sizePolicy().hasHeightForWidth())
        self.linRegrCheck.setSizePolicy(sizePolicy)
        self.linRegrCheck.setObjectName("linRegrCheck")
        self.gridLayout_3.addWidget(self.linRegrCheck, 0, 1, 1, 1)
        self.smoothCheck = QtWidgets.QCheckBox(self.groupBox_3)
        self.smoothCheck.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smoothCheck.sizePolicy().hasHeightForWidth())
        self.smoothCheck.setSizePolicy(sizePolicy)
        self.smoothCheck.setObjectName("smoothCheck")
        self.gridLayout_3.addWidget(self.smoothCheck, 3, 0, 1, 1)
        self.labelsCheck = QtWidgets.QCheckBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelsCheck.sizePolicy().hasHeightForWidth())
        self.labelsCheck.setSizePolicy(sizePolicy)
        self.labelsCheck.setObjectName("labelsCheck")
        self.gridLayout_3.addWidget(self.labelsCheck, 4, 0, 1, 1)
        self.polyRegrCheck = QtWidgets.QCheckBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polyRegrCheck.sizePolicy().hasHeightForWidth())
        self.polyRegrCheck.setSizePolicy(sizePolicy)
        self.polyRegrCheck.setObjectName("polyRegrCheck")
        self.gridLayout_3.addWidget(self.polyRegrCheck, 1, 1, 1, 1)
        self.detrendingCheck = QtWidgets.QCheckBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detrendingCheck.sizePolicy().hasHeightForWidth())
        self.detrendingCheck.setSizePolicy(sizePolicy)
        self.detrendingCheck.setObjectName("detrendingCheck")
        self.gridLayout_3.addWidget(self.detrendingCheck, 2, 1, 1, 1)
        self.legendCheck = QtWidgets.QCheckBox(self.groupBox_3)
        self.legendCheck.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.legendCheck.sizePolicy().hasHeightForWidth())
        self.legendCheck.setSizePolicy(sizePolicy)
        self.legendCheck.setObjectName("legendCheck")
        self.gridLayout_3.addWidget(self.legendCheck, 3, 1, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(ToolPSToolBar)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)
        self.xLabelEdit = QtWidgets.QLineEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xLabelEdit.sizePolicy().hasHeightForWidth())
        self.xLabelEdit.setSizePolicy(sizePolicy)
        self.xLabelEdit.setObjectName("xLabelEdit")
        self.gridLayout_2.addWidget(self.xLabelEdit, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setIndent(4)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.yLabelEdit = QtWidgets.QLineEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yLabelEdit.sizePolicy().hasHeightForWidth())
        self.yLabelEdit.setSizePolicy(sizePolicy)
        self.yLabelEdit.setObjectName("yLabelEdit")
        self.gridLayout_2.addWidget(self.yLabelEdit, 1, 1, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(ToolPSToolBar)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName("gridLayout")
        self.titleParam0Edit = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleParam0Edit.sizePolicy().hasHeightForWidth())
        self.titleParam0Edit.setSizePolicy(sizePolicy)
        self.titleParam0Edit.setObjectName("titleParam0Edit")
        self.gridLayout.addWidget(self.titleParam0Edit, 0, 0, 1, 1)
        self.titleParam0Combo = QtWidgets.QComboBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleParam0Combo.sizePolicy().hasHeightForWidth())
        self.titleParam0Combo.setSizePolicy(sizePolicy)
        self.titleParam0Combo.setObjectName("titleParam0Combo")
        self.gridLayout.addWidget(self.titleParam0Combo, 0, 1, 1, 1)
        self.titleParam1Edit = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleParam1Edit.sizePolicy().hasHeightForWidth())
        self.titleParam1Edit.setSizePolicy(sizePolicy)
        self.titleParam1Edit.setObjectName("titleParam1Edit")
        self.gridLayout.addWidget(self.titleParam1Edit, 1, 0, 1, 1)
        self.titleParam1Combo = QtWidgets.QComboBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleParam1Combo.sizePolicy().hasHeightForWidth())
        self.titleParam1Combo.setSizePolicy(sizePolicy)
        self.titleParam1Combo.setObjectName("titleParam1Combo")
        self.gridLayout.addWidget(self.titleParam1Combo, 1, 1, 1, 1)
        self.titleParam2Edit = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleParam2Edit.sizePolicy().hasHeightForWidth())
        self.titleParam2Edit.setSizePolicy(sizePolicy)
        self.titleParam2Edit.setObjectName("titleParam2Edit")
        self.gridLayout.addWidget(self.titleParam2Edit, 2, 0, 1, 1)
        self.titleParam2Combo = QtWidgets.QComboBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleParam2Combo.sizePolicy().hasHeightForWidth())
        self.titleParam2Combo.setSizePolicy(sizePolicy)
        self.titleParam2Combo.setObjectName("titleParam2Combo")
        self.gridLayout.addWidget(self.titleParam2Combo, 2, 1, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_5)

        self.retranslateUi(ToolPSToolBar)
        QtCore.QMetaObject.connectSlotsByName(ToolPSToolBar)

    def retranslateUi(self, ToolPSToolBar):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(_translate("ToolPSToolBar", "Scale options"))
        self.label.setText(_translate("ToolPSToolBar", "Min date"))
        self.minDateEdit.setDisplayFormat(_translate("ToolPSToolBar", "dd/MM/yyyy"))
        self.label_2.setText(_translate("ToolPSToolBar", "Max date"))
        self.maxDateEdit.setDisplayFormat(_translate("ToolPSToolBar", "dd/MM/yyyy"))
        self.refreshScaleButton.setToolTip(_translate("ToolPSToolBar", "Update"))
        self.refreshScaleButton.setText(_translate("ToolPSToolBar", "..."))
        self.label_3.setText(_translate("ToolPSToolBar", "Min Y"))
        self.label_4.setText(_translate("ToolPSToolBar", "Max Y"))
        self.groupBox_2.setTitle(_translate("ToolPSToolBar", "Replica"))
        self.replicaUpCheck.setText(_translate("ToolPSToolBar", "Up"))
        self.label_5.setText(_translate("ToolPSToolBar", "[mm]"))
        self.replicaDownCheck.setText(_translate("ToolPSToolBar", "Down"))
        self.groupBox_3.setTitle(_translate("ToolPSToolBar", "Chart options"))
        self.hGridCheck.setText(_translate("ToolPSToolBar", "H grid"))
        self.vGridCheck.setText(_translate("ToolPSToolBar", "V grid"))
        self.linesCheck.setText(_translate("ToolPSToolBar", "Lines"))
        self.linRegrCheck.setText(_translate("ToolPSToolBar", "Lin trend"))
        self.smoothCheck.setText(_translate("ToolPSToolBar", "Smooth"))
        self.labelsCheck.setText(_translate("ToolPSToolBar", "Labels"))
        self.polyRegrCheck.setText(_translate("ToolPSToolBar", "Poly trend"))
        self.detrendingCheck.setText(_translate("ToolPSToolBar", "Detrending"))
        self.legendCheck.setText(_translate("ToolPSToolBar", "Legend"))
        self.groupBox_4.setTitle(_translate("ToolPSToolBar", "Chart axis labels"))
        self.label_6.setText(_translate("ToolPSToolBar", "X axis \n"
"label"))
        self.xLabelEdit.setText(_translate("ToolPSToolBar", "[Date]"))
        self.label_7.setText(_translate("ToolPSToolBar", "Y axis \n"
"label"))
        self.yLabelEdit.setText(_translate("ToolPSToolBar", "[mm]"))
        self.groupBox_5.setTitle(_translate("ToolPSToolBar", "Chart title"))
        self.titleParam0Edit.setText(_translate("ToolPSToolBar", "coher.:"))
        self.titleParam1Edit.setText(_translate("ToolPSToolBar", "vel.:"))
        self.titleParam2Edit.setText(_translate("ToolPSToolBar", "v_stdev.:"))

