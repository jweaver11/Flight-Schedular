import flet as ft
import asyncio
from services.auth import verify_login


def LoginPage(page: ft.Page):

    if page.session.store.get("user") is not None:
        # User is already logged in — skip login page
        asyncio.create_task(page.push_route, "/view_selector")
        return

    async def login_user(e=None):
        error_text.value = ""
        progress_ring.visible = True
        progress_ring.update()
        await asyncio.sleep(0)

        email_val    = email.value.strip()
        password_val = password.value

        if not email_val or not password_val:
            error_text.value = "Please enter your email and password."
            error_text.visible = True
            error_text.update()
            progress_ring.visible = False
            progress_ring.update()
            return
        
        user = verify_login(email_val, password_val)
        
        if user is None:
            # Deliberately vague — don't reveal whether the email or password was wrong.
            error_text.value = "Invalid email or password."
            error_text.visible = True
            error_text.update()
            progress_ring.visible = False
            progress_ring.update()
            return
        
        # Set the session data to the user
        page.session.store.set("user", user)
        #print(page.session.store.get("user"))

        # ViewSelector will read session_data["user"]["role"] and route accordingly.
        await page.push_route("/view_selector")

    async def _push_register(e: ft.ControlEvent):
        
        await page.push_route("/register_account")

    # Student view
    return ft.SafeArea(
        ft.Column(
            [
        
                ft.Text("Login to Chopper Aviation Flight Scheduler", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                
                email := ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL),

                password := ft.TextField(label="Password", password=True, can_reveal_password=True, on_submit=login_user),

                progress_ring := ft.ProgressRing(visible=False),

                error_text := ft.Text("", color=ft.Colors.ERROR, size=13, visible=False),

                ft.Button(
                    "Login",
                    on_click=login_user,
                    #disabled=loading,
                    #icon=ft.Icons.LOOP if loading else None,
                ),
                    
                ft.Button("Sign Up", on_click=_push_register),
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        expand=True
    )