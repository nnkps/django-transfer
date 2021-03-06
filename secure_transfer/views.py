from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from django.views.generic.edit import CreateView, FormView

from .forms import ProtectedWithPasswordForm
from .models import ProtectedFile, ProtectedUrl, ProtectedItem


class ProtectedItemCreateView(LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        item = form.save(commit=False)
        password = item.create_random_password()
        item.owner = self.request.user
        item.save()
        return self.render_to_response(
            self.get_context_data(password=password, item=item)
        )


class ProtectedFileCreateView(ProtectedItemCreateView):
    model = ProtectedFile
    fields = ["uploaded_file"]


class ProtectedUrlCreateView(ProtectedItemCreateView):
    model = ProtectedUrl
    fields = ["url"]


class ProtectedFormView(FormView):
    template_name = "secure_transfer/protectedfile_form.html"
    form_class = ProtectedWithPasswordForm

    def get_initial(self):
        initial = super().get_initial()
        initial["token"] = self.request.resolver_match.kwargs.get("token")
        return initial

    def form_valid(self, form):
        item = form.item
        item.count_correct_redirect()
        item.save()
        return item.get_response()
