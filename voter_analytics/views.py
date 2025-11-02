from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Voter

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        qs = Voter.objects.all().order_by('last_name', 'first_name')

        party = self.request.GET.get('party', '').strip()
        min_dob_year = self.request.GET.get('min_dob_year', '')
        max_dob_year = self.request.GET.get('max_dob_year', '')
        voter_score = self.request.GET.get('voter_score', '')

        voted_20state = self.request.GET.get('v20state', '')
        voted_21town = self.request.GET.get('v21town', '')
        voted_21primary = self.request.GET.get('v21primary', '')
        voted_22general = self.request.GET.get('v22general', '')
        voted_23town = self.request.GET.get('v23town', '')

        if party:
            qs = qs.filter(party__iexact=party)
        if min_dob_year:
            qs = qs.filter(date_of_birth__endswith=min_dob_year)
        if max_dob_year:
            qs = qs.filter(date_of_birth__endswith=max_dob_year)
        if voter_score:
            qs = qs.filter(voter_score=voter_score)
        if voted_20state:
            qs = qs.filter(v20state__iexact='Y')
        if voted_21town:
            qs = qs.filter(v21town__iexact='Y')
        if voted_21primary:
            qs = qs.filter(v21primary__iexact='Y')
        if voted_22general:
            qs = qs.filter(v22general__iexact='Y')
        if voted_23town:
            qs = qs.filter(v23town__iexact='Y')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        raw_parties = Voter.objects.values_list('party', flat=True).distinct()
        parties = sorted({p.strip() for p in raw_parties if p is not None and p.strip() != ''})

        raw_dobs = Voter.objects.values_list('date_of_birth', flat=True)
        years = set()
        for dob in raw_dobs:
            if dob and len(dob) >= 4:
                year = dob[-4:]
                if year.isdigit():
                    years.add(year)
        years = sorted(years)

        raw_scores = Voter.objects.values_list('voter_score', flat=True).distinct()
        scores = sorted({s for s in raw_scores if s is not None})

        context['parties'] = parties
        context['years'] = years
        context['scores'] = scores
        context['current'] = {
            'party': self.request.GET.get('party', '').strip(),
            'min_dob_year': self.request.GET.get('min_dob_year', ''),
            'max_dob_year': self.request.GET.get('max_dob_year', ''),
            'voter_score': self.request.GET.get('voter_score', ''),
            'v20state': self.request.GET.get('v20state', ''),
            'v21town': self.request.GET.get('v21town', ''),
            'v21primary': self.request.GET.get('v21primary', ''),
            'v22general': self.request.GET.get('v22general', ''),
            'v23town': self.request.GET.get('v23town', ''),
        }
        return context


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
