# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                : PS Time Series Viewer
Description         : Computation and visualization of time series of speed for 
                    Permanent Scatterers derived from satellite interferometry
Date                : Oct 05, 2012 
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

from matplotlib.font_manager import FontManager
from .ui.graph_settings_dialog_ui import Ui_Dialog

class GraphSettings_Dlg(QDialog, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)

		self.titleBoldBtn.hide()
		self.titleItalicBtn.hide()
		self.labelsBoldBtn.hide()
		self.labelsItalicBtn.hide()

		# remove fonts matplotlib doesn't load
		for index in range(self.titleFontCombo.count()-1, -1, -1):
			found = False
			family = unicode( self.titleFontCombo.itemText( index ) )
			try:
				props = self.findFont( {'family':family} )
				if family == props['family']:
					found = True
			except KeyError:
				pass
			if not found:
				self.titleFontCombo.removeItem( index )
				self.labelsFontCombo.removeItem( index )

		self.initProps()

		QObject.connect(self.titleColorBtn, SIGNAL("clicked()"), self.chooseTitleColor)
		QObject.connect(self.labelsColorBtn, SIGNAL("clicked()"), self.chooseLabelsColor)
		QObject.connect(self.pointsColorBtn, SIGNAL("clicked()"), self.choosePointsColor)
		QObject.connect(self.pointsReplicasColorBtn, SIGNAL("clicked()"), self.choosePointsReplicasColor)
		QObject.connect(self.linesColorBtn, SIGNAL("clicked()"), self.chooseLinesColor)
		QObject.connect(self.linesThrendColorBtn, SIGNAL("clicked()"), self.chooseLinesThrendColor)

	def choosePointsColor(self):
		dlg = QColorDialog(self.pointsColor, self)
		if dlg.exec_():
			self.setPointsColor( dlg.selectedColor() )
		dlg.deleteLater()

	def setPointsColor(self, color):
		self.pointsColor = QColor( color )
		pixmap = QPixmap( 20,20 )
		pixmap.fill( self.pointsColor )
		self.pointsColorBtn.setIcon( QIcon(pixmap) )

	def pointsProps(self):
		props = {
			'marker' : 's',
			'color' : self.pointsColor.name()
		}
		return props

	def setPointsProps(self, props):
		self.setPointsColor( props.get('color', 'black') )


	def choosePointsReplicasColor(self):
		dlg = QColorDialog(self.pointsReplicasColor, self)
		if dlg.exec_():
			self.setPointsReplicasColor( dlg.selectedColor() )
		dlg.deleteLater()

	def setPointsReplicasColor(self, color):
		self.pointsReplicasColor = QColor( color )
		pixmap = QPixmap( 20,20 )
		pixmap.fill( self.pointsReplicasColor )
		self.pointsReplicasColorBtn.setIcon( QIcon(pixmap) )

	def pointsReplicasProps(self):
		props = {
			'marker' : 's',
			'color' : self.pointsReplicasColor.name(), 
		}
		return props

	def setPointsReplicasProps(self, props):
		self.setPointsReplicasColor( props.get('color', 'blue') )


	def chooseLinesColor(self):
		dlg = QColorDialog(self.linesColor, self)
		if dlg.exec_():
			self.setLinesColor( dlg.selectedColor() )
		dlg.deleteLater()

	def setLinesColor(self, color):
		self.linesColor = QColor( color )
		pixmap = QPixmap( 20,20 )
		pixmap.fill( self.linesColor )
		self.linesColorBtn.setIcon( QIcon(pixmap) )

	def linesProps(self):
		props = {
			'color' : self.linesColor.name()
		}
		return props

	def setLinesProps(self, props):
		self.setLinesColor( props.get('color', 'black') )


	def chooseLinesThrendColor(self):
		dlg = QColorDialog(self.linesThrendColor, self)
		if dlg.exec_():
			self.setLinesThrendColor( dlg.selectedColor() )
		dlg.deleteLater()

	def setLinesThrendColor(self, color):
		self.linesThrendColor = QColor( color )
		pixmap = QPixmap( 20,20 )
		pixmap.fill( self.linesThrendColor )
		self.linesThrendColorBtn.setIcon( QIcon(pixmap) )

	def linesThrendProps(self):
		props = {
			'color' : self.linesThrendColor.name(), 
		}
		return props

	def setLinesThrendProps(self, props):
		self.setLinesThrendColor( props.get('color', 'red') )


	def chooseTitleColor(self):
		dlg = QColorDialog(self.titleColor, self)
		if dlg.exec_():
			self.setTitleColor( dlg.selectedColor() )
		dlg.deleteLater()

	def setTitleColor(self, color):
		self.titleColor = QColor( color )
		pixmap = QPixmap( 20,20 )
		pixmap.fill( self.titleColor )
		self.titleColorBtn.setIcon( QIcon(pixmap) )


	def chooseLabelsColor(self):
		dlg = QColorDialog(self.labelsColor, self)
		if dlg.exec_():
			self.setLabelsColor( dlg.selectedColor() )
		dlg.deleteLater()

	def setLabelsColor(self, color):
		self.labelsColor = QColor( color )
		pixmap = QPixmap( 20,20 )
		pixmap.fill( self.labelsColor )
		self.labelsColorBtn.setIcon( QIcon(pixmap) )


	def titleFontProps(self):
		qfont = self.titleFontCombo.currentFont()
		qfont.setPointSize( self.titleSizeSpin.value() )
		if self.titleBoldBtn.isVisible() and self.titleBoldBtn.isChecked():
			qfont.setBold( True )
		if self.titleItalicBtn.isVisible() and self.titleItalicBtn.isChecked():
			qfont.setItalic( True )

		# search for the best match
		props = self.qfontToProps( qfont )
		props['color'] = self.titleColor.name()
		props['size'] = self.titleSizeSpin.value()
		return props

	def setTitleFontProps(self, props):
		if 'family' in props:
			index = self.titleFontCombo.findText( props['family'] )
			if index >= 0:
				self.titleFontCombo.setCurrentIndex( index )
		if 'size' in props:
			try:
				self.titleSizeSpin.setValue( int(props['size']) )
			except ValueError:
				pass

		self.setTitleColor( props.get('color', 'black') )
		self.titleBoldBtn.setChecked( props.get('weight', '') == 'bold' )
		self.titleItalicBtn.setChecked( props.get('style', '') == 'italic' )


	def labelsFontProps(self):
		qfont = self.labelsFontCombo.currentFont()
		qfont.setPointSize( self.titleSizeSpin.value() )
		if self.labelsBoldBtn.isVisible() and self.labelsBoldBtn.isChecked():
			qfont.setBold( True )
		if self.labelsItalicBtn.isVisible() and self.labelsItalicBtn.isChecked():
			qfont.setItalic( True )

		# search for the best match
		props = self.qfontToProps( qfont )
		props['color'] = self.labelsColor.name()
		props['size'] = self.labelsSizeSpin.value()
		return props

	def setLabelsFontProps(self, props):
		if 'family' in props:
			index = self.labelsFontCombo.findText( props['family'] )
			if index >= 0:
				self.labelsFontCombo.setCurrentIndex( index )
		if 'size' in props:
			try:
				self.labelsSizeSpin.setValue( int(props['size']) )
			except ValueError:
				pass

		self.setLabelsColor( props.get('color', 'black') )
		self.labelsBoldBtn.setChecked( props.get('weight', '') == 'bold' )
		self.labelsItalicBtn.setChecked( props.get('style', '') == 'italic' )


	def initProps(self):
		settings = QSettings()
		self.setTitleFontProps( self.settingsToDict( settings.value("/pstimeseries/titleProps", {}) ) )
		self.setLabelsFontProps( self.settingsToDict( settings.value("/pstimeseries/labelsProps", {}) ) )

		self.setPointsProps( self.settingsToDict( settings.value("/pstimeseries/pointsProps", {}) ) )
		self.setPointsReplicasProps( self.settingsToDict( settings.value("/pstimeseries/pointsReplicasProps", {}) ) )

		self.setLinesProps( self.settingsToDict( settings.value("/pstimeseries/linesProps", {}) ) )
		self.setLinesThrendProps( self.settingsToDict( settings.value("/pstimeseries/linesThrendProps", {}) ) )

	def accept(self):
		settings = QSettings()
		settings.setValue("/pstimeseries/titleProps", self.titleFontProps())
		settings.setValue("/pstimeseries/labelsProps", self.labelsFontProps())

		settings.setValue("/pstimeseries/pointsProps", self.pointsProps())
		settings.setValue("/pstimeseries/pointsReplicasProps", self.pointsReplicasProps())

		settings.setValue("/pstimeseries/linesProps", self.linesProps())
		settings.setValue("/pstimeseries/linesThrendProps", self.linesThrendProps())

		QDialog.accept(self)


	@classmethod
	def settingsToDict(self, s):
		r = {}
		for k,v in s.toPyObject().iteritems():
			r[ unicode(k) ] = unicode(v) if isinstance(v, (str, QString)) else v
		return r

	@classmethod
	def qfontToProps(self, qfont):
		props = {
			'family' : unicode(qfont.family()), 
			'stretch' : qfont.stretch(),
			'weight' : qfont.weight()
		}

		if qfont.style() == QFont.StyleItalic: style = 'italic'
		elif qfont.style() == QFont.StyleOblique: style = 'oblique'
		else: style = 'normal'
		props['style'] = style

		if qfont.capitalization() == QFont.SmallCaps:
			props['variant'] = 'small-caps'

		return self.findFont(props)

	@classmethod
	def findFont(self, props):
		from matplotlib.font_manager import FontProperties, findfont

		# search for the best match
		font = FontProperties( fname=findfont( FontProperties(**props) ) )

		props = {
			'family' : font.get_name(), 
			'weight' : font.get_weight(),
			'style' : font.get_style(),
		}
		return props

