# -*- coding: utf-8 -*-

"""
/****************************************************************************
Name			 	: GEM Modellers Toolkit plugin (GEM-MT)
Description			: Analysing and Processing Earthquake Catalogue Data
Date				: Jun 21, 2012 
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

# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui, QtCore

# Matplotlib Figure object
from matplotlib.figure import Figure

from datetime import datetime, date
from matplotlib.dates import date2num, num2date, YearLocator, MonthLocator, DayLocator, DateFormatter
from matplotlib.lines import Line2D

# import the Qt4Agg FigureCanvas object, that binds Figure to
# Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg

class PlotWdg(FigureCanvasQTAgg):
	"""Class to represent the FigureCanvas widget"""
	def __init__(self, data=None, labels=None, title=None, props=None):

		self.fig = Figure()
		self.axes = self.fig.add_subplot(111)

		# initialize the canvas where the Figure renders into
		FigureCanvasQTAgg.__init__(self, self.fig)

		self._dirty = False
		self.collections = []

		if not data: data = [None]
		self.setData( *data )

		if not labels: labels = [None]
		self.setLabels( *labels )

		self.setTitle( title )

		self.props = props if isinstance(props, dict) else {}

		yscale = self.props.get('yscale', None)
		if yscale:
			self.axes.set_yscale( yscale )


	def itemAt(self, index):
		if index >= len(self.x):
			return None
		return (self.x[index] if self.x else None, self.y[index] if self.y else None)


	def delete(self):
		self._clear()

		# unset delete function
		self.delete = lambda: None

	def __del__(self):
		self.delete()

	def deleteLater(self, *args):
		self.delete()
		return FigureCanvasQTAgg.deleteLater(self, *args)
		
	def destroy(self, *args):
		self.delete()
		return FigureCanvasQTAgg.destroy(self, *args)


	def setDirty(self, val):
		self._dirty = val

	def showEvent(self, event):
		if self._dirty:
			self.refreshData()
		return FigureCanvasQTAgg.showEvent(self, event)


	def refreshData(self):
		# remove the old stuff
		self._clear()
		# plot the new data
		self._plot()
		# update axis limits
		self.axes.relim()	# it doesn't shrink until removing all the objects on the axis
		# re-draw
		self.draw()
		# unset the dirty flag
		self._dirty = False


	def setData(self, x, y=None, info=None):
		self.x = x if x is not None else []
		self.y = y if y is not None else []
		self.info = info if info is not None else []
		self._dirty = True


	def getTitle(self):
		return self.axes.get_title()

	def setTitle(self, title, *args, **kwargs):
		self.axes.set_title( title or "", *args, **kwargs )
		self.draw()


	def getLabels(self):
		return self.axes.get_xlabel(), self.axes.get_ylabel()

	def setLabels(self, xLabel=None, yLabel=None, *args, **kwargs):
		self.axes.set_xlabel( xLabel or "", *args, **kwargs )
		self.axes.set_ylabel( yLabel or "", *args, **kwargs )
		self.draw()


	def getLimits(self):
		xlim = self.axes.get_xlim()
		is_x_date = isinstance(self.x[0], (datetime, date)) if len(self.x) > 0 else False
		if is_x_date:
			xlim = num2date(xlim)

		ylim = self.axes.get_ylim()
		is_y_date = isinstance(self.y[0], (datetime, date)) if self.y is not None and len(self.y) > 0 else False
		if is_y_date:
			ylim = num2date(ylim)

		return xlim, ylim

	def setLimits(self, xlim=None, ylim=None):
		""" update the chart limits """
		if xlim is not None:
			self.axes.set_xlim(xlim)
		if ylim is not None:
			self.axes.set_ylim(ylim)
		self.draw()

	def displayGrids(self, hgrid=False, vgrid=False):
		self.axes.xaxis.grid(vgrid, 'major')
		self.axes.yaxis.grid(hgrid, 'major')
		self.draw()


	def _removeItem(self, item):
		try:
			self.collections.remove( item )
		except ValueError:
			pass

		try:
			if isinstance(item, (list, tuple, set)):
				for i in item:
					i.remove()
			else:
				item.remove()
		except (ValueError, AttributeError):
			pass


	def _clear(self):
		for item in self.collections:
			self._removeItem( item )

		self.collections = []

	def _plot(self):
		# convert values, then create the plot
		x = map(PlotWdg._valueFromQVariant, self.x)
		y = map(PlotWdg._valueFromQVariant, self.y)

		items = self._callPlotFunc('plot', x, y)
		self.collections.append( items )


	def _callPlotFunc(self, plotfunc, x, y=None, *args, **kwargs):
		is_x_date = isinstance(x[0], (datetime, date)) if len(x) > 0 else False
		is_y_date = isinstance(y[0], (datetime, date)) if y is not None and len(y) > 0 else False

		if is_x_date: 
			self._setAxisDateFormatter( self.axes.xaxis, x )
			x = date2num(x)
		if is_y_date:
			self._setAxisDateFormatter( self.axes.yaxis, y )
			y = date2num(y)

		if y is not None:
			items = getattr(self.axes, plotfunc)(x, y, *args, **kwargs)
		else:
			items = getattr(self.axes, plotfunc)(x, *args, **kwargs)

		if is_x_date: 
			self.fig.autofmt_xdate()
		#if is_y_date:
		#	self.fig.autofmt_ydate()

		return items

	@classmethod
	def _setAxisDateFormatter(self, axis, data):
		timedelta = max(data) - min(data)
		if timedelta.days > 365*5:
			axis.set_major_formatter( DateFormatter('%Y') )
			#axis.set_major_locator( YearLocator() )
			#axis.set_minor_locator( MonthLocator() )
			#bins = timedelta.days * 4 / 356	# four bins for a year

		elif timedelta.days > 30*5:
			axis.set_major_formatter( DateFormatter('%Y-%m') )
			#axis.set_major_locator( MonthLocator() )
			#axis.set_minor_locator( DayLocator() )
			#bins = timedelta.days * 4 / 30	# four bins for a month

		else:
			axis.set_major_formatter( DateFormatter('%Y-%m-%d') )
			#axis.set_major_locator( DayLocator() )
			#axis.set_minor_locator( HourLocator() )
			#bins = timedelta.days * 4	# four bins for a day


	@staticmethod
	def _valueFromQVariant(val):
		""" function to convert values to proper types """
		if not isinstance(val, QtCore.QVariant):
			return val

		if val.type() == QtCore.QVariant.Int:
			return int(val)
		elif val.type() == QtCore.QVariant.Double:
			return float(val)
		elif val.type() == QtCore.QVariant.Date:
			return val.toDate().toPyDate()
		elif val.type() == QtCore.QVariant.DateTime:
			return val.toDateTime().toPyDateTime()

		# try to convert the value to a date
		s = unicode(val)
		try:
			return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
		except ValueError:
			pass
		try:
			return datetime.strptime(s, '%Y-%m-%d')
		except ValueError:
			pass

		v, ok = val
		if ok: return v
		v, ok = val
		if ok: return v
		v = val.toDateTime()
		if v.isValid(): return v.toPyDateTime()
		v = val.toDate()
		if v.isValid(): return v.toPyDate()

		return unicode(s)


class HistogramPlotWdg(PlotWdg):

	def __init__(self, *args, **kwargs):
		PlotWdg.__init__(self, *args, **kwargs)

	def _plot(self):
		# convert values, then create the plot
		x = map(PlotWdg._valueFromQVariant, self.x)

		items = self._callPlotFunc('hist', x, bins=50)
		self.collections.append( items )


class ScatterPlotWdg(PlotWdg):

	def __init__(self, *args, **kwargs):
		PlotWdg.__init__(self, *args, **kwargs)

	def _plot(self):
		# convert values, then create the plot
		x = map(PlotWdg._valueFromQVariant, self.x)
		y = map(PlotWdg._valueFromQVariant, self.y)

		items = self._callPlotFunc('scatter', x, y)
		self.collections.append( items )


class PlotDlg(QtGui.QDialog):
	def __init__(self, parent, *args, **kwargs):
		QtGui.QDialog.__init__(self, parent, QtCore.Qt.Window)
		self.setWindowTitle("Plot dialog")

		layout = QtGui.QVBoxLayout(self)

		self.plot = self.createPlot(*args, **kwargs)
		layout.addWidget(self.plot)

		self.nav = self.createToolBar()
		layout.addWidget(self.nav)


	def enterEvent(self, event):
		self.nav.set_cursor( NavigationToolbar.Cursor.POINTER )
		return QtGui.QDialog.enterEvent(self, event)

	def leaveEvent(self, event):
		self.nav.unset_cursor()
		return QtGui.QDialog.leaveEvent(self, event)

	def createPlot(self, *args, **kwargs):
		return PlotWdg(*args, **kwargs)

	def createToolBar(self):
		return NavigationToolbar(self.plot, self)


	def refresh(self):
		# query for refresh
		self.plot.setDirty(True)

		if self.isVisible():
			# refresh if it's already visible
			self.plot.refreshData()

	def setData(self, x, y=None, info=None):
		self.plot.setData(x, y, info)

	def setTitle(self, title):
		self.plot.setTitle(title)

	def setLabels(self, xLabel, yLabel):
		self.plot.setLabels(xLabel, yLabel)



class HistogramPlotDlg(PlotDlg):
	def __init__(self, *args, **kwargs):
		PlotDlg.__init__(self, *args, **kwargs)

	def createPlot(self, *args, **kwargs):
		return HistogramPlotWdg(*args, **kwargs)

class ScatterPlotDlg(PlotDlg):
	def __init__(self, *args, **kwargs):
		PlotDlg.__init__(self, *args, **kwargs)

	def createPlot(self, *args, **kwargs):
		return ScatterPlotWdg(*args, **kwargs)


# import the NavigationToolbar Qt4Agg widget
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg

class NavigationToolbar(NavigationToolbar2QTAgg):

	def __init__(self, *args, **kwargs):
		NavigationToolbar2QTAgg.__init__(self, *args, **kwargs)

		self.init_buttons()
		self.panAction.setCheckable(True)
		self.zoomAction.setCheckable(True)

		# remove the subplots action
		self.removeAction( self.subplotsAction )

	def configure_subplots(self, *args):
		pass	# do nothing

	class Cursor:
		# cursors defined in backend_bases (from matplotlib source code)
		HAND, POINTER, SELECT_REGION, MOVE = range(4)

		@classmethod
		def toQCursor(self, cursor):
			if cursor == self.MOVE:
				n = QtCore.Qt.SizeAllCursor
			elif cursor == self.HAND:
				n = QtCore.Qt.PointingHandCursor
			elif cursor == self.SELECT_REGION:
				n = QtCore.Qt.CrossCursor
			else:#if cursor == self.POINTER:
				n = QtCore.Qt.ArrowCursor
			return QtGui.QCursor( n )

	def set_cursor(self, cursor):
		if cursor != self._lastCursor:
			self.unset_cursor()
			QtGui.QApplication.setOverrideCursor( NavigationToolbar.Cursor.toQCursor(cursor) )
			self._lastCursor = cursor

	def unset_cursor(self):
		if self._lastCursor:
			QtGui.QApplication.restoreOverrideCursor()
			self._lastCursor = None

	def init_buttons(self):
		self.homeAction = self.panAction = self.zoomAction = self.subplotsAction = None

		for a in self.actions():
			if a.text() == 'Home':
				self.homeAction = a
			elif a.text() == 'Pan':
				self.panAction = a
			elif a.text() == 'Zoom':
				self.zoomAction = a
			elif a.text() == 'Subplots':
				self.subplotsAction = a

	def resetActionsState(self, skip=None):
		# reset the buttons state
		for a in self.actions():
			if skip and a == skip:
				continue
			a.setChecked( False )

	def pan( self, *args ):
		self.resetActionsState( self.panAction )
		NavigationToolbar2QTAgg.pan( self, *args )

	def zoom( self, *args ):
		self.resetActionsState( self.zoomAction )
		NavigationToolbar2QTAgg.zoom( self, *args )


class ClippedLine2D(Line2D):
	"""
	Clip the xlimits to the axes view limits
	"""

	def __init__(self, *args, **kwargs):
		Line2D.__init__(self, *args, **kwargs)

	def draw(self, renderer):
		x, y = self.get_data()

		if len(x) == 2 or len(y) == 2:
			xlim = self.axes.get_xlim()
			ylim = self.axes.get_ylim()

			x0, y0 = x[0], y[0]
			x1, y1 = x[1], y[1]

			if x0 == x1:	# vertical
				x, y = (x0, x0), ylim
			elif y0 == y1:	# horizontal
				x, y = xlim, (y0, y0)
			else:
				# coeff != 0
				coeff = float(y1 - y0) / (x1 - x0)

				minx = (ylim[0] - y0) / coeff + x0
				maxx = (ylim[1] - y0) / coeff + x0
				miny = coeff * (xlim[0] - x0) + y0
				maxy = coeff * (xlim[1] - x0) + y0

				if coeff > 0:
					x = max(minx, xlim[0]), min(maxx, xlim[1])
					y = max(miny, ylim[0]), min(maxy, ylim[1])
				else:
					x = max(maxx, xlim[0]), min(minx, xlim[1])
					y = min(miny, ylim[1]), max(maxy, ylim[0])


			self.set_data(x, y)

		Line2D.draw(self, renderer)


if __name__ == "__main__":
	# for command-line arguments
	import sys

	# Create the GUI application
	app = QtGui.QApplication(sys.argv)

	# show a histogram plot
	HistogramPlotWdg( [[1,2,1,1,4,3,4,5]], ["x", "y"] ).show()

	# show a scatter plot
	ScatterPlotWdg( data=([1,2,3,4,5],[10,9,7,4,0]), labels=("x", "y"), title="ScatterPlot" ).show()

	# start the Qt main loop execution, exiting from this script
	# with the same return code of Qt application
	sys.exit(app.exec_())

