import logging
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from .models import BlockedIP

logger = logging.getLogger(__name__)

class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Obtener credenciales de la solicitud
        username = request.headers.get('X-Username')
        api_key = request.headers.get('X-API-Key')
        
        if not username or not api_key:
            return None

        if username != 'valid_user' or api_key != 'valid_api_key':
            # Credenciales inválidas - bloquear IP
            client_ip = self.get_client_ip(request)
            self.block_ip(client_ip, "Intento de acceso con credenciales inválidas")
            logger.warning(f"Intento de acceso no autorizado: IP {client_ip} bloqueada")
            raise exceptions.AuthenticationFailed('Invalid credentials')
            

        return (username, None)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def block_ip(self, ip_address, reason):
        # Bloquear en base de datos
        block_expires = timezone.now() + timezone.timedelta(seconds=settings.IP_BLOCK_DURATION)
        BlockedIP.objects.update_or_create(
            ip_address=ip_address,
            defaults={
                'reason': reason,
                'block_expires': block_expires
            }
        )
        
        # Bloquear en caché para respuesta rápida
        cache.set(f'blocked_ip:{ip_address}', True, timeout=settings.IP_BLOCK_DURATION)