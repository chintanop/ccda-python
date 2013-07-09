from cdautils.cda.entry_finder import EntryFinder
from cdautils.cda.section_importer import SectionImporter
from cdautils.cda.narrative_reference_handler import NarrativeReferenceHandler

from cdautils.models import Medication

class MedicationImporter(SectionImporter):
    """ Imports the medication section """

    entry_templates_xpaths = [
        "//cda:section[cda:templateId/@root='2.16.840.1.113883.3.88.11.83.112']/cda:entry/cda:substanceAdministration",
        "//cda:section[cda:templateId/@root='2.16.840.1.113883.10.20.1.8']/cda:entry/cda:substanceAdministration",
    ]

    def __init__(self, entry_finder=EntryFinder(entry_templates_xpaths)):
        super(MedicationImporter, self).__init__(entry_finder)
        self.code_xpath         = "./cda:consumable/cda:manufacturedProduct/cda:manufacturedMaterial/cda:code"
        self.description_xpath  = "./cda:consumable/cda:manufacturedProduct/cda:manufacturedMaterial/cda:code/cda:originalText/cda:reference[@value]"
        self.med_description_xpath  = "./cda:consumable/cda:manufacturedProduct/cda:manufacturedMaterial/cda:code/cda:originalText"
        self.type_of_med_xpath  = "./cda:entryRelationship[@typeCode='SUBJ']/cda:observation[cda:templateId/@root='2.16.840.1.113883.3.88.11.83.8.1']/cda:code"
        self.indication_xpath   = "./cda:entryRelationship[@typeCode='RSON']/cda:observation[cda:templateId/@root='2.16.840.1.113883.10.20.1.28']/cda:code"
        self.vehicle_xpath      = "cda:participant/cda:participantRole[cda:code/@code='412307009' and cda:code/@codeSystem='2.16.840.1.113883.6.96']/cda:playingEntity/cda:code"
        self.fill_number_xpath  = "./cda:entryRelationship[@typeCode='COMP']/cda:sequenceNumber/@value"
        self.entry_class        = Medication
   

    def create_entry(self, entry_element, nrh=NarrativeReferenceHandler()):
        medication = super(MedicationImporter, self).create_entry(entry_element, nrh)

        if medication.description:
            medication.free_text = medication.description
       
        print medication.free_text

        if not medication.free_text:
           mdesc = entry_element.xpath(self.med_description_xpath) 
           print "here!"
           if mdesc:
            medication.description = mdesc[0].text
            medication.free_text    = mdesc[0].text

        self.extract_administration_timing(entry_element, medication)
        
        print medication.free_text
        medication.route = self.extract_code(entry_element, "./cda:routeCode")
        print medication.route
        medication.dose = self.extract_scalar(entry_element, "./cda:doseQuantity")
        print medication.dose
        medication.site = self.extract_code(entry_element, "./cda:approachSiteCode", 'SNOMED-CT')
        print medication.site
   
        medication.product_form = self.extract_code(entry_element, "./cda:administrationUnitCode", 'NCI Thesaurus')
        medication.delivery_method = self.extract_code(entry_element, "./cda:code", 'SNOMED-CT')
        print medication.delivery_method

        if self.type_of_med_xpath:
            medication.type_of_medication = self.extract_code(entry_element, self.type_of_med_xpath, 'SNOMED-CT') 

        if self.indication_xpath:
            medication.indication = self.extract_code(entry_element, self.indication_xpath, 'SNOMED-CT')

        if self.vehicle_xpath:
            medication.vehicle = self.extract_code(entry_element, self.vehicle_xpath, 'SNOMED-CT')

    def extract_administration_timing(self, parent_element, medication):
        administration_timing_element = parent_element.xpath("./cda:effectiveTime[2]")
        if administration_timing_element:
            administration_timing_element = administration_timing_element[0]
            at = {}
            #if administration_timing_element.get('institutionSpecified'):
            #    at['institutionSpecified'] = administration_timing_elementadministration_timing_elementinstitutionSpecified

            at['period'] = self.extract_scalar(administration_timing_element, "./cda:period")
            
            medication.administrationTiming = at
            print at 
