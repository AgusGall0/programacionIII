from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

ROLES_CON_ACCESO_AL_ADMIN = ['Administrador', 'Coordinador']

User = get_user_model()


@receiver(m2m_changed, sender=User.groups.through)
def actualizar_acceso_al_admin(sender, instance, action, reverse, pk_set, **kwargs):
    if action not in ('post_add', 'post_remove', 'post_clear') or (reverse and not pk_set):
        return
    usuarios = User.objects.filter(pk__in=pk_set) if reverse else [instance]
    for usuario in usuarios:
        es_staff = usuario.is_superuser or usuario.groups.filter(
            name__in=ROLES_CON_ACCESO_AL_ADMIN
        ).exists()
        if usuario.is_staff != es_staff:
            usuario.is_staff = es_staff
            usuario.save(update_fields=['is_staff'])
