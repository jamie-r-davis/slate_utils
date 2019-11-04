from umdriver import UMDriver
from selenium.webdriver.chrome.options import Options
import requests

def get_session(hostname, username, password):
    opts = Options()
    opts.headless = True
    with UMDriver(options=opts) as d:
        d.login(username, password)
        d.get(f"{hostname}/manage")
        s = requests.session()
        for c in d.get_cookies():
            s.cookies.set(c['name'], c['value'])
    headers = {
        'Host': hostname.replace('https://', ''),
        'Origin': hostname
    }
    s.headers.update(headers)
    return s

def get_external_session(hostname, username, password):
    """Returns an authenticated session for an external user.

    Parameters
    ----------
    hostname : str
        The hostname of the slate environment to use, including protocol (eg, https://slateuniversity.net)
    username : str
        The username to use for authentication
    password : str
        The password to use for authentication
    """
    url = f"{hostname}/manage/login?cmd=external"
    s = requests.session()
    s.headers.update({"Origin": hostname})
    r1 = s.get(url)
    r2 = s.post(r1.url, data={'user': username, 'password': password})
    r2.raise_for_status()
    return s

def steal_cookies(driver, session):
    """Steals the cookies from `driver` and adds them to `session`.

    Parameters
    ----------
    driver : webdriver
        Selenium webdriver instance where cookies will be taken from.
    session : requests.Session
        Session instance where cookies will be added.
    """
    for c in driver.get_cookies():
        session.cookies.set(c['name'], c['value'])
    return session
