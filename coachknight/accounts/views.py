from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from .models import UserProfile

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_role'] = self.request.GET.get('role', '')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        role = self.request.POST.get('role')
        if role in ['coach', 'vendor']:
            UserProfile.objects.create(user=self.object, role=role)
            login(self.request, self.object)
            messages.success(self.request, f'Account created successfully! Welcome as a {role}.')
        return response

@login_required
def dashboard(request):
    user_profile = request.user.userprofile
    if user_profile.is_coach:
        # Import here to avoid circular import
        from marketplace.models import CoachProfile
        try:
            coach_profile = user_profile.coachprofile
            return render(request, 'accounts/coach_dashboard.html', {
                'coach_profile': coach_profile
            })
        except CoachProfile.DoesNotExist:
            return redirect('accounts:coach_profile_edit')
    elif user_profile.is_vendor:
        # Import here to avoid circular import
        from marketplace.models import VendorProfile
        try:
            vendor_profile = user_profile.vendorprofile
            return render(request, 'accounts/vendor_dashboard.html', {
                'vendor_profile': vendor_profile
            })
        except VendorProfile.DoesNotExist:
            return redirect('marketplace:vendor_dashboard')
    return redirect('home')

@login_required
def coach_profile(request):
    user_profile = request.user.userprofile
    if not user_profile.is_coach:
        return redirect('accounts:dashboard')
    
    # Import here to avoid circular import
    from marketplace.models import CoachProfile
    coach_profile = get_object_or_404(CoachProfile, user_profile=user_profile)
    return render(request, 'accounts/coach_profile.html', {
        'coach_profile': coach_profile
    })

@login_required
def coach_profile_edit(request):
    user_profile = request.user.userprofile
    if not user_profile.is_coach:
        return redirect('accounts:dashboard')
    
    # Import here to avoid circular import
    from marketplace.models import CoachProfile
    coach_profile, created = CoachProfile.objects.get_or_create(user_profile=user_profile)
    
    if request.method == 'POST':
        # Update basic fields
        coach_profile.display_name = request.POST.get('display_name')
        coach_profile.bio = request.POST.get('bio', '')
        coach_profile.school_affiliation = request.POST.get('school_affiliation', '')
        coach_profile.grade_level = request.POST.get('grade_level')
        coach_profile.rating_text = request.POST.get('rating_text', '')
        coach_profile.years_experience = int(request.POST.get('years_experience', 0))
        coach_profile.age_groups_taught = request.POST.get('age_groups_taught', '')
        coach_profile.hourly_rate_min = request.POST.get('hourly_rate_min') or None
        coach_profile.hourly_rate_max = request.POST.get('hourly_rate_max') or None
        coach_profile.has_car = request.POST.get('has_car') == 'on'
        coach_profile.max_travel_miles = int(request.POST.get('max_travel_miles', 10))
        coach_profile.references_provided = request.POST.get('references_provided') == 'on'
        coach_profile.experience_with_schools = request.POST.get('experience_with_schools') == 'on'
        coach_profile.tournament_director_experience = request.POST.get('tournament_director_experience') == 'on'
        coach_profile.actively_looking = request.POST.get('actively_looking') == 'on'
        coach_profile.email = request.POST.get('email', '')
        coach_profile.phone = request.POST.get('phone', '')
        
        # Handle numeric ratings
        if request.POST.get('rating_rapid'):
            coach_profile.rating_rapid = int(request.POST.get('rating_rapid'))
        if request.POST.get('rating_blitz'):
            coach_profile.rating_blitz = int(request.POST.get('rating_blitz'))
        if request.POST.get('rating_bullet'):
            coach_profile.rating_bullet = int(request.POST.get('rating_bullet'))
        
        coach_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:coach_profile')
    
    return render(request, 'accounts/coach_profile_edit.html', {
        'coach_profile': coach_profile
    })
