class ConsolidateRecords:
    scopes = ["person", "dataset", "school", "relation", "relation_related", "school_key", "job_key"]

    def __init__(self, session):
        self.hostname = session.headers.get('origin')
        self.session = session

    def refresh_one(self, scope):
        url = f"{self.hostname}/manage/database/dedupe?cmd=refresh&scope={scope}"
        response = self.session.get(url)
        response.raise_for_status()
        return response

    def refresh_all(self):
        for scope in self.scopes:
            self.refresh_one(scope)