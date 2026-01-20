from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CoachProfile, VendorProfile, JobPost, Town

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
