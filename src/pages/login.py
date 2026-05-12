import flet as ft

@ft.component
def LoginPage():

    # if user id is admin, return admin view. 
    # Elif user id is instructor, return instructor view. 
    # Else return student view

    # Student view
    return ft.SafeArea(
        ft.Column(
            [
        
                ft.Text("Login to Chopper Aviation Flight Scheduler", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                
                ft.TextField(label="Email", ),

                ft.TextField(label="Password", password=True, can_reveal_password=True),
                
                ft.TextButton("Login", on_click=lambda: ft.context.page.navigate("/view_selector")),
                    
                ft.Row([
                    ft.TextButton("Sign Up", on_click=lambda: ft.context.page.navigate("/register_account")),
                    ft.TextButton("Forgot Password?", on_click=lambda: ft.context.page.navigate("/reset_password")),
                ], spacing=50, tight=True)
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        expand=True
    )