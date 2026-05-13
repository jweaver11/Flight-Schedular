''' Main view for instructors '''

import flet as ft
import datetime
from services.db import (
    bookings_col, students_col, instructors_col, aircrafts_col, equipment_col,
    cancel_booking, add_booking,
)

def InstructorViewPage(page: ft.Page):

    # ── Load data ──────────────────────────────────────────────────────────
    bookings_raw = list(bookings_col().find(
        {},
        {
            "date": 1, "time": 1, "duration": 1, "type": 1, "status": 1,
            "students": 1, "student": 1,
            "instructors": 1, "instructor": 1,
            "aircrafts": 1, "aircraft": 1,
            "equipment": 1,
            "instructor_time_off": 1, "aircraft_maintenance": 1,
        }
    ))
    for _b in bookings_raw:
        _b["_id"] = str(_b.get("_id", ""))
    bookings = bookings_raw

    students_list    = list(students_col().find({},   {"_id": 0, "name": 1, "email": 1}))
    instructors_list = list(instructors_col().find({}, {"_id": 0, "name": 1, "email": 1}))
    aircraft_list    = list(aircrafts_col().find({},  {"_id": 0, "name": 1, "type": 1}))
    equipment_list   = list(equipment_col().find({},  {"_id": 0, "name": 1, "count": 1}))

    today             = datetime.date.today()
    today_str         = today.isoformat()
    current_user      = page.session.store.get("user") or {}
    current_user_name = current_user.get("name", "")

    # ── Shared helpers ─────────────────────────────────────────────────────
    def _to_list(v):
        if isinstance(v, list): return v
        return [v] if v else []

    def _fmt_list(v):
        items = _to_list(v)
        return ", ".join(str(i) for i in items) if items else "N/A"

    def _is_my_booking(b):
        instructors_val = b.get("instructors") or b.get("instructor")
        return current_user_name in _to_list(instructors_val)

    def _show_success(msg: str):
        page.show_dialog(ft.SnackBar(
            ft.Text(msg, color=ft.Colors.ON_SURFACE),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            shape=ft.RoundedRectangleBorder(ft.BorderSide(2, ft.Colors.GREEN), radius=8),
        ))

    def _show_error(msg: str):
        page.show_dialog(ft.SnackBar(
            ft.Text(msg, color=ft.Colors.ON_SURFACE),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            shape=ft.RoundedRectangleBorder(ft.BorderSide(2, ft.Colors.RED), radius=8),
        ))

    def _list_card(content):
        return ft.Container(
            content,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=8,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        )

    # ── Filtered lists ─────────────────────────────────────────────────────
    your_upcoming = [
        b for b in bookings
        if b.get("status") != "cancelled"
        and _is_my_booking(b)
        and b.get("date", "") >= today_str
    ]
    all_future = [
        b for b in bookings
        if b.get("status") != "cancelled" and b.get("date", "") >= today_str
    ]
    all_past = [
        b for b in bookings
        if b.get("status") != "cancelled" and b.get("date", "") < today_str
    ]
    all_cancelled = [b for b in bookings if b.get("status") == "cancelled"]

    # ── Cancel booking ─────────────────────────────────────────────────────
    async def _cancel_booking_fn(e: ft.Event):
        booking = e.control.data

        async def _confirm(e=None):
            cancel_booking(booking["_id"])
            page.pop_dialog()
            _show_success("Booking cancelled.")
            await page.push_route("/view_selector")

        page.show_dialog(ft.AlertDialog(
            title="Cancel this booking?",
            actions=[
                ft.Button("Keep",           on_click=lambda: page.pop_dialog()),
                ft.Button("Cancel Booking", on_click=_confirm),
            ],
        ))

    # ── Booking card ───────────────────────────────────────────────────────
    def _booking_card(b, show_cancel=False):
        students_v    = _fmt_list(b.get("students")    or b.get("student"))
        instructors_v = _fmt_list(b.get("instructors") or b.get("instructor"))
        aircrafts_v   = _fmt_list(b.get("aircrafts")   or b.get("aircraft"))
        equipment_v   = _fmt_list(b.get("equipment"))
        booking_type  = b.get("type", "")
        is_time_off   = b.get("instructor_time_off", False)
        is_maint      = b.get("aircraft_maintenance", False)

        tag_row = ft.Row(
            [
                ft.Text(f"{b.get('date', '')}  {b.get('time', '')}", weight=ft.FontWeight.W_500),
                *(
                    [ft.Container(
                        ft.Text("Time Off", size=10, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.ORANGE, border_radius=4, padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                    )] if is_time_off else []
                ),
                *(
                    [ft.Container(
                        ft.Text("Maintenance", size=10, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.BLUE, border_radius=4, padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                    )] if is_maint else []
                ),
            ],
            spacing=8, wrap=True,
        )

        detail_col = ft.Column([
            tag_row,
            ft.Text(f"Students: {students_v}",       size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(f"Instructors: {instructors_v}",  size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(f"Aircraft: {aircrafts_v}",       size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(f"Equipment: {equipment_v}",      size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(f"Type: {booking_type}",          size=12, color=ft.Colors.ON_SURFACE_VARIANT)
            if booking_type else ft.Container(height=0),
        ], spacing=3, expand=True)

        return _list_card(ft.Row(
            [
                detail_col,
                ft.Button("Cancel", on_click=_cancel_booking_fn, data=b)
                if show_cancel else ft.Container(width=0),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ))

    def _booking_section(title, items, show_cancel=False):
        rows = (
            [_booking_card(b, show_cancel) for b in items]
            if items else
            [ft.Text("None.", color=ft.Colors.ON_SURFACE_VARIANT, size=12)]
        )
        return [
            ft.Text(title, theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                    weight=ft.FontWeight.W_600),
            ft.Divider(),
            *rows,
            ft.Container(height=16),
        ]

    # ── Add booking dialog ─────────────────────────────────────────────────
    async def _add_booking(e):
        date_f     = ft.TextField(label="Date (YYYY-MM-DD)", hint_text="2026-06-15", expand=True)
        time_f     = ft.TextField(label="Time (HH:MM)",      hint_text="09:00",      expand=True)
        duration_f = ft.TextField(label="Duration (min)",    value="60",             expand=True,
                                   keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter(),)
        type_f     = ft.TextField(label="Lesson Type", hint_text="Discovery Flight, Solo, Checkride…")
        time_off_cb = ft.Checkbox(label="Mark as Instructor Time Off",   value=False)
        maint_cb    = ft.Checkbox(label="Mark as Aircraft Maintenance",  value=False)

        # Pre-check the current user as an instructor
        instructor_checks = [
            ft.Checkbox(label=i["name"], value=(i["name"] == current_user_name), data=i["name"])
            for i in instructors_list
        ]
        student_checks  = [ft.Checkbox(label=s["name"],  value=False, data=s["name"])  for s in students_list]
        aircraft_checks = [ft.Checkbox(label=a["name"],  value=False, data=a["name"])  for a in aircraft_list]
        equipment_checks = [
            ft.Checkbox(label=f"{eq['name']} (qty: {eq.get('count', 0)})", value=False, data=eq["name"])
            for eq in equipment_list
        ]

        def _checked(checks):
            return [c.data for c in checks if c.value]

        def _multi_section(title, checks):
            body = (
                ft.Column(checks, spacing=0)
                if checks else
                ft.Text("None available.", size=12, color=ft.Colors.ON_SURFACE_VARIANT)
            )
            return ft.Column([
                ft.Text(title, weight=ft.FontWeight.W_600, size=13),
                body,
            ], spacing=4)

        async def _confirm_booking(e=None):
            if not date_f.value or not time_f.value:
                _show_error("Date and time are required.")
                return
            try:
                dur = int(duration_f.value or 60)
            except ValueError:
                _show_error("Duration must be a whole number.")
                return

            page.pop_dialog()
            try:
                add_booking(
                    date=date_f.value.strip(),
                    time=time_f.value.strip(),
                    duration=dur,
                    students=_checked(student_checks),
                    instructors=_checked(instructor_checks),
                    aircrafts=_checked(aircraft_checks),
                    equipment=_checked(equipment_checks),
                    type=type_f.value.strip(),
                    instructor_time_off=time_off_cb.value,
                    aircraft_maintenance=maint_cb.value,
                )
                await page.push_route("/view_selector")
                _show_success("Booking created successfully.")
            except ValueError as ex:
                _show_error(str(ex))

        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("Schedule Booking"),
            content=ft.Container(
                ft.Column([
                    ft.Container(height=10),
                    ft.Row([date_f, time_f, duration_f], spacing=8),
                    type_f,
                    ft.Divider(),
                    _multi_section("Students",    student_checks),
                    _multi_section("Instructors", instructor_checks),
                    _multi_section("Aircraft",    aircraft_checks),
                    _multi_section("Equipment",   equipment_checks),
                    ft.Divider(),
                    time_off_cb,
                    maint_cb,
                ], spacing=12, scroll=ft.ScrollMode.AUTO),
                width=540,
                height=500,
            ),
            actions=[
                ft.Button("Cancel",  on_click=lambda: page.pop_dialog()),
                ft.Button("Confirm", on_click=_confirm_booking),
            ],
        ))

    # ── Main layout ────────────────────────────────────────────────────────
    def _get_bookings():
        return ft.Column([
            *_booking_section("Your Upcoming Bookings", your_upcoming,  show_cancel=True),
            *_booking_section("All Upcoming Bookings",  all_future,     show_cancel=False),
            *_booking_section("All Past Bookings",      all_past,       show_cancel=False),
            *_booking_section("All Cancelled Bookings", all_cancelled,  show_cancel=False),
        ], expand=True, scroll=ft.ScrollMode.AUTO, spacing=4)
    
    instructor_name = current_user.get("name", "Instructor")

    #TODO: 
    # - Instructors edit schedule
    # - Fix booking available dates and times check based on included instructor, equip, and aircraft

    async def _edit_schedule(e):

        async def _confirm_schedule(e=None):
            pass

        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("Schedule Booking"),
            content=ft.Container(
                ft.Column([
                    ft.Container(height=10),
                    #ft.Row([date_f, time_f, duration_f], spacing=8),
                    
                ], spacing=12, scroll=ft.ScrollMode.AUTO),
                width=540,
                height=500,
            ),
            actions=[
                ft.Button("Cancel",  on_click=lambda: page.pop_dialog()),
                ft.Button("Confirm", on_click=_confirm_schedule),
            ],
        ))

    return ft.SafeArea(
        ft.Column([
            ft.Container(height=10),
            ft.Row([
                ft.Text(f"Bookings for {instructor_name}", theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                        weight=ft.FontWeight.BOLD, expand=True),
                ft.Button("Edit Schedule", icon=ft.Icons.ADD, on_click=_edit_schedule),
                ft.Button("Add Booking", icon=ft.Icons.ADD, on_click=_add_booking),
            ]),
            ft.Divider(),
            ft.Container(_get_bookings(), padding=ft.Padding.symmetric(horizontal=20), expand=True),
        ], expand=True, scroll=ft.ScrollMode.ALWAYS),
    )
