from services.task_storage_service import TaskStorageService
from models.task_models import TaskModel
from viewmodels.task_view_models import TaskViewModel

view = TaskViewModel()
# task1 = TaskModel("Task 1", "Description 1", "high", "2023-10-01", False, False, None, "2023-09-01T12:00:00Z", "2023-09-01T12:00:00Z")
# task2 = TaskModel("Task 2", "Description 2", "medium", "2023-10-02", True, False, None, "2023-09-02T12:00:00Z", "2023-09-02T12:00:00Z")
# task3 = TaskModel("Task 3", "Description 3", "low", "2023-10-03", False, True, task1.id, "2023-09-03T12:00:00Z", "2023-09-03T12:00:00Z")
task6 = TaskModel("Task 4", "Description 4", "high", "2023-10-04", False, True, None, "2023-09-04T12:00:00Z", "2023-09-04T12:00:00Z")
view.add_task(task6)
# TaskStorageService.save_all([task1, task2, task3, task4])
# test = TaskStorageService.load_all()
# print(test[0])
