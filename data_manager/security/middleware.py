import logging
from django.core.cache import cache
from django.http import HttpResponse
from .models import BlockedIP

logger = logging.getLogger(__name__)

class IPBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener IP del cliente
        client_ip = self.get_client_ip(request)
        
        # Verificar si la IP está en caché de bloqueados
        if cache.get(f'blocked_ip:{client_ip}'):
            logger.warning(f"Acceso bloqueado: IP {client_ip} está en la lista de bloqueo")
            return HttpResponse('Your IP has been blocked due to suspicious activity', status=403)
            
        # Verificar si la IP está en la base de datos de bloqueados
        is_blocked = BlockedIP.objects.filter(ip_address=client_ip).exists()
        if is_blocked:
            # Almacenar en caché para futuras verificaciones rápidas
            cache.set(f'blocked_ip:{client_ip}', True, timeout=3600)  # 1 hora
            logger.warning(f"Acceso bloqueado: IP {client_ip} está en la base de datos de bloqueados")
            return HttpResponse('Your IP has been blocked due to suspicious activity', status=403)
            
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip