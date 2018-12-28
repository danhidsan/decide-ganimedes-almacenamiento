from django.db import models
from base.models import BigBigField

class Vote(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField()

    def __str__(self):
        return '{}: {}'.format(self.voting_id, self.voter_id)

# class Vote(Document):
#     voting_id=fields.IntField()
#     voter_id=fields.IntField()
#     a=BigBigField()
#     b=BigBigField()
#     voted=fields.DateTimeField()
