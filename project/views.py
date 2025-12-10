from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import RoundAssignmentFormSet
from django.db.models import Sum

from .models import Team, Meet, RoundAssignment


class TeamListView(ListView):
    """List all teams."""

    model = Team
    template_name = "project/team_list.html"
    context_object_name = "teams"


class MeetListView(ListView):
    """List all meets for a given team (or all meets if no team provided)."""

    model = Meet
    template_name = "project/meet_list.html"
    context_object_name = "meets"

    def get_queryset(self):
        qs = super().get_queryset().select_related("team").order_by("-date")
        team_id = self.kwargs.get("team_id")
        if team_id is not None:
            qs = qs.filter(team_id=team_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_id = self.kwargs.get("team_id")
        if team_id is not None:
            context["team"] = get_object_or_404(Team, pk=team_id)
        return context


class MeetDetailView(DetailView):
    """Show a single meet along with lineup summary."""

    model = Meet
    template_name = "project/meet_detail.html"
    context_object_name = "meet"


class EditLineupView(View):
    """View to edit lineup (RoundAssignments) for a given Meet using an inline formset."""

    template_name = "project/edit_lineup.html"

    def dispatch(self, request, *args, **kwargs):
        self.meet = get_object_or_404(Meet, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        formset = RoundAssignmentFormSet(instance=self.meet)
        return render(request, self.template_name, {"meet": self.meet, "formset": formset})

    def post(self, request, *args, **kwargs):
        formset = RoundAssignmentFormSet(request.POST, instance=self.meet)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Lineup updated successfully.")
            return redirect("project:meet_detail", pk=self.meet.pk)
        else:
            # formset will carry errors including our custom ValidationError messages
            return render(request, self.template_name, {"meet": self.meet, "formset": formset})


# ---------------------- CRUD views ----------------------------
class TeamCreateView(CreateView):
    model = Team
    fields = ["name", "school_name", "coach_name", "coach_email"]
    template_name = "project/team_form.html"
    success_url = reverse_lazy("project:team_list")


class TeamUpdateView(UpdateView):
    model = Team
    fields = ["name", "school_name", "coach_name", "coach_email"]
    template_name = "project/team_form.html"
    success_url = reverse_lazy("project:team_list")


class TeamDeleteView(DeleteView):
    model = Team
    template_name = "project/team_confirm_delete.html"
    success_url = reverse_lazy("project:team_list")


class MeetCreateView(CreateView):
    model = Meet
    fields = ["date", "location", "opponent_league_name", "notes"]
    template_name = "project/meet_form.html"

    def form_valid(self, form):
        team_id = self.kwargs.get("team_id")
        form.instance.team_id = team_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("project:team_meets", kwargs={"team_id": self.object.team_id})


class MeetUpdateView(UpdateView):
    model = Meet
    fields = ["date", "location", "opponent_league_name", "notes"]
    template_name = "project/meet_form.html"

    def get_success_url(self):
        return reverse_lazy("project:meet_detail", kwargs={"pk": self.object.pk})


class MeetDeleteView(DeleteView):
    model = Meet
    template_name = "project/meet_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("project:team_meets", kwargs={"team_id": self.object.team_id})
