# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                : PS Time Series Viewer
Description         : Computation and visualization of time series of speed for 
                    Permanent Scatterers derived from satellite interferometry
Date                : Jul 25, 2012 
copyright           : (C) 2012 by Giuseppe Sucameli (Faunalia)
email               : brush.tyler@gmail.com

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4 import QtGui

from qgis.core import QgsFeature

import numpy as np
from matplotlib.dates import date2num

from .plot_wdg import PlotDlg, PlotWdg, NavigationToolbar
import resources_rc

from .graph_settings_dialog import GraphSettings_Dlg


class PSTimeSeries_Dlg(PlotDlg):

	def __init__(self, vl, fieldMap, parent=None):
		PlotDlg.__init__(self, parent=parent)
		self.setWindowTitle("PS Time Series Viewer")

		self._vl = vl
		self._fieldMap = fieldMap
		self._feat = None

		self.toolbar = ToolPSToolbar( self )
		self.layout().insertWidget( 0, self.toolbar )
		QObject.connect( self, SIGNAL("featureChanged"), self.toolbar.updateInfos )

		QObject.connect( self.nav, SIGNAL("updateRequested"), self.refresh )

		QObject.connect( self.toolbar, SIGNAL("updateLimits"), self.plot.setLimits )
		QObject.connect( self.toolbar, SIGNAL("updateReplicas"), self.plot.setReplicas )
		QObject.connect( self.toolbar, SIGNAL("updateGrids"), self.plot.displayGrids )
		QObject.connect( self.toolbar, SIGNAL("updateOptions"), self.updateOptions )
		QObject.connect( self.toolbar, SIGNAL("updateLabels"), self.plot.updateLabels )
		QObject.connect( self.toolbar, SIGNAL("updateTitle"), self.updateTitle )

		self.toolbar.init( self._fieldMap )

	def createPlot(self):
		return PlotGraph()

	def createToolBar(self):
		return NavToolbar(self.plot, self)

	def setFeatureId(self, fid):
		feat = QgsFeature()
		if not self._vl.featureAtId( fid, feat, False ):
			feat = None
		self._feat = feat

		# update toolbar widgets based on the new feature
		self.emit( SIGNAL("featureChanged") )

		return self._feat is not None


	def showEvent(self, event):
		PlotDlg.showEvent(self, event)
		# update the graph data limits
		self.updateLimits( *self.plot.getLimits() )

	def hideEvent(self, event):
		QtGui.QApplication.restoreOverrideCursor()
		PlotDlg.hideEvent(self, event)

	def refresh(self):
		lim = self.plot.getLimits()

		# change the plot colors/fonts
		self.plot.updateSettings()
		# refresh everything
		self.toolbar.updateAll()
		self.plot._plot()

		self.plot.setLimits( *lim )

	def updateOptions(self, options):
		""" update the chart options """
		self.plot.displayLines( options['lines'] )
		#self.plot.displayLegend( options['legend'] )
		self.plot.displaySmoothLines( options['smooth'] )
		self.plot.displayTrendLine( options['linregr'], 1 )
		self.plot.displayTrendLine( options['polyregr'], 3 )
		self.plot.displayDetrendedValues( options['detrending'] )

	def updateTitle(self, params):
		""" update the chart title """
		title = u""

		if self._feat:
			attrs = self._feat.attributeMap()

			# add the PS code
			for idx, fld in self._fieldMap.iteritems():
				if not fld.name().toLower().startsWith( "code" ):
					continue
				title = u"PS: %s" % attrs[ idx ].toString()

			# add the user-defined values
			for label, fldIdx in params:
				title += u" %s %s" % ( label, attrs[ fldIdx ].toString() )

		self.plot.updateTitle( title )

	def updateLimits(self, xlim, ylim):
		self.toolbar.setLimits( xlim, ylim, True )


