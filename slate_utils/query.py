class QueryTool:

    def __init__(self, hostname, session):
        self.hostname = hostname
        self.s = session

    def remove_run_id(self, run, id):
        """Remove an id from a query run.

        Parameters
        ----------
        run : str (guid)
           The guid of the query run (`[query.run.id].[run]`).
        id : str (guid)
           The id (`[query.run.id].[id]`) of the record to be removed.
        """
        url = f"{self.hostname}/manage/query/run?cmd=results&id={id}&run={run}"
        r = self.s.post(url, data={'cmd': 'remove'})
        r.raise_for_status()
        assert 'parent.FW.Dialog.Unload' in r.text

    def remove_run(self, query, run):
        """Remove a query run.

        Parameters
        ----------
        query : str (guid)
            The guid of the query (`[query.run].[query]`).
        id : str (guid)
            The id of the run to be removed (`[query.run].[id]`)
        """
        url = f"{self.hostname}/manage/query/run?cmd=edit&id={query}&run={run}"
        r = self.s.post(url, data={'cmd': 'delete'})
        r.raise_for_status()
        assert 'parent.FW.Dialog.Unload' in r.text

    def edit_notes(self, query, html):
        """Replace the notes attribute of the given query with the specified html.

        Parameters
        ----------
        query : str (guid)
            The id of the query to edit.
        html : str (html)
            The html string of the notes. Slate is looking for html>head[title]+body.
        """
        url = f"{self.hostname}/manage/query/query?cmd=notes&id={query}"
        r = self.s.post(url, data={'cmd': 'save', 'notes': html})
        r.raise_for_status()
        return r
