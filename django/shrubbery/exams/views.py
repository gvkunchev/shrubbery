from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from shrubbery.view_decorators import is_teacher

from users.models import Student
from .models import Exam, ExamResult
from .forms import ExamForm, ExamResultForm


@is_teacher
def exams(request):
    '''Exams page.'''
    return render(request, "exams/exams.html", {'exams': Exam.objects.all()})


@is_teacher
def exam(request, exam):
    '''Exam page.'''
    try:
        exam = Exam.objects.get(pk=exam)
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'exam': exam,
        'results': ExamResult.objects.filter(exam=exam)
    }
    return render(request, "exams/exam.html", context)


@is_teacher
def add_exam(request):
    '''Add new exam.'''
    form = ExamForm(request.POST)
    if form.is_valid():
        form.save()
        context = {
            'exams': Exam.objects.all(),
            'info': 'Успешно добави изпит'
        }
        # Keeping the POST data will refill
        # the inputs with it, which is useful on
        # error, but should not be done on success
        request.POST = {}
        return render(request, "exams/exams.html", context)
    else:
        context = {
            'exams': Exam.objects.all(),
            'errors': form.errors
        }
        return render(request, "exams/exams.html", context)


@is_teacher
def edit_exam(request, exam):
    '''Edit an exam.'''
    try:
        exam = Exam.objects.get(pk=exam)
    except ObjectDoesNotExist:
        return redirect('missing')
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            context = {
                'exams': Exam.objects.all(),
                'info': 'Успешно редактира изпит'
            }
            # Keeping the POST data will refill
            # the inputs with it, which is useful on
            # error, but should not be done on success
            request.POST = {}
            return render(request, "exams/exams.html", context)
        else:
            context = {
                'exam': exam,
                'errors': form.errors
            }
            return render(request, "exams/edit_exam.html", context)
    else:
        context = {
            'exam': exam
        }
        return render(request, "exams/edit_exam.html", context)


@is_teacher
def delete_exam(request, exam):
    '''Remove an exam.'''
    try:
        exam = Exam.objects.get(pk=exam)
    except ObjectDoesNotExist:
        return redirect('missing')
    exam.delete()
    return redirect('exams:exams')


@is_teacher
def delete_exam_results(request):
    '''Remove exam results.'''
    try:
        exam = Exam.objects.get(pk=request.POST.get('exam'))
    except ObjectDoesNotExist:
        return redirect('missing')
    results = []
    try:
        for field in request.POST:
            if field.startswith('exam_result_'):
                pk = field.replace('exam_result_', '')
                results.append(ExamResult.objects.get(pk=pk))
    except ObjectDoesNotExist:
        return redirect('missing')
    for result in results:
        result.delete()
    context = {
        'exam': exam,
        'results': ExamResult.objects.filter(exam=exam)
    }
    if len(results):
        context['info'] = 'Успешно изтри резултатите.'
    return render(request, "exams/exam.html", context)


@is_teacher
def add_exam_result(request):
    '''Add a new exam results.'''
    # Ensure exam exists
    try:
        exam = Exam.objects.get(pk=request.POST.get('exam'))
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'exam': exam,
        'results': ExamResult.objects.filter(exam=exam)
    }
    # Ensure student exists
    try:
        student = Student.objects.get(fn=request.POST.get('fn'))
    except ObjectDoesNotExist:
        context['error_single_result'] = 'Студент с този факултетен номер не е намерен.'
        return render(request, "exams/exam.html", context)
    # Prepare the data
    data = {
        'points': request.POST.get('points'),
        'owner': student,
        'exam': exam
    }
    # Determine whether it is a new record or chaning an old one
    overwrite = False
    try:
        result = ExamResult.objects.get(exam=exam, owner=student)
        form = ExamResultForm(data, instance=result)
        overwrite = True
    except ObjectDoesNotExist:
        form = ExamResultForm(data)
    # Validate and save the form
    if form.is_valid():
        form.save()
        if overwrite:
            context['info'] = 'Успешно редактира резултат.'
        else:
            context['info'] = 'Успешно добави резултат.'
        # Clear data to clear the form
        request.POST = []
        return render(request, "exams/exam.html", context)
    else:
        context['errors'] = form.errors
        return render(request, "exams/exam.html", context)
    

@is_teacher
def add_exam_results(request):
    '''Add new exam results from a file.'''
    # Ensure exam exists
    try:
        exam = Exam.objects.get(pk=request.POST.get('exam'))
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'exam': exam,
        'results': ExamResult.objects.filter(exam=exam)
    }
    # Try reading the csv
    try:
        csv_file = request.FILES["csv_file"]
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
    except:
        context['error_csv'] = 'Грешка при обработка на файла.'
        return render(request, "exams/exam.html", context)
    errors = []
    added = 0
    editted = 0
    for i, line in enumerate(lines):
        if not line:
            continue
        try:
            fn, points = line.split(',')
            fn = fn.strip()
            points = int(points.strip())
            # Ensure student exists
            try:
                student = Student.objects.get(fn=fn)
            except ObjectDoesNotExist:
                raise Exception('Студент с такъв факултетен номер не е намерен.')
            # Determine whether this is a new record or changing an old one
            data = {
                'points': points,
                'owner': student,
                'exam': exam
            }
            overwrite = False
            try:
                result = ExamResult.objects.get(exam=exam, owner=student)
                form = ExamResultForm(data, instance=result)
                overwrite = True
            except ObjectDoesNotExist:
                form = ExamResultForm(data)
            if form.is_valid():
                form.save()
                if overwrite:
                    editted += 1
                else:
                    added += 1
            else:
                errors.append((i, line, str(form.errors)))
        except Exception as e:
            errors.append((i, line, f'Грешка при обработка на реда: {e}'))
    context.update({
        'errors': {'csv_list': errors},
        'info': f'Добавени бяха {added} студента. Редактираниха бяха {editted} студента.',
        'results': ExamResult.objects.filter(exam=exam)
    })
    return render(request, "exams/exam.html", context)