class PlotGraph(PlotWdg):

	def __init__(self, *args, **kwargs):
		PlotWdg.__init__(self,	*args, **kwargs)

		self._origY = None
		self._showDetrendedValues = False

		self._points = None
		self._lines = None
		self._smoothLines = None
		self._trendLines = {}
		self._upReplica = None
		self._downReplica = None

		self.updateSettings()

	def updateSettings(self):
		settingsToDict = GraphSettings_Dlg.settingsToDict

		settings = QSettings()

		self._pointsSettings = settingsToDict( settings.value("/pstimeseries/pointsProps", {'marker':'s', 'c':'k'}) )
		self._linesSettings = settingsToDict( settings.value("/pstimeseries/linesProps", {'c':'k'}) )
		self._trendLineSettings = settingsToDict( settings.value("/pstimeseries/linesThrendProps", {'c':'r'}) )
		self._upReplicaSettings = settingsToDict( settings.value("/pstimeseries/pointsReplicasProps", {'marker':'s', 'c':'b'}) )
		self._downReplicaSettings = settingsToDict( settings.value("/pstimeseries/pointsReplicasProps", {'marker':'s', 'c':'b'}) )

		self._titleSettings = settingsToDict( settings.value("/pstimeseries/titleProps", {'fontsize':'large'}) )
		self._labelsSettings = settingsToDict( settings.value("/pstimeseries/labelsProps", {'fontsize':'medium'}) )


	def _plot(self):
		if self._showDetrendedValues:
			self._origY = self.y
			self.y = np.array( self.y ) - np.array( self._getTrendLineData()[1] )
			
		elif self._origY is not None:
			self.y = self._origY
			self._origY = None

		# remove and re-draw points
		self._removeItem( self._points )
		self._points = self._callPlotFunc('scatter', self.x, self.y, **self._pointsSettings)
		self.collections.append( self._points )

		# update lines related to the main plot
		self.displayLines( bool(self._lines) )
		for grade in self._trendLines:
			self.displayTrendLine( True, grade )
		self.displaySmoothLines( bool(self._smoothLines) )


	def displayLines(self, show=True):
		# destroy the lines
		if self._lines:
			self._removeItem( self._lines )
			self._lines = None

		if show:
			lim = self.getLimits()

			self._lines = self._callPlotFunc('plot', self.x, self.y, **self._linesSettings)
			self.collections.append( self._lines )

			self.setLimits( *lim )

		self.draw()

	def _getTrendLineData(self, d=1):
		x = date2num( np.array(self.x) )
		y = np.array(self.y)
		p = np.polyfit(x, y, d)
		return x, np.polyval(p, x)

	def displayTrendLine(self, show=True, grade=1):
		# destroy the trend line
		if grade in self._trendLines:
			self._removeItem( self._trendLines[grade] )
			del self._trendLines[ grade ]

		if show:
			lim = self.getLimits()

			x, y = self._getTrendLineData( grade )
			trendline = self._callPlotFunc('plot', x, y, **self._trendLineSettings)
			self.collections.append( trendline )
			self._trendLines[ grade ] = trendline

			self.setLimits( *lim )

		self.draw()

	def displayDetrendedValues(self, show):
		if self._showDetrendedValues == show:
			return

		self._showDetrendedValues = show
		self._plot()
		self.draw()


	def displaySmoothLines(self, show=True):
		# destroy the smooth line
		if self._smoothLines:
			self._removeItem( self._smoothLines )
			self._smoothLines = None

		if show:
			try:
				from scipy import interpolate
				x = date2num( np.array(self.x) )
				y = np.array(self.y)

				tck = interpolate.splrep(x,y)
				xmin, xmax = np.min(x), np.max(x)
				xnew = np.arange( xmin, xmax, float(xmax-xmin)/len(x)/20.0 )
				ynew = interpolate.splev(xnew, tck, der=0)
			except (ImportError, ValueError):
				return

			lim = self.getLimits()

			self._smoothLines = self._callPlotFunc('plot', xnew, ynew, **self._linesSettings)
			self.collections.append( self._smoothLines )

			self.setLimits( *lim )

		self.draw()


	def updateTitle(self, title):
		self.setTitle(title, fontdict=self._titleSettings)

	def updateLabels(self, xLabel, yLabel):
		self.setLabels(xLabel, yLabel, fontdict=self._labelsSettings)

	def setReplicas(self, dist, positions):
		""" set up and/or down replicas for the graph """
		up, down = positions

		if self._upReplica:
			self._removeItem( self._upReplica )
			self._upReplica = None

		if up:
			y = map(lambda v: v+dist, self.y)
			self._upReplica = self._callPlotFunc('scatter', self.x, y, **self._upReplicaSettings)
			self.collections.append( self._upReplica )

		if self._downReplica:
			self._removeItem( self._downReplica )
			self._downReplica = None

		if down:
			y = map(lambda v: v-dist, self.y)
			self._downReplica = self._callPlotFunc('scatter', self.x, y, **self._downReplicaSettings)
			self.collections.append( self._downReplica )

		self.draw()


