import flet as ft

from pages.register_account import RegisterAccountPage
from pages.reset_password import ResetPasswordPage
from pages.schedular import SchedularPage
from pages.login import LoginPage


@ft.component
def App():

    return ft.Router([
        ft.Route(path="/", index=True, component=LoginPage),                    # Default - login page
        ft.Route(path="schedular", component=SchedularPage),                    # Main schedular page
        ft.Route(path="register_account", component=RegisterAccountPage),       # Register new accounts page
        ft.Route(path="reset_password", component=ResetPasswordPage),           # Reset password page
    ])
        
 
ft.run(lambda page: page.render(App))
