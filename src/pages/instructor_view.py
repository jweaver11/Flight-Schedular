''' Main view for instructors '''

import flet as ft

#TODO: Ability to view and edit schedule that has bookings including them. 
# abilty to mark 1 or more days off and change their schedule
# Ability to book for themselves, duhhh
@ft.component
def InstructorViewPage():
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