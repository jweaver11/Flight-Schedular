''' Main view for the students'''

import flet as ft

@ft.component
def StudentViewPage():

    instructor = ""     # Instructor student has selected to book with
    aircraft = ""       # aircraft student has selected to book

    # Grab schedules here

    def _get_pricing() -> list[ft.Control]:

        # TODO: Go through pricing, return list of controls with pricing info

        return [
            ft.Text("Ground School - $50/hr"),
            ft.Text("Aircraft booking - $100/hr"),
            ft.Text("Aircraft with instructor booking - $150/hr"),
        ]

    def _get_instructors() -> list[ft.Control]:
        instructors = ["Tom", "Steven", "Kevin"]     # TODO: Get list of instructors from database
        instructor_controls = []

        
        for instructor in instructors:
            #TODO: Get schedule for each instructor, add to expansion tile
            instructor_controls.append(
                ft.ExpansionTile(
                    instructor, 
                    [
                        ft.Row([ft.Text("Sunday:", italic=True), ft.Text("None")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Text("Monday:", italic=True), ft.Text("9am - 5pm")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Text("Tuesday:", italic=True), ft.Text("9am - 5pm")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Text("Wednesday:", italic=True), ft.Text("9am - 5pm")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Text("Thursday:", italic=True), ft.Text("9am - 5pm")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Text("Friday:", italic=True), ft.Text("9am - 5pm")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Text("Saturday:", italic=True), ft.Text("None")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ],
                        
                    dense=True, collapsed_bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH, shape=ft.RoundedRectangleBorder(radius=6),
                    collapsed_shape=ft.RoundedRectangleBorder(radius=6),
                    controls_padding=ft.Padding.symmetric(horizontal=10, vertical=2)
                )
            )
        return instructor_controls
    
    def _get_aircrafts() -> list[ft.Control]:

        # Go through aircraft, return list of controls with their name and schedule
        # Aircraft 1, Aircraft 2, Aircraft 3, Aircraft 4

        return [
            ft.Text("Aircraft 1"),
            ft.Text("Aircraft 2"),
            ft.Text("Aircraft 3"),
            ft.Text("Aircraft 4"),
        ]
    

    #ft.context.page.show_dialog(date_picker)

    # TODO: Select either 1 instructor, 1 aircraft, or both
    # Handle time picker seperately

    return ft.SafeArea(
        ft.Column(
            [
        
                ft.Text("Book with Chopper Aviation", size=30, weight=ft.FontWeight.BOLD),
                ft.Divider(),

                ft.Row(
                    [

                        ft.Column(
                            [
                                ft.Text("Pricing", size=18, color=ft.Colors.ON_SURFACE_VARIANT, italic=True)
                            ] + _get_pricing() +

                            [
                                ft.Divider(),
                                ft.Text("Instructors", size=18, color=ft.Colors.ON_SURFACE_VARIANT, italic=True),
                            ] + _get_instructors() +

                            [
                                ft.Divider(),
                                ft.Text("Aircrafts", size=18, color=ft.Colors.ON_SURFACE_VARIANT, italic=True),  
                            ] + _get_aircrafts(),
                            width=200, scroll=ft.ScrollMode.AUTO, 
                        ),

                        # Book stuff here

                    ], 
                    expand=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            #scroll=ft.ScrollMode.AUTO
        ),
        minimum_padding=50,
        expand=True
    )