import flet as ft

@ft.component
def ResetPasswordPage():
    return ft.SafeArea(
        ft.Column(
            [
        
                ft.Text("Reset Password", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                
                
                ft.TextField("Email"),

                ft.TextButton("Send Reset Email"),
                
                
                ft.TextButton("Back to login", on_click=lambda: ft.context.page.navigate("/")),
               
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        expand=True
    )