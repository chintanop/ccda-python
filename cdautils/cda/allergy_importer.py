from cdautils.cda.entry_finder import EntryFinder
from cdautils.cda.section_importer import SectionImporter
from cdautils.cda.narrative_reference_handler import NarrativeReferenceHandler

from cdautils.models import Allergy

class AllergyImporter(SectionImporter): 
  
    entry_templates_xpaths = [
        "//cda:observation[cda:templateId/@root='2.16.840.1.113883.10.20.1.18']",
    ]

    def __init__(self, entry_finder=EntryFinder(entry_templates_xpaths)):
        super(AllergyImporter, self).__init__(entry_finder)
        self.entry_finder       = entry_finder
        self.code_xpath         = "./cda:participant/cda:participantRole/cda:playingEntity/cda:code"
        self.description_xpath  = "./cda:code/cda:originalText/cda:reference[@value] | ./cda:text/cda:reference[@value]"
        self.type_xpath     = "./cda:code"
        self.free_text_xpath= "./cda:participant/cda:participantRole/cda:playingEntity/cda:name"
        self.reaction_xpath = "./cda:entryRelationship[@typeCode='MFST']/cda:observation[cda:templateId/@root='2.16.840.1.113883.10.20.1.54']/cda:value"
        self.severity_xpath = "./cda:entryRelationship[@typeCode='SUBJ']/cda:observation[cda:templateId/@root='2.16.840.1.113883.10.20.1.55']/cda:value"
        self.status_xpath   = "./cda:entryRelationship[@typeCode='REFR']/cda:observation[cda:templateId/@root='2.16.840.1.113883.10.20.1.39']/cda:value"
        self.entry_class    = Allergy 


    def create_entry(self, entry_element, nrh = NarrativeReferenceHandler()):
        allergy = super(AllergyImporter, self).create_entry(entry_element, nrh)
        allergy.free_text = None
        
        ftext = entry_element.xpath(self.free_text_xpath)
        if ftext:
            allergy.free_text = ftext[0].text

        print allergy.free_text

        self.extract_negation(entry_element, allergy)
        allergy.type        = self.extract_code(entry_element, self.type_xpath)
        allergy.reaction    = self.extract_code(entry_element, self.reaction_xpath)
        allergy.severity    = self.extract_code(entry_element, self.severity_xpath)
        return  allergy
        
