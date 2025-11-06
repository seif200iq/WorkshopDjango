from django.shortcuts import render
from .models import CONFERENCE
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import conferenceForm
from django.contrib.auth.mixins import LoginRequiredMixin

def list_conferences(request):
    conf_list = CONFERENCE.objects.all()
    return render(request, "conference/liste.html", {"liste": conf_list})

class conferenceList(ListView):
    model = CONFERENCE
    context_object_name = "liste"
    template_name = "conference/liste.html"

class conferencedetail(DetailView):
    model = CONFERENCE
    context_object_name = "conference"
    template_name = "conference/detail.html"

class conferenceCreate(LoginRequiredMixin,CreateView):
    model = CONFERENCE
    template_name = "conference/form.html"
    #fields = "__all__"
    form_class = conferenceForm
    success_url = reverse_lazy("list_conferences")

class conferenceUpdate(LoginRequiredMixin,UpdateView):
    model = CONFERENCE
    template_name = "conference/form.html"
    #fields = "__all__"
    form_class = conferenceForm
    success_url = reverse_lazy("list_conferences")

class conferenceDelete(LoginRequiredMixin,DeleteView):
    model = CONFERENCE
    template_name = "conference/conference_confirm_delete.html"
    success_url = reverse_lazy("list_conferences")

    
