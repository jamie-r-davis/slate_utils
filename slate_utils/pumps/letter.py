import copy
import re

from slate_utils.common import patterns


class LetterPump:
    def __init__(self, src, dst):
        """Initialize a letter pump object.

        Parameters
        ----------
        src : SlateDB
            The source database that the pump will pull from.
        dst : SlateDb
            The target database the pump will move to.
        """
        self.src = src
        self.dst = dst

    def get(self, letter_id, db="src"):
        """Retrieve the given letter from the indicated database.

        Parameters
        ----------
        letter : str
            Either the guid of the letter or the name of the letter.
        db : str [src or dst]
            The database to use, either `src` or `dst`.
        """
        sql = "select * from [lookup.letter] where [summary] = ?"
        if re.match(patterns.GUID, letter_id):
            sql = "select * from [lookup.letter] where [id] = ?"
        if db == "dst":
            r = self.dst.select(sql, (letter_id,))
        else:
            r = self.src.select(sql, (letter_id,))
        return Letter(**next(r))

    def create(self, session, letter, rename_fields=True):
        """Create a new letter using the provided session and letter object.

        Parameters
        ----------
        session : requests.Session
            A logged-in session object that has an active session token.
        letter : slate_utils.pumps.letter.Letter
            The letter that will be used as a template to populate the new letter.
        rename_fields : bool (default: True)
            Whether to rename fields according to the field_rename xml in the src database.
        """
        hostname = session.headers.get("origin")
        url = f"{hostname}/manage/database/letter?cmd=edit&decision="
        payload = letter.serialize()
        payload["cmd"] = "save"
        if rename_fields:
            payload["html"] = self.rename_fields(payload["html"])
        r = session.post(url, data=payload)
        r.raise_for_status()
        guid = re.search(patterns.GUID, r.text).group(0)
        if guid:
            return guid
        raise ValueError("200 status code but no guid returned")

    @property
    def field_rename_dict(self):
        """Retrieve the mapping of fields that have been identified via the `field_rename` xml property.

        Returns
        -------
        dict
            A mapping of field names -> new field names as specified by the src database.
        """
        sql = """
            select
              [id] as k,
              xml.value('(//p[k="field_rename"]/v)[1]', 'varchar(200)') as v
            from [lookup.field]
            where
              xml.exist('//p[k="field_rename"]') = 1"""
        results = self.src.select(sql)
        rename_dict = {}
        for row in results:
            rename_dict[row.k] = row.v
        return rename_dict

    def rename_fields(self, html):
        """Replace any field tokens in the `html` provided using the mapping returned by `self.field_rename_dict`."""
        for k, v in self.field_rename_dict.items():
            html = re.sub(f"\\b{k}(_extended)?\\b", f"{v}\\1", html)
        return html


class Letter:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getattr__(self, attr):
        if attr in self.kwargs:
            return self.kwargs[attr]
        raise AttributeError

    def __repr__(self):
        return "<{name}: {summary} ({id})>".format(
            name=self.__class__.__name__, summary=self.summary, id=self.id
        )

    def serialize(self):
        """Return a serialized copy of the letter that can be consumed by Slate's API."""
        data = copy.deepcopy(self.kwargs)
        keys = (
            "advanced",
            "active",
            "summary",
            "export",
            "effective",
            "decision",
            "default",
            "images",
            "html",
        )
        payload = dict(((k, v) for k, v in data.items() if k in keys))
        for k, v in payload.items():
            if isinstance(v, bool):
                if v == True:
                    payload[k] = "1"
                else:
                    payload[k] = ""
        payload["effective"] = data["effective"].strftime("%m/%d/%Y")
        html = data.pop("template")
        payload["html"] = html
        return payload
