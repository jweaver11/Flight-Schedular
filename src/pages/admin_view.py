''' Main view for the students'''

import flet as ft


# TODO: Add/edit instructors and aircraft
@ft.component
def AdminViewPage():
    return ft.SafeArea(
        ft.Row([
            ft.Column(
                [
                    ft.Text("Insturctors", size=20, italic=True),
                    ft.Text("Kevin",),
                    ft.Text("Steven",),
                    ft.Text("Tom"),

                    ft.Divider(),
                    ft.Text("Aircrafts", size=20, italic=True),
                    ft.Text("Aircraft 1",),
                    ft.Text("Aircraft 2",),
                    ft.Text("Aircraft 3",),
                    ft.Text("Aircraft 4",),
                ],
                width=200
            ),
            ft.Column(
                [
            
                    ft.Text("Book with Chopper Aviation", size=30, weight=ft.FontWeight.BOLD),
                    ft.Container(height=20),

                
                    
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ]),
        expand=True
    )