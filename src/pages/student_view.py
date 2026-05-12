''' Main view for the students '''

import flet as ft
import datetime
import calendar as cal_module



def StudentViewPage():
    selected_tab,  set_selected_tab  = ft.use_state(0)
    current_year,  set_current_year  = ft.use_state(datetime.date.today().year)
    current_month, set_current_month = ft.use_state(datetime.date.today().month)

    # ── Mock data  (replace with DB calls) ────────────────────────────────
    student_name = "John Doe"

    # Days the student has already booked
    booked_days = {5, 12}
    # Days currently available to book
    available_days = {7, 8, 9, 14, 15, 16, 19, 20, 21, 22, 28, 29}

    instructors = ["Tom Williams", "Steven Jones", "Kevin Smith"]
    aircraft_list = [
        "Cessna 172 (N1234A)",
        "Piper PA-28 (N5678B)",
        "Robinson R22 (N9012C)",
    ]
    time_slots = [
        "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
        "1:00 PM", "2:00 PM", "3:00 PM",  "4:00 PM",
    ]
    my_bookings = [
        {"date": "May 5",  "time": "9:00–11:00 AM", "instructor": "Kevin Smith", "aircraft": "Cessna 172",  "type": "Flight Lesson"},
        {"date": "May 12", "time": "1:00–3:00 PM",  "instructor": "None",        "aircraft": "N/A",         "type": "Ground School"},
    ]

    # ── Month navigation ──────────────────────────────────────────────────
    def _prev_month():
        if current_month == 1:
            set_current_month(12)
            set_current_year(current_year - 1)
        else:
            set_current_month(current_month - 1)

    def _next_month():
        if current_month == 12:
            set_current_month(1)
            set_current_year(current_year + 1)
        else:
            set_current_month(current_month + 1)

    # ── Booking dialog ────────────────────────────────────────────────────
    def _open_booking_dialog(day: int):
        date_str = datetime.date(current_year, current_month, day).strftime("%B %d, %Y")

        def confirm(dlg):
            # TODO: validate fields, save to DB, trigger confirmation email
            ft.context.page.pop_dialog()
            sb = ft.SnackBar(
                ft.Text("Booking confirmed! A confirmation email has been sent."),
                bgcolor=ft.Colors.GREEN,
            )
            ft.context.page.snack_bar = sb
            sb.open = True
            ft.context.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Book a Session  —  {date_str}"),
            content=ft.Column([
                ft.Dropdown(
                    label="Session Type",
                    options=[
                        ft.dropdown.Option("Ground School"),
                        ft.dropdown.Option("Flight Lesson"),
                        ft.dropdown.Option("Aircraft Rental (Solo)"),
                        ft.dropdown.Option("Checkride Prep"),
                    ],
                    hint_text="Select a session type",
                ),
                ft.Dropdown(
                    label="Start Time",
                    options=[ft.dropdown.Option(t) for t in time_slots],
                    hint_text="Select a start time",
                ),
                ft.Dropdown(
                    label="Instructor (optional)",
                    options=[ft.dropdown.Option("None — Solo")] +
                            [ft.dropdown.Option(i) for i in instructors],
                    hint_text="Select an instructor",
                ),
                ft.Dropdown(
                    label="Aircraft (optional)",
                    options=[ft.dropdown.Option("None")] +
                            [ft.dropdown.Option(a) for a in aircraft_list],
                    hint_text="Select an aircraft",
                ),
                ft.Container(
                    ft.Text(
                        "A confirmation email will be sent after booking.\n"
                        "A reminder will be sent 1 hour before your session.",
                        size=12, color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                    border_radius=8, padding=10,
                ),
            ], tight=True, spacing=12),
            actions=[
                ft.TextButton("Cancel", on_click=lambda: ft.context.page.pop_dialog()),
                ft.ElevatedButton("Confirm Booking", on_click=lambda d=dlg: confirm(d)),
            ],
        )
        ft.context.page.show_dialog(dlg)

    # ── Monthly calendar ──────────────────────────────────────────────────
    def _build_calendar():
        month_cal  = cal_module.monthcalendar(current_year, current_month)
        month_name = cal_module.month_name[current_month]
        today      = datetime.date.today()

        day_headers = ft.Row([
            ft.Container(
                ft.Text(d, size=11, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                        text_align=ft.TextAlign.CENTER),
                width=44, alignment=ft.alignment.center,
            )
            for d in ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        ])

        week_rows = []
        for week in month_cal:
            day_cells = []
            for day in week:
                if day == 0:
                    day_cells.append(ft.Container(width=44, height=44))
                    continue

                day_date     = datetime.date(current_year, current_month, day)
                is_today     = day_date == today
                is_past      = day_date < today
                is_booked    = day in booked_days
                is_available = day in available_days and not is_past

                if is_today:
                    bg, fg, clickable = ft.Colors.PRIMARY, ft.Colors.WHITE, True
                elif is_booked:
                    bg, fg, clickable = ft.Colors.TERTIARY_CONTAINER, ft.Colors.ON_SURFACE, False
                elif is_available:
                    bg, fg, clickable = ft.Colors.SECONDARY_CONTAINER, ft.Colors.ON_SECONDARY_CONTAINER, True
                else:
                    bg, fg, clickable = None, ft.Colors.ON_SURFACE_VARIANT, False

                tip = "Click to book" if clickable and not is_booked else (
                      "Already booked" if is_booked else None)

                day_cells.append(
                    ft.Container(
                        ft.Text(str(day), size=13, color=fg,
                                text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.W_500 if is_today else None),
                        width=44, height=44,
                        bgcolor=bg, border_radius=22,
                        alignment=ft.alignment.center,
                        ink=clickable,
                        tooltip=tip,
                        on_click=(lambda d=day: _open_booking_dialog(d)) if clickable else None,
                    )
                )
            week_rows.append(ft.Row(day_cells, spacing=4))

        legend = ft.Row([
            ft.Container(width=12, height=12, bgcolor=ft.Colors.SECONDARY_CONTAINER, border_radius=6),
            ft.Text("Available",    size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Container(width=12, height=12, bgcolor=ft.Colors.TERTIARY_CONTAINER, border_radius=6),
            ft.Text("Booked",       size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Container(width=12, height=12, bgcolor=ft.Colors.PRIMARY,            border_radius=6),
            ft.Text("Today",        size=11, color=ft.Colors.ON_SURFACE_VARIANT),
        ], spacing=6)

        return ft.Column([
            ft.Row([
                ft.IconButton(ft.Icons.CHEVRON_LEFT,  on_click=lambda: _prev_month()),
                ft.Text(f"{month_name} {current_year}", weight=ft.FontWeight.BOLD,
                        size=18, expand=True, text_align=ft.TextAlign.CENTER),
                ft.IconButton(ft.Icons.CHEVRON_RIGHT, on_click=lambda: _next_month()),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Divider(),
            day_headers,
            ft.Column(week_rows, spacing=4),
            ft.Container(height=6),
            legend,
        ], spacing=4)

    # ── Sidebar helpers ───────────────────────────────────────────────────
    def _get_pricing():
        rates = [
            ("Ground School",          50.00),
            ("Aircraft Rental (Solo)", 100.00),
            ("Aircraft + Instructor",  150.00),
            ("Checkride Prep",         175.00),
        ]
        return [ft.Text(f"{name} – ${cost:.0f}/hr", size=13) for name, cost in rates]

    def _get_instructors():
        data = [
            ("Tom Williams",  "Tue–Sat 10am–6pm"),
            ("Steven Jones",  "Mon–Fri  9am–5pm"),
            ("Kevin Smith",   "Mon–Fri  9am–5pm"),
        ]
        return [
            ft.ExpansionTile(
                name,
                [
                    ft.Row([ft.Text("Schedule:", italic=True, size=12),
                            ft.Text(schedule, size=12)],
                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ],
                dense=True,
                collapsed_bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                shape=ft.RoundedRectangleBorder(radius=4),
                collapsed_shape=ft.RoundedRectangleBorder(radius=4),
                controls_padding=ft.Padding.symmetric(horizontal=10, vertical=2),
            )
            for name, schedule in data
        ]

    def _get_aircraft():
        data = [
            ("Cessna 172",   "Fixed-Wing",  4),
            ("Piper PA-28",  "Fixed-Wing",  4),
            ("Robinson R22", "Helicopter",  2),
        ]
        return [
            ft.ExpansionTile(
                name,
                [
                    ft.Row([ft.Text("Type:",  italic=True, size=12), ft.Text(ac_type, size=12)],
                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([ft.Text("Seats:", italic=True, size=12), ft.Text(str(seats), size=12)],
                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ],
                dense=True,
                collapsed_bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                shape=ft.RoundedRectangleBorder(radius=4),
                collapsed_shape=ft.RoundedRectangleBorder(radius=4),
                controls_padding=ft.Padding.symmetric(horizontal=10, vertical=2),
            )
            for name, ac_type, seats in data
        ]

    # ── Tab: Book ─────────────────────────────────────────────────────────
    def _build_book():
        sidebar = ft.Container(
            ft.Column(
                [ft.Text("Pricing", size=14, color=ft.Colors.ON_SURFACE_VARIANT, italic=True)]
                + _get_pricing()
                + [ft.Divider(),
                   ft.Text("Instructors", size=14, color=ft.Colors.ON_SURFACE_VARIANT, italic=True)]
                + _get_instructors()
                + [ft.Divider(),
                   ft.Text("Aircraft", size=14, color=ft.Colors.ON_SURFACE_VARIANT, italic=True)]
                + _get_aircraft(),
                spacing=6,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=220,
        )

        main_area = ft.Column([
            ft.Text("Select an available date to book",
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                    weight=ft.FontWeight.BOLD),
            ft.Divider(),
            _build_calendar(),
        ], expand=True, scroll=ft.ScrollMode.AUTO)

        return ft.Row([
            sidebar,
            ft.VerticalDivider(width=1),
            ft.Container(main_area, expand=True,
                         padding=ft.Padding.only(left=16)),
        ], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)

    # ── Tab: My Bookings ──────────────────────────────────────────────────
    def _build_my_bookings():
        if not my_bookings:
            return ft.Column([
                ft.Text("My Bookings",
                        theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                        weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Container(
                    ft.Column([
                        ft.Icon(ft.Icons.EVENT, size=48, color=ft.Colors.ON_SURFACE_VARIANT),
                        ft.Text("No upcoming bookings",
                                size=16, color=ft.Colors.ON_SURFACE_VARIANT),
                        ft.Text("Tap a highlighted date on the calendar to get started.",
                                size=13, color=ft.Colors.ON_SURFACE_VARIANT),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    alignment=ft.alignment.center, expand=True,
                ),
            ], spacing=8, expand=True)

        cards = [
            ft.Container(
                ft.Row([
                    ft.Container(
                        ft.Icon(
                            ft.Icons.FLIGHT_TAKEOFF if "Flight" in b["type"] else ft.Icons.SCHOOL,
                            color=ft.Colors.PRIMARY, size=22,
                        ),
                        bgcolor=ft.Colors.PRIMARY_CONTAINER,
                        border_radius=8, padding=10,
                    ),
                    ft.Column([
                        ft.Text(b["type"],  weight=ft.FontWeight.W_600),
                        ft.Text(f"{b['date']}  ·  {b['time']}",
                                size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                        ft.Text(f"Instructor: {b['instructor']}  ·  Aircraft: {b['aircraft']}",
                                size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ], spacing=2, expand=True),
                    ft.TextButton("Cancel",
                                  style=ft.ButtonStyle(color=ft.Colors.ERROR)),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                border_radius=10,
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            )
            for b in my_bookings
        ]

        return ft.Column([
            ft.Text("My Bookings",
                    theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"{len(my_bookings)} upcoming booking(s)",
                    size=13, color=ft.Colors.ON_SURFACE_VARIANT),
        ] + cards, spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)

    # ── Tab: Account ──────────────────────────────────────────────────────
    def _build_account():
        def open_change_password():
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Change Password"),
                content=ft.Column([
                    ft.TextField(label="Current Password", password=True, can_reveal_password=True),
                    ft.TextField(label="New Password",     password=True, can_reveal_password=True),
                    ft.TextField(label="Confirm Password", password=True, can_reveal_password=True),
                ], tight=True, spacing=12),
                actions=[
                    ft.TextButton("Cancel",   on_click=lambda: ft.context.page.pop_dialog()),
                    ft.ElevatedButton("Save", on_click=lambda: ft.context.page.pop_dialog()),  # TODO: persist
                ],
            )
            ft.context.page.show_dialog(dlg)

        return ft.Column([
            ft.Text("Account",
                    theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Container(
                ft.Row([
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=52, color=ft.Colors.PRIMARY),
                    ft.Column([
                        ft.Text(student_name,
                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                weight=ft.FontWeight.BOLD),
                        ft.Text("Flight Student", size=13,
                                color=ft.Colors.ON_SURFACE_VARIANT),
                    ], spacing=2),
                ], spacing=16, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                border_radius=12, padding=20,
            ),
            ft.Container(height=8),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOCK),
                title=ft.Text("Change Password"),
                subtitle=ft.Text("Update your login password"),
                trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                on_click=lambda: open_change_password(),
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.ERROR),
                title=ft.Text("Log Out", color=ft.Colors.ERROR),
                trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                on_click=lambda: ft.context.page.navigate("/"),
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        ], spacing=4, scroll=ft.ScrollMode.AUTO, expand=True)

    # ── Layout ────────────────────────────────────────────────────────────
    tabs = [_build_book, _build_my_bookings, _build_account]
    current_content = tabs[selected_tab]()

    return ft.SafeArea(
        ft.Column([
            # App bar
            ft.Container(
                ft.Row([
                    ft.Icon(ft.Icons.FLIGHT, color=ft.Colors.PRIMARY),
                    ft.Text("Chopper Aviation", weight=ft.FontWeight.BOLD, size=18),
                    ft.Container(expand=True),
                    ft.Text(f"Welcome, {student_name.split()[0]}",
                            size=13, color=ft.Colors.ON_SURFACE_VARIANT),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.Padding.symmetric(horizontal=16, vertical=8),
            ),
            # Content
            ft.Container(
                current_content, expand=True,
                padding=ft.Padding.symmetric(horizontal=16, vertical=8),
            ),
            # Bottom nav
            ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(
                        icon=ft.Icons.EVENT,
                        selected_icon=ft.Icons.EVENT,
                        label="Book",
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.LIST_ALT,
                        selected_icon=ft.Icons.LIST_ALT,
                        label="My Bookings",
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.PERSON,
                        selected_icon=ft.Icons.PERSON,
                        label="Account",
                    ),
                ],
                selected_index=selected_tab,
                on_change=lambda e: set_selected_tab(int(e.data)),
            ),
        ], expand=True),
        minimum_padding=0,
        expand=True,
    )

    instructor = ""     # Instructor student has selected to book with
    aircraft = ""       # Aircraft student has selected to book

    today = datetime.datetime.today()

    
    def _get_pricing() -> list[ft.Control]:
        ''' Gets our pricing from the database and returns it as a list of controls '''

        # Get pricing from database
        # TODO: Go through pricing, return list of controls with pricing info

        return [
            ft.Text("Ground School - $50/hr"),
            ft.Text("Aircraft booking - $100/hr"),
            ft.Text("Aircraft with instructor booking - $150/hr"),
        ]

    def _get_instructors() -> list[ft.Control]:
        ''' Gets our instructors from the database and returns it as a list of controls '''
        instructors = ["Tom", "Steven", "Kevin"]     # TODO: Get list of instructors from database
        instructor_controls = []

        
        for instructor in instructors:
            #TODO: Get schedule for each instructor, add to expansion tile. Add small about section
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
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH, shape=ft.RoundedRectangleBorder(radius=4),
                    collapsed_shape=ft.RoundedRectangleBorder(radius=4),
                    controls_padding=ft.Padding.symmetric(horizontal=10, vertical=2)
                )
            )
        return instructor_controls
    
    def _get_aircrafts() -> list[ft.Control]:
        ''' Gets our aircraft from the database and returns it as a list of controls '''
        aircrafts = ["Aircraft 1", "Aircraft 2", "Aircraft 3", "Aircraft 4"]     # TODO: Get list of aircraft from database
        aircraft_controls = []

        # Go through aircraft, return list of controls with their name and schedule
        # Aircraft 1, Aircraft 2, Aircraft 3, Aircraft 4

        for aircraft in aircrafts:
            aircraft_controls.append(
                ft.ExpansionTile(
                    aircraft,
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
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH, shape=ft.RoundedRectangleBorder(radius=4),
                    collapsed_shape=ft.RoundedRectangleBorder(radius=4),
                    controls_padding=ft.Padding.symmetric(horizontal=10, vertical=2)
                )
            )

        return aircraft_controls
    
    def _get_equipment() -> list[ft.Control]:
        ''' Gets our equipment from the database and returns it as a list of controls '''
        equipment = ["Headset", "Flight Bag", "Kneeboard"]     # TODO: Get list of equipment from database
        equipment_controls = []

        # Go through equipment, return list of controls with their name and schedule

        for item in equipment:
            equipment_controls.append(
                ft.Text(item)
            )

        return equipment_controls
    

    #ft.context.page.show_dialog(date_picker)

    # TODO: Select either 1 instructor, 1 aircraft, or both
    # Handle time picker seperately

    return ft.SafeArea(
        ft.Column(
            [
        
                ft.Text("Book with Chopper Aviation", theme_style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD),
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