import flet as ft

@ft.component
def RegisterAccountPage():
    return ft.SafeArea(
        ft.Column(
            [
        
                ft.Text("Register for Chopper Aviation Scheduling", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                
                
                ft.TextField(label="Email"),

                ft.TextField(label="Password", password=True, can_reveal_password=True),

                ft.TextButton("Submit"),
                
                
                ft.TextButton("Back to login", on_click=lambda: ft.context.page.navigate("/")),
               
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        expand=True
    )