from django.http import HttpResponse
from django.template import RequestContext, Context, loader
from django.shortcuts import render, render_to_response

from hesapla.models import Service

# Create your views here.
def Postyontemi(request):
  if(request.method=='POST'):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    serviceName = request.POST['service']
    typeOfProduct = request.POST['type-product']
    values = (int(request.POST['from-value']), int(request.POST['to-value']))

    # Format phone number 
    phone = format(int(phone[:-1]), ",").replace(",", "-") + phone[-1] 

    # Veri işlenmek için servise gönderilir.
    service = Service.foundService(serviceName, typeOfProduct, values)

    # Gelen veri işlendikten sonra geri döndürülür.
    subtemplate = loader.get_template('table.html')
    context = {
        'name': name,
        'email': email,
        'phone': phone,
        'type': typeOfProduct,
        'serviceName': serviceName,
        'docs': service.dokumCetveli,
    }
    return HttpResponse(subtemplate.render(context, request))

  template = loader.get_template('index.html')
  return HttpResponse(template.render(locals(), request))