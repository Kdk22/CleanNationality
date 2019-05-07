from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView


def home(request):
    return render(request, 'NationalityCleaner/home.html')

class IndexView(ListView):
    template_name = 'NationalityCleaner/index.html'
    allow_empty = True

    def get_allow_empty(self):

        """
        Return ``True`` if the view should display empty lists and ``False``
        if a 404 should be raised instead.
        """
        return self.allow_empty
