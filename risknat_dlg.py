# -*- coding: utf-8 -*-

"""
/****************************************************************************
Name			 	: RiskNat
Description			: RiskNat plugin
Date				: Jul 25, 2012 
copyright			: (C) 2012 by Giuseppe Sucameli (Faunalia)
email				: brush.tyler@gmail.com
 ****************************************************************************/

/****************************************************************************
 *																			*
 *	This program is free software; you can redistribute it and/or modify	*
 *	it under the terms of the GNU General Public License as published by	*
 *	the Free Software Foundation; either version 2 of the License, or		*
 *	(at your option) any later version.										*
 *																			*
 ****************************************************************************/
"""

from PyQt4 import QtGui, QtCore

from .plot_wdg import PlotDlg, PlotWdg, ClippedLine2D
import resources_rc

class RiskNatDlg(PlotDlg):

	def __init__(self, vl, fieldMap, parent=None):
		PlotDlg.__init__(self, parent=parent)
		self.setWindowTitle("RiskNat")

		self._vl = vl
		self._fieldMap = fieldMap
		self._feat = None

		self.toolbar = RiskNatToolbar( self )
		self.layout().insertWidget( self.plot, self.toolbar )

		self.toolbar.init( self._fieldMap )
		QObject.connect( self.toolbar, QtCore.SIGNAL("updateLimits"), self.plot.setLimits)
		QObject.connect( self.toolbar, QtCore.SIGNAL("updateReplicas"), self.plot.setReplicas)
		QObject.connect( self.toolbar, QtCore.SIGNAL("updateGrids"), self.plot.displayGrids)
		QObject.connect( self.toolbar, QtCore.SIGNAL("updateOptions"), self.updateOptions)
		QObject.connect( self.toolbar, QtCore.SIGNAL("updateLabels"), self.self.plot.setLabels)
		QObject.connect( self.toolbar, QtCore.SIGNAL("updateTitle"), self.updateTitle)

	def createPlot(self):
		return PlotGraph()

	def setFeatureId(self, fid):
		feat = QgsFeature()
		if not self._vl.featureAtId( fid, feat, False, self._fieldMap ):
			feat = None
		self._feat = feat
		return self._feat is not None


	def updateOptions(self, options):
		""" update the chart options """
		#self.plot.displayLines( options['lines'] )
		#self.plot.displayLegend( options['legend'] )
		#self.plot.setSmooth( options['smooth'] )
		self.plot.displayLinearRegression( options['linregr'] )

	def updateTitle(self, params):
		""" update the chart title """
		title = u""

		if self._feat:
			attrs = self._feat.attributeMap()

			# add the PS code
			for idx, fld in self._fieldMap.iteritems():
				if not fld.name().toLower().startWith( "code" ):
					continue
				title = u"PS: %s" % attrs[ idx ]

			# add the user-defined values
			for label, fldIdx in params:
				title += u" %s: %s" % ( label, attrs[ fldIdx ] )

		self.plot.setTitle( title )


class PlotGraph(PlotWdg):

	def __init__(self, *args, **kwargs):
		PlotWdg.__init__(self,	*args, **kwargs)

		self._linRegr = None
		self._upReplica = None
		self._downReplica = None

	def _plot(self):
		items = self._callPlotFunc('scatter', self.x, self.y, marker='s', c='k')
		self.collections.append( items )


	def displayGrids(self, hgrid=False, vgrid=False):
		self.xaxis.grid(hgrid, 'major')
		self.yaxis.grid(vgrid, 'major')

	def displayLinearRegression(self, show=True):
		import numpy as np
		x = np.array(self._x)
		y = np.array(self._y)
		p = np.polyfit(x, y, 1)
		y_lr = np.polyval(z, x)

		self._linRegr = self._callPlotFunc('plot', x, y_lr, c='r')
		self.collections.append( self._linRegr )

	def setReplicas(self, dist, positions):
		""" set up and/or down replicas for the graph """
		up, down = positions

		if self._upReplica:
			self.collections.remove( self._upReplica )
			self._upReplica.remove()
			self._upReplica = None

		if up:
			y = map(lambda v: v+dist, self.y)
			self._upReplica = self._callPlotFunc('scatter', self.x, y, marker='s', c='b')
			self.collections.append( self._upReplica )

		if self._downReplica:
			self.collections.remove( self._downReplica )
			self._downReplica.remove()
			self._downReplica = None

		if down:
			y = map(lambda v: v-dist, self.y)
			self._downReplica = self._callPlotFunc('scatter', self.x, y, marker='s', c='b')
			self.collections.append( self._downReplica )



from .ui.risknat_toolbar_ui import Ui_RiskNatToolBar 

