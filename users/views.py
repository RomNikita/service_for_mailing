from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView
import random
import string
from django.core.mail import send_mail
from users.forms import UserRegisterForm, VerificationForm
from users.models import User, VerificationCode


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('users:user_success_registration')

    def form_valid(self, form):
        response = super().form_valid(form)

        code = ''.join(random.choices(string.digits, k=6))

        user = self.object
        user.verification_code = code
        user.save()

        verification_code = VerificationCode.objects.create(code=code, user=user)

        subject = 'Код подтверждения'
        message = f'Ваш код подтверждения {code}'
        sender_email = 'noreplyskypro9@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, sender_email, recipient_list)

        return response

    def get_success_url(self):
        return reverse('users:success_regist')


def success_view(request):
    return render(request, 'user/user_success_registration.html')


class VerifyCodeView(View):
    template_name = 'user/user_verify.html'
    form_class = VerificationForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')

            try:
                verification_code = VerificationCode.objects.get(code=code)
                user = verification_code.user
                user.is_active = True
                user.save()
                messages.success(request, 'Регистрация прошла успешно!')
                verification_code.delete()
                return HttpResponseRedirect(reverse('main:home'))
            except VerificationCode.DoesNotExist:
                messages.error(request, 'Неправильный код верификации.')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'Пожалуйста, введите правильный код верификации.')
        return render(request, self.template_name, {'form': form})


    def get_success_url(self):
        return reverse('main:home')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'reset_password.html', {'error_message': 'Пользователя с таким email нет'})

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        user.set_password(new_password)
        user.save()

        subject = 'Новый пароль'
        message = f'Ваш новый пароль: {new_password}'
        from_email = 'noreplyskypro9@gmail.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        return render(request, 'user/password_reset_done.html')

    return render(request, 'user/reset_password.html')


