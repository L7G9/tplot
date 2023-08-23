from django.http import HttpResponseForbidden


class OwnerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().get_owner() != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )
