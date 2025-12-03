from django.utils.deprecation import MiddlewareMixin

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        bank_id = request.headers.get("X-Bank-Id")
        request.tenant_id = bank_id