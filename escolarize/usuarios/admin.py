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

class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ['nome']  # Remova 'created_at' e 'updated_at' se não existirem no modelo
    readonly_fields = []     # Remova 'created_at' e 'updated_at' se não existirem no modelo
    list_filter = []         # Remova 'created_at' e 'updated_at' se não existirem no modelo


# Registra o CustomUserAdmin
admin.site.register(Usuario, CustomUserAdmin)
admin.site.unregister(Usuario)


from django.contrib import admin
from .models import Aluno, PaiMae

admin.site.register(Aluno)
admin.site.register(PaiMae)