class RiskNatToolbar(QtGui.QWidget, Ui_RiskNatToolBar):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)

		# limits group
		#self.connect(self.minDateEdit, QtCore.SIGNAL("dateChanged(const QDate &)"), self.updateLimits)
		#self.connect(self.maxDateEdit, QtCore.SIGNAL("dateChanged(const QDate &)"), self.updateLimits)
		#self.connect(self.minYEdit, QtCore.SIGNAL("valueChanged(const QString &)"), self.updateLimits)
		#self.connect(self.minYEdit, QtCore.SIGNAL("valueChanged(const QString &)"), self.updateLimits)
		self.connect(self.refreshScaleBtn, QtCore.SIGNAL("clicked()"), self.updateLimits)

		# replica group
		self.connect(self.replicaUpCheck, QtCore.SIGNAL("toggled(bool)"), self.updateReplicas)
		self.connect(self.replicaDownCheck, QtCore.SIGNAL("toggled(bool)"), self.updateReplicas)
		self.connect(self.replicaDistCheck, QtCore.SIGNAL("valueChanged(const QString &)"), self.updateReplicas)

		# labels group
		self.connect(self.xLabelEdit, QtCore.SIGNAL("valueChanged(const QString &)"), self.updateLabels)
		self.connect(self.yLabelEdit, QtCore.SIGNAL("valueChanged(const QString &)"), self.updateLabels)

		# title group
		for i in range(3):
			edit = getattr(self, "titleParam%dEdit" % i)
			self.connect(edit, QtCore.SIGNAL("valueChanged(const QString &)"), self.updateTitle)
			combo = getattr(self, "titleParam%dCombo" % i)
			self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self.updateTitle)

		# options group
		self.connect(self.hGridCheck, QtCore.SIGNAL("toggled(bool)"), self.updateGrids)
		self.connect(self.vGridCheck, QtCore.SIGNAL("toggled(bool)"), self.updateGrids)
		self.connect(self.labelsCheck, QtCore.SIGNAL("toggled(bool)"), self.updateLabels)
		self.connect(self.linesCheck, QtCore.SIGNAL("toggled(bool)"), self.updateOptions)
		self.connect(self.linRegrCheck, QtCore.SIGNAL("toggled(bool)"), self.updateOptions)
		self.connect(self.smoothCheck, QtCore.SIGNAL("toggled(bool)"), self.updateOptions)
		self.connect(self.legendCheck, QtCore.SIGNAL("toggled(bool)"), self.updateOptions)

	def init(self, fieldMap):
		populateTitleParamCombos(fieldMap)

	def populateTitleParamCombos(self, fieldMap):
		""" populate the title param combos """
		for i in range(3):
			combo = getattr(self, "titleParam%dCombo" % i)
			# populate the title param combo with fields
			for fldIdx, fld in fieldMap.iteritems():
				combo.addItem( fld.name(), QVariant(fldIndex) )
			# do not select the same item in each combo
			combo.setCurrentIndex( i if i < combo.count() else combo.count()-1 )
		
	def updateReplicas(self):
		""" request the graph replicas updating """
		dist = self.replicaDistEdit.text()
		upReplica = self.replicaUpCheck.isChecked()
		downReplica = self.replicaDownCheck.isChecked()
		self.emit( QtCore.SIGNAL("updateReplicas"), dist, (upReplica, downReplica) )

	def updateGrids(self):
		""" request the chart grids updating """
		hgrid = self.hGridCheck.isChecked()
		vgrid = self.vGridCheck.isChecked()
		self.emit( QtCore.SIGNAL("updateGrids"), hgrid, vgrid )

	def updateOptions(self):
		""" request the chart options updating """
		options = {
			'lines': self.linesCheck.isChecked()
			'libregr': self.linRegrCheck.isChecked()
			'smooth': self.smoothCheck.isChecked()
			'legend': self.legendCheck.isChecked()

		self.emit( QtCore.SIGNAL("updateOptions"), options )

	def updateLimits(self):
		""" request the chart axis limits updating """
		xLimits = (self.minDateEdit.date().toPyDate(), self.maxDateEdit.date().toPyDate())
		yLimits = (self.minYEdit.text().toInt()[0], self.maxYEdit.text().toInt()[0])
		self.emit( QtCore.SIGNAL("updateLimits"), xLimits, yLimits )

	def updateLabels(self):
		""" request the chart axis labels updating """
		if self.labelsCheck.isChecked():
			xLabel = self.xLabelEdit.text()
			yLabel = self.yLabelEdit.text()
		else:
			xLabel = None
			yLabel = None
		self.emit( QtCore.SIGNAL("updateLabels"), xLabel, yLabel )

	def updateTitle(self):
		""" request the chart title updating """
		params = []

		for i in range(3):
			# get param label
			label = getattr(self, "titleParam%dEdit" % i).text()
			# get param value
			combo = getattr(self, "titleParam%dCombo" % i)
			fldIdx = combo.itemData( combo.currentIndex() )
			params.append( (label, fldIdx) )

		self.emit( QtCore.SIGNAL("updateTitle"), params)

