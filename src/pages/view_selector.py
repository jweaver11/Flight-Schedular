''' Reads the logged-in user's role from session_data and navigates to the correct view. '''

import flet as ft


def ViewSelector(page: ft.Page):
    user = ft.context.page.session_data.get("user")

    if user is None:
        # No session — send back to login
        return ft.context.page.navigate("/")

    role = user.get("role", "student")

    if role == "admin":
        return ft.context.page.navigate("/admin_view")
    elif role == "instructor":
        return ft.context.page.navigate("/instructor_view")
    else:
        return ft.context.page.navigate("/student_view")
