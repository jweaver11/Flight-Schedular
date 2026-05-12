import flet as ft
from pages.register_account import RegisterAccountPage
from pages.reset_password import ResetPasswordPage
from pages.login import LoginPage
from pages.view_selector import ViewSelector
from pages.admin_view import AdminViewPage
from pages.instructor_view import InstructorViewPage
from pages.student_view import StudentViewPage


@ft.component
def App():

    return ft.Router([
        ft.Route(path="/", index=True, component=LoginPage),                    # Default - login page
        ft.Route(path="student_view", component=StudentViewPage),               # Main scheduling view for students
        ft.Route(path="register_account", component=RegisterAccountPage),       # Register new accounts page
        ft.Route(path="reset_password", component=ResetPasswordPage),           # Reset password page

        ft.Route(path="view_selector", component=ViewSelector),                 # View selector - determines what view to show based on user id (student, instructor, admin)
        ft.Route(path="admin_view", component=AdminViewPage),                 # Main view for admins
        ft.Route(path="instructor_view", component=InstructorViewPage),            # Main view for instructors
        ft.Route(path="instructor_view", component=StudentViewPage),            # Main view for students
        
    ])
        
 
ft.run(lambda page: page.render(App))
