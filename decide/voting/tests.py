import random
import itertools
from django.utils import timezone
from django.conf import settings
from authentication.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from postproc.models import PostProcType


class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        v = Voting(name='test voting', postproc_type=PostProcType.IDENTITY)
        v.save()

        q1 = Question(desc='test question 1', voting=v)
        q1.save()
        for i in range(5):
            opt = QuestionOption(question=q1, option='option {}'.format(i + 1))
            opt.save()

        q2 = Question(desc='test question 2', voting=v)
        q2.save()
        for i in range(5):
            opt = QuestionOption(question=q2, option='option {}'.format(i + 1))
            opt.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL, defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v, q1, q2

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(email='testvoter{}@gmail.com'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.email = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v, q1, q2):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear1 = {}
        clear2 = {}

        votes = []

        options1 = QuestionOption.objects.filter(question=q1)
        for opt in options1:
            clear1[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'votes': [{"a": a, "b": b}],
                }
                clear1[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.email)
                voter = voters.pop()
                mods.post('store', json=data)

        options2 = QuestionOption.objects.filter(question=q2)
        for opt in options2:
            clear2[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'votes': [{"a": a, "b": b}],
                }
                clear2[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.email)
                voter = voters.pop()
                mods.post('store', json=data)

        return clear1, clear2, options1, options2

    def test_complete_voting(self):
        v, q1, q2 = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        c1, c2, o1, o2 = self.store_votes(v, q1, q2)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for opt in o1:
            self.assertEqual(tally.get(opt.number, 0), c1.get(opt.number, 0))

        for opt in v.postproc[str(q1.id)]:
            self.assertEqual(tally.get(opt["number"], 0), opt["votes"])

        for opt in o2:
            self.assertEqual(tally.get(opt.number, 0), c2.get(opt.number, 0))

        for opt in v.postproc[str(q2.id)]:
                self.assertEqual(tally.get(opt["number"], 0), opt["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin@gmail.com')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'questions': ['I want a '],
            'question_opts': [['cat', 'dog', 'horse']],
            'postproc_type': PostProcType.IDENTITY,
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        v, q1, q2 = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin@gmail.com')
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(v.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')
