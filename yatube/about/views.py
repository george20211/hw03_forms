from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):

    template_name = 'about/author.html'

    def xzchto(self, request):

        return render(request, "author.html")


class AboutTechView(TemplateView):

    template_name = 'about/tech.html'

    def xzchto2(self, request):

        return render(request, "tech.html")
