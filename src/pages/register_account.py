import flet as ft
import asyncio
from services.auth import register_student, EmailAlreadyExistsError


def RegisterAccountPage(page: ft.Page):

    async def _reset_errors(e: ft.Event=None):
        ''' Resets our state UI error displays when user starts changing input '''
        error_text.value = ""
        error_text.visible = False
        progress_ring.visible = False
        error_text.update()
        progress_ring.update()

    # Our textfields we use to get our user input
    name = ft.TextField(label="Full Name", on_change=_reset_errors)
    email = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL, on_change=_reset_errors)
    phone = ft.TextField(label="Phone Number", keyboard_type=ft.KeyboardType.PHONE, input_filter=ft.NumbersOnlyInputFilter(), on_change=_reset_errors)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, on_change=_reset_errors)
    confirm_password = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, on_change=_reset_errors)

    # State UI updaters
    progress_ring = ft.ProgressRing(visible=False)
    error_text = ft.Text("", color=ft.Colors.ERROR, visible=False) 

    
    
    
    async def submit(e: ft.Event=None):
        ''' Handles checking our info is complex enough and non-duplicated, and passes it where it needs to go '''

        progress_ring.visible = True
        progress_ring.update()
        await asyncio.sleep(0)

        email_val    = email.value.strip()
        name_val     = name.value.strip()
        phone_val    = phone.value.strip()
        password_val = password.value
        confirm_val  = confirm_password.value

        # Client-side validation
        if not name_val:
            error_text.value = "Full name is required."
            error_text.visible = True
            error_text.update()
            progress_ring.visible = False
            progress_ring.update()
            return

        if not email_val:
            error_text.value = "Email is required."
            error_text.visible = True
            error_text.update()
            progress_ring.visible = False
            progress_ring.update()
            return

        if not phone_val:
            error_text.value = "Phone number is required."
            error_text.visible = True
            error_text.update()
            progress_ring.visible = False
            progress_ring.update()
            return

        if not password_val:
            error_text.value = "Password is required."
            error_text.visible = True
            error_text.update()
            progress_ring.visible = False
            progress_ring.update()
            return

        if password_val != confirm_val:
            error_text.value = "Passwords do not match."
            error_text.visible = True
            error_text.update()
            progress_ring.visible = False
            progress_ring.update()
            return

        if len(password_val) < 8:
            error_text.value = "Password must be at least 8 characters"
            error_text.visible = True
            error_text.update()
            progress_ring.visible = False
            progress_ring.update()
            return

        #set_loading(True)
        try:
            register_student(
                email=email_val,
                raw_password=password_val,
                name=name_val,
                phone=phone_val,
            )
            # Show success snackbar then navigate to login
            sb = ft.SnackBar(
                ft.Text("Account created successfully! Please log in.", color=ft.Colors.ON_SURFACE),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                shape=ft.RoundedRectangleBorder(ft.BorderSide(2, ft.Colors.GREEN), radius=8),
            )
            await page.push_route("/")
            page.show_dialog(sb)
            
        except EmailAlreadyExistsError:
            error_text.value = "An account with that email already exists. Try logging in or resetting your password"
            error_text.visible = True
        except Exception:
            error_text.value = "Something went wrong. Please try again later."
            error_text.visible = True
        

    async def _push_login(e: ft.ControlEvent):
        progress_ring.visible = True
        progress_ring.update()
        await asyncio.sleep(0)
        await page.push_route("/")

    return ft.SafeArea(
        ft.Column(
            [
                ft.Text("Register for Chopper Aviation Scheduling", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),

                name,
                email,
                phone,
                password,
                confirm_password,

                progress_ring,
                error_text,

                ft.Button("Create Account", on_click=submit),
                ft.Button("Back to login", on_click=_push_login),

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True,
    )