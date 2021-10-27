#!/usr/bin/python
import os
import json
import requests
import pydash
import datetime

from dotenv import load_dotenv
from group import Project
from mockresponse import MockResponse



cPrivateToken = 'xxxx'
cGitLabURL = 'xxxx'
cGitLabGroup = 'xxxx'
xJustTryWithIdProject=0
xJustTryWithOneProject=False
cVerifyArchived = False
cRemoveOldMain = False
cRemoveMaster = False
cProtectMaster = False
cSimulate = True
cLogFile = open("logFile.txt", "a+")

vListProjects = []


def main():
    load_dotenv()
    logIt(' * * * * * * * * * * * * * * * * * * * * * * * *')
    logIt('Starting process...')

    global xJustTryWithIdProject
    xJustTryWithIdProject = os.environ.get('JUST_TRY_WITH')
    logIt("JUST_TRY_WITH = "+str(xJustTryWithIdProject))

    global xJustTryWithOneProject
    xJustTryWithOneProject = json.loads(os.environ.get('JUST_TRY_ONE').lower())
    logIt("JUST_TRY_ONE = "+str(xJustTryWithOneProject))

    global cPrivateToken
    cPrivateToken = os.environ.get('PRIVATE_TOKEN')
    if pydash.predicates.is_empty(cPrivateToken):
        raise Exception('Variable PRIVATE_TOKEN not found.')
    logIt("PRIVATE_TOKEN = *********")

    global cGitLabURL
    cGitLabURL = os.environ.get('GITLAB_URL')
    if pydash.predicates.is_empty(cGitLabURL):
        raise Exception('Variable GITLAB_URL not found. ')
    logIt("GITLAB_URL = "+cGitLabURL)

    global cGitLabGroup
    cGitLabGroup = os.environ.get('GITLAB_GROUP')
    if pydash.predicates.is_empty(cGitLabGroup):
        raise Exception('Variable GITLAB_GROUP not found. ')
    logIt("GITLAB_GROUP = "+cGitLabGroup)

    global cVerifyArchived
    cVerifyArchived = json.loads(os.environ.get('VERIFY_ARCHIVED_PROJECTS').lower())
    if pydash.predicates.is_empty(os.environ.get('VERIFY_ARCHIVED_PROJECTS')):
        raise Exception('Variable VERIFY_ARCHIVED_PROJECTS not found. ')
    logIt("VERIFY_ARCHIVED_PROJECTS = "+str(cVerifyArchived))

    global cRemoveOldMain
    cRemoveOldMain = json.loads(os.environ.get('REMOVE_OLD_MAIN').lower())
    if pydash.predicates.is_empty(os.environ.get('REMOVE_OLD_MAIN')):
        raise Exception('Variable REMOVE_OLD_MAIN not found. ')
    logIt("REMOVE_OLD_MAIN = "+str(cRemoveOldMain))

    global cProtectMaster
    cProtectMaster = json.loads(os.environ.get('PROTECT_MASTER').lower())
    if pydash.predicates.is_empty(os.environ.get('PROTECT_MASTER')):
        raise Exception('Variable PROTECT_MASTER not found. ')
    logIt("PROTECT_MASTER = "+str(cProtectMaster))

    global cRemoveMaster
    cRemoveMaster = json.loads(os.environ.get('REMOVE_MASTER').lower())
    if pydash.predicates.is_empty(os.environ.get('REMOVE_MASTER')):
        raise Exception('Variable REMOVE_MASTER not found. ')
    logIt("REMOVE_MASTER = "+str(cRemoveMaster))

    if(cProtectMaster & cRemoveMaster):
        raise Exception("Variable REMOVE_MASTER and PROTECT_MASTER can't be both True.")

    global cSimulate
    cSimulate = json.loads(os.environ.get('SIMULATE').lower())
    if (cSimulate):
        logIt('*** THE PROCESS JUST WILL PRINT SOME LOGS, NONE CHANGE WILL BE APPLIED. ***')
        logIt('*** If you want apply changes, change variable SIMULATE to FALSE. ***')

    logIt('Gitlab requesting...')
    requestGroup = requests.get(cGitLabURL + '/groups/' + cGitLabGroup,
                                headers={'Content-Type': 'application/json',
                                         'PRIVATE-TOKEN': cPrivateToken})
    if (requestGroup.status_code != 200):
        raise Exception(
            'Gitlab returned ' + str(requestGroup.status_code) + ' - ' + requestGroup.reason)

    Group = requestGroup.json()

    whileStr ="Your group name is: " + Group['name'] + ". Press Y + Enter to confirm! [y/n] => "
    logIt(whileStr)
    while input(whileStr) == "y":
        projects = Group['projects']
        shared_projects = Group['shared_projects']

        logIt(str(len(projects)+len(shared_projects)) +
              ' projects will be checked...')

        for p in range(len(projects)):
            if json.loads(str(projects[p]['archived']).lower()):
                if cVerifyArchived:
                    if (str(projects[p]['default_branch']).lower() == 'master'):
                        if (int(xJustTryWithIdProject) >= 1):
                            if int(projects[p]['id']) == int(xJustTryWithIdProject):
                                includ2Array(projects[p])
                        else:
                            includ2Array(projects[p])
            else:
                if (str(projects[p]['default_branch']).lower() == 'master'):
                    if (int(xJustTryWithIdProject) >= 1):
                        if int(projects[p]['id']) == int(xJustTryWithIdProject):
                            includ2Array(projects[p])
                    else:
                        includ2Array(projects[p])

        logIt(str(len(vListProjects)) + ' projects to apply changes...')

        checkProjects()

        logIt('Successfully completed!')
        break
    logIt(' ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~')

