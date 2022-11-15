from django.shortcuts import render

# Create your views here.


def softwaresCatalogue(request):
    return render(request, 'softwares/catalogue.html')
