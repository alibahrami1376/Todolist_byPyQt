from viewmodels.user_view_model import UserViewModel




class Config:
    """Configuration class for the application."""
    def __init__(self):
        self.user_view_model = UserViewModel()
        self.crate_user()
        # self.user_view_model.load_user_data()
        # self.user_view_model.load_user_preferences()    
        # self.user_view_model.load_user_settings()
        # self.user_view_model.load_user_notifications()
        # self.user_view_model.load_user_roles()
        # self.user_view_model.load_user_permissions()
        # self.user_view_model.load_user_groups()
        # self.user_view_model.load_user_sessions()
        # self.user_view_model.load_user_activity_logs()

    def crate_user(self):
        if self.user_view_model.get_user_by_username("ali"):
            return
        if self.user_view_model.get_user_by_username("bahram"):
            return
        self.user_view_model.create_user("ali", "1234")
        self.user_view_model.create_user("bahram", "1234")
    