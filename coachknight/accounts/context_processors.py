def user_profile(request):
    """Add user_profile to template context, handling missing profiles gracefully."""
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            return {
                'user_profile': profile,
                'is_coach': profile.is_coach,
                'is_vendor': profile.is_vendor,
            }
        except:
            pass
    return {
        'user_profile': None,
        'is_coach': False,
        'is_vendor': False,
    }
