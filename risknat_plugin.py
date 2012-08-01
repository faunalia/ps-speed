# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name			 	 : RiskNat
Description          : RiskNat plugin
Date                 : Jul 25, 2012 
copyright            : (C) 2012 by Giuseppe Sucameli (Faunalia)
email                : brush.tyler@gmail.com

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

import resources_rc

class RiskNat_Plugin:

	instance = None

	def __init__(self, iface):
		RiskNat_Plugin.instance = self

		self.iface = iface
		self.toolbar = None

	def initGui(self):
		# create the actions
		self.useActiveLayerAction = QAction( "Use active layer", self.iface.mainWindow() )	#QIcon( ":/risknat_plugin/icons/useActiveLayer.png" )
		QObject.connect( self.useActiveLayerAction, SIGNAL( "triggered()" ), self.useActiveLayer )

		self.useOCILayerAction = QAction( "Use Oracle Spatial layer", self.iface.mainWindow() )	#QIcon( ":/risknat_plugin/icons/useOCILayer.png" )
		QObject.connect( self.useOCILayerAction, SIGNAL( "triggered()" ), self.useOCILayer )

		self.aboutAction = QAction( QIcon( ":/risknat_plugin/icons/about" ), "About", self.iface.mainWindow() )
		QObject.connect( self.aboutAction, SIGNAL("triggered()"), self.about )

		# create a custom toolbar
		self.toolbar = self.iface.addToolBar( "RiskNat" )

		# add actions to toolbars and menus
		self.toolbar.addAction( self.useActiveLayerAction )
		self.toolbar.addAction( self.useOCILayerAction )
		self.iface.addPluginToMenu( "&RiskNat", self.useActiveLayerAction )
		self.iface.addPluginToMenu( "&RiskNat", self.useOCILayerAction )
		#self.iface.addPluginToMenu( "&RiskNat", self.aboutAction )

	def unload(self):
		# remove actions from toolbars and menus
		self.toolbar.removeAction( self.useActiveLayerAction )
		self.toolbar.removeAction( self.useOCILayerAction )
		self.iface.removePluginMenu( "&RiskNat", self.useActiveLayerAction )
		self.iface.removePluginMenu( "&RiskNat", self.useOCILayerAction )
		#self.iface.removePluginMenu( "&RiskNat", self.aboutAction )

		# delete the custom toolbar
		self.toolbar.deleteLater()
		self.toolbar = None

		RiskNat_Plugin.instance = None


	def about(self):
		""" display the about dialog """
		from about_dlg import AboutDlg
		dlg = AboutDlg( self.iface.mainWindow() )
		dlg.exec_()


	def useActiveLayer(self):
		layer = self.iface.activeLayer()
		if not layer or layer.type() != QgsMapLayer.VectorType:
			return

		from MapTools import FeatureFinder
		featFinder = FeatureFinder(self.iface.mapCanvas())
		QObject.connect(featFinder, SIGNAL( "pointEmitted" ), self.onEnd)

	def onPointClicked(self, point):
		layer = self.iface.activeLayer()
		if not layer or layer.type() != QgsMapLayer.VectorType:
			return

		from MapTools import FeatureFinder
		fid = FeatureFinder.findAtPoint(layer, point, onlyTheClosestOne=True, onlyIds=True)
		if fid is None:
			return

		provider = layer.providerKey()
		infoFields = layer.pendingAllAttributesList()

		if provider == 'ogr':
			if layer.source().endsWith( ".shp", Qt.CaseInsensitive ):	# Shapefile
				feat = QgsFeature()
				layer.featureAtId( fid, feat, False, layer.pendingAllAttributesList() )
				attrs = feat.attributeMap()

				x, y = [], []
				infoFields.clear()	# recreate the list of fields contain info
				for idx, fld in layer.dataProvider().fields().iteritems():
					if QRegExp( "D\d{8}", Qt.CaseInsensitive ).indexIn( fld.name().toUpper() ) < 0:
						# info fields are all except those containing dates
						infoFields[ idx ] = fld
					else:
						x.append( QDate.fromString( fld.name()[1:], "yyyyMMdd" ).toPyDate() )
						y.append( attrs[ idx ].toDouble()[0] )

			elif layer.source().startsWith( "OCI:", Qt.CaseInsensitive ):	# Oracle Spatial
				raise NotImplemented

			else:
				return

		elif provider in ['postgres', 'spatialite']:	# PostGIS e SpatiaLite
			raise NotImplemented

		from risknat_dlg import RiskNatDlg
		dlg = RiskNatDlg( layer, infoFields )
		dlg.setFeatureId( fid )
		dlg.setData( x, y )
		dlg.exec_()

