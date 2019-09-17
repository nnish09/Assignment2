from django import forms
from studentteacher.models import User,Assignment,AssignRequest,Submission,Review
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.files.images import get_image_dimensions
from django.template.defaultfilters import filesizeformat
from datetime import datetime,timedelta   



class SignUpForm(forms.ModelForm):
    USER_TYPE_CHOICES = (
      (1, 'student'),
      (2, 'teacher'),
    )
    username = forms.CharField(max_length=254)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254,required=True)
    role=forms.ChoiceField(widget=forms.Select(), choices =USER_TYPE_CHOICES)
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','role', 'phone_no', 'email')
        

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     # username = self.cleaned_data.get('username')
    #     if email and User.objects.filter(email=email).count() > 0:
    #         raise forms.ValidationError('This email address is already registered.')
    #     return email

    # def clean_phone_no(self):
    #     phone_no = self.cleaned_data.get('phone_no')
    #     # username = self.cleaned_data.get('username')
    #     if phone_no and User.objects.filter(phone_no=phone_no).count() > 0:
    #         raise forms.ValidationError('This phone number is already registered.')
    #     return phone_no





class SignUpForm1(forms.ModelForm):
    USER_TYPE_CHOICE = (
      (1, 'student'),
      
    )
    username = forms.CharField(max_length=254)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254,required=True)
    role=forms.ChoiceField(widget=forms.Select(), choices =USER_TYPE_CHOICE)
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','role','email')
        

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     # username = self.cleaned_data.get('username')
    #     if email and User.objects.filter(email=email).count() > 0:
    #         raise forms.ValidationError('This email address is already registered.')
    #     return email

    # def clean_phone_no(self):
    #     phone_no = self.cleaned_data.get('phone_no')
    #     # username = self.cleaned_data.get('username')
    #     if phone_no and User.objects.filter(phone_no=phone_no).count() > 0:
    #         raise forms.ValidationError('This phone number is already registered.')
    #     return phone_no










class SetPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
  
   
    class Meta:
        model = User
        fields = ('password', 'confirm_password')
        
    
    def clean(self):
        cleaned_data = super(SetPasswordForm, self).clean()
        password = cleaned_data.get('password')

        # check for min length
        min_length = 8
        if len(password) < min_length:
            msg = 'Password must be at least %s characters long.' %(str(min_length))
            self.add_error('password', msg)

        # check for digit
        if sum(c.isdigit() for c in password) < 1:
            msg = 'Password must contain at least 1 number.'
            self.add_error('password', msg)

       

        password_confirm = cleaned_data.get('password_confirm')


        if password and password_confirm:
            if password != password_confirm:
                msg = "The two password fields must match."
                self.add_error('password_confirm', msg)
        return cleaned_data


class LoginForm(forms.ModelForm):
    username=forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
  
   
    class Meta:
        model = User
        fields = ('username', 'password')

class RestrictedImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        if not self.max_upload_size:
            self.max_upload_size = settings.MAX_UPLOAD_SIZE
        super(RestrictedImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(RestrictedImageField, self).clean(*args, **kwargs)
        try:
            if data.size > self.max_upload_size:
                raise forms.ValidationError(_('File size must be under %s. Current file size is %s.') % (filesizeformat(self.max_upload_size), filesizeformat(data.size)))
        except AttributeError:
            pass

        return data



class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    profimg = RestrictedImageField(max_upload_size=2097152)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','phone_no','email','profimg','address')

     
    def clean_picture(self):
       profimg = self.cleaned_data.get("profimg")
       if not profimg:
           raise forms.ValidationError("No image!")
       else:
           w, h = get_image_dimensions(profimg)
           if w <= 500:
               raise forms.ValidationError("The image is %i pixel wide. It's supposed to be 500px" % w)
           if h <= 500:
               raise forms.ValidationError("The image is %i pixel high. It's supposed to be 500px" % h)
       return profimg




class AssignmentForm(forms.ModelForm):
    assignment=forms.FileField(required=True)
    title=forms.CharField(required=False)
    class Meta:
        model = Assignment
        fields = ('title','assignment','submission_date')



class SubmitAssignmentForm(forms.ModelForm):
    tea_assignment=forms.FileField(required=True)
    sub_title=forms.CharField(required=False)
    submitted_assignment = forms.FileField(required=True)
    submitted_at = forms.DateTimeField()
    class Meta:
        model = Submission
        fields = ('tea_assignment','submitted_assignment','sub_title','submitted_at')

    def clean_submitted_at(self):
        submitted_at = self.cleaned_data['submitted_at']
        a=Assignment.objects.filter()
        if submitted_at < datetime.date.now():
            raise forms.ValidationError('No past Date')
        return submitted_at

        

class RequestForm(forms.ModelForm):
    requested=forms.BooleanField(initial=True)
    class Meta:
        model = AssignRequest
        fields = ('requested',)

        
class ReviewAssignmentForm(forms.ModelForm):
    REVIEW_TYPE_CHOICES = (
    ('1 star', '1 star'),
    ('1.5 star', '1.5 star'),
    ('2 star', '2 star'),
    ('2.5 star', '2.5 star'),
    ('3 star', '3 star'),
    ('3.5 star', '3.5 star'),
    ('4 star', '4 star'),
    ('4.5 star', '4.5 star'),
    ('5 star', '5 star'),
    )
    review_assignment=forms.FileField(required=True)
    review_stars=forms.ChoiceField(widget=forms.Select(), choices =REVIEW_TYPE_CHOICES)

    class Meta:
        model = Review
        fields = ('review_assignment','review_stars')


