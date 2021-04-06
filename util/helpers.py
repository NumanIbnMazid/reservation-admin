from decouple import config, Csv
import psycopg2
# import boto3
import re
from django import forms
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from middlewares.middlewares import RequestMiddleware

"""
************************ Databse Helper Functions ************************
"""


def connect_db():
    """
    connect_db() => Connects to AWS RDS and returns connection instance.
    """
    try:
        con = psycopg2.connect(
            database=config('RDS_DB_NAME'),
            host=config('RDS_HOSTNAME'),
            port=config('RDS_PORT'),
            user=config('RDS_USERNAME'),
            password=config('RDS_PASSWORD'),
        )

        # return connection instance
        return con

    except Exception as E:
        raise Exception(
            "Django Failed to create db connection!"
        )


"""
************************ Get Dynamic Fields Helper Functions ************************
"""

def get_dynamic_fields(field=None, self=None):
    """
    get_dynamic_fields() => Helper function to get dynamic fields.
    params => field (string), self (instance)
    return => (field.name, value)
    """
    if field.name == 'x':
        return (field.name, self.x.title)
    else:
        value = "-"
        if not field.value_from_object(self) == None and not field.value_from_object(self) == "":
            value = field.value_from_object(self)
        return (field.name, value)


"""
************************ Validate Form Helper Functions ************************
"""


def validate_normal_form(field, field_qs, form, request):
    """
    validate_normal_form() => Validates form.
    params => field, field_qs, form, request
    return => int (0 or 1)
    """
    if not field_qs == None:
        if field_qs.exists():
            form.add_error(
                field, forms.ValidationError(
                    f"This {field} is already exists! Please try another one."
                )
            )
            return 0
    if 'update' in request.path or 'edit' in request.path:
        dynamic_msg = "Updated Successfully !!!"
    elif 'create' in request.path or 'add' in request.path:
        dynamic_msg = "Created Successfully !!!"
    else:
        dynamic_msg = "Manipulated Successfully !!!"
    messages.add_message(
        request, messages.SUCCESS,
        dynamic_msg
    )
    return 1


"""
************************ Retrieve Object Helper Functions ************************
"""

def get_simple_object(key='slug', model=None, self=None):
    """
    get_simple_object() => Retrieve object instance.
    params => key, model, self
    return => object (instane)
    """
    try:
        if key == 'id':
            id = self.kwargs['id']
            instance = model.objects.get(id=id)
        else:
            slug = self.kwargs['slug']
            instance = model.objects.get(slug=slug)
    except model.DoesNotExist:
        raise Http404('Not found!!!')
    except model.MultipleObjectsReturned:
        if key == 'id':
            id = self.kwargs['id']
            instance = model.objects.filter(id=id).first()
        else:
            slug = self.kwargs['slug']
            instance = model.objects.filter(slug=slug).first()
    except:
        raise Http404("Something went wrong !!!")
    return instance


"""
************************ Delete Object Helper Functions ************************
"""


def delete_simple_object(request, key, model, redirect_url):
    """
    delete_simple_object() => Deletes an object.
    params => request, key, model
    return => HttpResponseRedirect(url)
    """
    url = reverse('home')
    # user = request.user
    if request.method == "POST":
        if key == 'id':
            id = request.POST.get("id")
            qs = model.objects.filter(id=id)
        else:
            slug = request.POST.get("slug")
            qs = model.objects.filter(slug=slug)
        if qs.exists():
            # if qs.first().user == user.profile:
            qs.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "Deleted successfully!")
            if redirect_url is not None:
                url = reverse(redirect_url)
            else:
                url = request.META.get('HTTP_REFERER', '/')
        else:
            messages.add_message(request, messages.WARNING,
                                 "Not found!")
    return HttpResponseRedirect(url)


"""
************************ Context Data Helper Functions ************************
"""

def simple_context_data(context, model, page_title=None, update_url=None, delete_url=None, namespace=None, list_template=None):
    """
    simple_context_data() => Generates context data.
    params => context, model, page_title, update_url, delete_url, namespace, list_template
    return => context
    """
    context['page_title'] = page_title
    context['list_objects'] = model.objects.all()
    context['list_template'] = list_template
    context['fields_count'] = len(model._meta.get_fields()) - 1
    context['fields'] = dict([(f.name, f.verbose_name)
                              for f in model._meta.fields + model._meta.many_to_many])
    context['update_url'] = update_url
    context['delete_url'] = delete_url
    context['namespace'] = namespace
    return context


"""
************************ Character Validate Helper Functions ************************
"""

def validate_chars(field_data, allowed_chars=None, max_length=50):
    """
    validate_chars() => Validates character field.
    params => field_data, allowed_chars, max_length
    return => field_data
    """
    if not field_data == None:
        pattern = allowed_chars
        characters_to_remove = '^[]+$'
        for character in characters_to_remove:
            pattern = pattern.replace(character, "")
        if not allowed_chars == None:
            allowed_chars = re.match(allowed_chars, field_data)
            if not allowed_chars:
                raise forms.ValidationError(
                    f"Only [{pattern}] these characters are allowed!"
                )
        length = len(field_data)
        if length > max_length:
            raise forms.ValidationError(
                f"Maximum {max_length} characters allowed. Currently using {length}!"
            )
    return field_data



"""
************************ Form Widget Helper Functions ************************
"""


def simple_form_widget(self=None, field=None, maxlength=50, step=None, pattern=None, placeholder=None):
    """
    simple_form_widget() => Generates form widget.
    params => self, field, maxlength, step, pattern, placeholder
    """
    field_name = ' '.join(field.split('_')).title()
    allowed_chars = pattern
    print(pattern)
    if not pattern == None:
        characters_to_remove = '^[]{1,}$'
        for character in characters_to_remove:
            allowed_chars = allowed_chars.replace(character, "")
    if not placeholder == None:
        placeholder = placeholder
    else:
        placeholder = f'Enter {field_name}...'
    self.fields[field].widget.attrs.update({
        'id': f'{field}_id',
        'placeholder': placeholder,
        'maxlength': maxlength,
        'step': step,
        'pattern': pattern
    })
    if not pattern == None:
        self.fields[field].help_text = f"Only [{allowed_chars}] these characters are allowed."


"""
************************ Dynamic Field Helper Functions ************************
"""

def get_dynamic_fields(field=None, self=None):
    """
    get_dynamic_fields() => Gets model fields dynamically.
    params => field, self
    return => (field.name, value)
    """
    if field.name == 'x':
        return (field.name, self.x.title)
    else:
        value = "-"
        if not field.value_from_object(self) == None and not field.value_from_object(self) == "":
            value = field.value_from_object(self)
        return (field.name, value)


"""
************************ User Permission Checker Helper Functions ************************
"""


def user_has_permission(permission=None):
    """
    user_has_permission() => Checks if user has the required permissions to access the content.
    params => permission ('app_name.can_add_log_entry') => 'app_name.permission'
    """
    request = RequestMiddleware(get_response=None)
    request = request.thread_local.current_request
    if request.user.is_superuser == True or request.user.has_perm(permission) == True:
        return True
