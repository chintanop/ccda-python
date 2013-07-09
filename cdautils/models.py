from django.db import models

class Record(models.Model):
    title   = models.CharField(max_length=255, null=True)
    first   = models.CharField(max_length=255, null=True)
    last   = models.CharField(max_length=255, null=True)
    gender   = models.CharField(max_length=255, null=True)
    birthdate   = models.IntegerField(null=True)
    deathdate   = models.IntegerField(null=True)
    race        = models.CharField(max_length=255, null=True) #hash
    martial_status = models.CharField(max_length=255, null=True) #hhas
    medical_record_number = models.CharField(max_length=255, null=True)
    expired     = models.NullBooleanField()

class CodedValue(models.Model):
    code        = models.CharField(max_length=255, null=True) #hhas
    code_system  = models.CharField(max_length=255, null=True) #hhas

class PhysicalQuantityResultValue(models.Model):
    scalar  = models.CharField(max_length=255, null=True) #hhas
    units   = models.CharField(max_length=255, null=True) #hhas

class Entry(models.Model):
    record          = models.ForeignKey(Record, null=True)
    description     = models.TextField()
    specifics       = models.TextField()
    time            = models.IntegerField(null=True)
    values          = models.ManyToManyField(PhysicalQuantityResultValue)
    codes           = models.ManyToManyField(CodedValue)
    start_time      = models.IntegerField(null=True)
    end_time        = models.IntegerField(null=True)
    status_code     = models.CharField(max_length=255, null=True) #Hash
    free_text       = models.TextField()
    mood_code       = models.CharField(max_length=255, null=True)
    negationInd     = models.NullBooleanField()
    negationReason  = models.CharField(max_length=255, null=True) #Hash
    oid             = models.CharField(max_length=255, null=True)
    reason          = models.CharField(max_length=255, null=True) #Hash

    def set_value(self, scalar, units=None):
        pq_value = PhysicalQuantityResultValue(scalar=scalar, units=units)
        pq_value.save()
        self.values.add(pq_value)

    def add_code(self, code, code_system):
        cv = CodedValue(code=code, code_system=code_system)
        cv.save()
        self.codes.add(cv)

class Condition(Entry):
    type            = models.CharField(max_length=255, null=True) #Hash
    causeOfDeath    = models.NullBooleanField()
    time_of_death   = models.IntegerField(null=True)
    priority        = models.IntegerField(null=True)
    name            = models.CharField(max_length=255, null=True) #Hash
    ordinality      = models.CharField(max_length=255, null=True) #Hash
    severity        = models.CharField(max_length=255, null=True) #Hash

class Allergy(Entry):
    type      = models.CharField(max_length=255, null=True) #Hash
    severity  = models.CharField(max_length=255, null=True) #Hash
    reaction  = models.CharField(max_length=255, null=True) #Hash

class Medication(Entry):
    administrationTiming  = models.CharField(max_length=255, null=True) #Hash
    freeTextSig           = models.CharField(max_length=255, null=True) #Hash
    dose                  = models.CharField(max_length=255, null=True) #Hash
    typeOfMedication      = models.CharField(max_length=255, null=True) #Hash
    statusOfMedication    = models.CharField(max_length=255, null=True) #Hash
    route                 = models.CharField(max_length=255, null=True) #Hash
    site                  = models.CharField(max_length=255, null=True) #Hash
    doseRestriction          = models.CharField(max_length=255, null=True) #Hash
    fulfillmentInstructions = models.CharField(max_length=255, null=True) #Hash
    indication  = models.CharField(max_length=255, null=True) #Hash
    productForm = models.CharField(max_length=255, null=True) #Hash
    vehicle         = models.CharField(max_length=255, null=True) #Hash
    reaction        = models.CharField(max_length=255, null=True) #Hash
    deliveryMethod  = models.CharField(max_length=255, null=True) #Hash
    patientInstructions = models.CharField(max_length=255, null=True) #Hash
    doseIndicator       = models.CharField(max_length=255, null=True) #Hash

class LabResult(Entry):
    referenceRange      = models.CharField(max_length=255, null=True) #Hash
    interpretation      = models.CharField(max_length=255, null=True) #Hash


class Address(models.Model):
     street = models.CharField(max_length=255, null=True)
     city   = models.CharField(max_length=255, null=True)
     state  = models.CharField(max_length=255, null=True)
     zip    = models.CharField(max_length=255, null=True)
     country = models.CharField(max_length=255, null=True)
     use    = models.CharField(max_length=255, null=True)

class Telecom(models.Model):
     use        = models.CharField(max_length=255, null=True)
     value      = models.CharField(max_length=255, null=True)
     preffered  = models.NullBooleanField()
    
class Organization(models.Model):
    name        = models.CharField(max_length=255, null=True)
    address     = models.ManyToManyField(Address)
    telecoms    = models.ManyToManyField(Telecom)

class Provider(models.Model):
    npi = models.CharField(max_length=255, null=True) #Hash
    tin = models.CharField(max_length=255, null=True) #Hash
    specialty = models.CharField(max_length=255, null=True) #Hash
    phone = models.CharField(max_length=255, null=True) #Hash
    organization = models.ForeignKey(Organization, null=True)
    

