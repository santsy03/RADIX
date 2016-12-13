import re, random, string
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.utils.crypto import get_random_string
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, AdminPasswordChangeForm
from password_policies.models import PasswordChangeRequired
from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.auth.hashers import identify_hasher
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.conf.urls import patterns
from django.template import loader
from django.shortcuts import get_object_or_404
from django.utils.http import int_to_base36

class CusPassChangeForm(AdminPasswordChangeForm):
    """
    Password change override
    """
    MIN_LENGTH = 8
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # At least MIN_LENGTH long
        if len(password2) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)
        
        return password2

    def save(self, commit=True):
        user = self.user
        super(CusPassChangeForm, self).save(commit=commit)
        if PasswordChangeRequired.objects.filter(user=user).count() == 0:
            PasswordChangeRequired.objects.create(user=user)
        else:
			PasswordChangeRequired.objects.delete(user=user)

        return user

class BetterReadOnlyPasswordHashWidget(ReadOnlyPasswordHashWidget):
    """
    A ReadOnlyPasswordHashWidget that has a less intimidating output.
    """
    def render(self, name, value, attrs):
        from django.forms.util import flatatt
        #from django.contrib.auth.hashers import UNUSABLE_PASSWORD
        from django.contrib.auth.hashers import is_password_usable
        #from django.contrib.auth.models.User import has_usable_password
        #pcheck = value != UNUSABLE_PASSWORD
        pcheck = value != is_password_usable(value)
        final_attrs = flatatt(self.build_attrs(attrs))
        if not value or not pcheck:
            summary = ugettext("No password set.")
        else:
            try:
                identify_hasher(value)
            except ValueError:
                summary = ugettext("Invalid password format or unknown"
                                   " hashing algorithm.")
            else:
                summary = ugettext('*************')

        return format_html('<div{attrs}><strong>{summary}</strong></div>',
                           attrs=final_attrs, summary=summary)

class CustomUserCreationForm(UserCreationForm):
    """
    A UserCreationForm with optional password inputs.
    """
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.MIN_LENGTH = 8
        self.MIN_UNAME = 5
        self.username = ''
        self.email = ''
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'
        self.fields['password1'].widget.attrs['readonly'] = 'readonly'
        self.fields['password2'].widget.attrs['readonly'] = 'readonly'

    def clean_email(self):
        #Clean email address
        email = self.cleaned_data["email"]

        #Check if email is valid
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            raise forms.ValidationError("Enter a valid email address.")

        #Check if email address has been used
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError("This email address has already been used.")
       
        self.email = email 
        return email

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]

        # At least MIN_LENGTH long
        if len(username) < self.MIN_UNAME:
            raise forms.ValidationError("Username must be at least %d characters long." % self.MIN_UNAME)

        self.username = username
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        #password2 = super(UserCreationForm, self).clean_password2()
        password2 = self.cleaned_data.get("password2")
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        elif password1 and password2:
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords do not match")

            # At least MIN_LENGTH long
            if len(password2) < self.MIN_LENGTH:
                raise forms.ValidationError("The password must be at least %d characters long." % self.MIN_LENGTH)

            # At least one letter and one non-letter
            first_isalpha = password2[0].isalpha()
            if all(c.isalpha() == first_isalpha for c in password2):
                raise forms.ValidationError("The password must contain at least one letter and at least one digit.")

            # Mixed lower and upper case
            if password2.islower() or password2.isupper():
                raise forms.ValidationError("The password must contain both upper and lower cases.")

            # At least contain special characters
            if re.match("^[A-Za-z0-9_-]*$", password2 ):
                raise forms.ValidationError("The password must contain special characters.")

            #Check has no number
            if any(char.isdigit() for char in password2) == False:
                raise forms.ValidationError("The new password must contain at least one Number.")

            # No character from username in password
            cur_uname = str(self.username)
            uname = list(cur_uname.lower())
            wds, cnt, pwd_allowed = len(uname), 0, True
            for word in uname:
                pos = wds-cnt
                if pos > 3:
                    uparts = cur_uname[cnt:][:3]
                    if uparts in password2.lower():
                        pwd_allowed = False
                cnt += 1
            if pwd_allowed == False:
                raise forms.ValidationError("The password can not contain part of your username.")
        return password2

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    MIN_LENGTH = 8
    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        password = ReadOnlyPasswordHashField(label=_("Password"),
        widget=BetterReadOnlyPasswordHashWidget,
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))
        self.fields['password'] = password

class UserAdmin(UserAdmin):
    """
    A UserAdmin that sends a password-reset email when creating a new user,
    unless a password was entered.
    """
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'description': (
                "Enter the new user's name and email address and click save."
                " The user will be emailed a link allowing them to login to"
                " the site and set their password."
            ),
            'fields': ('email', 'username',),
        }),
        ('Password', {
            'description': "Optionally, you may set the user's password here if enabled.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )
    def save_model(self, request, obj, form, change):
        print 'DEBUG', obj, change
        if not change and not obj.has_usable_password():
            # Django's PasswordResetForm won't let us reset an unusable
            # password. We set it above super() so we don't have to save twice.
            chars = string.ascii_letters + string.digits + '!#$%&*()'
            new_password = ''.join(random.choice(chars) for i in range(10))
            obj.set_password( new_password )
            reset_password = True
        else:
            reset_password = False

        super(UserAdmin, self).save_model(request, obj, form, change)

        if not PasswordChangeRequired.objects.filter(user=obj).count():
            PasswordChangeRequired.objects.create(user=obj)

        if reset_password:
            from django.core.mail import send_mail
            gui_address = settings.GUI_ADDRESS
            subject_template_name = 'registration/account_creation_subject.txt'
            email_template_name = 'registration/account_creation_email.html'
            c = {
                'username': obj.username,
                'user_password': new_password,
                'gui_address': gui_address,
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, None, [obj.email]) 

    def reset_password(self, request, user_id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.model, pk=user_id)
        my_data = {'email': user.email,
                   'uid': int_to_base36(int(user_id))}
        form = PasswordResetForm(data=my_data)
        form.is_valid()

        form.save(email_template_name='registration/password_reset_email.html')
        return HttpResponseRedirect('..')

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()

        my_urls = patterns('',
            (r'^(\d+)/reset-password/$',
              self.admin_site.admin_view(self.reset_password)
            ),
        )
        return my_urls + urls

#admin.site.unregister(Site)
User = get_user_model()
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
