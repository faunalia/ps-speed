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

from qgis.core import QgsMapLayer, QgsFeature, QgsDataSourceURI, QgsVectorLayer, QgsRectangle

import resources_rc

class ToolPS_Plugin:

	def __init__(self, iface):
		self.iface = iface

	def initGui(self):
		# create the actions
		self.useActiveLayerAction = QAction( "PS Time Series Viewer", self.iface.mainWindow() )	#QIcon( ":/pstimeseries_plugin/icons/useActiveLayer.png" )
		QObject.connect( self.useActiveLayerAction, SIGNAL( "triggered()" ), self.useActiveLayer )

		self.aboutAction = QAction( QIcon( ":/pstimeseries_plugin/icons/about" ), "About", self.iface.mainWindow() )
		QObject.connect( self.aboutAction, SIGNAL("triggered()"), self.about )

		# add actions to toolbars and menus
		self.toolbar.addAction( self.useActiveLayerAction )
		self.iface.addPluginToMenu( "&PS Time Series", self.useActiveLayerAction )
		#self.iface.addPluginToMenu( "&PS Time Series", self.aboutAction )

	def unload(self):
		# remove actions from toolbars and menus
		self.toolbar.removeAction( self.useActiveLayerAction )
		self.iface.removePluginMenu( "&PS Time Series", self.useActiveLayerAction )
		#self.iface.removePluginMenu( "&PS Time Series", self.aboutAction )


	def about(self):
		""" display the about dialog """
		from about_dlg import AboutDlg
		dlg = AboutDlg( self.iface.mainWindow() )
		dlg.exec_()

	def useActiveLayer(self):
		layer = self.iface.activeLayer()
		if not layer or layer.type() != QgsMapLayer.VectorLayer:
			return

		from MapTools import FeatureFinder
		self.featFinder = FeatureFinder(self.iface.mapCanvas())
		QObject.connect(self.featFinder, SIGNAL( "pointEmitted" ), self.onPointClicked)
		self.iface.mapCanvas().setMapTool( self.featFinder )

	def onPointClicked(self, point):
		layer = self.iface.activeLayer()
		if not layer or layer.type() != QgsMapLayer.VectorLayer:
			return

		# get the feature id of the point under the mouse click
		from MapTools import FeatureFinder
		fid = FeatureFinder.findAtPoint(layer, point, canvas=self.iface.mapCanvas(), onlyTheClosestOne=True, onlyIds=True)
		if fid is None:
			return

		# get the attribute map of the selected feature
		feat = QgsFeature()
		layer.featureAtId( fid, feat, False )
		attrs = feat.attributeMap()

		fields = layer.dataProvider().fields()
		providerType = layer.providerType()

		x, y = [], []	# lists containg values
		infoFields = {}	# dict containing fields info

		if providerType == 'ogr' and layer.source().endsWith( ".shp", Qt.CaseInsensitive ):	# Shapefile
			for idx, fld in fields.iteritems():
				if QRegExp( "D\\d{8}", Qt.CaseInsensitive ).indexIn( fld.name() ) < 0:
					# info fields are all except those containing dates
					infoFields[ idx ] = fld
				else:
					x.append( QDate.fromString( fld.name()[1:], "yyyyMMdd" ).toPyDate() )
					y.append( attrs[ idx ].toDouble()[0] )

		elif providerType in ['postgres', 'spatialite'] or \
				( providerType == 'ogr' and layer.source().startsWith("OCI:", Qt.CaseInsensitive) ):	# PostGIS or SpatiaLite or Oracle Spatial
			infoFields = fields

			# get values of fields needed to join tables
			if providerType == 'ogr':
				# find the id_dataset and code_target
				code = dataset = None
				for idx, fld in fields.iteritems():
					if fld.name().startsWith( "code", Qt.CaseInsensitive ):
						code = attrs[ idx ].toString()
					elif fld.name().endsWith( "dataset", Qt.CaseInsensitive ):
						dataset = attrs[ idx ].toString()

				if code is None or dataset is None:
					return
				subset = u"code_target='%s' AND id_dataset='%s'" % (code, dataset)

				# create the uri
				uri = layer.source()
				pos = uri[4:].indexOf(':') < 0
				if pos < 0:
					return
				uri = u"%s:ts_%s" % (uri[0, pos], uri[pos+1:])

			else:
				# find the field code
				code = None
				for idx, fld in fields.iteritems():
					if fld.name().startsWith( "code", Qt.CaseInsensitive ):
						code = attrs[ idx ].toString()

				if code is None:
					return
				subset = u"code='%s'" % code

				# create the uri
				dsuri = QgsDataSourceURI( layer.source() )
				dsuri.setDataSource( dsuri.schema(), u"ts_%s" % dsuri.table(), QString() )
				uri = dsuri.uri()

			# create the vector layer containing data will be plotted
			vl = QgsVectorLayer( uri, "tool_ps", providerType )
			if not vl.isValid():
				return

			vl.setSubsetString( subset )
			try:
				# get indexes of date (x) and value (y) fields
				dateIdx, valueIdx = None, None
				for idx, fld in vl.dataProvider().fields().iteritems():
					if fld.name().startsWith( "dat", Qt.CaseInsensitive ):
						dateIdx = idx
					elif fld.name().startsWith( "val", Qt.CaseInsensitive ):
						valueIdx = idx

				if dateIdx is None or valueIdx is None:
					return

				# fetch and loop through all the features
				vl.select( [dateIdx, valueIdx], QgsRectangle(), False, True )
				f = QgsFeature()
				while vl.nextFeature( f ):
					# get x and y values
					a = f.attributeMap()
					x.append( QDate.fromString( a[ dateIdx ].toString(), "yyyyMMdd" ).toPyDate() )
					y.append( a[ valueIdx ].toDouble()[0] )

			finally:
				vl.deleteLater()
				del vl
			
		# display the plot dialog
		from tool_ps_dlg import ToolPSDlg
		dlg = ToolPSDlg( layer, infoFields )
		dlg.setFeatureId( fid )
		dlg.setData( x, y )
		dlg.exec_()

