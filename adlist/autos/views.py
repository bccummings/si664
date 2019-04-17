# from django.views import View
from django.views import generic
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile

from autos.models import Auto, Comment
from autos.forms import CommentForm
from autos.util import AutoListView, AutoDetailView, AutoCreateView, AutoUpdateView, AutoDeleteView
from autos.forms import CreateForm

class AutoListView(AutoListView):
    model = Auto
    template_name = "auto_list.html"

    def get(self, request) :
        auto_list = Auto.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}]  (A list of rows)
            rows = request.user.favorite_autos.values('id')
            favorites = [ row['id'] for row in rows ]
        ctx = {'auto_list' : auto_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)

class AutoDetailView(AutoDetailView):
    model = Auto
    template_name = "auto_detail.html"
    def get(self, request, pk) :
        auto = Auto.objects.get(id=pk)
        comments = Comment.objects.filter(auto=auto).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'auto' : auto, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

# class AutoCreateView(AutoCreateView):
#     model = Auto
#     fields = ['title', 'text', 'price']
#     template_name = "auto_form.html"

class AutoCreateView(LoginRequiredMixin, View):
    template = 'autos/auto_form.html'
    success_url = reverse_lazy('autos')
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
        auto = form.save(commit=False)
        auto.owner = self.request.user
        auto.save()
        return redirect(self.success_url)

# class AutoUpdateView(AutoUpdateView):
#     model = Auto
#     fields = ['title', 'text']
#     template_name = "auto_form.html"

class AutoUpdateView(LoginRequiredMixin, View):
    template = 'autos/auto_form.html'
    success_url = reverse_lazy('autos')
    def get(self, request, pk) :
        auto = get_object_or_404(Auto, id=pk, owner=self.request.user)
        form = CreateForm(instance=auto)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        auto = get_object_or_404(Auto, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=auto)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        auto = form.save(commit=False)
        auto.save()

        return redirect(self.success_url)

class AutoDeleteView(AutoDeleteView):
    model = Auto
    template_name = "auto_delete.html"

def stream_file(request, pk) :
    auto = get_object_or_404(Auto, id=pk)
    response = HttpResponse()
    response['Content-Type'] = auto.content_type
    response['Content-Length'] = len(auto.picture)
    response.write(auto.picture)
    return response

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Auto, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, auto=f)
        comment.save()
        return redirect(reverse_lazy('auto_detail', args=[pk]))

class CommentDeleteView(AutoDeleteView):
    model = Comment
    template_name = "comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        auto = self.object.auto
        return reverse_lazy('auto_detail', args=[auto.id])
