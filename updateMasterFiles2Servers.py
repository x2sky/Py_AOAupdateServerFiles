# -*- updateMasterFiles2Servers.py -*- #
"""
SYNOPSIS
    Copy the updated files from the master directory to the selected servers

DESCRIPTION
    description of the functions
   
EXAMPLES
    class listSrcFiles(folderSrc) - creates an object that contains folderSrc (the name of the subfolder in the source
    folder), path (the whole path of folderSrc), and listFiles (the list of files that need to be uploaded)
    def main(folderSrc, folderDest, folderSub) - upload files from folderSrc/folderSub to folderDest/folderSub

VERSION 0.0
AUTHOR
    Becket Hui 2020 07
    
"""
import glob, logging, os, sys, time
from shutil import copy


class listSrcFiles:
    def __init__(self, folderSrc):
        self.folderSrc = folderSrc
        self.pathSrc = ''
        self.listFiles = []


def main(folderSrc, folderDest, folderSub):
    # file types to copy:
    listExt = ['*.dll', '*.xml', '*.csv', '*.cs']
    # check if subfolders exist in source
    listSrcObj = []
    for subD in folderSub:
        path = os.path.join(folderSrc, subD)
        if not os.path.isdir(path):
            logger.error('Source folder ' + path + ' does not exist, exiting...')
            sys.exit(time.sleep(5))
        else:
            listObj = listSrcFiles(subD)
            listObj.pathSrc = path
            [listObj.listFiles.extend(glob.glob(os.path.join(path, extension))) for extension in listExt]
            listSrcObj.append(listObj)
    # start upload process
    logger.info('Start uploading process...')
    for destination in folderDest:
        # first check if destination folder exists
        if not os.path.isdir(destination):
            logger.warning('Destination ' + destination + ' cannot be found, skipping...')
            continue
        for srcObj in listSrcObj:
            # check if subfolder exists in the destination
            destPath = os.path.join(destination, srcObj.folderSrc)
            if not os.path.isdir(destPath):
                logger.warning(destPath + ' does not exist, skipping...')
                continue
            # if subfolder exists, copy newer files from source to destination
            logger.info('Copying files from ' + srcObj.folderSrc + ' to ' + destination)
            for srcFile in srcObj.listFiles:
                srcTime = os.path.getmtime(srcFile)
                destFilePath = os.path.join(destPath, os.path.basename(srcFile))
                destTime = os.path.getmtime(destFilePath) if os.path.exists(destFilePath) else None
                if destTime is None or destTime < srcTime:
                    copy(srcFile, destFilePath)
                    logger.debug('Copy ' + srcFile + ' to ' + destination + ' completed.')
                else:
                    logger.debug('Skip copying ' + srcFile + ', file in ' + destination + ' is newer.')
    return


if __name__ == '__main__':
    folderCurr = os.path.dirname(os.path.abspath(__file__))
    try:
        settingFile = os.path.join(folderCurr, 'updateMasterFilesSettings.txt')
        readDirSrc = False
        readDirDest = False
        readSubFolder = False
        folderSrc = ''
        folderSub = []
        folderDest = []
        with open(settingFile, 'r') as filePt:
            for line in filePt:
                if line.rstrip() == 'Source:':
                    readDirSrc = True
                    readDirDest = False
                    readSubFolder = False
                    continue
                if line.rstrip() == 'Destinations:':
                    readDirSrc = False
                    readDirDest = True
                    readSubFolder = False
                    continue
                if line.rstrip() == 'Subfolders:':
                    readDirSrc = False
                    readDirDest = False
                    readSubFolder = True
                    continue
                if readDirSrc is True:
                    folderSrc = line.rstrip()
                if readDirDest is True:
                    folderDest.append(line.rstrip())
                if readSubFolder is True:
                    folderSub.append(line.rstrip())
    except:
        print('Error in reading ' + settingFile + '!!')
        sys.exit(time.sleep(5))
    try:
        logFile = os.path.join(folderCurr, 'log.txt')
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)  # need to set logger level to lowest
        # set file handler
        fileHandler = logging.FileHandler(logFile, mode='w')
        fileHandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s',
                                                   datefmt='%Y/%m/%d %H:%M:%S'))
        fileHandler.setLevel(logging.DEBUG)
        logger.addHandler(fileHandler)
        # set console handler
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logging.Formatter('%(message)s'))
        consoleHandler.setLevel(logging.INFO)
        logger.addHandler(consoleHandler)
    except:
        print('Cannot open ' + logFile + ', please close the log file and restart.')
        sys.exit(time.sleep(5))
    logger.info('Start updateMasterFiles2Servers')
    logger.debug('Source folder:')
    logger.debug(folderSrc)
    logger.debug('Destination folders:')
    [logger.debug(folder) for folder in folderDest]
    main(folderSrc, folderDest, folderSub)
    logger.info('Transfer completed.')
    sys.exit(time.sleep(10))