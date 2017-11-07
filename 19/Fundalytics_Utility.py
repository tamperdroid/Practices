'''
    Project : "ArgusMedia"
    Created Date: 2016-07-13
    Module Name: AM_error_log.py
    Scope: To update ErrorReason in ScraperSchedule table and also write ErrorReason in logfile for all exception.
    
    2016-07-15 - Muthu babu - V1
    Details: First version module developed
'''

'''

Import required modules

'''

import pymysql
from datetime import datetime
import os, sys
import ConfigParser
import time
import boto
import glob
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
import redis


# Read settings from configuration file.
config = ConfigParser.ConfigParser()
config.read("D:/01_2017/18/Config.ini")


def redis_connection(datasourceid,key):
    value='Pending'
    try:
        red_con = redis.StrictRedis(host=config.get('redis', 'server'), port=config.get('redis', 'port'), db=config.get('redis', 'db'))
        
        val = red_con.set(key,value)
    except Exception as e:
        log(datasourceid,'Transform-Module',e,'RedisError','')
        pass
    return val



def s3_fileupload(filename,DataSourceID,TargetFilepath,module_name,control):
    
    AWS_ACCESS_KEY_ID=control.get('s3_backup','AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=control.get('s3_backup','AWS_SECRET_ACCESS_KEY')

    # Bucket name.
    bucket_name = control.get('s3_backup','bucket_name')
    
    # Source and destination file path.
    Sourcefilename = filename
   
    def percent_cb(complete, total):
        sys.stdout.write('')
        sys.stdout.flush()

    try:
        # Connecting the S3.
        aws_connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = aws_connection.get_bucket(bucket_name)

        # This function push the file to S3.
        k = Key(bucket)
        k.key =TargetFilepath+'/'+ os.path.basename(Sourcefilename);
        # k.key =  os.path.basename(Sourcefilename);
        k.set_contents_from_filename(Sourcefilename, cb=percent_cb, num_cb=10)
    except Exception as e:
        # print ("Error")
        log(DataSourceID, module_name, str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),'Error','')

    #os.remove(filename)
def date_validation_status (datasourceid,ValidatedDateStatus,count):
    connection = DB_connection()
    cur = connection.cursor()
    error_log=''
    if ('pymysql' in str(cur)) and str(datasourceid) != '':
        try:
            if str(ValidatedDateStatus) == 'Success':
                query = "UPDATE ScraperSchedule SET ValidatedDateStatus='"+str(ValidatedDateStatus)+"',NumberofRetry='' WHERE DataSourceID='"+str(datasourceid)+"'"
                cur.execute(query)
                connection.commit()
            else:
                query = "UPDATE ScraperSchedule SET ValidatedDateStatus='"+str(ValidatedDateStatus)+"' WHERE DataSourceID='"+str(datasourceid)+"'"
                cur.execute(query)
                connection.commit()
        except Exception as e:
            error_log=str(error_log)+" "+str(e)+" line no:"+str(sys.exc_traceback.tb_lineno)
            log(datasourceid,'Count-Update',error_log,'Error','')
    else:
        error_log=str(error_log)+" "+str(connection)
        log(datasourceid,'Count-Update',error_log,'Error','')

def s3_removefile(DataSourceID,Sourcefilename,module_name,control):
   
    AWS_ACCESS_KEY_ID=control.get('s3_backup','AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=control.get('s3_backup','AWS_SECRET_ACCESS_KEY')
    aws_connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    
    # Bucket name.
    bucket_name = control.get('s3_backup','bucket_name')
    bucket = aws_connection.get_bucket(bucket_name)
   
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    key = Key(bucket, Sourcefilename)
   
    try:
        key.delete()
    except boto.exception.S3ResponseError as e:
        log(DataSourceID, module_name, str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),'Error','')
        


