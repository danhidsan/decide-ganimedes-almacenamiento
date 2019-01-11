from authentication.models import User
from .models import Census
from voting.models import Question
from base.tests import BaseTestCase
from postproc.models import PostProcType
from voting.models import Voting

class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        voting1 = Voting.objects.create(name='Voting 1', postproc_type=PostProcType.IDENTITY)
        voting1.id = '40'
        voting1.save()

        voting2 = Voting.objects.create(name='Voting 2', postproc_type=PostProcType.IDENTITY)
        voting2.id = '50'
        voting2.save()

        self.census = Census(voting_id=1, voter_id=1)
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_list_voting(self):
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)

        self.login(user='noadmin@gmail.com')
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)

        self.login()
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [1]})

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, Census.objects.count())

    def test_add_new_voters_conflict(self):

        data = {'voting_id': 1, 'voters': [1]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    # Registramos a varios usuarios nuevos en el sistema, y creamos una nueva votación.
    # El número de censos después de hacer la llamada debe ser mayor que el número de censos anterior.
    def test_add_voters_registered(self):

        census_before = len(Census.objects.all().values_list('voting_id', flat=True))

        admin = User(email='administrador@gmail.com', password='qwerty')
        admin.is_staff = True
        admin.save()

        voting_id = "40"
        self.client.force_login(admin)
        response2 = self.client.get('/census/addAllRegistered/?voting_id={}'.format(voting_id))
        census_after = len(Census.objects.all().values_list('voting_id', flat=True))

        self.assertEqual(response2.status_code, 302)
        self.assertTrue(census_before < census_after)

    # Si introducimos un id de una votacion que no existe, el número de censos no debe
    #  variar
    def test_add_voters_registered_fail_votingId(self):

        census_before = len(Census.objects.all().values_list('voting_id', flat=True))

        user1 = User(email='user1@user1.com', password='user1user1', city='sevilla', sex='M')
        user1.save()

        admin = User(email='administrador@gmail.com', password='qwerty')
        admin.is_staff = True
        admin.save()

        self.client.force_login(admin)
        voting_id = "90"
        response2 = self.client.get('/census/addAllRegistered/?voting_id={}'.format(voting_id))
        census_after = len(Census.objects.all().values_list('voting_id', flat=True))

        self.assertEqual(response2.status_code, 302)
        self.assertTrue(census_before == census_after)

    # Si el usuario que está logueado no es staff, no se podrá crear el censo, por tanto, el número de censos
    # inicial será igual al número de censos final.
    def test_add_voters_registered_fail_not_staff(self):

        census_before = len(Census.objects.all().values_list('voting_id', flat=True))

        user1 = User(email='user1@user1.com', password='user1user1', city='sevilla', sex='M')
        user1.save()

        admin = User(email='administrador@gmail.com', password='qwerty', is_staff=False)
        admin.save()

        self.client.force_login(admin)
        voting_id = "90"
        response2 = self.client.get('/census/addAllRegistered/?voting_id={}'.format(voting_id))
        census_after = len(Census.objects.all().values_list('voting_id', flat=True))

        self.assertEqual(response2.status_code, 302)
        self.assertTrue(census_before == census_after)

    #   Creamos 3 usuarios nuevos, cada uno de una ciudad distinta. Uno de ellos será de la ciudad
    #   que queramos añadir el censo, en este caso, Sevilla. Hay que tener en cuenta que el algoritmo
    #   debe ignorar también las mayúsculas, por lo que usaremos la palabra Sevilla de dos formas distintas
    #   en la asignación de la ciudad del usuario y de la petición. Como sólo debe añadirse un censo al total,
    #   comprobamos que la función redirecciona a la vista(Codigo mensaje 302) y que tendremos 1 censo más
    #   en la base de datos.

    def test_add_voters_city(self):

        census_before = len(Census.objects.all().values_list('voting_id', flat=True))

        user1 = User(email='user1@user1.com', password='user1user1', city='sevilla', sex='M')
        user1.save()

        user2 = User(email='user2@user2.com', password='user2user2', city="Murcia", sex="N")
        user2.save()

        user3 = User(email='user3@user3.com', password='user3user3', city="Albacete", sex="W")
        user3.save()

        admin = User(email='administrador@gmail.com', password='qwerty')
        admin.is_staff = True
        admin.save()

        voting_id = "40"
        self.client.force_login(admin)
        response2 = self.client.get('/census/addAllInCity/?voting_id={}&city={}'.format(voting_id, 'Sevilla'))
        census_after = len(Census.objects.all().values_list('voting_id', flat=True))

        self.assertEqual(response2.status_code, 302)
        self.assertTrue(census_before + 1 == census_after)

    def test_add_voters_city_fail_votingId(self):

        census_before = len(Census.objects.all().values_list('voting_id', flat=True))

        user1 = User(email='user1@user1.com', password='user1user1', city='sevilla', sex='M')
        user1.save()

        user2 = User(email='user2@user2.com', password='user2user2', city="Murcia", sex="N")
        user2.save()

        user3 = User(email='user3@user3.com', password='user3user3', city="Albacete", sex="W")
        user3.save()

        admin = User(email='administrador@gmail.com', password='qwerty')
        admin.is_staff = True
        admin.save()

        voting_id = "99"
        self.client.force_login(admin)
        response2 = self.client.get('/census/addAllInCity/?voting_id={}&city={}'.format(voting_id, 'Sevilla'))
        census_after = len(Census.objects.all().values_list('voting_id', flat=True))

        self.assertEqual(response2.status_code, 302)
        self.assertTrue(census_before == census_after)

    def test_add_voters_city_fail_not_staff(self):

        census_before = len(Census.objects.all().values_list('voting_id', flat=True))

        user1 = User(email='user1@user1.com', password='user1user1', city='sevilla', sex='M')
        user1.save()

        user2 = User(email='user2@user2.com', password='user2user2', city="Murcia", sex="N")
        user2.save()

        user3 = User(email='user3@user3.com', password='user3user3', city="Albacete", sex="W")
        user3.save()

        admin = User(email='administrador@gmail.com', password='qwerty')
        admin.is_staff = False
        admin.save()

        voting_id = "40"
        self.client.force_login(admin)
        response2 = self.client.get('/census/addAllInCity/?voting_id={}&city={}'.format(voting_id, 'Sevilla'))
        census_after = len(Census.objects.all().values_list('voting_id', flat=True))

        self.assertEqual(response2.status_code, 302)
        self.assertTrue(census_before == census_after)

    def test_add_new_voters(self):

        user1 = User(email='user1@user1.com', id='60', password='user1user1', city='sevilla', sex='M')
        user1.save()

        user2 = User(email='user2@user2.com', id='61', password='user2user2', city="Murcia", sex="N")
        user2.save()

        data = {'voting_id': 40, 'voters': [60, 61]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.client.force_login(user1)

        user3 = User(email='user3@user3.com', id='62', password='user3user3', city="Zaragoza", sex="W")
        user3.save()
        data = {'voting_id': 40, 'voters': [62]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)

        user4 = User(email='user4@user4.com', id='63', password='user4user4', city="Tarragona", sex="W")
        user4.save()
        self.login()
        data = {'voting_id': 40, 'voters': [63]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)