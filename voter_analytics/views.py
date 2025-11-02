from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count
from .models import Voter
import plotly.graph_objects as go
from plotly.offline import plot

def _filter_queryset(request):
    qs = Voter.objects.all().order_by('last_name', 'first_name')

    party = request.GET.get('party', '').strip()
    min_dob_year = request.GET.get('min_dob_year', '')
    max_dob_year = request.GET.get('max_dob_year', '')
    voter_score = request.GET.get('voter_score', '')

    voted_20state = request.GET.get('v20state', '')
    voted_21town = request.GET.get('v21town', '')
    voted_21primary = request.GET.get('v21primary', '')
    voted_22general = request.GET.get('v22general', '')
    voted_23town = request.GET.get('v23town', '')

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

def _common_form_context():
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

    return parties, years, scores


class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        return _filter_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parties, years, scores = _common_form_context()
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


class VoterGraphsView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = _filter_queryset(self.request)
        parties, years, scores = _common_form_context()
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

        birth_counts = {}
        for v in qs:
            dob = v.date_of_birth or ''
            year = dob[-4:] if len(dob) >= 4 else 'Unknown'
            if not year.isdigit():
                year = 'Unknown'
            birth_counts[year] = birth_counts.get(year, 0) + 1
        birth_years = [y for y in birth_counts.keys()]
        birth_values = [birth_counts[y] for y in birth_years]
        birth_fig = go.Figure(data=[go.Bar(x=birth_years, y=birth_values)])
        birth_fig.update_layout(title='Voters by Year of Birth', xaxis_title='Year', yaxis_title='Count')
        birth_div = plot(birth_fig, output_type='div', include_plotlyjs=False)

        party_counts = {}
        for v in qs:
            p = (v.party or '').strip()
            if p == '':
                p = 'Unknown'
            party_counts[p] = party_counts.get(p, 0) + 1
        party_labels = list(party_counts.keys())
        party_values = [party_counts[l] for l in party_labels]
        party_fig = go.Figure(data=[go.Pie(labels=party_labels, values=party_values, hole=0)])
        party_fig.update_layout(title='Voters by Party')
        party_div = plot(party_fig, output_type='div', include_plotlyjs=False)

        elections = {
            '2020 State': qs.filter(v20state__iexact='Y').count(),
            '2021 Town': qs.filter(v21town__iexact='Y').count(),
            '2021 Primary': qs.filter(v21primary__iexact='Y').count(),
            '2022 General': qs.filter(v22general__iexact='Y').count(),
            '2023 Town': qs.filter(v23town__iexact='Y').count(),
        }
        elec_labels = list(elections.keys())
        elec_values = [elections[k] for k in elec_labels]
        elec_fig = go.Figure(data=[go.Bar(x=elec_labels, y=elec_values)])
        elec_fig.update_layout(title='Participation by Election', xaxis_title='Election', yaxis_title='Voted count')
        elec_div = plot(elec_fig, output_type='div', include_plotlyjs=False)

        context['birth_div'] = birth_div
        context['party_div'] = party_div
        context['election_div'] = elec_div
        return context
