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
