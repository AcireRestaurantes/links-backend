import random
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    SEXO_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Seu Nome Profissional")
    image = models.ImageField(upload_to='profiles/', default='profiles/default.jpg')
    is_free_user = models.BooleanField(default=True)
    theme = models.CharField(max_length=100, default='theme-default')
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, default='masculino')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Verifica se o objeto já existe no banco de dados
        if not self.pk:  # Somente se o objeto for novo
            if self.sexo == 'masculino':
                # Lista de imagens masculinas
                imagens_masculinas = [
                    "profiles/perfil-masculino-01.png",
                    "profiles/perfil-masculino-02.png",
                    "profiles/perfil-masculino-03.png",
                    "profiles/perfil-masculino-04.png",
                    "profiles/perfil-masculino-05.png",
                ]
                self.image = random.choice(imagens_masculinas)  # Seleciona uma imagem aleatória
            elif self.sexo == 'feminino':
                # Lista de imagens femininas
                imagens_femininas = [
                    "profiles/perfil-feminino-01.png",
                    "profiles/perfil-feminino-02.png",
                    "profiles/perfil-feminino-03.png",
                ]
                self.image = random.choice(imagens_femininas)  # Seleciona uma imagem aleatória

        super().save(*args, **kwargs)  # Chama o método save da classe pai
