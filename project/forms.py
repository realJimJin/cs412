from collections import defaultdict

from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import Meet, RoundAssignment


class RoundAssignmentForm(forms.ModelForm):
    class Meta:
        model = RoundAssignment
        fields = [
            "student",
            "round_number",
            "category_name",
            "role",
            "score",
        ]


class BaseRoundAssignmentInlineFormSet(BaseInlineFormSet):
    """Validate IMLEM lineup constraints inside a Meet.

    Constraints:
    1. No more than 6 students *competing* in any single category (A–E).
    2. Each student competes in **at most** 3 rounds (role = "COMPETE").
    3. Each student must be an alternate in **at least** 2 rounds (role = "ALTERNATE").
    """

    def clean(self):
        super().clean()

        if any(self.errors):
            # Skip further validation if individual forms are invalid.
            return

        category_compete_counts: dict[str, int] = defaultdict(int)
        student_compete_counts: dict[int, int] = defaultdict(int)
        student_alternate_counts: dict[int, int] = defaultdict(int)

        for form in self.forms:
            if self.can_delete and form.cleaned_data.get("DELETE", False):
                # Ignore forms marked for deletion.
                continue

            data = form.cleaned_data
            student = data.get("student")
            if student is None:
                # Should not happen because model field is required.
                continue

            role = data.get("role")
            cat = data.get("category_name")

            if role == RoundAssignment.ROLE_CHOICES[0][0]:  # "COMPETE"
                category_compete_counts[cat] += 1
                student_compete_counts[student.pk] += 1
            elif role == RoundAssignment.ROLE_CHOICES[1][0]:  # "ALTERNATE"
                student_alternate_counts[student.pk] += 1

        # 1. Category competitor limit
        for cat, count in category_compete_counts.items():
            if count > 6:
                raise forms.ValidationError(
                    f"More than 6 competitors assigned to category {cat}. Current: {count}."
                )

        # 2 & 3. Student round limits
        for student_pk, compete_count in student_compete_counts.items():
            if compete_count > 3:
                raise forms.ValidationError(
                    "A student is assigned to compete in more than 3 rounds."
                )
            alt_count = student_alternate_counts.get(student_pk, 0)
            if alt_count < 2:
                raise forms.ValidationError(
                    "Each student must be an alternate in at least 2 rounds."
                )


# Factory to be imported by views
RoundAssignmentFormSet = inlineformset_factory(
    parent_model=Meet,
    model=RoundAssignment,
    form=RoundAssignmentForm,
    formset=BaseRoundAssignmentInlineFormSet,
    extra=10,  # allow some blank assignments initially
    can_delete=True,
)
