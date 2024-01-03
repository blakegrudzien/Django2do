from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CompletedTasksStack, Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from .forms import TaskForm





@api_view(['GET', 'POST', 'OPTIONS'])
def Task_list(request, format=None):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return render(request, 'tasks/task_list.html')
    
def check_task(request, id=None):
    if id is not None:
        completed_tasks_stack, created = CompletedTasksStack.objects.get_or_create()
        completed_tasks_stack.add_completed_task(id)

        task = Task.objects.get(pk=id)
        task.completed = True
        task.save()
        
        tasks = Task.objects.filter(completed=False)
        return redirect('/')
    else:
        return HttpResponse("No Task ID provided")

def undo_task(request):
    if request.method == 'POST':
        if CompletedTasksStack.objects.exists():  # Check if the stack exists and is not empty
            completed_tasks_stack = CompletedTasksStack.objects.first()
            if completed_tasks_stack.is_empty():  # Check if the stack is empty
                # Handle the case where the stack is empty
                # For example, return an HttpResponse or render a specific template
                tasks = Task.objects.filter(completed=False)
                return redirect('/')

            task_id = completed_tasks_stack.pop_completed_task()  # Remove the most recent completed task ID
            if task_id:
                task = Task.objects.get(pk=task_id)
                task.completed = False  # Undo completion
                task.save()
                tasks = Task.objects.filter(completed=False)
                return redirect('/')

    return HttpResponse("No completed tasks to undo")





@api_view(['GET', 'PUT', 'DELETE'])
def Task_detail(request, id, format=None):
    try:
        task = Task.objects.get(pk=id)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def task_list(request):
    tasks = Task.objects.filter(completed=False)
    return render(request, 'tasks/task_view.html', {'tasks': tasks, 'completed_tasks_stack': CompletedTasksStack})





def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            tasks = Task.objects.all()
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to task list after editing the task
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})