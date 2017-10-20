from PIL import Image
from datetime import datetime

from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from hashtags.models import HashTag
from social_parsing.models import Network
from user_account.models import SimpleUsers


class HashtagAddingForm(ModelForm):

    def clean_user(self):
        data_tag = self.cleaned_data['user']

        if not User.objects.filter(id=data_tag.id).exists():
            raise ValidationError(_('Such user does not exist.'))

        return data_tag

    def clean_tag(self):
        data_tag = self.cleaned_data['tag']

        if data_tag is None or len(data_tag) > 40:
            raise ValidationError(_('Invalid line length - line is too long or has nothing in it.'))
        try:
            check_tag = HashTag.objects.get(user=self.user, tag=data_tag)
        except (ObjectDoesNotExist):
            check_tag = list()

        if not check_tag:
            return data_tag
        else:
            raise ValidationError(_('Tag already exists.'))

    def clean_networks(self):
        data_networks = self.cleaned_data['networks']

        for network in data_networks:
            if not Network.objects.filter(guid=network).exists():
                raise ValidationError(_('Such social network is not registred. Please, contact administrator.'))

        return data_networks

    class Meta:
        model = HashTag
        fields = ['tag', 'networks', 'user']
        widgets = {'user': forms.HiddenInput()}
        labels = {'tag': _('Tag text'), 'network_id': _('Choose social network '), }
        help_texts = {'tag': _('Enter a text for the tag.'),
                      'networks': _('Choose social network, where you want to control tags.'), }

    def __init__(self, *args, **kwargs):
        try:
            self.user = args[0].get('user')
        except (IndexError):
            pass
        super(HashtagAddingForm, self).__init__(*args, **kwargs)
        self.fields['networks'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                           choices=[(network.guid, network) for network in Network.objects.all()], )
        self.fields['networks'].required = False


class HashtagEditingForm(ModelForm):
    def clean_tag(self):
        data_tag = self.cleaned_data['tag']

        if data_tag is None or len(data_tag) > 40:
            raise ValidationError(_('Invalid line length - line is too long or has nothing in it.'))

        return data_tag

    def clean_network(self):
        data_networks = self.cleaned_data['networks']

        for network in data_networks:
            if not Network.objects.filter(guid=network).exists():
                raise ValidationError(_('Such social network is not registred. Please, contact administrator.'))

        return data_networks

    class Meta:
        model = HashTag
        fields = ['tag', 'networks']
        labels = {'tag': _('Tag text'), 'network_id': _('Choose social networks'), }
        help_texts = {'tag': _('Enter a text for the tag.'),
                      'network': _('Choose social networks, where you want to control tags.'), }

    def __init__(self, *args, **kwargs):
        super(HashtagEditingForm, self).__init__(*args, **kwargs)
        self.fields['networks'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                           choices=[(network.guid, network) for network in Network.objects.all()], )
        self.fields['networks'].required = False


class UserEditForm(ModelForm):
    def clean_avatar(self):
        image = self.cleaned_data['avatar']

        if image:
            img = Image.open(image)
            w, h = img.size

            max_width = 380
            max_height = 500
            if w > max_width or h > max_height:
                raise ValidationError(
                    _('Please use an image that is smaller or equal to '
                      '{} x {} pixels.'.format(max_width, max_height)))

            main = img.format
            if not main.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']:
                raise ValidationError(_('Please use a JPEG or PNG image.'))

        return image

    def clean_bio(self):
        bio = self.cleaned_data['bio']

        if bio and len(bio) > 400:
            raise ValidationError(_('Too many symbols. Please make your bio shorter.'))

        return bio

    def clean_company(self):
        company = self.cleaned_data['company']

        if company and len(company) > 50:
            raise ValidationError(_('Too many symbols. Please make name of your company shorter.'))

        return company

    def clean_birthdate(self):
        birth_date = get_date_from_parameter(self.cleaned_data['birth_date'])

        if type(birth_date) != datetime:
            raise ValidationError(_('Invalid data for birthday date.'))

        return birth_date

    class Meta:
        model = SimpleUsers
        exclude = ['user']
        fields = ['avatar', 'bio', 'country_name', 'company', 'birth_date']
        labels = {'avatar': _('Image'),
                  'bio': ('Some words about you'),
                  'country_name': ('Country you live in'),
                  'company': ('Your company'),
                  'birth_date': ('Your birthday'), }
        help_texts = {'avatar': _('Choose an image: JPG, JPEG or PNG images are allowed.\
                                   Maximum size: 380x500 pixels. '), }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget = forms.FileInput()
        self.fields['birth_date'].widget.format = '%m/%d/%Y'
        self.fields['birth_date'].input_formats = ['%m/%d/%Y']


def get_date_from_parameter(raw_data_value):
    month, day, year = raw_data_value.split('/')
    return datetime(int(year), int(month), int(day))
