class NarrativeReferenceHandler(object):
    """ Extract human readable narratives from different sections in the CCDA """

    def __init__(self):
        self.id_map = {}

    def build_id_map(self, doc):
        path    = "//*[@ID]"
        ids     = doc.xpath(path)

        for id in ids:
            tag = id.get('ID')
            value = id.text
            if value:
                self.id_map[tag.strip()] = value.strip()
                print "Adding "+tag+" = "+value.strip()


    def lookup_tag(self, tag):

        tag = tag.strip()
        value = None
        if tag in self.id_map:
            value = self.id_map[tag]

        if not value and tag[0] == '#':
            tag = tag[1:len(tag)]
            value = self.id_map[tag]

        return value
