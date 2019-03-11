from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import (ChatSession, ChatSessionMember,ChatSessionMessage, deserialize_user)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions



# Create your views here.

class ChatSessionView(APIView):
    """Manage chat session"""
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        user = request.user
        chat_session = ChatSession.objects.create(owner = user)

        return Response({
            'status': 'SUCCESS', 
            'uri': chat_session.uri,
            'message': 'Novo chat criado'
        })
    def patch(self, request, *args, **kwargs):
        """Adiciona usuario para um sessao de chat"""
        User = get_user_model()

        uri = kwargs['uri']
        username = request.data['username']
        user = User.objects.get(username = username)
        chat_session = ChatSession.objects.get(uri = uri)
        owner = chat_session.owner

        if owner != user:
            chat_session.members.get_or_create(
                user = user, chat_session = chat_session
            )
        owner = deserialize_user(owner)
        members = [
            deserialize_user(chat_session.user)
            for chat_session in  chat_session.members.all()
        ]
        members.insert(0, owner) #coloca o criador do chat como o primeiro membro

        return Response({
            'status':'SUCCESS',
            'members': members,
            'message':'%s entrou para a conversa' % user.username,
            'user':deserialize_user(user)


        })
class ChatSessionMessageView(APIView):
    """Cria mensagens na sessao"""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """retorna todas as mensagens no chat"""
        uri = kwargs['uri']
        chat_session = ChatSession.objects.get(uri = uri)
        messages = [
            chat_session_messsage.to_join()
            for chat_session_messsage in chat_session.messages.all()
        ]
        return Response({
            'id': chat_session.id,
            'uri': chat_session.uri,
            'message': messages

        })
    def post(self, request, *args, **kwargs):
        """Cria uma nova mensagem na sessao"""

        uri = kwargs['uri']
        message = request.data['message']

        user = request.user

        chat_session = ChatSession.objects.get(uri = uri)

        ChatSessionMessage.objects.create(
            user = user,
            chat_session = chat_session,
            message = message,

        )
        return Response({
            'status': 'SUCCESS',
            'uri': chat_session.uri,
            'message': message,
            'user': deserialize_user(user)

        })