from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken
from rest_framework import status
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers
import json

from django.utils import timezone

from Links.models import Link
from Profile.models import UserProfile

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            name = data.get('name')  # Novo campo: nome
            sexo = data.get('sexo')  # Novo campo: sexo
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados JSON inválidos."}, status=400)

        # Validação dos campos
        if not username or not email or not password or not name or not sexo:
            return JsonResponse({"error": "Todos os campos são obrigatórios."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Nome de usuário já existe."}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email já está em uso."}, status=400)

        # Criando o novo usuário
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Para salvar a senha de forma segura
        )

        # Criação do UserProfile associado ao usuário com valores padrão
        userprofile = UserProfile.objects.create(user=user, name=name, sexo=sexo)

        # Criando os tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return JsonResponse({
            'message': 'Usuário criado com sucesso.',
            'accessToken': access_token,
            'refreshToken': refresh_token
        }, status=status.HTTP_201_CREATED)

    return JsonResponse({"error": "Método não permitido."}, status=405)



@csrf_exempt
def verify_refresh_token(request):
    if request.method == 'POST':
        try:
            # Decodifica o corpo da solicitação JSON
            body = json.loads(request.body)
            refresh_token = body.get('refreshToken')

            if refresh_token:
                try:
                    # Decodifica o refresh token
                    refresh_token_obj = RefreshToken(refresh_token)
                    user_id = refresh_token_obj.get('user_id')
                    user = User.objects.get(id=user_id)

                    # Retorna informações do usuário, se o token for válido
                    return JsonResponse({
                        'username': user.username,
                        'email': user.email
                    }, status=status.HTTP_200_OK)
                except TokenError:
                    # Token inválido ou expirado
                    return JsonResponse({'error': 'Token inválido ou expirado'}, status=status.HTTP_401_UNAUTHORIZED)
                except User.DoesNotExist:
                    # Usuário não encontrado para o ID
                    return JsonResponse({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            else:
                # Tokens não fornecidos
                return JsonResponse({'error': 'Tokens não fornecidos'}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Erro ao processar o corpo da solicitação'}, status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse({"error": "Método não permitido."}, status=405)





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

@api_view(['PUT'])
def update_username(request):
    if request.method == 'PUT':
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            new_username = serializer.validated_data.get('username')
            
            if User.objects.filter(username=new_username).exists():
                return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

            user.username = new_username
            user.save()
            return Response({"message": "Username updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def user_detail(request, username):
    
    token = request.headers.get('Authorization')

    def retrieve_user_profile(authenticated=False, token_expired=False):
        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
            links = Link.objects.filter(user=user)
            link_data = [{'text': link.text, 'url': link.url} for link in links]

            user_data = {
                'authenticated': authenticated,
                'status': True,
                'name': profile.name,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'image': profile.image.url,
                'is_free_user': profile.is_free_user,
                'theme': profile.theme,
                'links': link_data,
                'tokenexpired': token_expired
            }

            return JsonResponse(user_data)

        except User.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': 'Usuário não encontrado',
                'tokenexpired': token_expired
            }, status=404)
        except UserProfile.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': 'Perfil não encontrado',
                'tokenexpired': token_expired
            }, status=404)

    if token:
        refresh_token = refresh_token[7:]  
        try:
            # Cria um objeto RefreshToken a partir do token recebido
            refresh_token_obj = RefreshToken(refresh_token)
            
            # Obtém o user_id diretamente do refresh token
            user_id = refresh_token_obj['user_id']
            user = User.objects.get(id=user_id)
            
            if username != user.username:
                return retrieve_user_profile(authenticated=False, token_expired=False)
            else:
                return retrieve_user_profile(authenticated=True, token_expired=False)
        
        except TokenError:
            # Se o refresh token for inválido ou tiver algum erro relacionado a ele
            return retrieve_user_profile(authenticated=False, token_expired=True)

    else:
        return retrieve_user_profile(authenticated=False, token_expired=False)