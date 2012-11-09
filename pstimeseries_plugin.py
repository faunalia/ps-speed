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
from PyQt4.QtGui import *

from qgis.core import QgsMapLayer, QgsFeature, QgsDataSourceURI, QgsVectorLayer, QgsRectangle, QgsMessageLog

import resources_rc

class PSTimeSeries_Plugin:

	def __init__(self, iface):
		self.iface = iface
		self.featFinder = None

		# used to know where to ask for a new time-series tablename
		self.last_ps_layerid = None
		self.ts_tablename = None

	def initGui(self):
		# create the actions
		self.action = QAction( QIcon( ":/pstimeseries_plugin/icons/logo" ), "PS Time Series Viewer", self.iface.mainWindow() )
		QObject.connect( self.action, SIGNAL( "triggered()" ), self.run )
		self.action.setCheckable( True )

		self.aboutAction = QAction( QIcon( ":/pstimeseries_plugin/icons/about" ), "About", self.iface.mainWindow() )
		QObject.connect( self.aboutAction, SIGNAL("triggered()"), self.about )

		# add actions to toolbars and menus
		self.iface.addToolBarIcon( self.action )
		self.iface.addPluginToMenu( "&Permanent Scatterers", self.action )
		#self.iface.addPluginToMenu( "&Permanent Scatterers", self.aboutAction )

	def unload(self):
		# remove actions from toolbars and menus
		self.iface.removeToolBarIcon( self.action )
		self.iface.removePluginMenu( "&Permanent Scatterers", self.action )
		#self.iface.removePluginMenu( "&Permanent Scatterers", self.aboutAction )


	def about(self):
		""" display the about dialog """
		from about_dlg import AboutDlg
		dlg = AboutDlg( self.iface.mainWindow() )
		dlg.exec_()

	def run(self):
		# create a maptool to select a point feature from the canvas
		if not self.featFinder:
			from MapTools import FeatureFinder
			self.featFinder = FeatureFinder(self.iface.mapCanvas())
			self.featFinder.setAction( self.action )
			QObject.connect(self.featFinder, SIGNAL( "pointEmitted" ), self.onPointClicked)

		# enable the maptool and set a message in the status bar 
		self.featFinder.startCapture()
		self.iface.mainWindow().statusBar().showMessage( u"Click on a point feature in canvas" )


	def onPointClicked(self, point):
		layer = self.iface.activeLayer()
		if not layer or layer.type() != QgsMapLayer.VectorLayer:
			QMessageBox.information(self.iface.mainWindow(), "PS Time Series Viewer", u"Select a vector layer and try again.")
			return

		# set the waiting cursor
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		try:
			dlg = self._onPointClicked( layer, point )
		finally:
			# restore the cursor
			QApplication.restoreOverrideCursor()

		if dlg:
			dlg.exec_()

		self.run()


	def _onPointClicked(self, ps_layer, point):
		# get the id of the point feature under the mouse click
		from .MapTools import FeatureFinder
		fid = FeatureFinder.findAtPoint(ps_layer, point, canvas=self.iface.mapCanvas(), onlyTheClosestOne=True, onlyIds=True)
		if fid is None:
			return

		# get the attribute map of the selected feature
		feat = QgsFeature()
		ps_layer.featureAtId( fid, feat, False )
		attrs = feat.attributeMap()

		x, y = [], []	# lists containg x,y values
		infoFields = {}	# hold the index->name of the fields containing info to be displayed

		ps_source = ps_layer.source()
		ps_fields = ps_layer.dataProvider().fields()

		providerType = ps_layer.providerType()
		if providerType == 'ogr' and ps_source.endsWith( ".shp", Qt.CaseInsensitive ):
			# Shapefile
			for idx, fld in ps_fields.iteritems():
				if QRegExp( "D\\d{8}", Qt.CaseInsensitive ).indexIn( fld.name() ) < 0:
					# info fields are all except those containing dates
					infoFields[ idx ] = fld
				else:
					x.append( QDate.fromString( fld.name()[1:], "yyyyMMdd" ).toPyDate() )
					y.append( attrs[ idx ].toDouble()[0] )

		elif providerType == 'ogr' and (ps_source.startsWith("OCI:", Qt.CaseInsensitive) or ps_source.endsWith(".vrt", Qt.CaseInsensitive)):	# Oracle Spatial

			# fields containing values
			dateField = "data_misura"
			valueField = "spost_rel_mm"
			infoFields = ps_fields

			# search for the id_dataset and code_target fields needed to join 
			# PS and TS tables
			idDataset = codeTarget = None
			for idx, fld in ps_fields.iteritems():
				if fld.name().toLower() == "id_dataset":
					idDataset = attrs[ idx ].toString()
				if fld.name().toLower() == "code_target":
					codeTarget = attrs[ idx ].toString()

			if idDataset is None or codeTarget is None:
				QgsMessageLog.logMessage( u"idDataset is %s, codeTarget is %s. Exiting" % (idDataset, codeTarget), "PSTimeSeriesViewer" )
				return
			subset = u"id_dataset='%s' AND code_target='%s'" % (idDataset, codeTarget)

			# create the uri
			if ps_source.startsWith( "OCI:", Qt.CaseInsensitive ):
				default_tbl_name = "RNAT_TARGET_SSTO"
			elif ps_source.endsWith(".vrt", Qt.CaseInsensitive):
				default_tbl_name = "RNAT_TARGET_SSTO.vrt"
			else:
				default_tbl_name = ""
			if not self._askTStablename( ps_layer,  default_tbl_name ):
				return

			if ps_source.startsWith( "OCI:", Qt.CaseInsensitive ):
				# uri is like OCI:userid/password@database:table
				uri = ps_source
				pos = uri.indexOf(':', 4)
				if pos >= 0:
					uri = uri[0:pos]
				uri = u"%s:%s" % (uri, self.ts_tablename)
			else:
				uri = u"%s/%s" % (QFileInfo(ps_source).dir().path(), self.ts_tablename)

			# load the layer containing time series
			ts_layer = self._createTSlayer( uri, providerType, subset )
			if ts_layer is None:
				return

			# get time series X and Y values
			try:
				x, y = self._getXYvalues( ts_layer, dateField, valueField )
			finally:
				ts_layer.deleteLater()
				del ts_layer

		elif providerType in ['postgres', 'spatialite']:# either PostGIS or SpatiaLite

			# fields containing values
			dateField = "dataripresa"
			valueField = "valore"
			infoFields = ps_fields

			# search for the id_dataset and code_target fields needed to join 
			# PS and TS tables
			code = None
			for idx, fld in ps_fields.iteritems():
				if fld.name().toLower() == "code":
					code = attrs[ idx ].toString()

			if code is None:
				QgsMessageLog.logMessage( u"code is None. Exiting" % code, "PSTimeSeriesViewer" )
				return
			subset = u"code='%s'" % code

			# create the uri
			dsuri = QgsDataSourceURI( ps_layer.source() )
			default_tbl_name = u"ts_%s" % dsuri.table()
			if not self._askTStablename( ps_layer,  default_tbl_name ):
				return
			dsuri.setDataSource( dsuri.schema(), self.ts_tablename, QString() )
			uri = dsuri.uri()

			# load the layer containing time series
			ts_layer = self._createTSlayer( uri, providerType, subset )
			if ts_layer is None:
				return

			# get time series X and Y values
			try:
				x, y = self._getXYvalues( ts_layer, dateField, valueField )
			finally:
				ts_layer.deleteLater()
				del ts_layer

		if len(x) * len(y) <= 0:
			QMessageBox.warning( self.iface.mainWindow(), 
					"PS Time Series Viewer", 
					u"The layer '%s' wasn't found." % self.ts_tablename )
			return
			
		# display the plot dialog
		from .pstimeseries_dlg import PSTimeSeries_Dlg
		dlg = PSTimeSeries_Dlg( ps_layer, infoFields )
		dlg.setFeatureId( fid )
		dlg.setData( x, y )
		return dlg



	def _getXYvalues(self, ts_layer, dateField, valueField):
		# utility function used to get the X and Y values
		x, y = [], []

		# get indexes of date (x) and value (y) fields
		dateIdx, valueIdx = None, None
		for idx, fld in ts_layer.dataProvider().fields().iteritems():
			if fld.name().toLower() == dateField:
				dateIdx = idx
			elif fld.name().toLower() == valueField:
				valueIdx = idx

		if dateIdx is None or valueIdx is None:
			QgsMessageLog.logMessage(u"field %s -> index %s, field %s -> index %s. Exiting" % (dateField, dateIdx, valueField, valueIdx), "PSTimeSeriesViewer")
			return

		# fetch and loop through all the features
		ts_layer.select( [dateIdx, valueIdx], QgsRectangle(), False, True )
		f = QgsFeature()
		while ts_layer.nextFeature( f ):
			# get x and y values
			a = f.attributeMap()
			x.append( QDate.fromString( a[ dateIdx ].toString(), "yyyyMMdd" ).toPyDate() )
			y.append( a[ valueIdx ].toDouble()[0] )

		return x, y

	def _askTStablename(self, ps_layer, default_tblname=None):
		# utility function used to ask to the user the name of the table
		# containing time series data
		if default_tblname is None:
			default_tblname = ""

		# ask a tablename to the user
		if ps_layer.id() != self.last_ps_layerid or not self.ts_tablename:
			tblname, ok = QInputDialog.getText( self.iface.mainWindow(), 
					"PS Time Series Viewer", 
					"Insert the name of the table containing time-series", 
					text=default_tblname )
			if not ok:
				return False

			self.ts_tablename = tblname
			self.last_ps_layerid = ps_layer.id()

		return True

	def _createTSlayer(self, uri, providerType, subset=None):
		# utility function used to create the vector layer containing time 
		# series data
		layer = QgsVectorLayer( uri, "time_series_layer", providerType )
		if not layer.isValid():
			QMessageBox.warning( self.iface.mainWindow(), 
					"PS Time Series Viewer", 
					u"The layer '%s' wasn't found." % self.ts_tablename )
			self.ts_tablename = None
			return

		if subset is not None:
			layer.setSubsetString( subset )

		return layer