def s3_filedownload(TargetFilepath,DataSourceID,Sourcefilename,module_name,control):
   
    AWS_ACCESS_KEY_ID=control.get('s3_backup','AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=control.get('s3_backup','AWS_SECRET_ACCESS_KEY')
    aws_connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    
    # Bucket name.
    bucket_name = control.get('s3_backup','bucket_name')
    bucket = aws_connection.get_bucket(bucket_name)
   
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    key = Key(bucket, Sourcefilename)
    mode = 'wb'
     
    try:
        with open(TargetFilepath, mode) as f:
            key.get_contents_to_file(f)
            f.truncate()
    except boto.exception.S3ResponseError as e:
        log(DataSourceID, module_name, str(e) + ' line no: ' + str(sys.exc_traceback.tb_lineno),'Error','')
        return e.status
    


def DB_connection():
    attempts = 0
    
    # Connecting production Mysql database.
    while attempts < 3:
        try:
            connection = pymysql.connect(host="" + str(config.get('mysql', 'host')) + "",
                                         database="" + str(config.get('mysql', 'name')) + "",
                                         user="" + str(config.get('mysql', 'user')) + "",
                                         password="" + str(config.get('mysql', 'password')) + "")
            return connection
            break
        except Exception as e:
            error_log = e;
            print error_log
            attempts += 1
            time.sleep(5)

    # If production data base down to connecting backup Mysql database.
    if attempts == 3:
        attempts = 0
        while attempts < 3:
            try:
                connection = pymysql.connect(host="" + str(config.get('mysql', 'host')) + "",
                                             database="" + str(config.get('mysql', 'name')) + "",
                                             user="" + str(user=config.get('mysql', 'user')) + "",
                                             password="" + str(password=config.get('mysql', 'password')) + "")
                return connection
                break
            except Exception as e:
                error_log = e;
                attempts += 1
                time.sleep(5)

def count_update (datasourceid,value_count):
    connection = DB_connection()
    cur = connection.cursor()
    error_log=''
    if ('pymysql' in str(cur)) and str(datasourceid) != '':
        try:
            query = "UPDATE ScraperSchedule SET NumberofRecords='"+str(value_count)+"' WHERE DataSourceID='"+str(datasourceid)+"'"
            cur.execute(query)
            connection.commit()
        except Exception as e:
            error_log=str(error_log)+" "+str(e)+" line no:"+str(sys.exc_traceback.tb_lineno)
            log(datasourceid,'Count-Update',error_log,'Error','')
    else:
        error_log=str(error_log)+" "+str(connection)
        log(datasourceid,'Count-Update',error_log,'Error','')
        
def log(datasourceid,module,error,status,filepath):
    '''
    Get current date and time
    '''
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d %H:%M:%S")
    error_log=''
    ''' Format the error log - DATETIME_MODULE_ERROR '''
    if str(error) != '':
        error_log= str(current_date)+"_"+str(module)+"_"+str(error).strip()
    
    
    ''' Database connection'''
    
    connection = DB_connection()
    cur = connection.cursor()
    error_log=str(error_log).replace('\'','')
#     sys.exit()
    ''' Update the error log into database '''
    if ('pymysql' in str(cur)) and str(datasourceid) != '':
        if str(status) == 'Extracted':
            try:
                query = "UPDATE ScraperSchedule SET TaskStatus='"+str(status)+"', ErrorReason='"+str(error_log)+"',RawFilePath='"+str(filepath)+"' WHERE DatasourceID='"+str(datasourceid)+"' and TaskStatus<>'Error'"
                cur.execute(query)
                connection.commit()
            except Exception as e:
                error_log=str(error_log)+" "+str(e)+" line no:"+str(sys.exc_traceback.tb_lineno)
        elif str(status) == 'Transformed':
            try:
                query = "UPDATE ScraperSchedule SET TaskStatus='"+str(status)+"', ErrorReason='"+str(error_log)+"',CookedFilePath='"+str(filepath)+"' WHERE DatasourceID='"+str(datasourceid)+"' and TaskStatus<>'Error'"
                cur.execute(query)
                connection.commit()
            except Exception as e:
                error_log=str(error_log)+" "+str(e)+" line no:"+str(sys.exc_traceback.tb_lineno)
        elif str(status) == 'Extraction Started':
            try:
                query = "UPDATE ScraperSchedule SET TaskStatus='"+str(status)+"', ErrorReason='"+str(error_log)+"',CookedFilePath='"+str(filepath)+"' WHERE DatasourceID='"+str(datasourceid)+"' and TaskStatus<>'Error'"
                cur.execute(query)
                connection.commit()
            except Exception as e:
                error_log=str(error_log)+" "+str(e)+" line no:"+str(sys.exc_traceback.tb_lineno)
        else:
            try:
                query = "UPDATE ScraperSchedule SET TaskStatus='"+str(status)+"', ErrorReason='"+str(error_log)+"' WHERE DatasourceID='"+str(datasourceid)+"' and TaskStatus<>'Error'"
                cur.execute(query)
                connection.commit()
            except Exception as e:
                error_log=str(error_log)+" "+str(e)+" line no:"+str(sys.exc_traceback.tb_lineno)
    else:
        error_log=str(error_log)+" "+str(connection)
    if str(error) != '':    
        ''' Append the error log into log file '''    
        log_file=open("AM_ErrorReason.log","a")
        log_file.write(str(error_log)+"\n")
        log_file.close()

# Database status update


# Redis Queue connection
class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue'):
       self.__db = redis.Redis(host = config.get('redis', 'server'), port = config.get('redis', 'port'), db = config.get('redis', 'q_db'))
       self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue. 

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)