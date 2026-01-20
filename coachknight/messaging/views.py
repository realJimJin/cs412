from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .models import Thread, Message

@login_required
def inbox(request):
    user_profile = request.user.userprofile
    if user_profile.is_coach:
        from marketplace.models import CoachProfile
        try:
            coach = user_profile.coachprofile
            threads = Thread.objects.filter(coach=coach).order_by('-updated_at')
        except CoachProfile.DoesNotExist:
            threads = []
    elif user_profile.is_vendor:
        from marketplace.models import VendorProfile
        try:
            vendor = user_profile.vendorprofile
            threads = Thread.objects.filter(vendor=vendor).order_by('-updated_at')
        except VendorProfile.DoesNotExist:
            threads = []
    else:
        threads = []
    
    return render(request, 'messaging/inbox.html', {'threads': threads})

@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    thread_messages = thread.messages.all().order_by('created_at')
    return render(request, 'messaging/thread_detail.html', {
        'thread': thread,
        'messages': thread_messages,
    })

@login_required
def send_message(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            user_profile = request.user.userprofile
            sender_type = 'coach' if user_profile.is_coach else 'vendor'
            Message.objects.create(
                thread=thread,
                sender=request.user,
                sender_type=sender_type,
                body=body,
            )
            thread.save()  # Update updated_at
    return redirect('messaging:thread_detail', pk=pk)

@login_required
def start_thread_with_coach(request, coach_pk):
    """Vendor starts a thread with a coach"""
    from marketplace.models import CoachProfile, VendorProfile
    user_profile = request.user.userprofile
    if not user_profile.is_vendor:
        return redirect('home')
    
    coach = get_object_or_404(CoachProfile, pk=coach_pk)
    vendor = VendorProfile.objects.get(user_profile=user_profile)
    
    # Find or create thread
    thread, created = Thread.objects.get_or_create(
        coach=coach,
        vendor=vendor,
        defaults={'job_post': None}
    )
    return redirect('messaging:thread_detail', pk=thread.pk)

@login_required
def start_thread_with_vendor(request, vendor_pk):
    """Coach starts a thread with a vendor (e.g., to apply for a job)"""
    from marketplace.models import CoachProfile, VendorProfile
    user_profile = request.user.userprofile
    if not user_profile.is_coach:
        return redirect('home')
    
    vendor = get_object_or_404(VendorProfile, pk=vendor_pk)
    coach = CoachProfile.objects.get(user_profile=user_profile)
    
    # Find or create thread
    thread, created = Thread.objects.get_or_create(
        coach=coach,
        vendor=vendor,
        defaults={'job_post': None}
    )
    return redirect('messaging:thread_detail', pk=thread.pk)
