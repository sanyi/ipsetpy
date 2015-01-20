__author__ = 'sanyi'


class IpsetError(Exception):
    pass


class IpsetNotFound(Exception):
    pass


class IpsetNoRights(Exception):
    pass


class IpsetInvalidResponse(Exception):
    pass


class IpsetCommandHangs(Exception):
    pass


class IpsetSetNotFound(Exception):
    pass


class IpsetEntryNotFound(Exception):
    pass
