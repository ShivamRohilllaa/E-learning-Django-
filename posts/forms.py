from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from .models import *
from django.forms import inlineformset_factory


class PostForm(forms.ModelForm):
    maincourse = forms.ModelMultipleChoiceField(
            queryset=MainCourse.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True)
    
    class Meta:
        model = Post
        fields = '__all__'

class EditPostForm(forms.ModelForm):
    maincourse = forms.ModelMultipleChoiceField(
            queryset=MainCourse.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True)    
    class Meta:
        model = Post
        fields = '__all__'


class Curriculamform(forms.ModelForm):
    class Meta:
        model = Curriculam
        fields =  '__all__'

class featuresform(forms.ModelForm):
    class Meta:
        model = features
        fields =  '__all__'

class timingform(forms.ModelForm):
    class Meta:
        model = timing
        fields =  '__all__'

class CatForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = '__all__'

class EditCatForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = '__all__'

class Maincourse(forms.ModelForm):
    
    class Meta:
        model = MainCourse
        fields = ['title']

class EditMaincourse(forms.ModelForm):
    
    class Meta:
        model = MainCourse
        fields = ['title']


# User Creation Forms
class CustomerAuthForm(AuthenticationForm):
    username = forms.EmailField(required=True , label="Email")

class CustomerCreationForm(UserCreationForm):
    
    username = forms.EmailField(required=True , label="Email" )
    first_name = forms.CharField(required=True , label="First Name")
    last_name = forms.CharField(required=True , label="Last Name")
    class Meta:
        model = User
        fields = ['username' ,'first_name' , "last_name" ]

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name')
        if len(value.strip()) < 4 :
            raise ValidationError("First Name must be 4 char long...")
        return value.strip()
    
    def clean_last_name(self):
        value = self.cleaned_data.get('last_name')
        if len(value.strip()) < 4 :
            raise ValidationError("Last Name must be 4 char long...")
        return value.strip()

class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['address','mobile','profile_pic']

class CustomerEditForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['address','mobile','profile_pic','Country','Company','City','State','Zip_Code','Telephone','Extension']

class CustomerCreationEditForm(UserChangeForm):
    # password = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden'}))
    username = forms.EmailField(required=True , label="Email" )
    first_name = forms.CharField(required=True , label="First Name")
    last_name = forms.CharField(required=True , label="Last Name")
    class Meta:
        model = User
        fields = ['username' ,'first_name' , "last_name"]
        exclude = ['password']

class changepassword(UserCreationForm):    
    class Meta:
        model = User
        fields = ['password1']
        exclude = ['username', 'first_name','last_name']

class Customerloginform(AuthenticationForm):
    username = forms.EmailField(required=True, label="Email") #Isme emailfield isliye liye hai qki humne isme username use ni kiya isme, username ki jagah humne isme email use ki hai to that's why we use this!!
    password = forms.PasswordInput()


class Userpermission(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Group.objects.all())    

    class Meta:
        model = User
        fields = ['first_name','last_name']

class videoform(forms.ModelForm):

    class Meta:
        model = video
        fields = '__all__'

class faqForm(forms.ModelForm):
    
    class Meta:
        model = faq
        fields = '__all__'

class subcatg(forms.ModelForm):
    
    class Meta:
        model = subcat
        fields = '__all__'

class blogform(forms.ModelForm):
    
    class Meta:
        model = blog
        fields = '__all__'

class blankform(forms.ModelForm):
    
    class Meta:
        model = blankpage
        fields = '__all__'

class tcblog(forms.ModelForm):
    
    class Meta:
        model = tcforblog
        fields = '__all__'

class promoform(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Promo Code',    
    }))
    
class leftmenu(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['top_three_cat', 'more']    

class middlemenu(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['parent', 'top_three_cat', 'logo1', 'logo2']    

class rightmenu(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['parent', 'more', 'logo1', 'logo2']    

class admin_reviewsform(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = '__all__'          

class checkoutform(forms.Form):
    mobile = forms.IntegerField()        
    street_address = forms.CharField()        
    apartment_address = forms.CharField(required=False)
    country = forms.CharField(label="Country")
    zipcode = forms.CharField()
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.BooleanField(widget=forms.RadioSelect())         

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
    }))

class approve_certForm(forms.ModelForm):
    certificate = forms.BooleanField(widget=forms.CheckboxInput())
    class Meta:
        model = Cart
        fields = ['certificate']

class sendmessage(forms.ModelForm):

    class Meta:
        model = message
        fields = '__all__'
        exclude = ['wp']
       
class ribbonform(forms.ModelForm):

    class Meta:
        model = offers
        fields = '__all__'
