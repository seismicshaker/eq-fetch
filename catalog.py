"""
An 'EventCatalog' holds an

"""


class EventCatalog:
    """
    EventCatalog
    """

    def __init__(self):
        """Create a new 'EventCatalog'.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._start_date = None
        self._end_date = None

    def bibli_search(self, args=()):
        """

        :param search_params: A collection of user-specified search criteria.
        :return: An 'EventCatalog' object.
        """
        from bibliography_search import format_search_paraams, format_url

        search_params = format_search_paraams(args)
        print(search_params)
        # TODO: import url formatter

        return self

    def hypo_search(self, args=()):
        """

        :param search_params: A collection of user-specified search criteria.
        :return: An 'EventCatalog' object.
        """
        print("here hypo")
        print(args)
        return self

    def get_search_params(self):
        """Return str(self)"""
        output = ""
        if self._start_date is not None:
            output += f"Start date={self._start_date}\n"
        if self._end_date is not None:
            output += f"End date={self._end_date}\n"
        if output == "":
            output = "No search parameters defined"
        print(output)

    def __str__(self):
        return "catalog results placeholder"
