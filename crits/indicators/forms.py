from django.conf import settings
from django import forms
from django.forms.widgets import RadioSelect

from crits.campaigns.campaign import Campaign
from crits.core import form_consts
from crits.core.forms import add_bucketlist_to_form, add_ticket_to_form
from crits.core.widgets import CalWidget, ExtendedChoiceField
from crits.core.handlers import get_source_names, get_item_names, get_object_types
from crits.core.user_tools import get_user_organization
from crits.indicators.indicator import IndicatorAction

class IndicatorActionsForm(forms.Form):
    """
    Django form for adding actions.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    action_type = forms.ChoiceField(widget=forms.Select, required=True)
    begin_date = forms.DateTimeField(
        widget=CalWidget(format='%Y-%m-%d %H:%M:%S',
                         attrs={'class': 'datetimeclass',
                                'size': '25',
                                'id': 'id_action_begin_date'}),
        input_formats=settings.PY_FORM_DATETIME_FORMATS,
        required=False)
    end_date = forms.DateTimeField(
        widget=CalWidget(format='%Y-%m-%d %H:%M:%S',
                         attrs={'class': 'datetimeclass',
                                'size': '25',
                                'id': 'id_action_end_date'}),
        input_formats=settings.PY_FORM_DATETIME_FORMATS,
        required=False)
    performed_date = forms.DateTimeField(
        widget=CalWidget(format='%Y-%m-%d %H:%M:%S',
                         attrs={'class': 'datetimeclass',
                                'size': '25',
                                'id': 'id_action_performed_date'}),
        input_formats=settings.PY_FORM_DATETIME_FORMATS,
        required=False)
    active = forms.ChoiceField(
        widget=RadioSelect,
        choices=(('on', 'on'),
                 ('off', 'off')))
    reason = forms.CharField(
        widget=forms.TextInput(attrs={'size': '50'}),
        required=False)
    date = forms.CharField(
        widget=forms.HiddenInput(attrs={'size': '50',
                                        'readonly': 'readonly',
                                        'id': 'id_action_date'}))

    def __init__(self, *args, **kwargs):
        super(IndicatorActionsForm, self).__init__(*args, **kwargs)
        self.fields['action_type'].choices = [
            (c.name, c.name) for c in get_item_names(IndicatorAction, True)]

class IndicatorActivityForm(forms.Form):
    """
    Django form for adding activity.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    description = forms.CharField(
        widget=forms.TextInput(attrs={'size': '50'}),
        required=False)
    start_date = forms.DateTimeField(
        widget=CalWidget(format='%Y-%m-%d %H:%M:%S',
                         attrs={'class': 'datetimeclass',
                                'size': '25',
                                'id': 'id_activity_start_date'}),
        input_formats=settings.PY_FORM_DATETIME_FORMATS,
        required=False)
    end_date = forms.DateTimeField(
        widget=CalWidget(format='%Y-%m-%d %H:%M:%S',
                         attrs={'class': 'datetimeclass',
                                'size': '25',
                                'id': 'id_activity_end_date'}),
        input_formats=settings.PY_FORM_DATETIME_FORMATS,
        required=False)
    date = forms.CharField(
        widget=forms.HiddenInput(attrs={'size': '50',
                                        'readonly': 'readonly',
                                        'id': 'id_activity_date'}))

