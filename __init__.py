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

def name():
	return "RiskNat"

def description():
	return "RiskNat plugin "

def authorName():
	return "Giuseppe Sucameli (Faunalia)"

def icon():
	return "icons/logo.png"

def version():
	return "0.0.1"

def qgisMinimumVersion():
	return "1.5"

def classFactory(iface):
	from risknat_plugin import RiskNat_Plugin
	return RiskNat_Plugin(iface)

