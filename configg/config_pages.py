from configg.page_registery import PageRegistry
from controllers.auth_controller import AuthController
from views.main_frameless_window import MainFramelessWindow
from controllers.task_controller import TaskController
class ConfigPages:
    def __init__(self):
        self.pages = PageRegistry()
        self.window = MainFramelessWindow()
        self.add_page()
        self.auth = AuthController(
            login_page=self.pages.login,
            userdash_page=self.pages.userdash,
            register_page=self.pages.register,
            page_manager=self.window
        )
        self.task_controler = TaskController(
            page_todolist=self.pages.todo,
            page_showtask=self.pages.show_task,
            page_editore=self.pages.edit_task,
            page_manager=self.window
        ) 
    def add_page(self):
        # ایجاد صفحه MoreFeatures با page_manager
        from views.pages.more_features_page import MoreFeaturesPage
        from views.pages.checklist_page import ChecklistPage
        from views.pages.habits_page import HabitsPage
        self.pages.more_features = MoreFeaturesPage(page_manager=self.window)
        self.pages.checklist = ChecklistPage(page_manager=self.window)
        self.pages.habits_page = HabitsPage(page_manager=self.window)
             
        self.window.add_page(self.pages.dash,"Dashboard")
        self.window.add_page(self.pages.calendar,"Calendar")
        self.window.add_page(self.pages.settings, "Settings")
        self.window.add_page(self.pages.login, "Login")
        self.window.add_page(self.pages.about, "About")
        self.window.add_page(self.pages.journal, "Journal")
        self.window.add_page(self.pages.timer, "Timer")  # Timer هنوز برای دسترسی مستقیم موجود است
        self.window.add_page(self.pages.calculator, "Calculator")  # ماشین حساب
        self.window.add_page(self.pages.checklist, "Checklist")  # چک‌لیست عادت‌ها - صفحه لانچر
        # صفحات جدید habit
        self.window.add_page(self.pages.habits_page, "Habits")  # مدیریت عادت‌های روزانه
        self.window.add_page(self.pages.habits_weekly_page, "HabitsWeekly")  # عادت‌های هفتگی
        self.window.add_page(self.pages.habits_monthly_page, "HabitsMonthly")  # عادت‌های ماهانه
        self.window.add_page(self.pages.habit_reflection_page, "HabitReflection")  # بازتاب روزانه
        self.window.add_page(self.pages.habit_motivation_page, "HabitMotivation")  # انگیزش روزانه
        self.window.add_page(self.pages.habit_statistics_page, "HabitStatistics")  # آمار و نمودارها
        self.window.add_page(self.pages.more_features, "MoreFeatures")  # صفحه جدید امکانات بیشتر
        self.window.add_page(self.pages.todo, "TodoList")
        self.window.add_page(self.pages.userdash,"usdash")
        self.window.add_page(self.pages.fields, "Fields")
        self.window.add_page(self.pages.ideas, "Ideas")
        self.window.add_page(self.pages.projects, "Projects")
        self.window.add_page(self.pages.learning_paths, "LearningPaths")