from .ui.tool_ps_toolbar_ui import Ui_ToolPSToolBar 

class ToolPSToolbar(QtGui.QWidget, Ui_ToolPSToolBar):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)

		self.legendCheck.hide()
		self.smoothCheck.hide()

		self.refreshScaleButton.setIcon( QtGui.QIcon( ":/pstimeseries_plugin/icons/refresh" ) )

		# limits group
		#self.connect(self.minDateEdit, SIGNAL("dateChanged(const QDate &)"), self.updateLimits)
		#self.connect(self.maxDateEdit, SIGNAL("dateChanged(const QDate &)"), self.updateLimits)
		#self.connect(self.minYEdit, SIGNAL("valueChanged(const QString &)"), self.updateLimits)
		#self.connect(self.minYEdit, SIGNAL("valueChanged(const QString &)"), self.updateLimits)
		self.connect(self.refreshScaleButton, SIGNAL("clicked()"), self.updateLimits)

		# replica group
		self.connect(self.replicaUpCheck, SIGNAL("toggled(bool)"), self.updateReplicas)
		self.connect(self.replicaDownCheck, SIGNAL("toggled(bool)"), self.updateReplicas)
		self.connect(self.replicaDistEdit, SIGNAL("textChanged(const QString &)"), self.updateReplicas)

		# labels group
		self.connect(self.xLabelEdit, SIGNAL("textChanged(const QString &)"), self.updateLabels)
		self.connect(self.yLabelEdit, SIGNAL("textChanged(const QString &)"), self.updateLabels)

		# title group
		for i in range(3):
			edit = getattr(self, "titleParam%dEdit" % i)
			self.connect(edit, SIGNAL("textChanged(const QString &)"), self.updateTitle)
			combo = getattr(self, "titleParam%dCombo" % i)
			self.connect(combo, SIGNAL("currentIndexChanged(int)"), self.updateTitle)

		# options group
		self.connect(self.hGridCheck, SIGNAL("toggled(bool)"), self.updateGrids)
		self.connect(self.vGridCheck, SIGNAL("toggled(bool)"), self.updateGrids)
		self.connect(self.labelsCheck, SIGNAL("toggled(bool)"), self.updateLabels)
		self.connect(self.linesCheck, SIGNAL("toggled(bool)"), self.updateOptions)
		self.connect(self.linRegrCheck, SIGNAL("toggled(bool)"), self.updateOptions)
		self.connect(self.polyRegrCheck, SIGNAL("toggled(bool)"), self.updateOptions)
		self.connect(self.detrendingCheck, SIGNAL("toggled(bool)"), self.updateOptions)
		self.connect(self.smoothCheck, SIGNAL("toggled(bool)"), self.updateOptions)
		self.connect(self.legendCheck, SIGNAL("toggled(bool)"), self.updateOptions)

	def init(self, fieldMap):
		self.populateTitleParamCombos( fieldMap )
		self.labelsCheck.setChecked( True )


	def updateAll(self):
		self.updateTitle()
		self.updateLabels()
		self.updateReplicas()
		self.updateOptions()

	def updateInfos(self):
		self.updateTitle()


	def populateTitleParamCombos(self, fieldMap):
		""" populate the title param combos """
		for i in range(3):
			edit = getattr(self, "titleParam%dEdit" % i)
			combo = getattr(self, "titleParam%dCombo" % i)
			# populate the title param combo with fields
			for fldIdx, fld in fieldMap.iteritems():
				combo.addItem( fld.name(), QVariant( fldIdx ) )
				if fld.name().startsWith( edit.text()[:-2], Qt.CaseInsensitive ):
					combo.setCurrentIndex( combo.count()-1 )
		
	def updateReplicas(self):
		""" request the graph replicas updating """
		dist, ok = self.replicaDistEdit.text().toDouble()
		if not ok:
			return
		upReplica = self.replicaUpCheck.isChecked()
		downReplica = self.replicaDownCheck.isChecked()
		self.emit( SIGNAL("updateReplicas"), dist, (upReplica, downReplica) )

	def updateGrids(self):
		""" request the chart grids updating """
		hgrid = self.hGridCheck.isChecked()
		vgrid = self.vGridCheck.isChecked()
		self.emit( SIGNAL("updateGrids"), hgrid, vgrid )

	def updateOptions(self):
		""" request the chart options updating """
		options = {
			'lines': self.linesCheck.isChecked(),
			'smooth': self.smoothCheck.isChecked(),
			'linregr': self.linRegrCheck.isChecked(),
			'polyregr': self.polyRegrCheck.isChecked(),
			'detrending': self.detrendingCheck.isChecked(),
			'legend': self.legendCheck.isChecked(),
		}

		self.emit( SIGNAL("updateOptions"), options )

	def setLimits(self, xlim, ylim, update=False):
		self.minDateEdit.setDate(xlim[0])
		self.maxDateEdit.setDate(xlim[1])
		self.minYEdit.setText("%s" % ylim[0])
		self.maxYEdit.setText("%s" % ylim[1])
		if update:
			self.updateLimits()

	def updateLimits(self):
		""" request the chart axis limits updating """
		xLimits = (self.minDateEdit.date().toPyDate(), self.maxDateEdit.date().toPyDate())
		yLimits = (self.minYEdit.text().toDouble()[0], self.maxYEdit.text().toDouble()[0])
		self.emit( SIGNAL("updateLimits"), xLimits, yLimits )

	def updateLabels(self):
		""" request the chart axis labels updating """
		if self.labelsCheck.isChecked():
			xLabel = self.xLabelEdit.text()
			yLabel = self.yLabelEdit.text()
		else:
			xLabel = None
			yLabel = None
		self.emit( SIGNAL("updateLabels"), xLabel, yLabel )

	def updateTitle(self):
		""" request the chart title updating """
		params = []

		for i in range(3):
			# get param label
			label = getattr(self, "titleParam%dEdit" % i).text()
			# get param value
			combo = getattr(self, "titleParam%dCombo" % i)
			fldIdx = combo.itemData( combo.currentIndex() ).toInt()[0]
			params.append( (label, fldIdx) )

		self.emit( SIGNAL("updateTitle"), params)


class NavToolbar(NavigationToolbar):
	def __init__(self, canvas, parent=None):
		NavigationToolbar.__init__(self, canvas, parent)

		# add toolbutton to change fonts/colors
		self.fontColorAction = QtGui.QAction( QtGui.QIcon(":/pstimeseries_plugin/icons/settings"), "Change fonts and colors", self )
		self.fontColorAction.setToolTip( "Change fonts and colors" )
		self.insertAction(self.homeAction, self.fontColorAction)
		self.connect(self.fontColorAction, SIGNAL("triggered()"), self.openFontColorSettings)

		self.insertSeparator(self.homeAction)

	def openFontColorSettings(self):
		dlg = GraphSettings_Dlg(self)
		if dlg.exec_():
			self.emit( SIGNAL("updateRequested") )

