from django.shortcuts import render

def custom_404_view(request, exception):
    if request.path.startswith('/auth/') or request.path.startswith('/admin/'):
        return render(request, 'backend/404.html', status=404)
    return render(request, 'frontend/404.html', status=404)
