from django.db import models
from django.contrib.auth.models import User


""" User """
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=255, 
                                   blank=True, default='')

    def __unicode__(self):
        if (self.affiliation == ""):
            return self.user.__unicode__()
        else:
            return " - ".join([self.user.__unicode__(), self.affiliation])
    
    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        get_latest_by = 'user__date_joined'
        app_label='wc'


""" Parameter """ 
class Parameter(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __unicode__(self):
        return self.name


    class Meta:
        app_label='wc'


class ParameterValue(models.Model):
    parameter = models.ForeignKey('Parameter')
    value = models.FloatField()

    def __unicode__(self):
        return " = ".join([self.parameter.__unicode__(), str(self.value)])


    class Meta:
        app_label='wc'


""" Option """
class Option(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


    class Meta:
        app_label='wc'


class OptionValue(models.Model):
    option = models.ForeignKey('Option')
    value = models.TextField()

    def __unicode__(self):
        return " = ".join([self.option.__unicode__(), self.value])


    class Meta:
        app_label='wc'


""" Process """
class Process(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Processes'
        app_label='wc'

    def __unicode__(self):
        return self.name


""" StateProperty """
class StateProperty(models.Model):
    state_name = models.CharField(max_length=255)
    property_name = models.CharField(max_length=255)

    def __unicode__(self):
        return " - ".join([self.state_name, self.property_name])
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        app_label='wc'


""" Models """
class WCModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    organism = models.CharField(max_length=255, default=name)

    parameters  = models.ManyToManyField('Parameter')
    options     = models.ManyToManyField('Option')
    processes   = models.ManyToManyField('Process')
    state_properties = models.ManyToManyField('StateProperty')

    def __unicode__(self):
        return ", ".join([self.name, self.organism])

    ''' Return a QuerySet of StateProperties from the specified state '''
    def state(self, state):
        return self.state_properties.filter(state_name=state)


    class Meta:
        verbose_name = 'Model'
        verbose_name_plural = 'Models'
        app_label='wc'



class SimulationManager(models.Manager):
    def create_simulation(self, name, wcmodel, user, batch="", description="",
            replicate_index=0, ip='0.0.0.0', length=0.0):
        simulation = self.create(name=name, batch=batch, wcmodel=wcmodel, 
                                user=user, length=length, ip=ip,
                                description=description,
                                replicate_index=replicate_index)
        for state_property in wcmodel.state_properties.all():
            StatePropertyValue.objects.create(
                    state_property=state_property,
                    simulation=simulation)


""" Simulation """
class Simulation(models.Model):
    name            = models.CharField(max_length=255)
    batch           = models.CharField(max_length=255)
    description     = models.TextField()
    replicate_index = models.PositiveIntegerField()

    ip     = models.IPAddressField()
    length = models.FloatField()
    date = models.DateTimeField(auto_now=True, auto_now_add=True)
    user = models.ForeignKey('UserProfile', editable=False)

    wcmodel = models.ForeignKey('WCModel')

    parameter_values = models.ManyToManyField('ParameterValue')
    option_values    = models.ManyToManyField('OptionValue')

    objects = SimulationManager()

    class Meta:
        get_latest_by = 'date'
        app_label='wc'

    
    def __unicode__(self):
        return self.name


""" StatePropertyValue """
class StatePropertyValue(models.Model):
    state = models.ForeignKey(StateProperty)
    simulation      = models.ForeignKey('Simulation')
    

    def __unicode__(self):
        return 

    def get_path(self):
        return "/".join(['/states', 
                        this.stateproperty__state_name,
                        this.stateproperty__property_name])

    def file_name(self):
        return ".".join([self.simulation__name, "h5"])


    """
    This method runs the h5py code necessary to fetch the dataset
    as a numpy array
    """
    def dataset(self):
        f = h5py.File(self.file_name(), 'r')
        return f[self.get_path()]


    class Meta:
        app_label='wc'


