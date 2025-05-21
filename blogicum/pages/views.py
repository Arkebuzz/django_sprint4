from django.shortcuts import render


def about(request):
    template_name = 'pages/about.html'
    return render(request, template_name)


def rules(request):
    template_name = 'pages/rules.html'
    return render(request, template_name)


def page404(request, _):
    return render(request, 'pages/404.html', status=404)


def page403(request, _):
    return render(request, 'pages/403csrf.html', status=403)


def page500(request):
    return render(request, 'pages/500.html', status=500)
