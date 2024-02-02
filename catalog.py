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
        self.start_date = None
        self.end_date = None
        self.shape = None
        self.coords = None
        self.sort_by = None
        self.published_min_year = None
        self.published_max_year = None
        self.published_author = None
        self.publisher = None

    def bibli_search(self, args=()):
        """

        :param search_params: A collection of user-specified search criteria.
        :return: An 'EventCatalog' object.
        """
        from bibliography_search import fetch_url, format_url, parse_bibli_page

        url = format_url(args)
        body = fetch_url(url)
        # TODO: parse bibli page
        cat = parse_bibli_page(body)
        # TODO: TEST (1) is search empty
        # TODO: TEST (2) is search too full

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
        if self.start_date is not None:
            output += f"Start date={self.start_date}\n"
        if self.end_date is not None:
            output += f"End date={self.end_date}\n"
        if output == "":
            output = "No search parameters defined"
        print(output)

    def __str__(self):
        return "catalog results placeholder"
