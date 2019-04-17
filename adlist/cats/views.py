# from django.views import View
from django.views import generic
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile

from cats.models import Cat, Comment
from cats.forms import CommentForm
from cats.forms import CreateForm
from cats.util import CatListView, CatDetailView, CatCreateView, CatUpdateView, CatDeleteView

class CatListView(CatListView):
    model = Cat
    template_name = "cats/cat_list.html"

class CatDetailView(CatDetailView):
    model = Cat
    template_name = "cats/cat_detail.html"
    def get(self, request, pk) :
        cat = Cat.objects.get(id=pk)
        comments = Comment.objects.filter(cat=cat).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'cat' : cat, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

# class CatCreateView(CatCreateView):
#     model = Cat
#     fields = ['title', 'text', 'price']
#     template_name = "cat_form.html"

class CatCreateView(LoginRequiredMixin, View):
    template = 'cats/cat_form.html'
    success_url = reverse_lazy('cats')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Catd owner to the model before saving
        cat = form.save(commit=False)
        cat.owner = self.request.user
        cat.save()
        return redirect(self.success_url)

# class CatUpdateView(CatUpdateView):
#     model = Cat
#     fields = ['title', 'text']
#     template_name = "cat_form.html"

class CatUpdateView(LoginRequiredMixin, View):
    template = 'cats/cat_form.html'
    success_url = reverse_lazy('cats')
    def get(self, request, pk) :
        cat = get_object_or_404(Cat, id=pk, owner=self.request.user)
        form = CreateForm(instance=cat)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        cat = get_object_or_404(Cat, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=cat)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        cat = form.save(commit=False)
        cat.save()

        return redirect(self.success_url)

class CatDeleteView(CatDeleteView):
    model = Cat
    template_name = "cats/cat_delete.html"

def stream_file(request, pk) :
    cat = get_object_or_404(Cat, id=pk)
    response = HttpResponse()
    response['Content-Type'] = cat.content_type
    response['Content-Length'] = len(cat.picture)
    response.write(cat.picture)
    return response

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Cat, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, cat=f)
        comment.save()
        return redirect(reverse_lazy('cat_detail', args=[pk]))

class CommentDeleteView(CatDeleteView):
    model = Comment
    template_name = "cats/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        cat = self.object.cat
        return reverse_lazy('cat_detail', args=[cat.id])
