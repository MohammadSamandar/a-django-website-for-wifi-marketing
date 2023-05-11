import csv
from io import StringIO

from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.generic.list import ListView

from surveys import app_settings
from surveys.app_settings import SURVEYS_ADMIN_BASE_PATH
from surveys.models import Survey, Question, UserAnswer
from surveys.mixin import ContextTitleMixin
from surveys.utils import NewPaginator
from surveys.forms import BaseSurveyForm
from surveys.summary import SummaryResponse

# لیست نظرسنجی ها
# @method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SurveyListView(ContextTitleMixin, ListView):
    model = Survey
    template_name = "surveys/admins/survey_list.html"
    title_page = 'Survey List'
    paginate_by = app_settings.SURVEY_PAGINATION_NUMBER['survey_list']
    paginator_class = NewPaginator

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        page_number = self.request.GET.get('page', 1)
        context = super().get_context_data(**kwargs)
        page_range = context['page_obj'].paginator.get_elided_page_range(number=page_number)
        context['page_range'] = page_range
        return context



# لیست جواب های کاربران
# @method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DetailSurveyView(ContextTitleMixin, DetailView):
    model = Survey
    template_name = "surveys/admins/answer_list.html"
    title_page = "Survey Detail"
    paginate_by = app_settings.SURVEY_PAGINATION_NUMBER['answer_list']

    def dispatch(self, request, *args, **kwargs):
        survey = self.get_object()
        if not self.request.user.is_superuser and survey.private_response:
            messages.warning(request, gettext("You can't access this page. You don't have permission."))
            return redirect("surveys:index")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user_answers = UserAnswer.objects.filter(survey=self.get_object()) \
            .select_related('user').prefetch_related('answer_set__question')
        paginator = NewPaginator(user_answers, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        page_range = paginator.get_elided_page_range(number=page_number)
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj
        context['page_range'] = page_range
        return context





# نظرسنجی
# @method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AdminCrateSurveyView(ContextTitleMixin, CreateView):
    model = Survey
    template_name = 'surveys/admins/form.html'
    fields = [
        'name', 'description', 'duplicate_entry',
    ]
    title_page = _("Add New Survey")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            survey = form.save()
            self.success_url = reverse("surveys:admin_forms_survey", args=[survey.slug])
            messages.success(self.request, gettext("%(page_action_name)s succeeded.") % dict(page_action_name=capfirst(self.title_page.lower())))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# @method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AdminEditSurveyView(ContextTitleMixin, UpdateView):
    model = Survey
    template_name = 'surveys/admins/form.html'
    fields = [
        'name', 'description', 'editable', 'deletable', 
        'duplicate_entry', 'private_response'
    ]
    title_page = _("Edit Survey")

    def get_success_url(self):
        survey = self.get_object()
        return reverse("surveys:admin_forms_survey", args=[survey.slug])


# @method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AdminSurveyFormView(ContextTitleMixin, FormMixin, DetailView):
    model = Survey
    template_name = 'surveys/admins/form_preview.html'
    form_class = BaseSurveyForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(survey=self.object, user=self.request.user, **self.get_form_kwargs())

    def get_title_page(self):
        return self.object.name

    def get_sub_title_page(self):
        return self.object.description


# @method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AdminDeleteSurveyView(DetailView):
    model = Survey

    def get(self, request, *args, **kwargs):
        survey = self.get_object()
        survey.delete()
        messages.success(request, gettext("Survey %(name)s succesfully deleted.") % dict(name=survey.name))
        return redirect("surveys:SurveyListView")








# سوالات
@method_decorator(login_required, name='dispatch')
class AdminCreateQuestionView(ContextTitleMixin, CreateView):
    model = Question
    template_name = 'surveys/admins/question_form.html'
    success_url = reverse_lazy("surveys:")
    fields = ['label', 'key', 'type_field', 'choices', 'help_text', 'required']
    title_page = _("Add Question")
    survey = None

    def dispatch(self, request, *args, **kwargs):
        self.survey = get_object_or_404(Survey, id=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = self.survey
            question.save()
            messages.success(self.request, gettext("%(page_action_name)s succeeded.") % dict(page_action_name=capfirst(self.title_page.lower())))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("surveys:admin_forms_survey", args=[self.survey.slug])


@method_decorator(login_required, name='dispatch')
class AdminUpdateQuestionView(ContextTitleMixin, UpdateView):
    model = Question
    template_name = 'surveys/admins/question_form.html'
    success_url = SURVEYS_ADMIN_BASE_PATH
    fields = ['label', 'key', 'type_field', 'choices', 'help_text', 'required']
    title_page = _("Add Question")
    survey = None

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        self.survey = question.survey
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("surveys:admin_forms_survey", args=[self.survey.slug])


@method_decorator(login_required, name='dispatch')
class AdminDeleteQuestionView(DetailView):
    model = Question
    survey = None

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        self.survey = question.survey
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        question = self.get_object()
        question.delete()
        messages.success(request, gettext("Question %(name)s succesfully deleted.") % dict(name=question.label))
        return redirect("surveys:admin_forms_survey", slug=self.survey.slug)


@method_decorator(login_required, name='dispatch')
class AdminChangeOrderQuestionView(View):
    def post(self, request, *args, **kwargs):
        ordering = request.POST['order_question'].split(",")
        for index, question_id in enumerate(ordering):
            if question_id:
                question = Question.objects.get(id=question_id)
                question.ordering = index
                question.save()

        data = {
            'message': gettext("Update ordering of questions succeeded.")
        }
        return JsonResponse(data, status=200)













@method_decorator(login_required, name='dispatch')
class DownloadResponseSurveyView(DetailView):
    model = Survey

    def get(self, request, *args, **kwargs):
        survey = self.get_object()
        user_answers = UserAnswer.objects.filter(survey=survey)
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        rows = []
        header = []
        for index, user_answer in enumerate(user_answers):
            if index == 0:
                header.append('user')
                header.append('update_at')

            rows.append(user_answer.user.username if user_answer.user else 'no auth')
            rows.append(user_answer.updated_at.strftime("%Y-%m-%d %H:%M:%S"))
            for answer in user_answer.answer_set.all():
                if index == 0:
                    header.append(answer.question.label)
                rows.append(answer.get_value_for_csv)

            if index == 0:
                writer.writerow(header)
            writer.writerow(rows)
            rows = []

        response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
        response['Content-Disposition'] = f'attachment; filename={survey.slug}.csv'
        return response








@method_decorator(login_required, name='dispatch')
class SummaryResponseSurveyView(ContextTitleMixin, DetailView):
    model = Survey
    template_name = "surveys/admins/summary.html"
    title_page = _("Summary")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        summary = SummaryResponse(survey=self.get_object())
        context['summary'] = summary
        return context
