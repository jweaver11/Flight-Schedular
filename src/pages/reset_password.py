import flet as ft

def ResetPasswordPage(page: ft.Page):

    async def _push_login(e: ft.ControlEvent):
        await page.push_route("/")

    return ft.SafeArea(
        ft.Column(
            [
        
                ft.Text("Reset Password", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                
                
                ft.TextField("Email"),

                ft.TextButton("Send Reset Email"),
                
                
                ft.TextButton("Back to login", on_click=_push_login),
               
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        expand=True
    )