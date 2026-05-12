import flet as ft

from services.auth import verify_login


def LoginPage(page: ft.Page):
    #error_text, set_error_text = ft.use_state("")
    #loading,    set_loading    = ft.use_state(False)

    async def login_user():
        #set_error_text("")
        email_val    = email.value.strip()
        password_val = password.value

        if not email_val or not password_val:
            #set_error_text("Please enter your email and password.")
            return

        #set_loading(True)
        user = verify_login(email_val, password_val)
        #set_loading(False)

        if user is None:
            # Deliberately vague — don't reveal whether the email or password was wrong.
            #set_error_text("Invalid email or password.")
            return

        # Store the logged-in user's info for use across pages.
        #page.session_data["user"] = user

        # ViewSelector will read session_data["user"]["role"] and route accordingly.
        await page.push_route("/view_selector")

    async def _push_register(e: ft.ControlEvent):
        await page.push_route("/register_account")

    async def _push_reset(e: ft.ControlEvent):
        await page.push_route("/reset_password")

    # Student view
    return ft.SafeArea(
        ft.Column(
            [
        
                ft.Text("Login to Chopper Aviation Flight Scheduler", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                
                email := ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL),

                password := ft.TextField(label="Password", password=True, can_reveal_password=True),

                #ft.Text(error_text, color=ft.Colors.ERROR, size=13, visible=bool(error_text)),

                ft.Button(
                    "Login",
                    on_click=login_user,
                    #disabled=loading,
                    #icon=ft.Icons.LOOP if loading else None,
                ),
                    
                ft.Row([
                    ft.Button("Sign Up", on_click=_push_register),
                    ft.Button("Forgot Password?", on_click=_push_reset),
                ], spacing=50, tight=True)
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        expand=True
    )