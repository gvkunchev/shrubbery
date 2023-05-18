from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from shrubbery.view_decorators import is_teacher, is_student

from users.models import Student
from .models import Voucher
from .forms import VoucherForm

@is_teacher
def vouchers(request):
    '''Vouchers overview.'''
    return render(request, "vouchers/vouchers.html", {'vouchers': Voucher.objects.all()})


@is_teacher
def add_vouchers(request):
    '''Add new vouchers from a file.'''
    try:
        csv_file = request.FILES["csv_file"]
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
    except:
        context = {
            'vouchers': Voucher.objects.all(),
            'errors': {'csv': 'Грешка при обработка на файла.'}
        }
        return render(request, "vouchers/vouchers.html", context)
    errors = []
    counter = 0
    for i, line in enumerate(lines):
        if not line:
            continue
        try:
            token, points = line.split(',')
            token = token.strip()
            points = points.strip()
            data = {
                'token': token,
                'points': points,
            }
            form = VoucherForm(data)
            if form.is_valid():
                form.save()
                counter += 1
            else:
                errors.append((i, line, str(form.errors)))
        except Exception as e:
            errors.append((i, line, f'Грешка при обработка на реда: {e}'))
    context = {
        'vouchers': Voucher.objects.all(),
        'errors': {'csv_list': errors},
        'info': f'Добавени бяха {counter} ваучера.'
    }
    return render(request, "vouchers/vouchers.html", context)

@is_teacher
def remove_vouchers(request):
    '''Remove vouchers.'''
    vouchers = []
    try:
        for field in request.POST:
            if field.startswith('voucher_'):
                pk = field.replace('voucher_', '')
                vouchers.append(Voucher.objects.get(pk=pk))
    except ObjectDoesNotExist:
        return redirect('missing')
    for voucher in vouchers:
        voucher.delete()
    context = {
        'vouchers': Voucher.objects.all()
    }
    if len(vouchers):
        context['info'] = 'Успешно изтри ваучерите.'
    return render(request, "vouchers/vouchers.html", context)

@is_student
def redeemed(request):
    '''Remove vouchers.'''
    context = {
        'vouchers': Voucher.objects.filter(owner=request.user)
    }
    return render(request, "redeemed/redeemed.html", context)


def redeem(request):
    '''Redeem a voucher.'''
    context = {
        'vouchers': Voucher.objects.filter(owner=request.user)
    }
    try:
        token = request.POST.get('token')
        voucher = Voucher.objects.get(token=token)
        if voucher.owner and voucher.owner.pk == request.user.pk:
            context['error'] = 'Вече си завил този ваучер'
        elif voucher.owner:
            raise ObjectDoesNotExist
        else:
            voucher.owner = Student.objects.get(pk=request.user.pk)
            voucher.update_date()
            voucher.save()
            context['info'] = 'Успешно заяви ваучер'
    except ObjectDoesNotExist:
        context['error'] = 'Невалиден ваучер'
    return render(request, "redeemed/redeemed.html", context)
