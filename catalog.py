"""
A 'SearchCatalog' holds search params and catalog results

"""


class SearchCatalog:
    """
    EventCatalog
    """

    def __init__(self):
        """Create a new 'SearchCatalog'."""
        self.start_date = None
        self.end_date = None
        self.earthquake_catalog = None

    def bibli_search(self, args=()):
        """
        :param args: A collection of user-specified search criteria.
        :return: A pandas object of earthquakes within search criteria.
        """
        from bibliography_search import fetch_url, format_url, parse_bibli_page

        # Format URL from search criteria
        url = format_url(self, args)
        body = fetch_url(url)
        parse_bibli_page(self, body)

        return self

    def hypo_search(self, args=()):
        """
        :param search_params: A collection of user-specified search criteria.
        :return: An 'SearchCatalog' object.
        """
        from hypocenter_search import fetch_url, format_url, parse_quakeML

        url = format_url(self, args)
        xml = fetch_url(url)
        parse_quakeML(self, xml)

        return self

    def gcmt_search(self, args=()):
        """
        :param search_params: A collection of user-specified search criteria.
        :return: An 'SearchCatalog' object.
        """
        print("here gcmt")
        print(args)
        return self

    def get_params(self):
        """Return list of Search Criteria keys and vaules"""
        search_params = {}
        if self.start_date is not None:
            for attr in self.__dict__.items():
                if attr[1] is None:
                    continue
                if str(attr[1]) == "":
                    continue
                if attr[0] == "earthquake_catalog":
                    continue
                search_params[attr[0]] = str(attr[1])
        else:
            raise Exception("Empty search parameters")
        return search_params

    def __str__(self):
        """Return str(self)"""
        output = ""
        if self.start_date is not None:
            for attr in self.__dict__.items():
                if attr[1] is None or str(attr[1]) == "":
                    continue
                if attr[0] == "earthquake_catalog":
                    continue
                title = attr[0].replace("_", " ").title()
                output += f"{title} = {attr[1]}\n"
        else:
            raise Exception("Empty Search parameters")
        output += "\n\nSearch Results:"
        output += f"\n{self.earthquake_catalog.head()}"

        return output
