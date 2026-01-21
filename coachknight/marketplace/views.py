from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import CoachProfile, VendorProfile, JobPost, Town, VendorWaitlistEntry


def staff_required(view_func):
    """Decorator to require staff access"""
    decorated = user_passes_test(lambda u: u.is_staff)(view_func)
    return decorated


# ============ COACH INTAKE FLOW ============

def coach_join(request):
    """Coach intake landing page - redirects to signup if not logged in"""
    if request.user.is_authenticated:
        # Check if they already have a profile
        try:
            user_profile = request.user.userprofile
            if user_profile.is_coach:
                try:
                    coach_profile = user_profile.coachprofile
                    # Already has profile, go to dashboard
                    return redirect('marketplace:coach_dashboard')
                except CoachProfile.DoesNotExist:
                    # Has account but no profile, show intake form
                    return redirect('marketplace:coach_intake')
            else:
                # They're a vendor, show error
                messages.error(request, "You're registered as a vendor. Contact us to switch roles.")
                return redirect('home')
        except:
            # No user profile, something's wrong
            return redirect('accounts:signup')
    
    # Not logged in - show landing page with signup/login options
    return render(request, 'marketplace/coach_join.html')


@login_required
def coach_intake(request):
    """Coach intake form - collects profile info"""
    try:
        user_profile = request.user.userprofile
        if not user_profile.is_coach:
            messages.error(request, "This page is for coaches only.")
            return redirect('home')
    except:
        return redirect('accounts:signup')
    
    # Check if they already have a profile
    try:
        coach_profile = user_profile.coachprofile
        # Already has profile, redirect to dashboard
        return redirect('marketplace:coach_dashboard')
    except CoachProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        # Get availability checkboxes
        availability_list = request.POST.getlist('availability')
        availability = ','.join(availability_list)
        
        # Create the profile
        coach_profile = CoachProfile.objects.create(
            user_profile=user_profile,
            display_name=request.POST.get('full_name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            town=request.POST.get('town', ''),
            zip_code=request.POST.get('zip_code', ''),
            max_travel_miles=int(request.POST.get('willing_travel_miles', 10)),
            has_car=request.POST.get('has_car') == 'on',
            availability=availability,
            grade_level=request.POST.get('age_bracket', 'other'),
            chesscom_username=request.POST.get('chesscom_username', ''),
            lichess_username=request.POST.get('lichess_username', ''),
            rating_range=request.POST.get('rating_range', ''),
            teaching_experience=request.POST.get('teaching_experience', ''),
            status='new',
        )
        
        messages.success(request, "You're in! We'll review your profile shortly.")
        return redirect('marketplace:coach_intake_success')
    
    return render(request, 'marketplace/coach_intake.html', {
        'user': request.user,
    })


@login_required
def coach_intake_success(request):
    """Success page after coach intake"""
    return render(request, 'marketplace/coach_intake_success.html')


@login_required
def coach_dashboard(request):
    """Coach dashboard showing their profile and status"""
    try:
        user_profile = request.user.userprofile
        if not user_profile.is_coach:
            return redirect('home')
    except:
        return redirect('accounts:signup')
    
    try:
        coach_profile = user_profile.coachprofile
    except CoachProfile.DoesNotExist:
        return redirect('marketplace:coach_intake')
    
    return render(request, 'marketplace/coach_dashboard.html', {
        'coach_profile': coach_profile,
    })


# ============ VENDOR WAITLIST FLOW ============

def vendor_join(request):
    """Vendor waitlist form"""
    if request.method == 'POST':
        VendorWaitlistEntry.objects.create(
            org_name=request.POST.get('org_name', ''),
            contact_name=request.POST.get('contact_name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            towns=request.POST.get('towns', ''),
            needs_text=request.POST.get('needs_text', ''),
        )
        messages.success(request, "Thanks! We'll be in touch soon.")
        return redirect('marketplace:vendor_join_success')
    
    return render(request, 'marketplace/vendor_join.html')


def vendor_join_success(request):
    """Success page after vendor waitlist signup"""
    return render(request, 'marketplace/vendor_join_success.html')


# ============ STAFF ADMIN VIEWS ============

@login_required
@staff_required
def staff_overview(request):
    """Staff overview dashboard with counts"""
    from accounts.models import UserProfile
    
    total_coaches = CoachProfile.objects.count()
    approved_coaches = CoachProfile.objects.filter(status='approved').count()
    new_coaches = CoachProfile.objects.filter(status='new').count()
    total_vendors = VendorProfile.objects.count()
    total_jobs = JobPost.objects.count()
    vendor_waitlist = VendorWaitlistEntry.objects.filter(status='new').count()
    
    recent_coaches = CoachProfile.objects.order_by('-created_at')[:10]
    recent_vendor_waitlist = VendorWaitlistEntry.objects.order_by('-created_at')[:10]
    
    return render(request, 'marketplace/staff_overview.html', {
        'total_coaches': total_coaches,
        'approved_coaches': approved_coaches,
        'new_coaches': new_coaches,
        'total_vendors': total_vendors,
        'total_jobs': total_jobs,
        'vendor_waitlist': vendor_waitlist,
        'recent_coaches': recent_coaches,
        'recent_vendor_waitlist': recent_vendor_waitlist,
    })


@login_required
@staff_required
def staff_coaches(request):
    """Staff page to review and approve coaches"""
    status_filter = request.GET.get('status', '')
    town_filter = request.GET.get('town', '')
    
    coaches = CoachProfile.objects.all().order_by('-created_at')
    
    if status_filter:
        coaches = coaches.filter(status=status_filter)
    if town_filter:
        coaches = coaches.filter(town__icontains=town_filter)
    
    # Handle approve/reject actions
    if request.method == 'POST':
        coach_id = request.POST.get('coach_id')
        action = request.POST.get('action')
        
        if coach_id and action in ['approve', 'reject']:
            coach = get_object_or_404(CoachProfile, pk=coach_id)
            if action == 'approve':
                coach.status = 'approved'
                messages.success(request, f"Approved {coach.display_name}")
            else:
                coach.status = 'rejected'
                messages.success(request, f"Rejected {coach.display_name}")
            coach.save()
            return redirect('marketplace:staff_coaches')
    
    return render(request, 'marketplace/staff_coaches.html', {
        'coaches': coaches,
        'status_filter': status_filter,
        'town_filter': town_filter,
    })

def search_coaches(request):
    coaches = CoachProfile.objects.filter(actively_looking=True).order_by('-created_at')
    return render(request, 'marketplace/search.html', {'coaches': coaches})

def coach_detail(request, pk):
    coach = get_object_or_404(CoachProfile, pk=pk)
    return render(request, 'marketplace/coach_detail.html', {'coach': coach})

def job_list(request):
    jobs = JobPost.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'marketplace/job_list.html', {'jobs': jobs})

@login_required
def job_create(request):
    user_profile = request.user.userprofile
    if not user_profile.is_vendor:
        return redirect('home')
    
    vendor_profile, created = VendorProfile.objects.get_or_create(user_profile=user_profile)
    towns = Town.objects.all().order_by('name')
    
    if request.method == 'POST':
        job = JobPost.objects.create(
            vendor=vendor_profile,
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            town_id=request.POST.get('town') or None,
            age_group=request.POST.get('age_group', ''),
            num_students=int(request.POST.get('num_students', 10)),
            day_of_week=request.POST.get('day_of_week', ''),
            start_time=request.POST.get('start_time') or None,
            end_time=request.POST.get('end_time') or None,
            pay_rate_min=request.POST.get('pay_rate_min') or None,
            pay_rate_max=request.POST.get('pay_rate_max') or None,
            is_active=True,
        )
        messages.success(request, 'Job posted successfully!')
        return redirect('marketplace:job_detail', pk=job.pk)
    
    return render(request, 'marketplace/job_form.html', {
        'vendor_profile': vendor_profile,
        'towns': towns,
    })

def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    return render(request, 'marketplace/job_detail.html', {'job': job})

@login_required
def job_edit(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    user_profile = request.user.userprofile
    if not user_profile.is_vendor or job.vendor.user_profile != user_profile:
        return redirect('home')
    
    towns = Town.objects.all().order_by('name')
    
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.description = request.POST.get('description', '')
        job.town_id = request.POST.get('town') or None
        job.age_group = request.POST.get('age_group', '')
        job.num_students = int(request.POST.get('num_students', 10))
        job.day_of_week = request.POST.get('day_of_week', '')
        job.start_time = request.POST.get('start_time') or None
        job.end_time = request.POST.get('end_time') or None
        job.pay_rate_min = request.POST.get('pay_rate_min') or None
        job.pay_rate_max = request.POST.get('pay_rate_max') or None
        job.is_active = request.POST.get('is_active') == 'on'
        job.save()
        messages.success(request, 'Job updated successfully!')
        return redirect('marketplace:job_detail', pk=job.pk)
    
    return render(request, 'marketplace/job_form.html', {
        'job': job,
        'towns': towns,
    })

@login_required
def vendor_dashboard(request):
    user_profile = request.user.userprofile
    if not user_profile.is_vendor:
        return redirect('home')
    
    vendor_profile, created = VendorProfile.objects.get_or_create(
        user_profile=user_profile,
        defaults={'organization_name': request.user.username, 'contact_name': request.user.username}
    )
    jobs = vendor_profile.job_posts.all().order_by('-created_at')
    
    return render(request, 'marketplace/vendor_dashboard.html', {
        'vendor_profile': vendor_profile,
        'jobs': jobs,
    })
