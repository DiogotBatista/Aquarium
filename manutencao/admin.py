from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tipo_Aquario, Tipo_Manutencao, Tipo_Especime, Aquario, Manutencao, Especime, Populacao, Aviso, Notas
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'is_staff', 'is_active', 'is_superuser', 'first_name', 'last_name', 'data_cadastro', 'last_access',]
    search_fields = ('email', 'first_name', 'last_name',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),'fields': ('email', 'first_name', 'last_name', 'password1', 'password2',)}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')}),
    )
    ordering = ('email',)


@admin.register(Tipo_Aquario)
class Tipo_AquarioAdmin(admin.ModelAdmin):
    list_display = ('tipo_aquario',)

@admin.register(Tipo_Manutencao)
class Tipo_ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('tipo_manutencao',)

@admin.register(Tipo_Especime)
class Tipo_EspecimeAdmin(admin.ModelAdmin):
    list_display = ('tipo_especime',)


@admin.register(Aquario)
class AquarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'tipo', 'volume','data_cadastro', 'data_montagem', 'observacao', 'foto',)
    search_fields = ('nome', 'usuario__email', 'tipo__tipo_aquario',)

@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('aquario', 'data', 'tipo_manutencao', 'ph', 'temperatura','observacao',)
    search_fields = ('aquario__nome', 'tipo_manutencao__tipo_manutencao',)

@admin.register(Notas)
class NotasAdmin(admin.ModelAdmin):
    list_display = ('aquario', 'data', 'titulo', 'texto')
    search_fields = ('aquario__nome', 'titulo',)

@admin.register(Especime)
class EspecimeAdmin(admin.ModelAdmin):
    list_display = ('nome_popular', 'tipo_especime', 'nome_cientifico', 'observacao', 'imagem',)
    search_fields = ('nome_popular', 'tipo_especime__tipo_especime', 'nome_cientifico',)

@admin.register(Populacao)
class PopulacaoAdmin(admin.ModelAdmin):
    list_display = ('aquario', 'especime', 'quantidade', 'observacao',)
    search_fields = ('aquario__nome', 'especime__nome_popular', )


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_criacao', 'ordenacao',)
    list_filter = ('data_criacao',)


admin.site.site_header = "AQUARIUM - Administração"
admin.site.site_title = "AQUARIUM - Administração"
admin.site.index_title = "AQUARIUM - ADM"
