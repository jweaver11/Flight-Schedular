''' Main view for the admin '''

import flet as ft
import datetime
from services.db import (
    students_col, instructors_col, aircrafts_col, equipment_col, pricing_col, bookings_col,
    delete_student, delete_instructor, delete_aircraft, delete_equipment, delete_pricing,
    cancel_booking, add_aircraft, add_equipment, add_pricing,
)
from services.auth import verify_login, register_instructor, EmailAlreadyExistsError
import asyncio

def AdminViewPage(page: ft.Page):

    # Load all our data so we can access it
    students_cursor = students_col().find({}, {"_id": 0, "name": 1, "email": 1})
    students = list(students_cursor)
    instructors_cursor = instructors_col().find({}, {"_id": 0, "name": 1, "email": 1, "schedule": 1})
    instructors = list(instructors_cursor)
    aircrafts_cursor = aircrafts_col().find({}, {"_id": 0, "name": 1, "type": 1, "capacity": 1})
    aircraft = list(aircrafts_cursor)
    equipment_cursor = equipment_col().find({}, {"_id": 0, "name": 1, "count": 1})
    equipment = list(equipment_cursor)
    pricing_cursor = pricing_col().find({}, {"_id": 0, "name": 1, "cost": 1})
    pricing = list(pricing_cursor)
    bookings_raw = list(bookings_col().find(
        {}, {"date": 1, "time": 1, "student": 1, "instructor": 1, "aircraft": 1, "type": 1, "status": 1}
    ))
    for _b in bookings_raw:
        _b["_id"] = str(_b.get("_id", ""))
    bookings = bookings_raw

    today = datetime.date.today()

    # ── Shared helper widgets ──────────────────────────────────────────────
    def _stat_card(label, value, icon):
        return ft.Container(
            ft.Column([
                ft.Icon(icon, size=28, color=ft.Colors.PRIMARY),
                ft.Text(value, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                        weight=ft.FontWeight.BOLD),
                ft.Text(label, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=12,
            padding=16,
            width=200,
            height=200,
        )

    def _list_card(content):
        return ft.Container(
            content,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=8,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        )

    def _section_header(title, btn_label, on_add):
        return ft.Row([
            ft.Text(title, theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    weight=ft.FontWeight.BOLD),
            ft.Button(btn_label, icon=ft.Icons.ADD, on_click=lambda: on_add()),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

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

    # ── Section: Dashboard ────────────────────────────────────────────────
    def _build_dashboard():
        today_str     = today.isoformat()
        next_week_str = (today + datetime.timedelta(days=7)).isoformat()
        upcoming = [
            b for b in bookings
            if b.get("status") != "cancelled"
            and today_str <= b.get("date", "") <= next_week_str
        ]
        booking_rows = (
            [_list_card(ft.Row([
                ft.Column([
                    ft.Text(b.get("student", "Unknown"), weight=ft.FontWeight.W_500),
                    ft.Text(
                        f"{b.get('instructor', 'N/A')}  ·  {b.get('aircraft', 'N/A')}",
                        size=12, color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                ], spacing=2, expand=True),
                ft.Column([
                    ft.Text(b.get("date", ""), size=12),
                    ft.Text(b.get("time", ""), size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ], spacing=2),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
               vertical_alignment=ft.CrossAxisAlignment.CENTER))
             for b in upcoming]
            if upcoming else
            [ft.Text("No upcoming bookings in the next 7 days.",
                     color=ft.Colors.ON_SURFACE_VARIANT, size=13)]
        )
        return ft.Column([
            ft.Text("Dashboard", theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([
                _stat_card("Total Students",    str(len(students)),    ft.Icons.REDUCE_CAPACITY),
                _stat_card("Total Instructors", str(len(instructors)), ft.Icons.PERSON),
                _stat_card("Total Aircraft",    str(len(aircraft)),    ft.Icons.FLIGHT),
            ], wrap=True, spacing=12, run_spacing=12),
            ft.Container(height=12),
            ft.Text("Upcoming Bookings — Next 7 Days",
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.W_600),
            ft.Divider(),
            *booking_rows,
        ], spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)

    # ── Section: Students ─────────────────────────────────────────────────
    def _build_students():

        async def _delete_student(e: ft.Event):
            ''' Confirms the deletion '''

            async def _confirm_delete(e: ft.Event=None): 
                ''' Deletes the student from the database'''

                #student = e.control.data
                delete_student(student["name"], student["email"])
                page.pop_dialog()
                page.show_dialog(
                    ft.SnackBar(
                        ft.Text(f"Student Successfully Deleted: {student['name']}", color=ft.Colors.ON_SURFACE), 
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                        shape=ft.RoundedRectangleBorder(ft.BorderSide(2, ft.Colors.GREEN), radius=8),
                    )
                )
                await page.push_route("/view_selector")  # Refresh the view to reflect changes

            student = e.control.data
            page.show_dialog(
                ft.AlertDialog(
                    title=f"Confirm Deletion of student: {student.get('name', "")}?",
                    actions=[
                        ft.Button("Cancel", on_click=lambda: page.pop_dialog()),
                        ft.Button("Delete", on_click=_confirm_delete),
                    ]
                )
            )
            pass

        return ft.Column([
            ft.Text("Students", theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    weight=ft.FontWeight.BOLD),
            ft.Divider(),
            _stat_card("Total Students", str(len(students)), ft.Icons.REDUCE_CAPACITY),
            ft.Divider(),
            ft.Row([
                _list_card(
                    ft.Container(
                        ft.Row([
                            ft.Text(student.get('name', 'N/A')),
                            ft.Text(student.get('email', 'N/A'), size=12, color=ft.Colors.ON_SURFACE_VARIANT, expand=True),
                            ft.Button("Delete Student", on_click=_delete_student, data=student),
                        ], spacing=20),
                        
                    ) 
                )for student in students
            ], expand=True, wrap=True)
        ], spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)

    # ── Section: Instructors ──────────────────────────────────────────────
    def _build_instructors():

        

        def open_add():

            async def _add_instructor(e: ft.Event=None):
                ''' Adds the instructor to the database '''

                
                progress_ring.visible = True
                progress_ring.update()    
                await asyncio.sleep(0)  # Allow UI to update before processing
      
                
                page.pop_dialog()
                try:
                    register_instructor(email_f.value, pwd_f.value, name=name_f.value)
                    page.pop_dialog()
                    await page.push_route("/view_selector")  # Refresh the view to reflect changes
                    page.show_dialog(
                        ft.SnackBar(
                            ft.Text(f"Instructor Created Successfully", color=ft.Colors.ON_SURFACE), 
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                            shape=ft.RoundedRectangleBorder(ft.BorderSide(2, ft.Colors.GREEN), radius=8),
                        )
                    )
                except EmailAlreadyExistsError:
                    progress_ring.visible = False
                    progress_ring.update()
                    page.show_dialog(
                        ft.SnackBar(
                            ft.Text(f"Error creating instructor. Email already in use", color=ft.Colors.ON_SURFACE), 
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                            shape=ft.RoundedRectangleBorder(ft.BorderSide(2, ft.Colors.RED), radius=8),
                        )
                    )
                    return
                

            name_f  = ft.TextField(label="Full Name")
            email_f = ft.TextField(label="Email")
            pwd_f   = ft.TextField(label="Password", password=True, can_reveal_password=True)
            progress_ring = ft.ProgressRing(visible=False)
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Add Instructor"),
                content=ft.Column([name_f, email_f, pwd_f, progress_ring], tight=True, spacing=12),
                actions=[
                    ft.Button("Cancel",  on_click=lambda: page.pop_dialog()),
                    ft.Button("Add", on_click=_add_instructor), 
                ],
            )
            page.show_dialog(dlg)

        async def _delete_instructor(e: ft.Event):
            ''' Confirms the deletion '''

            async def _confirm_delete(e: ft.Event=None): 
                ''' Deletes the instructor from the database'''

                #instructor = e.control.data
                delete_instructor(instructor["name"], instructor["email"])
                page.pop_dialog()
                page.show_dialog(
                    ft.SnackBar(
                        ft.Text(f"Instructor Successfully Deleted: {instructor['name']}", color=ft.Colors.ON_SURFACE), 
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                        shape=ft.RoundedRectangleBorder(ft.BorderSide(2, ft.Colors.GREEN), radius=8),
                    )
                )
                await page.push_route("/view_selector")  # Refresh the view to reflect changes

            instructor = e.control.data
            page.show_dialog(
                ft.AlertDialog(
                    title=f"Confirm Deletion of Instructor: {instructor.get('name', '')}?",
                    actions=[
                        ft.Button("Cancel", on_click=lambda: page.pop_dialog()),
                        ft.Button("Delete", on_click=_confirm_delete),
                    ]
                )
            )

        cards = [
            _list_card(ft.Row([
                    ft.Text(i["name"],     weight=ft.FontWeight.W_500),
                    ft.Text(i["email"],    size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Text(i["schedule"], size=12, color=ft.Colors.ON_SURFACE_VARIANT, expand=True),
                ft.Button("Delete Instructor", on_click=_delete_instructor, data=i),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER))
            for i in instructors
        ]
        return ft.Column(
            [_section_header("Instructors", "Add Instructor", open_add), ft.Divider()] + cards,
            spacing=8, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ── Section: Aircraft ─────────────────────────────────────────────────
    def _build_aircraft():
        def open_add():
            name_f     = ft.TextField(label="Name / Tail Number")
            type_f     = ft.TextField(label="Type / Model")
            capacity_f = ft.TextField(label="Seat Capacity", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter(),)
            weight_f   = ft.TextField(label="Weight Capacity (lbs)", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter(),)

            async def _add(e=None):
                try:
                    cap = int(capacity_f.value or 0)
                    wt  = float(weight_f.value or 0)
                except ValueError:
                    _show_error("Capacity and weight must be numbers.")
                    return
                page.pop_dialog()
                if add_aircraft(name_f.value.strip(), type_f.value.strip(), cap, wt):
                    await page.push_route("/view_selector")
                    _show_success(f"Aircraft Added: {name_f.value.strip()}")
                else:
                    _show_error("An aircraft with that name already exists.")

            page.show_dialog(ft.AlertDialog(
                modal=True,
                title=ft.Text("Add Aircraft"),
                content=ft.Column([name_f, type_f, capacity_f, weight_f], tight=True, spacing=12),
                actions=[
                    ft.Button("Cancel", on_click=lambda: page.pop_dialog()),
                    ft.Button("Add",    on_click=_add),
                ],
            ))

        async def _delete_aircraft_fn(e: ft.Event):
            async def _confirm(e=None):
                delete_aircraft(ac["name"])
                page.pop_dialog()
                _show_success(f"Aircraft Removed: {ac['name']}")
                await page.push_route("/view_selector")

            ac = e.control.data
            page.show_dialog(ft.AlertDialog(
                title=f"Remove aircraft: {ac.get('name', '')}?",
                actions=[
                    ft.Button("Cancel", on_click=lambda: page.pop_dialog()),
                    ft.Button("Remove", on_click=_confirm),
                ],
            ))

        cards = [
            _list_card(ft.Row([
                ft.Column([
                    ft.Text(a["name"], weight=ft.FontWeight.W_500),
                    ft.Text(f"{a.get('type', 'N/A')}  ·  {a.get('capacity', '?')} seats",
                            size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ], spacing=2, expand=True),
                ft.Button("Remove", on_click=_delete_aircraft_fn, data=a),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER))
            for a in aircraft
        ]
        return ft.Column(
            [_section_header("Aircraft", "Add Aircraft", open_add), ft.Divider()] + cards,
            spacing=8, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ── Section: Equipment ────────────────────────────────────────────────
    def _build_equipment():
        def open_add():
            name_f  = ft.TextField(label="Equipment Name")
            count_f = ft.TextField(label="Quantity", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter(),)

            async def _add(e=None):
                try:
                    count = int(count_f.value or 0)
                except ValueError:
                    _show_error("Quantity must be a number.")
                    return
                page.pop_dialog()
                add_equipment(name_f.value.strip(), count)
                await page.push_route("/view_selector")
                print("Added equi")
                _show_success(f"Equipment Added: {name_f.value.strip()}")

            page.show_dialog(ft.AlertDialog(
                modal=True,
                title=ft.Text("Add Equipment"),
                content=ft.Column([name_f, count_f], tight=True, spacing=12),
                actions=[
                    ft.Button("Cancel", on_click=lambda: page.pop_dialog()),
                    ft.Button("Add",    on_click=_add),
                ],
            ))

        async def _delete_equipment_fn(e: ft.Event):
            async def _confirm(e=None):
                delete_equipment(eq["name"])
                page.pop_dialog()
                _show_success(f"Equipment Removed: {eq['name']}")
                await page.push_route("/view_selector")

            eq = e.control.data
            page.show_dialog(ft.AlertDialog(
                title=f"Remove equipment: {eq.get('name', '')}?",
                actions=[
                    ft.Button("Cancel", on_click=lambda: page.pop_dialog()),
                    ft.Button("Remove", on_click=_confirm),
                ],
            ))

        cards = [
            _list_card(ft.Row([
                ft.Column([
                    ft.Text(eq["name"], weight=ft.FontWeight.W_500),
                    ft.Text(f"Qty: {eq.get('count', 0)}", size=12,
                            color=ft.Colors.ON_SURFACE_VARIANT),
                ], spacing=2, expand=True),
                ft.Button("Remove", on_click=_delete_equipment_fn, data=eq),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER))
            for eq in equipment
        ]
        return ft.Column(
            [_section_header("Equipment", "Add Equipment", open_add), ft.Divider()] + cards,
            spacing=8, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ── Section: Pricing ──────────────────────────────────────────────────
    def _build_pricing():
        def open_add():
            name_f = ft.TextField(label="Service Name")
            cost_f = ft.TextField(label="Rate ($/hr)", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter(),)

            async def _add(e=None):
                try:
                    cost = float(cost_f.value or 0)
                except ValueError:
                    _show_error("Rate must be a number.")
                    return
                page.pop_dialog()
                if add_pricing(name_f.value.strip(), cost):
                    await page.push_route("/view_selector")
                    _show_success(f"Pricing Added: {name_f.value.strip()}")
                else:
                    _show_error("A pricing entry with that name already exists.")

            page.show_dialog(ft.AlertDialog(
                modal=True,
                title=ft.Text("Add Pricing Rate"),
                content=ft.Column([name_f, cost_f], tight=True, spacing=12),
                actions=[
                    ft.Button("Cancel", on_click=lambda: page.pop_dialog()),
                    ft.Button("Add",    on_click=_add),
                ],
            ))

        async def _delete_pricing_fn(e: ft.Event):
            async def _confirm(e=None):
                delete_pricing(pr["name"])
                page.pop_dialog()
                _show_success(f"Pricing Removed: {pr['name']}")
                await page.push_route("/view_selector")

            pr = e.control.data
            page.show_dialog(ft.AlertDialog(
                title=f"Remove pricing: {pr.get('name', '')}?",
                actions=[
                    ft.Button("Cancel", on_click=lambda: page.pop_dialog()),
                    ft.Button("Remove", on_click=_confirm),
                ],
            ))

        cards = [
            _list_card(ft.Row([
                ft.Text(p["name"], weight=ft.FontWeight.W_500, expand=True),
                ft.Text(f"${p.get('cost', 0):.2f}/hr", weight=ft.FontWeight.W_500,
                        color=ft.Colors.PRIMARY),
                ft.Button("Remove", on_click=_delete_pricing_fn, data=p),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER))
            for p in pricing
        ]
        return ft.Column(
            [_section_header("Pricing", "Add Rate", open_add), ft.Divider()] + cards,
            spacing=8, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ── Section: Bookings ─────────────────────────────────────────────────
    def _build_bookings():
        today_str = today.isoformat()
        future_bookings    = [b for b in bookings if b.get("status") != "cancelled" and b.get("date", "") >= today_str]
        past_bookings      = [b for b in bookings if b.get("status") != "cancelled" and b.get("date", "") <  today_str]
        cancelled_bookings = [b for b in bookings if b.get("status") == "cancelled"]

        async def _cancel_booking_fn(e: ft.Event):
            async def _confirm(e=None):
                cancel_booking(booking["_id"])
                page.pop_dialog()
                page.show_dialog(ft.SnackBar(
                    ft.Text("Booking cancelled.", color=ft.Colors.ON_SURFACE),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                    shape=ft.RoundedRectangleBorder(ft.BorderSide(2, ft.Colors.ORANGE), radius=8),
                ))
                await page.push_route("/view_selector")

            booking = e.control.data
            page.show_dialog(ft.AlertDialog(
                title="Cancel this booking?",
                actions=[
                    ft.Button("Keep",           on_click=lambda: page.pop_dialog()),
                    ft.Button("Cancel Booking", on_click=_confirm),
                ],
            ))

        def _booking_card(b, show_cancel=False):
            return _list_card(ft.Row([
                ft.Column([
                    ft.Text(b.get("student", "Unknown"), weight=ft.FontWeight.W_500),
                    ft.Text(
                        f"{b.get('instructor', 'N/A')}  ·  {b.get('aircraft', 'N/A')}  ·  {b.get('type', '')}",
                        size=12, color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                ], spacing=2, expand=True),
                ft.Column([
                    ft.Text(b.get("date", ""), size=12),
                    ft.Text(b.get("time", ""), size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ], spacing=2),
                ft.Button("Cancel", on_click=_cancel_booking_fn, data=b)
                if show_cancel else ft.Container(width=0),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
               vertical_alignment=ft.CrossAxisAlignment.CENTER))

        def _booking_section(title, items, show_cancel):
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
        
        async def _add_booking(e):

            #non_cancelled_bookings = [b for b in bookings if b.get("cancelled") != True]    

            async def _confirm_booking(e=None):
                pass
            page.show_dialog(
                ft.AlertDialog(
                    ft.Row([
                        ft.Dropdown(label="Student(s)", expand=True, dense=True),
                        ft.Dropdown(label="Instructor", expand=True, dense=True),
                        ft.Dropdown(label="Aircraft", expand=True, dense=True),
                        ft.Dropdown(label="Equipment", expand=True, dense=True)
                    ], expand=True),
                    title="Schedule Booking",
                    actions=[
                        ft.Button("Cancel", on_click=lambda: page.pop_dialog()),
                        ft.Button("Confirm", on_click=_confirm_booking),
                    ],
                    expand=True,
                )
            )

        return ft.Column(
            [
                ft.Row([
                    ft.Text("Bookings", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, expand=True),
                    ft.Button("Add Booking", icon=ft.Icons.ADD, on_click=_add_booking),
                ]),
                ft.Divider(),
                *_booking_section("Upcoming / Future Bookings", future_bookings,    show_cancel=True),
                *_booking_section("Past Bookings",               past_bookings,      show_cancel=False),
                *_booking_section("Cancelled Bookings",          cancelled_bookings, show_cancel=False),
            ],
            spacing=8, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ── Navigation rail ───────────────────────────────────────────────────
    sections = [
        ("Dashboard",   ft.Icons.DASHBOARD,       _build_dashboard),
        ("Students",    ft.Icons.REDUCE_CAPACITY,  _build_students),
        ("Instructors", ft.Icons.PERSON,           _build_instructors),
        ("Aircraft",    ft.Icons.FLIGHT,           _build_aircraft),
        ("Equipment",   ft.Icons.INVENTORY,        _build_equipment),
        ("Pricing",     ft.Icons.ATTACH_MONEY,     _build_pricing),
        ("Bookings",    ft.Icons.CALENDAR_MONTH,   _build_bookings),
    ]

    def _set_selected_index(e: ft.Event[ft.NavigationRail]):
        selected_index = e.control.selected_index
        e.control.update()
        current_content.content = sections[selected_index][2]()
        current_content.update()
        page.session.store.set("current_rail_index", selected_index)

    selected_index = page.session.store.get("current_rail_index")

    return ft.SafeArea(
        ft.Row([
            ft.NavigationRail(
                destinations=[
                    ft.NavigationRailDestination(icon=icon, label=label)
                    for label, icon, _ in sections
                ],
                selected_index=selected_index if selected_index is not None else 0,
                on_change=_set_selected_index,
                label_type=ft.NavigationRailLabelType.ALL,
            ),
            ft.VerticalDivider(width=1),
            current_content := ft.Container(sections[selected_index if selected_index is not None else 0][2](), expand=True, padding=20),
        ], expand=True),
        minimum_padding=0,
        expand=True,
    )