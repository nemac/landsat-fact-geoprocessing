#! /usr/bin/python
#-------------------------------------------------------------------------------
# Name:         update_missing_dn.py
# Purpose:      LandsatFACT application script that calls needed functions to
#               updagte missing records for dn
#
# Author:       LandsatFACT Project Team
#               support@landsatfact.com
'''This code was developed in the public domain.  This code is provided as is, without warranty of any kind,
 express or implied, including but not limited to the warranties of
 merchantability, fitness for a particular purpose and noninfringement.
 In no event shall the authors be liable for any claim, damages or
 other liability, whether in an action of contract, tort or otherwise,
 arising from, out of or in connection with the software or the use or
 other dealings in the software.'''
#-----------------------------------------------------------------------------
def main():
    pass

if __name__ == '__main__':
    main()

import os, sys, re, traceback
import landsatFactTools_GDAL
import rasterAnalysis_GDAL
import numpy as np
import psycopg2
from LSF import *
import localLib
import pdb

DNminDict = {}

print 'Updating produicts with no status'
#find products listed as null or blank as on disk and update according to actual disk status
tableName = 'vw_list_products_files'
tableColumnList = ['file','product_id','is_on_disk']
statement = "SELECT {0},{1},{2} FROM {3} WHERE is_on_disk = '' or is_on_disk is null;".format(tableColumnList[0],tableColumnList[1],tableColumnList[2],tableName)
resultsTup = landsatFactTools_GDAL.postgresCommand(statement)

for file in resultsTup:

    if os.path.exists(file[0]) == True:
        statement = "SELECT update_is_on_disk('{0}', '{1}')".format(file[1],'YES')
        try:
            resultsTup = landsatFactTools_GDAL.postgresCommand(statement)
        except BaseException as e:
            print "Error updating product " + file[1]
         
    else: 
        print 'file ' + file[0] + ' does NOT exist!'
        statement = "SELECT update_is_on_disk('{0}', '{1}')".format(file[1],'NO')
        try:
            resultsTup = landsatFactTools_GDAL.postgresCommand(statement)
        except BaseException as e:
            print "Error updating product " + file[1]

print ''
print 'Updating produicts with status marked YES'
#list all products in the database that are listed as on disk then only update when the file is no longer on disk - switch is_on_disk from 'YES' to 'NO'
tableName = 'vw_list_products_files'
tableColumnList = ['file','product_id','is_on_disk']
statement = "SELECT {0},{1},{2} FROM {3} WHERE is_on_disk = 'YES';".format(tableColumnList[0],tableColumnList[1],tableColumnList[2],tableName)
resultsTup = landsatFactTools_GDAL.postgresCommand(statement)

for file in resultsTup:

    if os.path.exists(file[0]) == True:
        print  "nothing to update for product " + file[1]
    else:
        print 'file ' + file[0] + ' does NOT exist!'
        statement = "SELECT update_is_on_disk('{0}', '{1}')".format(file[1],'NO')
        try:
            resultsTup = landsatFactTools_GDAL.postgresCommand(statement)
        except BaseException as e:
            print "Error updating product " + file[1]

print ''
print 'Updating produicts with status marked NO'
#list all products in the database that are listed as not on disk then only update when the file is on disk - switch is_on_disk from 'NO' to 'YES'
tableName = 'vw_list_products_files'
tableColumnList = ['file','product_id','is_on_disk']
statement = "SELECT {0},{1},{2} FROM {3} WHERE is_on_disk = 'NO';".format(tableColumnList[0],tableColumnList[1],tableColumnList[2],tableName)
resultsTup = landsatFactTools_GDAL.postgresCommand(statement)

for file in resultsTup:

    if os.path.exists(file[0]) == True:
        statement = "SELECT update_is_on_disk('{0}', '{1}')".format(file[1],'YES')
        try:
            resultsTup = landsatFactTools_GDAL.postgresCommand(statement)
        except BaseException as e:
            print "Error updating product " + file[1]
    else:
        print  "nothing to update for product " + file[1] 

print ''
print 'Done updating status.'
sys.exit()
