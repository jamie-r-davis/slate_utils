import html
import requests


class Importer:

    def __init__(self, session):
        self.session = session

    def force_pickup(self, verbose=False):
        """
        Trigger a force pickup.

        Parameters
        ----------
        verbose : bool
            When True, the
        """
        url = f"https://{self.hostname}/manage/service/import?cmd=pickup"
        r = self.session.get(url, stream=True, hooks={'response': print_response})
        r.raise_for_status()

    def force_import(self, verbose=False):
        """
        Trigger a force import.
        """
        url = f"http://{self.hostname}/manage/import/load?cmd=process"
        r = self.session.get(url, stream=True, hooks={'response': print_response})
        r.raise_for_status()

def print_response(r, *args, **kwargs):
    for line in r.iter_lines(decode_unicode=True):
        if line:
            print(html.unescape(line).replace('<br />', '\n'))
