from django.views.generic import ListView
from users.models import Student


class StudentPaginationView(ListView):
    paginate_by = 10
    model = Student