class UploadIndicatorCSVForm(forms.Form):
    """
    Django form for uploading Indicators via a CSV file.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    filedata = forms.FileField()
    source = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'no_clear'}),
        label=form_consts.Indicator.SOURCE,
        required=True)
    method = forms.CharField(
        widget=forms.TextInput,
        label=form_consts.Indicator.SOURCE_METHOD,
        required=False)
    reference = forms.CharField(
        widget=forms.TextInput(attrs={'size': '90'}),
        label=form_consts.Indicator.SOURCE_REFERENCE,
        required=False)

    def __init__(self, username, *args, **kwargs):
        super(UploadIndicatorCSVForm, self).__init__(*args, **kwargs)
        self.fields['source'].choices = [
            (c.name, c.name) for c in get_source_names(True, True, username)]
        self.fields['source'].initial = get_user_organization(username)

class UploadIndicatorTextForm(forms.Form):
    """
    Django form for uploading Indicators via a CSV blob.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    source = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'no_clear'}),
        label=form_consts.Indicator.SOURCE,
        required=True)
    method = forms.CharField(
        widget=forms.TextInput,
        label=form_consts.Indicator.SOURCE_METHOD,
        required=False)
    reference = forms.CharField(
        widget=forms.TextInput(attrs={'size': '90'}),
        label=form_consts.Indicator.SOURCE_REFERENCE,
        required=False)
    data = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '80', 'rows': '20'}),
        required=True)
    def __init__(self, username, *args, **kwargs):
        super(UploadIndicatorTextForm, self).__init__(*args, **kwargs)
        self.fields['source'].choices = [
            (c.name, c.name) for c in get_source_names(True, True, username)]
        self.fields['source'].initial = get_user_organization(username)
        dt = "Indicator, Type, Campaign, Campaign Confidence, Confidence, Impact, Bucket List, Ticket, Action\n"
        self.fields['data'].initial = dt

class UploadIndicatorForm(forms.Form):
    """
    Django form for uploading a single Indicator.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    indicator_type = ExtendedChoiceField(required=True)
    value = forms.CharField(
        widget=forms.TextInput(attrs={'size': '100'}),
        required=True)
    confidence = forms.ChoiceField(widget=forms.Select, required=True)
    impact = forms.ChoiceField(widget=forms.Select, required=True)
    campaign = forms.ChoiceField(widget=forms.Select, required=True)
    campaign_confidence = forms.ChoiceField(widget=forms.Select, required=True)
    source = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'no_clear'}),
        label=form_consts.Indicator.SOURCE,
        required=True)
    method = forms.CharField(
        widget=forms.TextInput,
        label=form_consts.Indicator.SOURCE_METHOD,
        required=False)
    reference = forms.CharField(
        widget=forms.TextInput(attrs={'size': '90'}),
        label=form_consts.Indicator.SOURCE_REFERENCE,
        required=False)

    def __init__(self, username, choices=None, *args, **kwargs):
        super(UploadIndicatorForm, self).__init__(*args, **kwargs)
        self.fields['source'].choices = [
            (c.name, c.name) for c in get_source_names(True, True, username)]
        self.fields['source'].initial = get_user_organization(username)
        if not choices:
            #only valid types for indicators are those which don't require file upload
            choices = [
                (c[0], c[0], {'datatype': c[1].keys()[0],
                              'datatype_value': c[1].values()[0]})
                for c in get_object_types(active=True, query={'datatype.file': {'$exists': 0},
                                                              'datatype.enum': {'$exists': 0}})]

        self.fields['indicator_type'].choices = choices
        self.fields['indicator_type'].widget.attrs = {'class': 'object-types'}
        self.fields['campaign'].choices = [("", "")]
        self.fields['campaign'].choices += [
            (c.name, c.name) for c in get_item_names(Campaign, True)]
        self.fields['campaign_confidence'].choices = [
            ("", ""),
            ("low", "low"),
            ("medium", "medium"),
            ("high", "high")]
        self.fields['confidence'].choices = [
            ("unknown", "unknown"),
            ("benign", "benign"),
            ("low", "low"),
            ("medium", "medium"),
            ("high", "high")]
        self.fields['impact'].choices = [
            ("unknown", "unknown"),
            ("benign", "benign"),
            ("low", "low"),
            ("medium", "medium"),
            ("high", "high")]

        add_bucketlist_to_form(self)
        add_ticket_to_form(self)

class NewIndicatorActionForm(forms.Form):
    """
    Django form for adding a new Indicator Action.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    action = forms.CharField(widget=forms.TextInput, required=True)
