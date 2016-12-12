import logging
from packages.models import Packages
from django.core import serializers
from django.http import HttpResponse

def GetPackages():
    return Packages.objects.filter(gui=1)

def packagesJson(request):
    """
    Retrieve all packages defined in the databases in a JSON object
    """
    data_packages = serializers.serialize('json', GetPackages())
    return HttpResponse(data_packages, mimetype='application/json; charset=utf8')

def packagesXml(request):
    """
    Retrieve all packages defined in the database as a XML object
    """
    data_packages = serializers.serialize('xml', GetPackages())
    return HttpResponse(data_packages, mimetype='application/xml; charset=utf8')
