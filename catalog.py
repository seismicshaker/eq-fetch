"""
An 'EventCatalog' holds an

"""


class SearchCatalog:
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
        self.shape = "POLY"
        self.coords = ""
        self.sort_by = "day"
        self.published_min_year = ""
        self.published_max_year = ""
        self.published_author = ""
        self.publisher = ""

    def bibli_search(self, args=()):
        """

        :param search_params: A collection of user-specified search criteria.
        :return: An 'EventCatalog' object.
        """
        from bibliography_search import (_dict_bibli_search, fetch_url,
                                         format_url, parse_bibli_page)

        bibli_search = _dict_bibli_search(args)
        url = format_url(bibli_search)
        body = fetch_url(url)
        cat = parse_bibli_page(body)

        return cat

    def hypo_search(self, args=()):
        """

        :param search_params: A collection of user-specified search criteria.
        :return: An 'EventCatalog' object.
        """
        print("here hypo")
        print(args)
        return self

    def get_params(self):
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
