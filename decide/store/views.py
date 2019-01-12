from django.utils import timezone
from django.utils.dateparse import parse_datetime
import django_filters.rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from voting.models import Voting
from census.models import Census
from .models import Vote
from .serializers import VoteSerializer,VotingSerializer,VoterSerializer
from base import mods
from base.perms import UserIsStaff
from authentication.models import User


class VotingView(generics.ListAPIView):

    def get(self, request, voting_id):
        voting_id = self.kwargs['voting_id']
        voters = []
        votes = Vote.objects.filter(voting_id=voting_id).values('voter_id')
        for v in votes:
            voter = User.objects.filter(pk=v['voter_id']).values('id', 'last_login', 'is_superuser', 'first_name',
                                                                 'last_name', 'email', 'is_staff', 'is_active')
            voters.append(voter)
        return Response(voters, status=status.HTTP_200_OK)


class VoterView(generics.ListAPIView):
    serializer_class = VoterSerializer

    def get(self, request, voter_id):
        voter_id = self.kwargs['voter_id']
        votings = []
        census = Census.objects.filter(voter_id=voter_id).values('voting_id')
        for c in census:
            voting = Voting.objects.filter(pk=c['voting_id']).values('id', 'name', 'start_date', 'end_date')
            votings.append(voting)
        if len(votings) > 0:
            result = Response(votings, status=status.HTTP_200_OK)
        else:
            result = Response(votings, status=status.HTTP_204_NO_CONTENT)
        return result


class StoreView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('voting_id', 'voter_id')

    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
         * voting: id
         * voter: id
         * votes: [{ "a": int, "b": int }, ...]
        """

        vid = request.data.get('voting')
        voting = mods.get('voting', params={'id': vid})
        if not voting or not isinstance(voting, list):
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting[0].get('start_date', None)
        end_date = voting[0].get('end_date', None)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            return Response(
                {"message": "voting not started or is closed"},
                status=status.HTTP_401_UNAUTHORIZED)

        uid = int(request.data.get('voter'))
        votes = request.data.get('votes')

        if not vid or not uid or not votes:
            return Response(
                {"message": "voting id or voter id or votes is empty"},
                status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        token = request.auth.key
        voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
        voter_id = voter.get('id', None)
        if not voter_id or voter_id != uid:
            return Response(
                {"message": "voter id is not authorized"},
                status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get('census/{}'.format(vid), params={'voter_id': uid}, response=True)
        if perms.status_code == 401:
            return Response(
                {"message": "voter id is not in census"},
                status=status.HTTP_401_UNAUTHORIZED)

        # check if voter has been already vote in current voting
        old_votes = Vote.objects.filter(voting_id=vid, voter_id=uid)
        if old_votes:
            # deleting votes
            for vote in old_votes:
                vote.delete()

        # Iterate in new votes
        for vote in votes:
            # get primes from vote
            a = vote.get("a")
            b = vote.get("b")

            # creating new vote
            v = Vote(voting_id=vid, voter_id=uid, a=a, b=b)

            # save vote
            v.save()

        return Response({"message": "votes stored successfully"})

