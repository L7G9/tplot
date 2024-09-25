from django.http import HttpResponseForbidden


class OwnerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().get_owner() != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )


class RolePermissionMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user_role = (
            self.get_object().get_timeline().get_role(self.request.user)
        )
        if user_role < self.required_role:
            return HttpResponseForbidden()

        return super(RolePermissionMixin, self).dispatch(
            request, *args, **kwargs
        )


class RoleContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timeline = self.get_object().get_timeline()
        user = self.request.user
        context["user_role"] = timeline.get_role(user)
        return context
