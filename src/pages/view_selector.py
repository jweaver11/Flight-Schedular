''' Reads the logged-in user's role from session_data and navigates to the correct view. '''

import flet as ft


async def ViewSelector(page: ft.Page):
    user: dict = page.session.store.get("user")

    # Should be impossible, but catches errors
    if user is None:
        # No session — send back to login
        await page.push_route("/")
        return

    role = user.get("role", "student")

    if role == "admin":
        await page.push_route("/admin_view")
    elif role == "instructor":
        await page.push_route("/instructor_view")
    else:
        await page.push_route("/student_view")
