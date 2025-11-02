from django.db import models
import os
from django.conf import settings

class Voter(models.Model):
    '''
    Represent one registered voter from Newton, MA.
    CSV columns (in this order):
    Voter ID Number, Last Name, First Name,
    Residential Address - Street Number, Residential Address - Street Name,
    Residential Address - Apartment Number, Residential Address - Zip Code,
    Date of Birth, Date of Registration, Party Affiliation, Precinct Number,
    v20state, v21town, v21primary, v22general, v23town, voter_score
    '''

    voter_id_number = models.CharField(max_length=20)
    last_name = models.TextField()
    first_name = models.TextField()

    res_street_number = models.TextField(blank=True)
    res_street_name = models.TextField(blank=True)
    res_apartment = models.TextField(blank=True)
    res_zip = models.TextField(blank=True)

    date_of_birth = models.TextField(blank=True)
    date_of_registration = models.TextField(blank=True)

    party = models.CharField(max_length=2, blank=True)
    precinct = models.TextField(blank=True)

    v20state = models.TextField(blank=True)
    v21town = models.TextField(blank=True)
    v21primary = models.TextField(blank=True)
    v22general = models.TextField(blank=True)
    v23town = models.TextField(blank=True)

    voter_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.last_name}, {self.first_name} (Pct {self.precinct})'


def load_data():
    '''Load voters from CSV inside voter_analytics directory.'''

    # very dangerous!
    Voter.objects.all().delete()

    filename = os.path.join(settings.BASE_DIR, 'voter_analytics', 'newton_voters.csv')
    f = open(filename, 'r', encoding='utf-8')

    # discard headers
    f.readline()

    created = 0

    for line in f:
        fields = line.strip().split(',')
        if len(fields) < 17:
            print("Skipping short line:", line)
            continue
        try:
            voter = Voter(
                voter_id_number = fields[0].strip(),
                last_name = fields[1].strip(),
                first_name = fields[2].strip(),
                res_street_number = fields[3].strip(),
                res_street_name = fields[4].strip(),
                res_apartment = fields[5].strip(),
                res_zip = fields[6].strip(),
                date_of_birth = fields[7].strip(),
                date_of_registration = fields[8].strip(),
                party = fields[9].strip(),
                precinct = fields[10].strip(),
                v20state = fields[11].strip(),
                v21town = fields[12].strip(),
                v21primary = fields[13].strip(),
                v22general = fields[14].strip(),
                v23town = fields[15].strip(),
                voter_score = int(fields[16]) if fields[16].strip() else None,
            )
            voter.save()
            created += 1
        except Exception as e:
            print("Error on line:", line)
            print(e)

    f.close()
    print(f"Done. Created {created} Voters")

# Create your models here.
