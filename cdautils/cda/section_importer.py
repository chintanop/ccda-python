from cdautils.models import Entry

from cdautils.cda.narrative_reference_handler import NarrativeReferenceHandler
from cdautils.cda.utils import timestamp_to_integer

class SectionImporter(object):
    """ Parent Section Importer. Provides several utility functions for various data elements in the CCDA
    """

    def __init__(self, entry_finder):
       
        self.entry_finder   = entry_finder
        self.code_xpath     = './cda:code'
        self.status_xpath   = './cda:statusCode' 
        self.priority_xpath = None
        self.description_xpath = "./cda:code/cda:originalText/cda:reference[@value] | ./cda:text/cda:reference[@value]"
        self.check_for_usable = True
        self.entry_class = Entry

   
    def create_enteries(self, doc, nrh = NarrativeReferenceHandler()):
        entry_list      = []
        entry_elements  = self.entry_finder.entries(doc)

        if entry_elements:
            for entry_element in entry_elements:
                entry = self.create_entry(entry_element, nrh)


    def create_entry(self, entry_element, nrh = NarrativeReferenceHandler()):
        entry = self.entry_class()
        entry.save()
        self.extract_codes(entry_element, entry)
        self.extract_dates(entry_element, entry)
        self.extract_value(entry_element, entry)
        ctext  = entry_element.xpath("./cda:text")
        if ctext:
            entry.free_text = ctext[0].text
        if self.status_xpath:
            self.extract_status(entry_element, entry)
        if self.description_xpath:
            self.extract_description(entry_element, entry, nrh)

        return entry

    def extract_status(self, parent_element, entry):
        """ Extract status codes """

        status_element = parent_element.xpath(self.status_xpath)
        if status_element:
            status_element = status_element[0]
            entry.status_code = status_element.get('code')
            print entry.status_code

    def extract_description(self, parent_element, entry, nrh):
        """ Extract description """
        code_elements = parent_element.xpath(self.description_xpath)

        for code_element in code_elements:
            tag = code_element.get('value')
            print "Description:"+tag
            entry.description = nrh.lookup_tag(tag)
            print entry.description

    def extract_codes(self, parent_element, entry):

        code_elements = parent_element.xpath(self.code_xpath)

        for code_element in code_elements:
            self.add_code_if_present(code_element, entry)
            translations = code_element.xpath('cda:translation')
            for translation in translations:
                self.add_code_if_present(translation, entry)

    def extract_code(self, parent_element, code_xpath, code_system=None):
        """ Get the code and code system """

        code_element = parent_element.xpath(code_xpath)
        if code_element:
            code_element = code_element[0]
            code_hash    = {'code':code_element.get('code')}
            if code_system:
                code_hash['codeSystem'] = code_system
            else:
                code_hash['codeSystemOid'] = code_element.get('codeSystem')
                code_hash['codeSystem'] = code_element.get('codeSystemName') #TODO: RETURN GET SYSTEM

            return code_hash


    def add_code_if_present(self, code_element, entry):
        if code_element.get('codeSystem') and code_element.get('code'): 
           entry.add_code(code_element.get('codeSystem'), code_element.get('code')) 

    def extract_dates(self, parent_element, entry, element_name="effectiveTime"):
        if parent_element.xpath("cda:"+element_name+"/@value"):
            entry.time      = timestamp_to_integer(parent_element.xpath("cda:"+element_name+"/@value")[0].get('value'))
        if parent_element.xpath("cda:"+element_name+"/cda:low"):
            entry.start_time = timestamp_to_integer(parent_element.xpath("cda:"+element_name+"/cda:low")[0].get('value'))
        if parent_element.xpath("cda:"+element_name+"/cda:high"):
            entry.end_time = timestamp_to_integer(parent_element.xpath("cda:"+element_name+"/cda:high")[0].get('value'))
        if parent_element.xpath("cda:"+element_name+"/cda:center"):
            entry.time = timestamp_to_integer(parent_element.xpath("cda:"+element_name+"/cda:center")[0].get('value'))

    def extract_value(self, parent_element, entry):
        
        value_element = parent_element.xpath("cda:value")
        if value_element:
            if isinstance(value_element,list):
                value_element = value_element[0]
            value = value_element.get('value')
            unit = value_element.get('unit')
            print value, unit
            if value:
                entry.set_value(value.strip(), unit)


    #TODO: implement negation extraction
    def extract_negation(self, parent_element, entry):
        pass

    def extract_scalar(self, parent_element, scalar_xpath): 
        scalar_element = parent_element.xpath(scalar_xpath)
        if scalar_element:  
            scalar_element = scalar_element[0]
            return {'unit':scalar_element.get('unit'),
                    'value':scalar_element.get('value')}
        else:
            return None


