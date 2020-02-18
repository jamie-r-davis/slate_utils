class ForceExecutor:
    def __init__(self, session):
        self.session = session
        self.hostname = session.headers.get("origin")

    def force_execute(self, guid, scope="person"):
        """Force the given record to execute.

        Parameters
        ----------
        guid : str
            The guid of the record to execute.
        """
        uri = f"/manage/lookup/record?id={guid}"
        if scope == "dataset":
            uri = f"/manage/lookup/record?id={guid}"
        url = f"{self.hostname}/{uri}"
        data = {"cmd": "defer"}
        r = self.session.post(url, data=data)
        r.raise_for_status()
        return r
