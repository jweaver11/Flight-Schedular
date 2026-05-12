''' Main view for instructors '''

import flet as ft
import datetime
import calendar as cal_module


def _open_dialog(dialog):
    if dialog not in ft.context.page.overlay:
        ft.context.page.overlay.append(dialog)
    dialog.open = True
    ft.context.page.update()


def _close_dialog(dialog):
    dialog.open = False
    ft.context.page.update()


def InstructorViewPage():
    selected_tab,  set_selected_tab  = ft.use_state(0)
    current_year,  set_current_year  = ft.use_state(datetime.date.today().year)
    current_month, set_current_month = ft.use_state(datetime.date.today().month)

    # ── Mock data  (replace with DB calls) ────────────────────────────────
    instructor_name = "Kevin Smith"

    # Days in the current month that have bookings
    booked_days = {5, 7, 12, 14, 19, 21}

    upcoming_sessions = [
        {"student": "John Doe",     "date": "May 14", "time": "9:00–11:00 AM",    "type": "Flight Lesson",  "aircraft": "Cessna 172"},
        {"student": "Jane Smith",   "date": "May 14", "time": "1:00–3:00 PM",     "type": "Ground School",  "aircraft": "N/A"},
        {"student": "Mike Johnson", "date": "May 19", "time": "10:00 AM–12:00 PM","type": "Flight Lesson",  "aircraft": "Piper PA-28"},
        {"student": "Sarah Lee",    "date": "May 21", "time": "2:00–4:00 PM",     "type": "Checkride Prep", "aircraft": "Cessna 172"},
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
                is_today  = datetime.date(current_year, current_month, day) == today
                is_booked = day in booked_days
                bg    = ft.Colors.PRIMARY           if is_today  else (ft.Colors.SECONDARY_CONTAINER if is_booked else None)
                fg    = ft.Colors.WHITE             if is_today  else (ft.Colors.ON_SECONDARY_CONTAINER if is_booked else None)
                tip   = "Booking on this day"       if is_booked else None
                day_cells.append(
                    ft.Container(
                        ft.Text(str(day), size=13, color=fg,
                                text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.W_500 if is_today else None),
                        width=44, height=44,
                        bgcolor=bg, border_radius=22,
                        alignment=ft.alignment.center,
                        tooltip=tip,
                    )
                )
            week_rows.append(ft.Row(day_cells, spacing=4))

        legend = ft.Row([
            ft.Container(width=12, height=12, bgcolor=ft.Colors.PRIMARY,            border_radius=6),
            ft.Text("Today",   size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Container(width=12, height=12, bgcolor=ft.Colors.SECONDARY_CONTAINER, border_radius=6),
            ft.Text("Booking", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
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

    # ── Tab: My Schedule ──────────────────────────────────────────────────
    def _build_schedule():
        def open_time_off():
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Request Time Off"),
                content=ft.Column([
                    ft.Text("Mark a date range as unavailable for bookings.",
                            size=13, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.TextField(label="Start Date  (YYYY-MM-DD)"),
                    ft.TextField(label="End Date    (YYYY-MM-DD)"),
                    ft.TextField(label="Reason (optional)"),
                ], tight=True, spacing=12),
                actions=[
                    ft.TextButton("Cancel",    on_click=lambda: _close_dialog(dlg)),
                    ft.ElevatedButton("Submit",on_click=lambda: _close_dialog(dlg)),  # TODO: persist
                ],
            )
            _open_dialog(dlg)

        return ft.Column([
            ft.Row([
                ft.Text("My Schedule",
                        theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                        weight=ft.FontWeight.BOLD),
                ft.OutlinedButton("Request Time Off", icon=ft.Icons.EVENT_BUSY,
                                  on_click=lambda: open_time_off()),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            _build_calendar(),
        ], spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)

    # ── Tab: Upcoming Sessions ────────────────────────────────────────────
    def _build_sessions():
        cards = [
            ft.Container(
                ft.Row([
                    ft.Container(
                        ft.Icon(
                            ft.Icons.FLIGHT_TAKEOFF if "Flight" in s["type"] else ft.Icons.SCHOOL,
                            color=ft.Colors.PRIMARY, size=22,
                        ),
                        bgcolor=ft.Colors.PRIMARY_CONTAINER,
                        border_radius=8, padding=10,
                    ),
                    ft.Column([
                        ft.Text(s["student"], weight=ft.FontWeight.W_600),
                        ft.Text(f"{s['type']}  ·  {s['aircraft']}",
                                size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                        ft.Text(f"{s['date']}  ·  {s['time']}",
                                size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ], spacing=2, expand=True),
                    ft.IconButton(ft.Icons.CANCEL, tooltip="Cancel session",
                                  icon_color=ft.Colors.ERROR),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                border_radius=10,
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            )
            for s in upcoming_sessions
        ]

        return ft.Column([
            ft.Text("Upcoming Sessions",
                    theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"{len(upcoming_sessions)} sessions scheduled",
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
                    ft.TextButton("Cancel",   on_click=lambda: _close_dialog(dlg)),
                    ft.ElevatedButton("Save", on_click=lambda: _close_dialog(dlg)),  # TODO: persist
                ],
            )
            _open_dialog(dlg)

        return ft.Column([
            ft.Text("Account",
                    theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Container(
                ft.Row([
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=52, color=ft.Colors.PRIMARY),
                    ft.Column([
                        ft.Text(instructor_name,
                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                weight=ft.FontWeight.BOLD),
                        ft.Text("Flight Instructor", size=13,
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
    tabs = [_build_schedule, _build_sessions, _build_account]
    current_content = tabs[selected_tab]()

    return ft.SafeArea(
        ft.Column([
            # App bar
            ft.Container(
                ft.Row([
                    ft.Icon(ft.Icons.FLIGHT, color=ft.Colors.PRIMARY),
                    ft.Text("Chopper Aviation", weight=ft.FontWeight.BOLD, size=18),
                    ft.Container(expand=True),
                    ft.Text(f"Welcome, {instructor_name.split()[0]}",
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
                        icon=ft.Icons.DATE_RANGE,
                        selected_icon=ft.Icons.DATE_RANGE,
                        label="Schedule",
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.LIST_ALT,
                        selected_icon=ft.Icons.LIST_ALT,
                        label="Sessions",
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