"""
An 'EventCatalog' holds an

"""


class SearchCatalog:
    """
    EventCatalog
    """

    def __init__(self):
        """Create a new 'SearchCatalog'."""
        self.start_date = None
        self.end_date = None
        self.shape = "POLY"
        self.coords = ""
        self.sort_by = "day"
        self.published_min_year = ""
        self.published_max_year = ""
        self.published_author = ""
        self.publisher = ""
        self.earthquake_catalog = None

    def bibli_search(self, args=()):
        """

        :param args: A collection of user-specified search criteria.
        :return: A pandas object of earthquakes within search criteria.
        """
        from bibliography_search import (dict_bibli_search, fetch_url,
                                         format_url, parse_bibli_page)

        # Save args to self
        dict_bibli_search(self, args)
        # Format URL from search criteria
        url = format_url(self)
        body = fetch_url(url)
        parse_bibli_page(self, body)

        return self

    def hypo_search(self, args=()):
        """

        :param search_params: A collection of user-specified search criteria.
        :return: An 'EventCatalog' object.
        """
        print("here hypo")
        print(args)
        return self

    def __str__(self):
        """Return str(self)"""
        output = ""
        if self.start_date is not None:
            for attr in self.__dict__.items():
                if attr[1] is None or str(attr[1]) == "":
                    continue
                title = attr[0].replace("_", " ").title()
                output += f"{title} = {attr[1]}\n"

        if output == "":
            output = "No search parameters defined"
        return output
