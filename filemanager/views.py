from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from Stackfile.response import api_response
from filemanager.models import User, ToDoList, Item
from filemanager.serializers import SignupSerializer, ToDoListSerializer



class Signup(APIView):
    """
    user signup api
    """
    permission_classes = (AllowAny,)

    @api_response
    def post(self, request, format='json', **kwargs):

        data = dict(request.data)
        ser_user = SignupSerializer(data=data)

        if not ser_user.is_valid():
            return {'status': 0, 'message': ser_user.sg_errors}
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['email'],
            email=data['email']
        )
        user.set_password(data['password'])

        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        res = {}
        res.update({
            'uid': user.id,
            'token': token.key,
            'first_name': user.first_name or "",
            'last_name': user.last_name or "",
            'email': user.email,
        })
        return {'status': 1, 'data': res}


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
@api_response
def signin(request):
    """
    :param request:
    :return: return user token everytime user logged in
    """
    data = request.data
    username = data.get("username");
    password = request.data.get("password")
    if not username or not password:
        return {'status': 0, 'message': "Please provide both username and password"}


    user = authenticate(username=username, password=password)
    if not user:
        return {'status': 0, 'message': "Invalid credentials!"}

    try:
        if user.auth_token:
            user.auth_token.delete()
    except Exception:
        pass


    user.last_login = timezone.now()
    user.save()

    token, _ = Token.objects.get_or_create(user=user)

    user_data = {
        'token': token.key,
        'uid': user.id,
        'first_name': user.first_name or "",
        'last_name': user.last_name or "",
        'email': user.email or ""
    }

    return {'status': 1,'data': user_data}

@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes((IsAuthenticated,))
@api_response
def signout(request):
    """user's session will be deleted"""
    user = request.user
    user.auth_token.delete()
    request.session.delete()
    return {'status': 1, "data": "You have successfully logged out"}





class ToDoListView(APIView):
    """upload file"""

    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @api_response
    def get(self, request):
        """get all the files uploaded by user"""
        user = request.user
        todolists = ToDoList.objects.filter(user=user)
        todolists_serializer = ToDoListSerializer(todolists, many=True).data

        return {'status': 1, "data": todolists_serializer}


    @api_response
    def post(self, request):
        """upload file and details"""
        user = request.user
        input_data = request.data

        try:
            title = input_data.get('title', '')
            description = input_data.get('description', '')
            make_public = input_data.get('make_public', False)
            todo_list = ToDoList.objects.create(user=user,
                                                title=title,
                                                description=description,
                                                make_public=make_public)

            todo_list.tags = input_data['tags']
            todo_list.save()

            items = input_data['items']
            for item in items:
                todoitem = Item.objects.create(**item, todolist=todo_list)
                todoitem.save()

            return {'status': 1, "data": "You have successfully Uploaded File"}

        except Exception:
            return {'status': 0, 'message': "Invalid data!"}

    @api_response
    def put(self, request):
        """
        update the to do list for now it will update make_public we could
        edit other fields too here.
        :param request:
        :return:
        """

        try:
            todolists = ToDoList.objects.get(id=request.data['todolist_id'])
            make_public = request.data['make_public']
            if make_public:
                todolists.make_public = make_public
                todolists.save()
            return {'status': 1, "data": "You have successfully updated list"}
        except Exception:
            return {'status': 0, 'message': "Invalid data provided!"}




class GeneratePublicUrl(APIView):
    """generate public url for to do list"""

    @api_response
    def post(self, request):
        """create unique url with to do list id"""

        try:
            todo_list = ToDoList.objects.get(id=request.data['todolist_id'])
            if not todo_list.unique_url:
                unique_url = todo_list.get_unique_url()
                todo_list.unique_url = unique_url
                todo_list.save()
            unique_url = todo_list.unique_url
            return {'status': 1, "data": unique_url}
        except Exception:
            return {'status': 0, 'message': "Invalid ToDO List!"}


class AccesslistView(APIView):
    """access list with given unique url"""

    permission_classes = (AllowAny,)

    @api_response
    def get(self, request):
        """fetch list using unique id"""

        try:
            unique_url = request.GET['unique_url']
            todolist = ToDoList.objects.get(unique_url=unique_url)
            todolist_serializer = ToDoListSerializer(todolist).data
            return {'status': 1, "data": todolist_serializer}

        except Exception:
            return {'status': 0, 'message': "Invalid URL!"}

