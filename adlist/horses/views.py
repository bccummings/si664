# from django.views import View
from django.views import generic
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile

from horses.models import Horse, Comment
from horses.forms import CommentForm
from horses.forms import CreateForm
from horses.util import HorseListView, HorseDetailView, HorseCreateView, HorseUpdateView, HorseDeleteView

class HorseListView(HorseListView):
    model = Horse
    template_name = "horses/horse_list.html"

class HorseDetailView(HorseDetailView):
    model = Horse
    template_name = "horses/horse_detail.html"
    def get(self, request, pk) :
        horse = Horse.objects.get(id=pk)
        comments = Comment.objects.filter(horse=horse).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'horse' : horse, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

# class HorseCreateView(HorseCreateView):
#     model = Horse
#     fields = ['title', 'text', 'price']
#     template_name = "horse_form.html"

class HorseCreateView(LoginRequiredMixin, View):
    template = 'horses/horse_form.html'
    success_url = reverse_lazy('horses')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Horsed owner to the model before saving
        horse = form.save(commit=False)
        horse.owner = self.request.user
        horse.save()
        return redirect(self.success_url)

# class HorseUpdateView(HorseUpdateView):
#     model = Horse
#     fields = ['title', 'text']
#     template_name = "horse_form.html"

class HorseUpdateView(LoginRequiredMixin, View):
    template = 'horses/horse_form.html'
    success_url = reverse_lazy('horses')
    def get(self, request, pk) :
        horse = get_object_or_404(Horse, id=pk, owner=self.request.user)
        form = CreateForm(instance=horse)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        horse = get_object_or_404(Horse, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=horse)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        horse = form.save(commit=False)
        horse.save()

        return redirect(self.success_url)

class HorseDeleteView(HorseDeleteView):
    model = Horse
    template_name = "horses/horse_delete.html"

def stream_file(request, pk) :
    horse = get_object_or_404(Horse, id=pk)
    response = HttpResponse()
    response['Content-Type'] = horse.content_type
    response['Content-Length'] = len(horse.picture)
    response.write(horse.picture)
    return response

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Horse, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, horse=f)
        comment.save()
        return redirect(reverse_lazy('horse_detail', args=[pk]))

class CommentDeleteView(HorseDeleteView):
    model = Comment
    template_name = "horses/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        horse = self.object.horse
        return reverse_lazy('horse_detail', args=[horse.id])
