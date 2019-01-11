from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404, HttpResponseRedirect

from .forms import UserCreateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from .serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from .schemas import ManualSchema
from rest_framework.views import APIView

from base import mods
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, TruncYear

from django.shortcuts import render
from datetime import date,  timedelta
User=get_user_model()
    
class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)



def contador(request):
    ##############################################################
    #  This method receives a request with tuple 'list'
    # 'list' value is a list of users id
    # This method returns a dictionary with keys:
    # 'man', 'woman','non-binary','total','minor', 'fullage' and 'all'
    # 'all' is a counter by gender group by year
    #############################################################
    id_list=[]
    #rcv   
    #TODO fake id_list . Change at integration moment (visualizer)     
    # if request:
    #     id_list= request.data.get('list', '')
    id_list=['2','4','3','5']
    id_list = list(map(int, id_list))

    #filtered users. In this way, we call only one time to db
    users = User.objects.filter(id__in=id_list)
    
    #count gender python    
    num_total=users.count()
    objectsM = users.filter(sex= User.SEX_OPTIONS[0][0]).count()
    objectsW = users.filter(sex=User.SEX_OPTIONS[1][0]).count()
    objectsN = users.filter(sex=User.SEX_OPTIONS[2][0]).count()

    #count age        
    today = date.today()
    age_legal = 18
    date_legal = date(today.year - age_legal - 1, today.month, today.day) + timedelta(days = 1)
    age_max=130
    date_max = date(today.year - age_max - 1, today.month, today.day) + timedelta(days = 1)
    objects_minor = users.filter(birthdate__range=(date_legal, today)).count()
    objects_fullage = users.filter(birthdate__range= (date_max, date_legal)).count()

    #count ( only 1 db). Grouping by date, and inside the date by gender
       
    queryset = User.objects.filter(id__in=id_list).annotate(
        date=TruncYear('birthdate'),
        ).values('date').annotate(
        total_entries=Count('id'),
        total_m=Count('id', filter=Q(sex=User.SEX_OPTIONS[0][0])),
        total_w=Count('id', filter=Q(sex=User.SEX_OPTIONS[1][0])),
        total_n=Count('id', filter=Q(sex=User.SEX_OPTIONS[2][0])),
        )
    queryset=list(queryset)
    
    #return
    data = { 'man' : objectsM,
     'woman' : objectsW,
     'non-binary' : objectsN, 
     'total' : num_total,
     'minor' : objects_minor,
     'fullage' : objects_fullage,
     'all' : queryset
     }
  
    return Response({'data': data})





class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})



class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()

def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UserCreateForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreateForm()
    return render(request, 'authentication/nuevo_usuario.html', {'formulario':formulario})

