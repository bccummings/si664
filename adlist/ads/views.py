# from django.views import View
from django.views import generic
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile

from ads.models import Ad
from ads.util import AdListView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView
from ads.forms import CreateForm

class AdListView(AdListView):
    model = Ad
    template_name = "ad_list.html"

class AdDetailView(AdDetailView):
    model = Ad
    template_name = "ad_detail.html"

# class AdCreateView(AdCreateView):
#     model = Ad
#     fields = ['title', 'text', 'price']
#     template_name = "ad_form.html"

class AdCreateView(LoginRequiredMixin, View):
    template = 'ads/ad_form.html'
    success_url = reverse_lazy('ads')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(self.success_url)

# class AdUpdateView(AdUpdateView):
#     model = Ad
#     fields = ['title', 'text']
#     template_name = "ad_form.html"

class AdUpdateView(LoginRequiredMixin, View):
    template = 'ads/ad_form.html'
    success_url = reverse_lazy('ads')
    def get(self, request, pk) :
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        ad = form.save(commit=False)
        ad.save()

        return redirect(self.success_url)

class AdDeleteView(AdDeleteView):
    model = Ad
    template_name = "ad_delete.html"

def stream_file(request, pk) :
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response
