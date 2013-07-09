from cdautils.cda.namespaces import NSMAP

class EntryFinder(object):

    def __init__(self, entry_xpaths):
        self.entry_xpaths = entry_xpaths

    def entries(self, doc):

        for entry_xpath in self.entry_xpaths:
            elements = doc.xpath(entry_xpath, namespaces = NSMAP)
            if elements:
                return elements

