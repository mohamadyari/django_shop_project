from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import *
from order.models import *
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from random import randint
import ghasedak
from django.core.mail import EmailMessage
from django.views import View
# from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


# Create your views here

class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.id) + text_type(timestamp)


email_generator = EmailToken()


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        remember = form.cleaned_data.get('remember')
        user_name = form.cleaned_data.get('user_name')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(10000 * 60 * 60 * 24 * 2)
            # messages.success(request, 'you are successfully login')
            return redirect('/')
        else:
            form.add_error('user_name', 'کاربری با مشخصات وارد شده یافت نشد')

    context = {
        'form': form
    }

    return render(request, 'account/login.html', context)


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        user = User.objects.create_user(username=data['user_name'], email=data['email'], password=data['password'],
                                        first_name=data['first_name'],
                                        last_name=data['last_name'])

        user.is_active = False
        user.save()
        domain = get_current_site(request).domain
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        url = reverse('account:active', kwargs={'uidb64': uidb64, 'token': email_generator.make_token(user)})
        link = 'http//' + domain + url
        email = EmailMessage(
            'active user',
            link,
            '',
            [data['email']]
        )
        email.send(fail_silently=False)
        messages.warning(request, 'کاربر محترم برای فعال سازی به ایمیل خود مراجعه کنید')
        return redirect('account:user_login')

    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'account/register.html', context)


class RegisterEmail(View):
    def get(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('account:user_login')


def log_out(request):
    logout(request)
    messages.success(request, 'you are successfully exist')
    return redirect('/login')


@login_required(login_url='account:login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'account/profile.html', {'profile': profile})


@login_required(login_url='account:login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'update successfully')
            return redirect('account:user_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'account/update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'successfully change password')
            return redirect('account:user_profile')
        else:
            messages.error(request, 'you are password is false')
            return redirect('account:change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change.html', {'form': form})


def phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            global random_code, phone
            data = form.cleaned_data
            phone = f"0{data['phone']}"
            random_code = randint(100, 1000)
            sms = ghasedak.Ghasedak("")
            sms.send({'message': random_code, '': phone, '': ""})
            return redirect('account:verify')
    else:
        form = PhoneForm()
    return render(request, 'account/phone.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            if random_code == form.cleaned_data['code']:
                profile = Profile.objects.get(phone=phone)
                user = User.objects.get(profile__id=profile.id)
                login(request, user)
                messages.success(request, 'hi user')
                return redirect('home:home')
            else:
                messages.error(request, 'you are code Wrong')
    else:
        form = CodeForm()
    return render(request, 'account/verify.html', {'form': form})


def favourite(request):
    product = request.user.fa_user.all()
    return render(request, 'account/favourite.html', {'product': product})


def history(request):
    data = ItemOrder.objects.filter(user_id=request.user.id)
    return render(request, 'account/history.html', {'data': data})


def product_view(request):
    product = Views.objects.filter(ip=request.META.get('REMOTE_ADDR')).order_by('-create')[:2]
    return render(request, 'account/view.html', {'product': product})


class ResetPassword(auth_views.PasswordResetView):
    template_name = 'account/reset.html'
    success_url = reverse_lazy('account:reset_done')
    email_template_name = 'account/link.html'


class DonePassword(auth_views.PasswordResetDoneView):
    template_name = 'account/done.html'


class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'account/confirm.html'
    success_url = reverse_lazy('account:complete')


class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'account/complete.html'
