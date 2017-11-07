#!/usr/bin/python
'''
    Project : "ArgusMedia"
    Module Name: Fundalytics_Scrapy.py
    Created Date: 2016-07-28
    Scope: Integration of Extract and Transform
;
    Version:V1: 2016-8-24
    Details:Solved Module Issue
'''

# Importing required python libraries
import ConfigParser
import sys,os
import importlib
import subprocess
import imp
Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/01_2017/12/Fundalytics_Utility.py')


# Read settings from configuration file.
try:
    config = ConfigParser.ConfigParser()
    config.read('D:/01_2017/12/Config.ini')
    
    # arguments 
    config.dsId    = sys.argv[1]
    config.dsName     = sys.argv[2]
    config.mName     = sys.argv[3]
    config.scraperParameterName     = sys.argv[4]
    try:
        config.machineName     = sys.argv[5]
    except:
        Hostname = subprocess.Popen(['hostname -I'], stdout=subprocess.PIPE,shell=True)
        config.machineName = Hostname.communicate()[0]
    inifile = 'D:/01_2017/12/'+str(sys.argv[2])+'.ini'
    config.read(config.read(inifile))
    Fundalytics_Extract = imp.load_source('Fundalytics_Extract', 'D:/01_2017/12/Fundalytics_Extract.py')
    
#     extConfig=''
#     if config.get('default', 'E_SCRAPY') != 'n/a':
#         customName = config.get('default', 'E_SCRAPY')
#         cutomFile = 'Fundalytics_Custom_Extract_' + customName
#         newModule = __import__(cutomFile)
#         extConfig = newModule.main(config)
#     else:
#         extConfig = Fundalytics_Extract.main(config)
    extConfig=config
    extConfig.add_section('filename')
    extConfig.add_section('status')	
												
    # extConfig.set("filename", "extractfilename",'Hidmet_Weather_Forecast_Serbia_Towns_none_20161116_1203.html')
    extConfig.set("filename", "extractfilename",'Casc_Market_Coupling_Price_20170110_1703.xlsx')
    # extConfig.set("filename", "extractfilename",'Ovf_Hydro_Lakes_Daily_20161124_1531.html')
    # extConfig.set("filename", "extractfilename",'Eustream_Gcvandwi_20161025_1254.json')
    # extConfig.set("filename", "extractfilename",'Eustream_Nomination_20161025_1648.json')
    # extConfig.set("filename", "extractfilename",'Eustream_Flows_20161025_1642.json')
    # extConfig.set("filename", "extractfilename",'Ambergrid_Capacities_20161021_1611.xlsx')
    # extConfig.set("filename", "extractfilename","Eustream_Flows_20161018_1658.json")
    # extConfig.set("filename", "extractfilename",'Nlogportal_Production_Facility_20161014_1309.xlsx')
    # extConfig.set("filename", "extractfilename",'Nlogportal_Production_Licence_20161014_1315.xlsx')
    # extConfig.set("filename", "extractfilename",'Nlogportal_Production_Field_20161014_1320.xlsx')
    extConfig.set("status", "extractStatus", "1")
    if (extConfig.get("status","extractStatus")=="1"):
        if config.get('default', 'T_SCRAPY') != 'n/a':
            customName = config.get('default', 'T_SCRAPY')
            cutomFile = 'Fundalytics_Custom_Transform_' + customName
            newModule = __import__(cutomFile)
            extConfig = newModule.main(config)
        else:
            print "Transform started"
            Fundalytics_Transform = imp.load_source('Fundalytics_Transform','D:/01_2017/12/Fundalytics_Transform.py')
            trnsConfig = Fundalytics_Transform.main(extConfig)
    else:
        print "Exception to be raised"
except Exception as e:
    error_log = str(e).replace('\'', '\'\'')+" line::"+str(sys.exc_traceback.tb_lineno)
    print error_log
    # Fundalytics_Utility.log(sys.argv[1],'Scrapy',error_log,'Error','')
    print "Exception to be raised"