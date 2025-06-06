from django.shortcuts import render


def page404(request, exception):
    return render(request, 'pages/404.html', status=404)


def page403(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def page500(request):
    return render(request, 'pages/500.html', status=500)