def includ2Array(project):
    prj = Project(project['id'], project['path'])
    if prj not in vListProjects:
        vListProjects.append(prj)

def checkProjects():
    for i in range(len(vListProjects)):

        getBranchMain = getBranch(vListProjects[i])
        global xJustTryWithOneProject
        if xJustTryWithOneProject:
            whileStr ='You were given the option to change only one project. So, see what is: ' + str(vListProjects[i].id) + ' - '+ vListProjects[i].name +'. Press ENTER to continue.'
            logIt(whileStr)
            while input(whileStr)  != "":
                break

        if (getBranchMain.status_code == 200):
            logIt('The "'+vListProjects[i].name +'" project already has a branch named "main".')
            removeMain = removeOldMain(vListProjects[i])
            if (removeMain.status_code == 204):
                newMain = createMain(vListProjects[i])
            else:
                continue
        else:
            newMain = createMain(vListProjects[i])

        if (newMain.status_code == 201):
            putMain = setMainDefault(vListProjects[i])

        if(putMain.status_code == 200):
            delMaster = deleteMaster(vListProjects[i])
            if delMaster.status_code != 204:
                protectMaster(vListProjects[i])

        if xJustTryWithOneProject:
            break


def getBranch(project):
    if (cSimulate):
        return MockResponse({"key1": "value1"}, 404)
    else:
        return requests.get(cGitLabURL + '/projects/' + str(project.id) + '/repository/branches/main',
                            headers={'Content-Type': 'application/json',
                                     'PRIVATE-TOKEN': cPrivateToken})


def removeOldMain(project):
    if (cRemoveOldMain):
        if (cSimulate):
            logIt('Removing branch "main" from "' +str(project.name)+'" project.')
            return MockResponse({"key1": "value1"}, 204)
        else:
            logIt('Removing branch "main" from "' +str(project.name)+'" project.')
            return requests.delete(cGitLabURL + '/projects/' + str(project.id) + '/repository/branches/main',
                                   headers={'Content-Type': 'application/json',
                                            'PRIVATE-TOKEN': cPrivateToken})


def createMain(project):
    if(cSimulate):
        logIt('Creating a branch "main" to "' + project.name+'" project.')
        logIt('Branch "main" created with success to "' +project.name+'" project.')
        return MockResponse({"key1": "value1"}, 201)
    else:
        postBranch = requests.post(cGitLabURL + '/projects/' + str(project.id) + '/repository/branches?branch=main&ref=master',
                                   headers={'Content-Type': 'application/json',
                                            'PRIVATE-TOKEN': cPrivateToken})

        if (postBranch.status_code == 201):
            logIt('Branch "main" created with success to "' +project.name+'" project.')
            return postBranch
        else:
            raise Exception('Branch "main" WAS NOT created to "' + project.name+'" project. ' + str(
                postBranch.status_code) + ' - ' + postBranch.reason)


def setMainDefault(project):
    if (cSimulate):
        logIt('Changing default branch to "main" at "' +project.name+'" project.')
        logIt('Default branch changed to "main" at "' +project.name+'" project with success!')
        return MockResponse({"key1": "value1"}, 200)
    else:
        logIt('Changing default branch to "main" at "' +project.name+'" project.')
        putBranch = requests.put(cGitLabURL + '/projects/' + str(project.id) + '?default_branch=main',
                                  headers={'Content-Type': 'application/json',
                                           'PRIVATE-TOKEN': cPrivateToken})
        if(putBranch.status_code == 200):
            logIt('Default branch changed to "main" at "' +project.name+'" project!')
            return putBranch
        else:
            logIt('Fail to change default branch to "main" at "' +project.name+'" project!')
            return putBranch


def deleteMaster(project):
    if(cRemoveMaster) and (not cProtectMaster):
        if(cSimulate):
            logIt('Deleting branch "master" from "' +project.name+'" project.')
            logIt('Branch "master" removed with success from "' +project.name+'" project.')
            return MockResponse({"key1": "value1"}, 204)
        else:
            deleteBranch = requests.delete(cGitLabURL + '/projects/' + str(project.id) + '/repository/branches/master',
                                           headers={'Content-Type': 'application/json',
                                                    'PRIVATE-TOKEN': cPrivateToken})
            if(deleteBranch.status_code == 204):
                logIt('Branch "master" removed with success from "' +project.name+'" project.')
                return deleteBranch
            else:
                logIt('Branch "master" was not found in "' +project.name+'" project.')
                return deleteBranch
    else:
        return MockResponse({"key1": "value1"}, 404)

def protectMaster(project):
    if(not cSimulate) and (cProtectMaster) and (not cRemoveMaster):
        protectBranch = requests.post(cGitLabURL + '/projects/' + str(project.id) + '/protected_branches?name=master&push_access_level=30&merge_access_level=30&unprotect_access_level=40',
                                           headers={'Content-Type': 'application/json',
                                                    'PRIVATE-TOKEN': cPrivateToken})
        if (protectBranch.status_code in (409,201)):
            logIt('The branch "master" of "' +project.name+'" project, has been protected')
        
def logIt(str):
    global cLogFile
    xNow = datetime.datetime.now()
    xDate = xNow.strftime("%d/%m/%Y %H:%M:%S")
    xLog = xDate + " - " + str + "\n"
    cLogFile.write(xLog)
    print(xLog)
    cLogFile.flush()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logIt(e)
    
    cLogFile.close()
