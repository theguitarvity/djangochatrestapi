from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model

User = get_user_model()

def deserialize_user(user):
    """responsavel por deserializar o user para json"""
    return {
        'id': user.id, 
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

# Create your models here.


class TrackableDateModel(models.Model):
     """Abstract model to Track the creation/updated date for a model."""

     create_date = models.DateTimeField(auto_now_add=True)
     update_date = models.DateTimeField(auto_now=True)

     class Meta:
         abstract = True
def _generate_unique_uri():
    """Gera uma uri unica para a sessao do chat"""
    return str(uuid4()).replace('-', '')[:15]

class ChatSession(TrackableDateModel):
    """
        Chat session
        Com a uri gerada pelos 15 primeiros caracteres do uuid
    """
    owner = models.ForeignKey(User, on_delete = models.PROTECT)
    uri = models.URLField(default=_generate_unique_uri)

    def __str__(self):
        return self.uri
class ChatSessionMessage(TrackableDateModel):
    """Registra as mensagens para a sessao"""

    user = models.ForeignKey(User, on_delete = models.PROTECT)
    chat_session = models.ForeignKey(
        ChatSession, related_name='messages', on_delete = models.PROTECT
    )
    message = models.TextField(max_length=2000)

    def to_json(self):
        """desserializa a mensagem par json"""
        return {
            'user': deserialize_user(self.user), 'message':self.message
        }
class ChatSessionMember(TrackableDateModel):
    """Registra todos os usuario numa sessao"""
    chat_session = models.ForeignKey(
        ChatSession, related_name='members', on_delete = models.PROTECT
    )
    user = models.ForeignKey(User, on_delete = models.PROTECT)
