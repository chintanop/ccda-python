from cdautils.cda.entry_finder import EntryFinder
from cdautils.cda.section_importer import SectionImporter
from cdautils.cda.narrative_reference_handler import NarrativeReferenceHandler

class ResultImporter(SectionImporter):

    entry_templates_xpaths = [
        "//cda:observation[cda:templateId/@root='2.16.840.1.113883.3.88.11.83.15.1'] | //cda:observation[cda:templateId/@root='2.16.840.1.113883.3.88.11.83.15']",
    ]

    def __init__(self, entry_finder=EntryFinder(entry_templates_xpaths)):
        super(ResultImporter, self).__init__(entry_finder)
    
    
    def create_entry(self, entry_element, nrh = NarrativeReferenceHandler()):
        result = super(ResultImporter, self).create_entry(entry_element, nrh)
        self.extract_value(entry_element, result)
        self.extract_interpretation(entry_element, result)
        self.extract_negation(entry_element, result)
 
