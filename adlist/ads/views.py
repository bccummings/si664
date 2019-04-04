from ads.models import Ad
from django.views import View
from django.views import generic
from django.shortcuts import render

from ads.util import AdListView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView

class AdListView(AdListView):
    model = Ad
    template_name = "ad_list.html"

class AdDetailView(AdDetailView):
    model = Ad
    template_name = "ad_detail.html"

class AdCreateView(AdCreateView):
    model = Ad
    fields = ['title', 'text']
    template_name = "ad_form.html"

class AdUpdateView(AdUpdateView):
    model = Ad
    fields = ['title', 'text']
    template_name = "ad_form.html"

class AdDeleteView(AdDeleteView):
    model = Ad
    template_name = "ad_delete.html"
