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
import sys,os,socket
import importlib
import subprocess
import imp,math
import datetime
from dateutil.relativedelta import relativedelta
# print "loading"

Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/01_2017/06/Fundalytics_Utility.py')
# Fundalytics_Utility = imp.load_source('Fundalytics_Utility', 'D:/argus_media/backfilling_data/Fundalytics_Utility.py')


# DB connection function.
connection=Fundalytics_Utility.DB_connection()
mysql_connection=connection.cursor()

# Global variable
error_log=''

# To get the host name of the Running server
# hostname = socket.gethostname()
# Host_IP = socket.gethostbyname(hostname)

config = ConfigParser.ConfigParser()
config.read('D:/01_2017/06/Config.ini')

try:
    dsID = sys.argv[1]
    dsName = sys.argv[2]
    mName = sys.argv[3]
    ScraperParameters = sys.argv[4]
    try:
        config.machineName     = sys.argv[5]
    except:
		Hostname = subprocess.Popen(['hostname -I'], stdout=subprocess.PIPE, shell=True)
		config.machineName = Hostname.communicate()[0]
    config.dsId = dsID
    config.dsName = dsName
    config.mName = mName
    config.scraperParameterName = ScraperParameters
    inifile = 'D:/01_2017/06/' + str(dsName) + '.ini'
	# print "ini file:",inifile
    config.read(config.read(inifile))
    Fundalytics_Extract = imp.load_source('Fundalytics_Extract','D:/01_2017/06/Fundalytics_Extract.py')
    extConfig = ''
    try:
		if '/B' in dsID:
			# print "backfilling:"
			backFillQuery = "SELECT DataSourceID, BackFillFromDate, BackFillToDate, IsBackFill FROM `ScraperSchedule` WHERE IsBackFill = 'yes' and DataSourceID='" + str(dsID) + "'"
			mysql_connection.execute(backFillQuery)
			count = mysql_connection.rowcount
			print count
			# Condition to check if the query output is not empty
			if count > 0:
				result = mysql_connection.fetchone()
				dsID = result[0]
				BackFillFrom = datetime.datetime.strptime(str(result[1]), '%Y-%m-%d %H:%M:%S')
				BackFillTo = datetime.datetime.strptime(str(result[2]), '%Y-%m-%d %H:%M:%S')
				IsBackFill = str(result[3]).upper()
				Interval = config.get('backfilling-' + config.mName, 'E_INTERVAL')
				if str(Interval) == 'n/a':
					Fundalytics_Utility.log(sys.argv[1], 'Scrapy', "There is no way to backfill the DataSource ",'Error', '')
					sys.exit()
				else:

					'''backfilling process'''
					BackFillNextStartDate = BackFillFrom
					NoOfDays = (BackFillTo - BackFillFrom).days

					if int(NoOfDays) >= 31:
						# Error "above 31 days"
						Fundalytics_Utility.log(sys.argv[1], 'Scrapy',"Backfill date is out of range,it should be within 31 days ",'Error', '')
						sys.exit()
					else:
						DateRange = float(NoOfDays + 1) / int(Interval)
						for dateTry in range(int(math.ceil(DateRange))):

							'''Setting back fill from and to date'''
							StartDate = BackFillNextStartDate
							EndDate = StartDate + relativedelta(days=int(int(Interval) - 1))
							if (EndDate <= BackFillTo) == True:
								BackFillNextStartDate = EndDate + relativedelta(days=int(1))
							else:
								EndDate = BackFillTo

							'''if startdate==end date,then startdate-1 if interval is not 1'''
							if (StartDate == EndDate) == True:
								if int(Interval) != 1:
									StartDate = StartDate + relativedelta(days=-1)
									EndDate = EndDate

							# print"BackFillStartDate:", StartDate
							# print "BackFillEndDate:", EndDate

							config.add_section('backfill_data-' + config.mName)
							config.set("backfill_data-" + config.mName, str(config.dsName) + "BackFillFrom",str(StartDate))
							config.set("backfill_data-" + config.mName, str(config.dsName) + "BackFillTo",str(EndDate))
							config.set("backfill_data-" + config.mName, str(config.dsName) + "IsBackFill",str(IsBackFill))

							# call Extract.py and transform.py
							if config.get('default', 'E_SCRAPY') != 'n/a':
								customName = config.get('default', 'E_SCRAPY')
								cutomFile = 'Fundalytics_Custom_Extract_' + customName
								print 'D:/01_2017/06/' + cutomFile + '.py'
								cutomFile = imp.load_source(cutomFile, 'D:/01_2017/06/' + str(cutomFile) + '.py')
								extConfig = cutomFile.main(config)
							else:
								extConfig = Fundalytics_Extract.main(config)

							Fundalytics_Transform = imp.load_source('Fundalytics_Transform','D:/01_2017/06/Fundalytics_Transform.py')
							if (extConfig.get("status", "extractStatus") == "1"):
								trnsConfig = Fundalytics_Transform.main(extConfig)
							else:
								print "Exception to be raised"

							config.remove_section('backfill_data-' + config.mName)
							config.remove_section('status')
							config.remove_section('filename')
							config.remove_section('statustr')

			else:
				Fundalytics_Utility.log(sys.argv[1], 'Scrapy',"There is no backfill days for this " + str(config.dsName) + " DataSource ",'Error', '')
				sys.exit()
			updatequery = "update `ScraperSchedule` set IsBackFill = 'No' where DataSourceID='" + str(dsID) + "'"
			mysql_connection.execute(updatequery)
			connection.commit()
		else:
			try:
				if config.get('backfilling-' + config.mName, 'E_BACKDATEDDATA') == 'YES':
					BackData = config.get('backfilling-' + config.mName, 'E_BACKDATEDDATA')
				else:
					BackData = 'n/a'
				if BackData != 'n/a':
					for dateTry in range(6):
						print "dateTry_Value:", dateTry
						config.add_section("BackDatedData-" + str(config.mName))

						config.set("BackDatedData-" + str(config.mName), str(config.dsName) + str("BackData"),
								   str(dateTry))
						print "backdated", config.get("BackDatedData-" + str(config.mName),
													  str(config.dsName) + str("BackData"))

						# call Extract.py and transform.py
						if config.get('default', 'E_SCRAPY') != 'n/a':
							customName = config.get('default', 'E_SCRAPY')
							cutomFile = 'Fundalytics_Custom_Extract_' + customName
							print 'D:/01_2017/06/' + cutomFile + '.py'
							cutomFile = imp.load_source(cutomFile,
														'D:/01_2017/06/' + str(cutomFile) + '.py')
							extConfig = cutomFile.main(config)
						else:
							extConfig = Fundalytics_Extract.main(config)

						Fundalytics_Transform = imp.load_source('Fundalytics_Transform',
																'D:/01_2017/06/Fundalytics_Transform.py')
						if (extConfig.get("status", "extractStatus") == "1"):
							trnsConfig = Fundalytics_Transform.main(extConfig)
						else:
							print "Exception to be raised"

						config.remove_section('BackDatedData-' + config.mName)
						config.remove_section('status')
						config.remove_section('filename')
						config.remove_section('statustr')

			except:
				raise Exception
    except Exception as e:

		# call Extract and transform
		if config.get('default', 'E_SCRAPY') != 'n/a':
			customName = config.get('default', 'E_SCRAPY')
			cutomFile = 'Fundalytics_Custom_Extract_' + customName
			print 'D:/01_2017/06/' + cutomFile + '.py'
			cutomFile = imp.load_source(cutomFile, 'D:/01_2017/06/' + str(cutomFile) + '.py')
			extConfig = cutomFile.main(config)
		else:
			extConfig = Fundalytics_Extract.main(config)

		Fundalytics_Transform = imp.load_source('Fundalytics_Transform',
												'D:/01_2017/06/Fundalytics_Transform.py')
		if (extConfig.get("status", "extractStatus") == "1"):
			trnsConfig = Fundalytics_Transform.main(extConfig)
		else:
			print "Exception to be raised"

    #return "SUCCESS"
	
except Exception as e:
    print e
    error_log = str(e).replace('\'', '\'\'') + " line::" + str(sys.exc_traceback.tb_lineno)
    print error_log
    Fundalytics_Utility.log(sys.argv[1], 'Scrapy', error_log, 'Error', '')
    print "Exception to be raised"
#     return "FAILURE"