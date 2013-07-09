CCDA Python Parser
==================

A stand-alone Python/Django module for parsing CCDA documents. This parser design is inspired by 
the [ccdaReceiver](https://github.com/chb/ccdaReceiver) project in Javascript

This code is still under heavy development and by no means complete. Currently, 
it supports parsing the Conditions, Medications and Allergies sections from the CDA and returns Python objects

* * *

Requirements
------------
- Python 2.7
- Django 1.4 or above
- lxml 

* * *

Install/Setup
-------------

1. Copy the cdautils module into your Django project
2. Add 'cdautils' in your INSTALLED_APPS in settings.py
3. Create the data tables, python manage.py syncdb
4. Call the parser as shown below


```
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


```


LICENSE
-------
Copyright (c) 2013 by Applied Informatics Inc. Licensed under the [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html) license.
