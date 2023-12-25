from django.http import HttpResponse


def main_view(request):
    return HttpResponse('This is the main panel')
