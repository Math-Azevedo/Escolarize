from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Responsavel, Usuario

User = get_user_model()

# Configuração inline para Responsável
class ResponsavelInline(admin.StackedInline):
    model = Responsavel
    can_delete = False
    verbose_name_plural = 'Responsável'
    fk_name = 'user'

# Estende o UserAdmin padrão do Django
class CustomUserAdmin(UserAdmin):
    inlines = (ResponsavelInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_responsavel_info')
    list_select_related = ('responsavel', )
    
    def get_responsavel_info(self, obj):
        try:
            return f"CPF: {obj.responsavel.cpf} - Tel: {obj.responsavel.telefone}"
        except Responsavel.DoesNotExist:
            return "Não é responsável"
    get_responsavel_info.short_description = 'Informações do Responsável'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Configuração do modelo Responsável
@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('get_nome_completo', 'cpf', 'telefone', 'endereco', 'sexo', 'created_at')
    list_filter = ('sexo', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'cpf', 'telefone', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': (('user',),)
        }),
        ('Informações Pessoais', {
            'fields': (
                'cpf',
                'telefone',
                'data_nascimento',
                'sexo',
                'endereco',
            )
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_nome_completo(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_nome_completo.short_description = 'Nome Completo'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

# Registra o CustomUserAdmin
admin.site.register(Usuario, CustomUserAdmin)
admin.site.unregister(Usuario)
