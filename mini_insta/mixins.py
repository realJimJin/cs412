from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Profile

class MustOwnProfileMixin(LoginRequiredMixin):
    """For views where the logged-in user must own the target Profile/Post."""
    login_url = "mini_insta:login"

    def get_current_profile(self):
        return get_object_or_404(Profile, user=self.request.user)
