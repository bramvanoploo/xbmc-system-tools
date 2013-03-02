import config
import datetime

def debug(message, method = ''):
    if config.debug:
        debugLog = open(config.debug_log_file, 'a')
        debugLog.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' : ' +method+ ' : ' +message+ '\n')
        debugLog.close()

def error(message, method = ''):
    errorLog = open(config.error_log_file, 'a')
    errorLog.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' : ' +method+ ' : ' +message+ '\n')
    errorLog.close()

def info(message, method = ''):
    infoLog = open(config.info_log_file, 'a')
    infoLog.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' : ' +method+ ' : ' +message+ '\n')
    infoLog.close()