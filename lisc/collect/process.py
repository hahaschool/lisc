"""Functions to process tags from collected data."""

from lisc.core.decorators import catch_none

###################################################################################################
###################################################################################################

def get_info(tag, label, how):
    """Get information from a tag.

    Parameters
    ----------
    tag : bs4.element.Tag
        The data object to find the information from.
    label : str
        The name of the tag to get information from.
    how : {'raw', 'all' , 'txt', 'str'}
        Method to use to get the information.
            raw      - get an embedded tag
            str      - get text and convert to string
            all      - get all embedded tags
            all-str  - get all embedded tags, and convert to string
            all-list - get all embedded tags, and collect into a list

    Returns
    -------
    {bs4.element.Tag, bs4.element.ResultSet, unicode, str, None}
        Requested data from the tag. Returns None is requested tag is unavailable.
    """

    if how not in ['raw', 'str', 'all', 'all-str', 'all-list']:
        raise ValueError('Value for how is not understood.')

    # Use try to be robust to missing tag
    try:
        if how == 'raw':
            return tag.find(label)
        elif how == 'str':
            return tag.find(label).text
        elif how == 'all':
            return tag.find_all(label)
        elif how == 'all-str':
            return ' '.join([part.text for part in tag.find_all(label)])
        elif how == 'all-list':
            return [part.text for part in tag.find_all(label)]

    except AttributeError:
        return None


def ids_to_str(ids):
    """Convert a list of article IDs to a comma separated string of IDs.

    Parameters
    ----------
    ids : bs4.element.ResultSet
        List of article IDs.

    Returns
    -------
    ids_str : str
        A string of all concatenated IDs.
    """

    # Check how many IDs in list & initialize string with first ID
    n_ids = len(ids)
    ids_str = str(ids[0].text)

    # Loop through rest of the ID's, appending to end of id_str
    for ind in range(1, n_ids):
        ids_str = ids_str + ',' + str(ids[ind].text)

    return ids_str


@catch_none(1)
def process_authors(authors):
    """Get information for and process authors.

    Parameters
    ----------
    authors : bs4.element.Tag
        AuthorList tag, which contains tags related to author data.

    Returns
    -------
    out : list of tuple of (str, str, str, str)
        List of authors, each as (LastName, FirstName, Initials, Affiliation).
    """

    # Pull out all author tags from the input
    authors = get_info(authors, 'Author', 'all')

    # Get data for each author
    out = []
    for author in authors:
        out.append((get_info(author, 'LastName', 'str'), get_info(author, 'ForeName', 'str'),
                    get_info(author, 'Initials', 'str'), get_info(author, 'Affiliation', 'str')))

    return out


@catch_none(1)
def process_pub_date(pub_date):
    """Get information for and process publication dates.

    Parameters
    ----------
    pub_date : bs4.element.Tag
        PubDate tag, which contains tags with publication date information.

    Returns
    -------
    year : int or None
        Year the article was published.
    """

    # Get the year, convert to int if not None
    year = get_info(pub_date, 'Year', 'str')
    year = int(year) if year else year

    return year


@catch_none(1)
def process_ids(ids, id_type):
    """Get information for and process IDs.

    Parameters
    ----------
    ids : bs4.element.ResultSet
        All the ArticleId tags, with all IDs for the article.
    id_type : {'pubmed', 'doi'}
        Which type of ID to get & process.

    Returns
    -------
    out : str or list or None
        A str or list of available IDs, if any are available, otherwise None.
    """

    lst = [str(cur_id.contents[0]) for cur_id in ids if cur_id.attrs == {'IdType' : id_type}]

    if not lst:
        out = None
    elif len(lst) == 1:
        out = lst[0]
    else:
        out = lst

    return out
