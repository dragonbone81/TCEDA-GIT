from django.shortcuts import render
from dataToExcel import *


def index(request):
    """
    homepage for tceda
    :param request:
    :return:
    """
    if request.POST:
        if request.POST.get('name') == 'getPopulation':
            return population_toExcel()
        if request.POST.get('name') == 'gethouseholdIncome':
            return householdIncome_toExcel()
        if request.POST.get('name') == 'getRaceInfo':
            return race_toExcel()
        if request.POST.get('name') == 'getLang':
            return language_dist_toExcel()
        if request.POST.get('name') == 'getIncomeDist':
            return income_dist_toExcel()
    return render(request, 'TCEDA_WEB/index.html', {})
