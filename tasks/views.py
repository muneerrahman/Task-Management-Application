from django.shortcuts import render,get_object_or_404, redirect
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth import get_user_model
User = get_user_model()



#template views
@login_required
def task_list_view(request):
  
    if request.user.role in ['superadmin', 'admin']:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

    allowed_roles = ['superadmin', 'admin']
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'allowed_roles': allowed_roles})

@login_required
def task_detail_view(request, pk):
   
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        report = request.POST.get('completion_report')
        hours = request.POST.get('worked_hours') or 0

        if status == 'completed' and (not report or not hours):
            return render(request, 'tasks/task_detail.html', {
                'task': task,
                'error': 'Completion report and worked hours are required when completing a task.'
            })

        task.status = status
        task.completion_report = report
        task.worked_hours = hours
        task.save()
        return redirect('task-list-web')

    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_report_view(request, pk):
   
    if request.user.role not in ['superadmin', 'admin']:
        return redirect('task-list-web')

    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_report.html', {'task': task})


#superadmin views for admin

@login_required
def superadmin_admin_list(request):
    if request.user.role != 'superadmin':
        return redirect('task-list-web')
    admins = User.objects.filter(role='admin')
    return render(request, 'tasks/superadmin_admin_list.html', {'admins': admins})

@login_required
def superadmin_edit_admin(request, admin_id):
    if request.user.role != 'superadmin':
        return redirect('task-list-web')

    admin = get_object_or_404(User, id=admin_id, role='admin')

    if request.method == 'POST':
        admin.username = request.POST.get('username')
        admin.is_staff = request.POST.get('is_staff') == 'on'
        admin.save()
        return redirect('superadmin_admin_list')

    return redirect('superadmin_admin_list')

@login_required
def superadmin_delete_admin(request, admin_id):
    if request.user.role != 'superadmin':
        return redirect('task-list-web')

    admin = get_object_or_404(User, id=admin_id, role='admin')

    if request.method == 'POST':
        admin.delete()
        return redirect('superadmin_admin_list')


#superadmin views for user
@login_required
def superadmin_user_list(request):
    if request.user.role != 'superadmin':
        return redirect('task-list-web')
    users = User.objects.filter(role='user')
    admins = User.objects.filter(role='admin')
    return render(request, 'tasks/superadmin_user_list.html', {'users': users, 'admins': admins})

@login_required
def superadmin_create_user(request):
    if request.user.role != 'superadmin':
        return redirect('task-list-web')

    admins = User.objects.filter(role='admin') 

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # 'superadmin', 'admin', 'user'
        is_staff = request.POST.get('is_staff') == 'on'
        assigned_admin_id = request.POST.get('assigned_admin')  # optional, for users only

        user = User.objects.create_user(username=username, password=password, role=role, is_staff=is_staff)

        if role == 'user' and assigned_admin_id:
            admin = get_object_or_404(User, id=assigned_admin_id, role='admin')
            user.admin = admin
            user.save()

        return redirect('superadmin_user_list')

    return render(request, 'tasks/superadmin_create_user.html', {'admins': admins})


@login_required
def superadmin_assign_user_to_admin(request):
    if request.user.role != 'superadmin':
        return redirect('task-list-web')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        admin_id = request.POST.get('admin_id')  
        user = get_object_or_404(User, id=user_id, role='user')
        
        if admin_id:
            admin = get_object_or_404(User, id=admin_id, role='admin')
            user.admin = admin
        else:
            user.admin = None 

        user.save()
        return redirect('superadmin_user_list')

@login_required
def superadmin_delete_user(request, user_id):
    if request.user.role != 'superadmin':
        return redirect('task-list-web')

    user = get_object_or_404(User, id=user_id, role='user')

    if request.method == 'POST':
        user.delete()
        return redirect('superadmin_user_list')

@login_required
def superadmin_edit_user(request, user_id):
    if request.user.role != 'superadmin':
        return redirect('task-list-web')

    user = get_object_or_404(User, id=user_id, role='user')
    admins = User.objects.filter(role='admin')

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.role = request.POST.get('role')
        user.is_staff = request.POST.get('is_staff') == 'on'

        assigned_admin_id = request.POST.get('assigned_admin')
        if user.role == 'user' and assigned_admin_id:
            admin = get_object_or_404(User, id=assigned_admin_id, role='admin')
            user.admin = admin
        else:
            user.admin = None

        user.save()
        return redirect('superadmin_user_list')



#admin views
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('task-list-web')

    # Users assigned to this admin
    users = User.objects.filter(admin=request.user, role='user')

    # Tasks assigned to these users
    tasks = Task.objects.filter(assigned_to__in=users)

    # Handle task creation
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        assigned_user = get_object_or_404(User, id=assigned_to_id, admin=request.user)
        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_user,
            status='Pending',
            due_date=due_date
        )
        return redirect('admin_dashboard')

    return render(request, 'tasks/admin_dashboard.html', {'users': users, 'tasks': tasks})

@login_required
def admin_task_delete(request, task_id):
    if request.user.role != 'admin':
        return redirect('task-list-web')

    task = get_object_or_404(Task, id=task_id, assigned_to__admin=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('admin_dashboard')
    
@login_required
def admin_task_create_view(request):
    if request.user.role != 'admin':
        return redirect('task-list-web')

    # Only users assigned to this admin
    users = User.objects.filter(admin=request.user, role='user')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        assigned_user = get_object_or_404(User, id=assigned_to_id)
        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_user,
            status='Pending',
            due_date=due_date
        )
        return redirect('tasks/admin_task_create.html')

    return render(request, 'tasks/admin_task_create.html', {'users': users})




#serializer views
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assigned_to=user)

class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskReportView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'superadmin']:
            return Task.objects.filter(status='completed')
        return Task.objects.none()  
