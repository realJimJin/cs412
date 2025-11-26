from django.db import models


class Team(models.Model):
    """A math team that competes in IMLEM meets."""

    name = models.CharField(max_length=100)
    school_name = models.CharField(max_length=200)
    coach_name = models.CharField(max_length=100)
    coach_email = models.EmailField()

    def __str__(self):
        return f"{self.school_name} – {self.name}"


class Student(models.Model):
    """A student on a math team."""

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="students",
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    grade = models.PositiveSmallIntegerField()
    imlem_id = models.CharField(
        max_length=20,
        blank=True,
        help_text="Optional league ID or number."
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.team.name})"


class CategoryStrength(models.Model):
    """How strong a student is in a particular IMLEM category."""

    CATEGORY_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="category_strengths",
    )
    category_name = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
    )
    strength_score = models.PositiveSmallIntegerField(
        help_text="Higher number = stronger in this category."
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} – {self.category_name} ({self.strength_score})"


class Meet(models.Model):
    """A single IMLEM meet for one team."""

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="meets",
    )
    date = models.DateField()
    location = models.CharField(max_length=200)
    opponent_league_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional: division / league / host info."
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Meet for {self.team.name} on {self.date}"


class RoundAssignment(models.Model):
    """Assignment of a student to a round and category in a meet."""

    CATEGORY_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
    ]

    ROLE_CHOICES = [
        ("COMPETE", "Compete"),
        ("ALTERNATE", "Alternate"),
    ]

    meet = models.ForeignKey(
        Meet,
        on_delete=models.CASCADE,
        related_name="round_assignments",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="round_assignments",
    )
    round_number = models.PositiveSmallIntegerField(
        help_text="Individual round number (1–5)."
    )
    category_name = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
    )
    score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Optional: points earned for this round."
    )

    class Meta:
        unique_together = ("meet", "student", "round_number")

    def __str__(self):
        return (
            f"{self.meet} – R{self.round_number} "
            f"{self.category_name}: {self.student} ({self.role})"
        )
