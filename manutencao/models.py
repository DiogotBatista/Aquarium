import os
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.deconstruct import deconstructible


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo Email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField("Nome", max_length=40)
    last_name = models.CharField('Sobrenome', max_length=40)
    data_cadastro = models.DateField('Data de cadastro', auto_now_add=True, editable=False, null=True, blank=True)
    last_access = models.DateTimeField('Último Acesso', null=True, blank=True)
    # Remova 'username' e adicione quaisquer outros campos necessários aqui

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # 'username' removido daqui

    def is_in_equipe_group(self):
        return self.groups.filter(name='equipe').exists()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email


class Tipo_Aquario(models.Model):
    tipo_aquario = models.CharField('Tipo do aquario', max_length=20, unique=True)

    class Meta:
        ordering = ['tipo_aquario']
        verbose_name = 'Tipo de Aquario'
        verbose_name_plural = 'Tipos de Aquários'

    def __str__(self):
        return self.tipo_aquario


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)


class Aquario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField('Nome do Aquario', max_length=100)
    tipo = models.ForeignKey(Tipo_Aquario, on_delete=models.PROTECT)
    volume = models.IntegerField('Volume')
    data_cadastro = models.DateField('Data de cadastro', auto_now_add=True, editable=False)
    data_montagem = models.DateField('Data da Montagem')
    observacao = models.TextField('Observação', null=True, blank=True)
    foto = models.ImageField(
        upload_to=PathAndRename('aquarios/'),
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )

    class Meta:
        verbose_name = 'Aquario'
        verbose_name_plural = 'Aquarios'

    def __str__(self):
        return self.nome

    def delete(self, *args, **kwargs):
        if self.foto:
            if os.path.isfile(self.foto.path):
                os.remove(self.foto.path)
        super(Aquario, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Aquario'
        verbose_name_plural = 'Aquarios'

    def __str__(self):
        return self.nome


class Tipo_Manutencao(models.Model):
    tipo_manutencao = models.CharField('Tipo da manutenção', max_length=50, unique=True)

    class Meta:
        ordering = ['tipo_manutencao']
        verbose_name = 'Tipo de Manutenção'
        verbose_name_plural = 'Tipos de Manutenção'

    def __str__(self):
        return self.tipo_manutencao


class Manutencao(models.Model):
    aquario = models.ForeignKey(Aquario, on_delete=models.CASCADE, related_name='manutencoes')
    data = models.DateField("Data da manutenção")
    tipo_manutencao = models.ForeignKey(Tipo_Manutencao, on_delete=models.PROTECT)
    ph = models.DecimalField('Ph', max_digits=4, decimal_places=1, null=True, blank=True)
    temperatura = models.IntegerField("Temperatura", null=True, blank=True)
    observacao = models.TextField('Observação', null=True, blank=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'

    def __str__(self):
        return f"{self.tipo_manutencao} em {self.data}"


class Tipo_Especime(models.Model):
    tipo_especime = models.CharField('Espécime', max_length=100, unique=True)

    class Meta:
        ordering = ['tipo_especime']
        verbose_name = 'Tipo de espécime'
        verbose_name_plural = 'Tipos de Espécimes'

    def __str__(self):
        return self.tipo_especime


class Especime(models.Model):
    nome_popular = models.CharField('Nome popular', max_length=100, unique=True)
    tipo_especime = models.ForeignKey(Tipo_Especime, on_delete=models.PROTECT)
    nome_cientifico = models.CharField('Nome científico', max_length=100, default='Nome Científico')
    observacao = models.TextField('Observação', null=True, blank=True)
    imagem = models.ImageField(
        upload_to=PathAndRename('especimes/'),
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )

    class Meta:
        ordering = ['nome_popular']
        verbose_name = 'Espécime'
        verbose_name_plural = 'Espécimes'

    def __str__(self):
        return self.nome_popular

    def save(self, *args, **kwargs):
        self.nome_popular = self.nome_popular.upper()  # Converte nome_popular para maiúsculas
        self.nome_cientifico = self.nome_cientifico.upper()  # Converte nome_cientifico para maiúsculas
        super(Especime, self).save(*args, **kwargs)  # Chama o método save original


class Populacao(models.Model):
    aquario = models.ForeignKey(Aquario, on_delete=models.CASCADE, related_name='populacao')
    especime = models.ForeignKey(Especime, on_delete=models.PROTECT)
    quantidade = models.IntegerField('Quantidade')
    observacao = models.TextField('Observação', null=True, blank=True)

    class Meta:
        ordering = ['especime']
        verbose_name = 'População'
        verbose_name_plural = 'Populações'

    def __str__(self):
        return f"{self.especime.nome_popular} - {self.quantidade}"


class Aviso(models.Model):
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    ordenacao = models.IntegerField('Ordenação')

    class Meta:
        ordering = ['ordenacao']

    def __str__(self):
        return self.titulo


class Notas(models.Model):
    aquario = models.ForeignKey(Aquario, on_delete=models.CASCADE, related_name='notas')
    data = models.DateField("Data da manutenção")
    titulo = models.CharField(max_length=200)
    texto = models.TextField()

    class Meta:
        ordering = ['data']
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return self.titulo
