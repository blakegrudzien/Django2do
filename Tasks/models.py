from django.db import models
from django.shortcuts import render
from django.utils import timezone

class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.CharField(max_length=500)
  completed = models.BooleanField(default=False)
  due_date = models.DateField(default = timezone.now)
  URGENCY_WORDS = {0: "None", 1: 'Low', 2: 'Medium', 3: 'High', 4: "Very High"}
  URGENCY_COLORS = {0: "grey", 1: 'green', 2: 'blue', 3: 'orange', 4: "red"}

  urgency = models.IntegerField()

  def get_urgency_word(self):
      return self.URGENCY_WORDS.get(self.urgency)

  def get_urgency_color(self):  
      return self.URGENCY_COLORS.get(self.urgency, "#ccc")
  


  def __str__(self):
    return self.title

class CompletedTasksStack(models.Model):
    task_ids = models.TextField(default='')

    def add_completed_task(self, task_id):
        task_ids_list = self.task_ids.split(',') if self.task_ids else []
        task_ids_list.append(str(task_id))
        self.task_ids = ','.join(task_ids_list)
        self.save()

    def pop_completed_task(self):
        # Remove and return the most recent completed task ID from the stack
        task_ids_list = self.task_ids.split(',') if self.task_ids else []
        if task_ids_list:
            popped_task = task_ids_list.pop()
            self.task_ids = ','.join(task_ids_list)
            self.save()
            try:
                return int(popped_task)  
            except ValueError:
                return None  # Return None for non-integer values
        return None  # Return None when the stack is empty

    def is_empty(self):
        # Check if the task_ids field is empty
        return not self.task_ids