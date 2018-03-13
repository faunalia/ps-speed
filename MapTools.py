# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : Omero RT
Description          : Omero plugin map tools
Date                 : August 15, 2010
copyright            : (C) 2010 by Giuseppe Sucameli (Faunalia)
email                : sucameli@faunalia.it
 ***************************************************************************/

Omero plugin
Works done from Faunalia (http://www.faunalia.it) with funding from Regione
Toscana - S.I.T.A. (http://www.regione.toscana.it/territorio/cartografia/index.html)

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtWidgets import QApplication

from qgis.core import QgsWkbTypes, QgsFeatureRequest, QgsRectangle, QgsGeometry, QgsFeature, QgsSettings, Qgis
from qgis.gui import QgsMapToolEmitPoint, QgsMapTool, QgsRubberBand


class MapToolEmitPoint(QgsMapToolEmitPoint):
	geometryEmitted = pyqtSignal(object)

	def __init__(self, canvas):
		QgsMapToolEmitPoint.__init__(self, canvas)

		self.canvas = canvas
		self.action = None

		self.canvas.mapToolSet.connect(self._toolChanged)

	def deleteLater(self, *args):
		self.canvas.mapToolSet.disconnect(self._toolChanged)
		return QgsMapToolEmitPoint.deleteLater(self, *args)

	def setAction(self, action):
		self.action = action

	def action(self):
		return self.action

	def _toolChanged(self, tool):
		if self.action:
			self.action.setChecked( tool == self )

	def startCapture(self):
		self.canvas.setMapTool( self )

	def stopCapture(self):
		self._toolChanged( None )
		self.canvas.unsetMapTool( self )

	def deactivate(self):
		QgsMapTool.deactivate(self)
		self.deactivated.emit()


class Drawer(MapToolEmitPoint):
	def __init__(self, canvas, isPolygon=False, props=None):
		MapToolEmitPoint.__init__(self, canvas)

		self.isPolygon = isPolygon
		self.props = props if props is not None else {}

		self.action = None
		self.isEmittingPoints = False

		self.rubberBand = qgis.gui.QgsRubberBand( self.canvas, QgsWkbTypes.PolygonGeometry if self.isPolygon else QgsWkbTypes.LineGeometry )
		self.rubberBand.setColor( self.props.get('color', Qt.red) )
		self.rubberBand.setWidth( self.props.get('border', 1) )

		self.snapper = self.canvas.snappingUtils()

	def deleteLater(self, *args):
		self.reset()
		del self.rubberBand
		del self.snapper
		return MapToolEmitPoint.deleteLater(self, *args)

	def setColor(self, color):
		self.rubberBand.setColor( color )

	def reset(self):
		self.isEmittingPoints = False
		self.rubberBand.reset( QgsWkbTypes.PolygonGeometry if self.isPolygon else QgsWkbTypes.LineGeometry )

	def canvasPressEvent(self, e):
		if e.button() == Qt.RightButton:
			prevIsEmittingPoints = self.isEmittingPoints
			self.isEmittingPoints = False
			if not self.isEmittingPoints:
				self.onEnd( self.geometry() )
			else:
				self.onEnd( None )
			return

		if e.button() != Qt.LeftButton:
			return

		if not self.isEmittingPoints:	# first click
			self.reset()
		self.isEmittingPoints = True

		point = self.toMapCoordinates( e.pos() )
		self.rubberBand.addPoint( point, True )	# true to update canvas
		self.rubberBand.show()

	def canvasMoveEvent(self, e):
		if not self.isEmittingPoints:
			return

		if not self.props.get('enableSnap', True):
			point = self.toMapCoordinates( e.pos() )
		else:
			snapResults = self.snapper.snapToMap( e.pos() )
			if snapResults.isValid():
				point = snapResults.point()
			else:
				point = self.toMapCoordinates( e.pos() )

		self.rubberBand.movePoint( point )

	def canvasReleaseEvent(self, e):
		if not self.isEmittingPoints:
			return

		if self.isPolygon:
			return

		if self.props.get('mode', None) != 'segment':
			return

		self.isEmittingPoints = False
		self.onEnd( self.geometry() )

	def isValid(self):
		return self.rubberBand.numberOfVertices() > 0

	def geometry(self):
		if not self.isValid():
			return None
		geom = self.rubberBand.asGeometry()
		if geom == None:
			return
		return geom

	def onEnd(self, geometry):
		#self.stopCapture()
		self.geometryEmitted.emit( geometry )

	def deactivate(self):
		if not self.props.get('keepAfterEnd', False):
			self.reset()

		return MapToolEmitPoint.deactivate(self)


class PolygonDrawer(Drawer):
	def __init__(self, canvas, props=None):
		Drawer.__init__(self, canvas, True, props)


class LineDrawer(Drawer):
	def __init__(self, canvas, props=None):
		Drawer.__init__(self, canvas, False, props)


class SegmentDrawer(Drawer):
	def __init__(self, canvas, props=None):
		props = props if isinstance(props, dict) else {}
		props['mode'] = 'segment'
		Drawer.__init__(self, canvas, False, props)


class FeatureFinder(MapToolEmitPoint):

	pointEmitted = pyqtSignal(object, object)

	def __init__(self, canvas):
		MapToolEmitPoint.__init__(self, canvas)
		self.canvasClicked.connect(self.onEnd)

	def onEnd(self, point, button):
		self.stopCapture()
		self.pointEmitted.emit(point, button)

	@classmethod
	def findAtPoint(self, layer, point, canvas, onlyTheClosestOne=True, onlyIds=False):
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		# recupera il valore del raggio di ricerca
		settings = QgsSettings()
		radius = settings.value( "/Map/searchRadiusMM", Qgis.DEFAULT_SEARCH_RADIUS_MM, type=float)
		if radius <= 0:
			radius = Qgis.DEFAULT_SEARCH_RADIUS_MM
		radius = canvas.extent().width() * radius/100

		# crea il rettangolo da usare per la ricerca
		rect = QgsRectangle()
		rect.setXMinimum(point.x() - radius)
		rect.setXMaximum(point.x() + radius)
		rect.setYMinimum(point.y() - radius)
		rect.setYMaximum(point.y() + radius)
		rect = canvas.mapSettings().mapToLayerCoordinates(layer, rect)

		# recupera le feature che intersecano il rettangolo
		ret = None

		if onlyTheClosestOne:
			request=QgsFeatureRequest()
			request.setFilterRect(rect)

			minDist = -1
			featureId = None
			rect = QgsGeometry.fromRect(rect)
			count = 0

			for f in layer.getFeatures(request):
				if onlyTheClosestOne:
					geom = f.geometry()
					distance = geom.distance(rect)
					if minDist < 0 or distance < minDist:
						minDist = distance
						featureId = f.id()

			if onlyIds:
				ret = featureId
			elif featureId != None:
				f = QgsFeature()
				feats = layer.getFeature( QgsFeatureRequest(featureId) )
				feats.nextFeature(f)
				ret = f

		else:
			IDs = []
			for f in layer.getFeatures():
				IDs.append( f.id() )

			if onlyIds:
				ret = IDs
			else:
				ret = []
				request = QgsFeatureRequest()
				QgsFeatureRequest.setFilterFids(IDs)
				for f in layer.getFeatures( request ):
					ret.append( f )

		QApplication.restoreOverrideCursor()
		return ret
