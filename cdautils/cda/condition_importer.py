from cdautils.cda.entry_finder import EntryFinder
from cdautils.cda.section_importer import SectionImporter
from cdautils.cda.narrative_reference_handler import NarrativeReferenceHandler

from cdautils.models import Condition

class ConditionImporter(SectionImporter): 
    entry_templates_xpaths = [
        "//cda:section[cda:templateId/@root='2.16.840.1.113883.3.88.11.83.103']/cda:entry/cda:act/cda:entryRelationship/cda:observation",
    ]

    def __init__(self, entry_finder=EntryFinder(entry_templates_xpaths)):
        super(ConditionImporter, self).__init__(entry_finder)
        self.code_xpath         = "./cda:value"
        self.status_xpath       = "./cda:entryRelationship/cda:observation[cda:templateId/@root='2.16.840.1.113883.10.20.1.50']/cda:value"
        self.ordinality_xpath   = "./cda:priorityCode"
        self.description_xpath  = "./cda:text/cda:reference"
        self.free_text_xpath    = "./cda:value"
        self.provider_xpath     = "./cda:act[cda:templateId/@root='2.16.840.1.113883.10.20.1.27']/cda:performer"
        self.priority_xpath     = "../cda:sequenceNumber"
        self.entry_class        = Condition
 
    def create_entry(self, entry_element, nrh = NarrativeReferenceHandler()):
        condition = super(ConditionImporter, self).create_entry(entry_element, nrh)

        print condition.description
        if not condition.description:
            ftext = entry_element.xpath(self.free_text_xpath)
            if ftext:
                print ftext[0]
                condition.free_text = ftext[0].get('displayName')
        print condition.free_text
        print condition.status_code
        #self.extract_ordinality(entry_element, condition)
        self.extract_negation(entry_element, condition)
        #self.extract_priority(entry_element, condition)

