from bs4 import BeautifulSoup
import requests
import time

def timeParser(wait_time):
    if wait_time == 'Instant' or wait_time == 'No Minimum':
        wait_time = None
    elif 'minutes' in wait_time:
        if '60' in wait_time:
            wait_time = time.gmtime(60 * 60)
        else:
            wait_time = time.strptime(wait_time, '%M minutes')
        wait_time = time.strftime('%H:%M', wait_time)
    elif 'Hours' in wait_time:
        wait_time = time.strptime(wait_time, '%H Hours')
        wait_time = time.strftime('%H:%M', wait_time)
    elif 'day' in wait_time:
        wait_time = time.strptime(wait_time, '%d day %H hrs')
        wait_time = time.strftime('%d:%H:%M', wait_time)
    else:
        wait_time = time.strptime(wait_time, '%Hhr %Mmin')
        wait_time = time.strftime('%H:%M', wait_time)
        
    return wait_time

def getMissionInfo(mission):
    name = mission.find('div', class_='mh').text
    missionInfo = mission.find_all('div', class_='mz')
    total = int(missionInfo[0].find('div', class_='m2').text)
    maximum = int(missionInfo[1].find('div', class_='m2').text)
    waitingTime = missionInfo[2].find('div', class_='m2').text
    waitingTimeTotal = missionInfo[4].find('div', class_='m2').text
    waitingTime = timeParser(waitingTime)
    waitingTimeTotal = timeParser(waitingTimeTotal)

    mission = {
        'name': name,
        'total': total,
        'maximum': maximum,
        'wait_time': waitingTime,
        'total_wait_time': waitingTimeTotal
    }
    return mission

def getSessionInfo(session):
    missonsDiv = session.find_all('div', class_='ml')
    session = {
        'session':int(session.find('div', class_='nnh').text.split()[4]),
        'missions':[]
    }
    for missionDiv in missonsDiv:
        mission = getMissionInfo(missionDiv)
        session['missions'].append(mission)
    return session

def getLapInfo(lapDiv):
    lap = {
        'lap': int(lapDiv.find('div', class_='nnh').text.split()[1]),
        'sessions':[]
    }
    sessionsdiv = lapDiv.find_all('div', class_='nn')
    for session in sessionsdiv:
        lap['sessions'].append(getSessionInfo(session))

    return lap

def getAllLaps():
    hr_url = 'https://deetlist.com/dragoncity/events/race/'
    page_html = requests.get(hr_url).text
    soup = BeautifulSoup(page_html, 'html.parser')

    lapsHTML = soup.find_all('div', class_='hl')
    laps = []
    for lap in lapsHTML:
        laps.append(getLapInfo(lap))
    return laps

getAllLaps()