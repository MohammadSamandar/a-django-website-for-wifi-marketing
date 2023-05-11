from celery.worker.state import requests
from django.urls import reverse_lazy, reverse
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from surveys.models import Survey, UserAnswer
from surveys.forms import CreateSurveyForm, EditSurveyForm
from surveys.mixin import ContextTitleMixin
from surveys import app_settings
from surveys.utils import NewPaginator





class SurveyFormView(FormMixin, DetailView):
    template_name = 'surveys/form.html'
    # success_url = reverse_lazy("surveys:detail_result")

    def get_success_url(self):
        survey = Survey()
        answer = UserAnswer.objects.filter(survey=survey, user=self.request.user.id).first()

        # return reverse_lazy("surveys:detail_result", pk=answer.id)
        return reverse_lazy("surveys:DetailSurveyView", kwargs={'pk': answer.id})


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            form.save()
            messages.success(self.request, gettext("%(page_action_name)s succeeded.") % dict(page_action_name=capfirst(self.title_page.lower())))
            return self.form_valid(form)
        else:
            messages.error(self.request, gettext("متاسفانه مشکلی رخ داده است."))
            return self.form_invalid(form)

# صفحه سوال نظر سنجی
class CreateSurveyFormView(ContextTitleMixin, SurveyFormView):

    def get_success_url(self):
        # survey = self.get_object()
        answer = UserAnswer.objects.filter( user=self.request.user.id).first()

        # return reverse_lazy("surveys:detail_result", pk=answer.id)
        return reverse_lazy("surveys:detail_result", kwargs={'pk': answer.id})

    model = Survey
    form_class = CreateSurveyForm
    title_page = _("Add Survey")

    # def dispatch(self, request, *args, **kwargs):
    #     survey = self.get_object()
    #     # handle if survey can_anonymous_user
    #     if not request.user.is_authenticated and not survey.can_anonymous_user:
    #         messages.warning(request, gettext("ابتدا وارد حساب کاربری خود شوید"))
    #         return redirect("login_page")
    #
    #     # handle if user have answer survey
    #     if request.user.is_authenticated and not survey.duplicate_entry and \
    #             UserAnswer.objects.filter(survey=survey, user=request.user).exists():
    #         messages.warning(request, gettext("جواب شما در این نظرسنجی ثبت شد"))
    #         return redirect("surveys:detail_result", pk=UserAnswer.pk)
    #     return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(survey=self.get_object(), user=self.request.user, **self.get_form_kwargs())

    def get_title_page(self):
        return self.get_object().name

    def get_sub_title_page(self):
        return self.get_object().description


# ویرایش یا اصلاح امتیازی که کاربر وارد کرده توسط خودش
class EditSurveyFormView(ContextTitleMixin, SurveyFormView):
    form_class = EditSurveyForm
    title_page = "Edit Survey"
    model = UserAnswer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object().survey
        return context

    # def dispatch(self, request, *args, **kwargs):
    #     # handle if user not same
    #     user_answer = self.get_object()
    #     if user_answer.user != request.user or not user_answer.survey.editable:
    #         messages.warning(request, gettext("شما مجوز لازم برای ویرایش این نظرسنجی را ندارید"))
    #         return redirect("surveys:index")
    #     return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        user_answer = self.get_object()
        return form_class(user_answer=user_answer, **self.get_form_kwargs())

    def get_title_page(self):
        return self.get_object().survey.name

    def get_sub_title_page(self):
        return self.get_object().survey.description

# حذف جواب های سوالات نظر سنجی
class DeleteSurveyAnswerView(DetailView):
    model = UserAnswer

    def dispatch(self, request, *args, **kwargs):
        # handle if user not same
        user_answer = self.get_object()
        if user_answer.user != request.user or not user_answer.survey.deletable:
            messages.warning(request, gettext("شما مجوز لازم برای حذف جواب این نظرسنجی را ندارید"))
            return redirect("surveys:DetailSurveyView" ,slug=user_answer.survey.slug)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_answer = self.get_object()
        user_answer.delete()
        messages.success(self.request, gettext("جواب با موفقیت حذف شد."))
        return redirect("surveys:DetailSurveyView" ,slug=user_answer.survey.slug)



# نمایش نتیجه جوابی که کاربر به سوال نظر سنجی داده
class DetailResultSurveyView(ContextTitleMixin, DetailView):
    title_page = _("Survey Result")
    template_name = "surveys/detail_result.html"
    model = UserAnswer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['on_detail'] = True
        return context

    # def dispatch(self, request, *args, **kwargs):
    #     # handle if user not same
    #     user_answer = self.get_object()
    #     if user_answer.user != request.user:
    #         messages.warning(request, gettext("شما مجوز لازم برای دسترسی به این صفحه را ندارید."))
    #
    #         slug = user_answer.survey.slug
    #         return redirect("surveys:create", slug=slug)
    #     return super().dispatch(request, *args, **kwargs)

    def get_title_page(self):
        return self.get_object().survey.name

    def get_sub_title_page(self):
        return self.get_object().survey.description

# اشتراک گذاری لینک نظر سنجی
def share_link(request, slug):
    # this func to handle link redirect to create form or edit form
    survey = get_object_or_404(Survey, slug=slug)
    if request.user.is_authenticated:
        user_answer = UserAnswer.objects.filter(survey=survey, user=request.user).last()
        if user_answer:
            return redirect(reverse_lazy("surveys:edit", kwargs={'pk': user_answer.id}))
    return redirect(reverse_lazy("surveys:create", kwargs={'slug': survey.slug}))
