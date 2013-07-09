#
# Import Django Settings
# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# 

from lxml import etree as ET
from cdautils.cda.medication_importer import ConditionImporter
from cdautils.cda.medication_importer import ResultImporter
from cdautils.cda.medication_importer import MedicationImporter
from cdautils.cda.narrative_reference_handler import NarrativeReferenceHandler

if __name__ == "__main__":
    
    tree = ET.parse("ccd.xml")

    doc = tree.getroot()

    ns = ET.FunctionNamespace('urn:hl7-org:v3')
    ns.prefix = 'cda'


    section_importers = {
        'medications':MedicationImporter(),
        'results':ResultImporter(),
        'condition':ConditionImporter()
    }

    nrh = NarrativeReferenceHandler()
    nrh.build_id_map (doc)

    for sec, importer in section_importers.items():
        importer.create_enteries(doc, nrh)


    
    


