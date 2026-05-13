import flet as ft
from pages.register_account import RegisterAccountPage
from pages.reset_password import ResetPasswordPage
from pages.login import LoginPage
from pages.view_selector import ViewSelector
from pages.admin_view import AdminViewPage
from pages.instructor_view import InstructorViewPage
from pages.student_view import StudentViewPage


async def main(page: ft.Page):

    # TEMP: Create admin accounts
    #from models.admin import generate_admin_json
    #generate_admin_json()

    async def _route_change(e: ft.RouteChangeEvent):
        page.controls.clear()

        route = page.route
        match route:
            case "/":
                page.add(AdminViewPage(page))
                #page.add(InstructorViewPage(page))
                #page.add(LoginPage(page))
            case "/register_account":
                page.add(RegisterAccountPage(page))
            case "/reset_password":
                page.add(ResetPasswordPage(page))
            case "/view_selector":
                await ViewSelector(page)
            case "/admin_view":
                page.add(AdminViewPage(page))
            case "/instructor_view":
                page.add(InstructorViewPage(page))
            case "/student_view":
                page.add(StudentViewPage(page))
            case _:
                page.add(ft.Text("404: Page not found"))

    page.on_route_change = _route_change
    page.theme_mode = ft.ThemeMode.SYSTEM

    # Start at the login page
    page.add(LoginPage(page))

    
 
ft.run(main)
