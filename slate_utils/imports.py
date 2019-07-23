import html
import requests


class Importer:

    def __init__(self, hostname, username, password):
        self.hostname = hostname.replace('https://', '')
        self.username = username
        self.password = password

    def force_pickup(self, verbose=False):
        """
        Trigger a force pickup.

        Parameters
        ----------
        verbose : bool
            When True, the
        """
        url = f"https://{self.hostname}/manage/service/import?cmd=pickup"
        r = requests.get(url, auth=(self.username, self.password), stream=True, hooks={'response': print_response})
        r.raise_for_status()

    def force_import(self, verbose=False):
        """
        Trigger a force import.
        """
        url = f"http://{self.hostname}/manage/import/load?cmd=process"
        r = requests.get(url, auth=(self.username, self.password), stream=True, hooks={'response': print_response})
        r.raise_for_status()

def print_response(r, *args, **kwargs):
    for line in r.iter_lines(decode_unicode=True):
        if line:
            print(html.unescape(line).replace('<br />', '\n'))
