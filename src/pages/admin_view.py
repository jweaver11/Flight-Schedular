''' Main view for the admin '''

import flet as ft
import datetime


def _open_dialog(dialog):
    if dialog not in ft.context.page.overlay:
        ft.context.page.overlay.append(dialog)
    dialog.open = True
    ft.context.page.update()


def _close_dialog(dialog):
    dialog.open = False
    ft.context.page.update()


@ft.component
def AdminViewPage():
    selected_index, set_selected_index = ft.use_state(0)

    # ── Mock data  (replace with DB calls) ────────────────────────────────
    instructors = [
        {"id": 1, "name": "Kevin Smith",  "email": "kevin@chopperaviation.com",  "schedule": "Mon–Fri  9 am–5 pm"},
        {"id": 2, "name": "Steven Jones", "email": "steven@chopperaviation.com", "schedule": "Mon–Fri  9 am–5 pm"},
        {"id": 3, "name": "Tom Williams", "email": "tom@chopperaviation.com",    "schedule": "Tue–Sat 10 am–6 pm"},
    ]
    aircraft = [
        {"id": 1, "name": "Cessna 172 (N1234A)",   "type": "Fixed-Wing", "capacity": 4},
        {"id": 2, "name": "Piper PA-28 (N5678B)",  "type": "Fixed-Wing", "capacity": 4},
        {"id": 3, "name": "Robinson R22 (N9012C)", "type": "Helicopter", "capacity": 2},
    ]
    equipment = [
        {"id": 1, "name": "Headset",           "count": 6},
        {"id": 2, "name": "Flight Bag",        "count": 4},
        {"id": 3, "name": "Kneeboard",         "count": 8},
        {"id": 4, "name": "iPad w/ ForeFlight","count": 3},
    ]
    pricing = [
        {"id": 1, "name": "Ground School",           "cost": 50.00},
        {"id": 2, "name": "Aircraft Rental (Solo)",  "cost": 100.00},
        {"id": 3, "name": "Aircraft + Instructor",   "cost": 150.00},
        {"id": 4, "name": "Checkride Prep",          "cost": 175.00},
    ]

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
            width=140,
        )

    def _booking_row(student, instructor_name, aircraft_name, date_str, time_str, status):
        color = ft.Colors.GREEN if status == "Confirmed" else ft.Colors.ORANGE
        return ft.Container(
            ft.Row([
                ft.Column([
                    ft.Text(student, weight=ft.FontWeight.W_500),
                    ft.Text(f"{instructor_name}  ·  {aircraft_name}",
                            size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ], spacing=2),
                ft.Column([
                    ft.Text(date_str, size=12),
                    ft.Text(time_str, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ], spacing=2),
                ft.Container(
                    ft.Text(status, size=12, color=ft.Colors.WHITE),
                    bgcolor=color, border_radius=20,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
               vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=8,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
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
            ft.ElevatedButton(btn_label, icon=ft.Icons.ADD, on_click=lambda: on_add()),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # ── Section: Overview ─────────────────────────────────────────────────
    def _build_overview():
        return ft.Column([
            ft.Text("Dashboard", theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([
                _stat_card("Students",    "24",                  ft.Icons.GROUP),
                _stat_card("Instructors", str(len(instructors)), ft.Icons.PERSON),
                _stat_card("Aircraft",    str(len(aircraft)),    ft.Icons.FLIGHT),
                _stat_card("Today",       "3 Bookings",          ft.Icons.EVENT),
            ], wrap=True, spacing=12, run_spacing=12),
            ft.Container(height=12),
            ft.Text("Recent Bookings",
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.W_600),
            ft.Divider(),
            _booking_row("John Doe",     "Kevin Smith",  "Cessna 172",
                         today.strftime("%b %d"), "9:00–11:00 AM", "Confirmed"),
            _booking_row("Jane Smith",   "Steven Jones", "Piper PA-28",
                         today.strftime("%b %d"), "1:00–3:00 PM",  "Confirmed"),
            _booking_row("Mike Johnson", "Tom Williams", "Robinson R22",
                         (today + datetime.timedelta(days=1)).strftime("%b %d"),
                         "10:00 AM–12:00 PM", "Pending"),
        ], spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)

    # ── Section: Instructors ──────────────────────────────────────────────
    def _build_instructors():
        def open_add():
            name_f  = ft.TextField(label="Full Name")
            email_f = ft.TextField(label="Email")
            pwd_f   = ft.TextField(label="Temporary Password",
                                   password=True, can_reveal_password=True)
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Add Instructor"),
                content=ft.Column([name_f, email_f, pwd_f], tight=True, spacing=12),
                actions=[
                    ft.TextButton("Cancel",  on_click=lambda: ft.context.page.pop_dialog()),
                    ft.ElevatedButton("Add", on_click=lambda: ft.context.page.pop_dialog()),  # TODO: persist
                ],
            )
            _open_dialog(dlg)

        def open_edit(inst):
            name_f  = ft.TextField(label="Full Name",  value=inst["name"])
            email_f = ft.TextField(label="Email",      value=inst["email"])
            sched_f = ft.TextField(label="Schedule",   value=inst["schedule"])
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit Instructor"),
                content=ft.Column([name_f, email_f, sched_f], tight=True, spacing=12),
                actions=[
                    ft.TextButton("Cancel",   on_click=lambda: ft.context.page.pop_dialog()),
                    ft.ElevatedButton("Save", on_click=lambda: ft.context.page.pop_dialog()),  # TODO: persist
                ],
            )
            _open_dialog(dlg)

        cards = [
            _list_card(ft.Row([
                ft.Column([
                    ft.Text(i["name"],     weight=ft.FontWeight.W_500),
                    ft.Text(i["email"],    size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Text(i["schedule"], size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ], spacing=2, expand=True),
                ft.IconButton(ft.Icons.EDIT,   tooltip="Edit",   on_click=lambda inst=i: open_edit(inst)),
                ft.IconButton(ft.Icons.DELETE, tooltip="Remove", icon_color=ft.Colors.ERROR),
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
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Add Aircraft"),
                content=ft.Column([
                    ft.TextField(label="Name / Tail Number"),
                    ft.TextField(label="Type  (e.g. Fixed-Wing, Helicopter)"),
                    ft.TextField(label="Seat Capacity",      keyboard_type=ft.KeyboardType.NUMBER),
                    ft.TextField(label="Weight Limit (lbs)", keyboard_type=ft.KeyboardType.NUMBER),
                ], tight=True, spacing=12),
                actions=[
                    ft.TextButton("Cancel",  on_click=lambda: ft.context.page.pop_dialog()),
                    ft.ElevatedButton("Add", on_click=lambda: ft.context.page.pop_dialog()),  # TODO: persist
                ],
            )
            _open_dialog(dlg)

        def open_edit(ac):
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit Aircraft"),
                content=ft.Column([
                    ft.TextField(label="Name / Tail Number", value=ac["name"]),
                    ft.TextField(label="Type",               value=ac["type"]),
                    ft.TextField(label="Seat Capacity",      value=str(ac["capacity"]),
                                 keyboard_type=ft.KeyboardType.NUMBER),
                ], tight=True, spacing=12),
                actions=[
                    ft.TextButton("Cancel",   on_click=lambda: ft.context.page.pop_dialog()),
                    ft.ElevatedButton("Save", on_click=lambda: ft.context.page.pop_dialog()),  # TODO: persist
                ],
            )
            _open_dialog(dlg)

        cards = [
            _list_card(ft.Row([
                ft.Column([
                    ft.Text(a["name"], weight=ft.FontWeight.W_500),
                    ft.Text(f"{a['type']}  ·  {a['capacity']} seats",
                            size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ], spacing=2, expand=True),
                ft.IconButton(ft.Icons.EDIT,   tooltip="Edit",   on_click=lambda ac=a: open_edit(ac)),
                ft.IconButton(ft.Icons.DELETE, tooltip="Remove", icon_color=ft.Colors.ERROR),
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
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Add Equipment"),
                content=ft.Column([
                    ft.TextField(label="Equipment Name"),
                    ft.TextField(label="Quantity", keyboard_type=ft.KeyboardType.NUMBER),
                ], tight=True, spacing=12),
                actions=[
                    ft.TextButton("Cancel",  on_click=lambda: ft.context.page.pop_dialog()),
                    ft.ElevatedButton("Add", on_click=lambda: ft.context.page.pop_dialog()),  # TODO: persist
                ],
            )
            _open_dialog(dlg)

        def open_edit(eq):
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit Equipment"),
                content=ft.Column([
                    ft.TextField(label="Equipment Name", value=eq["name"]),
                    ft.TextField(label="Quantity",       value=str(eq["count"]),
                                 keyboard_type=ft.KeyboardType.NUMBER),
                ], tight=True, spacing=12),
                actions=[
                    ft.TextButton("Cancel",   on_click=lambda: ft.context.page.pop_dialog()),
                    ft.ElevatedButton("Save", on_click=lambda: ft.context.page.pop_dialog()),  # TODO: persist
                ],
            )
            _open_dialog(dlg)

        cards = [
            _list_card(ft.Row([
                ft.Column([
                    ft.Text(e["name"],          weight=ft.FontWeight.W_500),
                    ft.Text(f"Qty: {e['count']}", size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ], spacing=2, expand=True),
                ft.IconButton(ft.Icons.EDIT,   tooltip="Edit",   on_click=lambda eq=e: open_edit(eq)),
                ft.IconButton(ft.Icons.DELETE, tooltip="Remove", icon_color=ft.Colors.ERROR),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER))
            for e in equipment
        ]
        return ft.Column(
            [_section_header("Equipment", "Add Equipment", open_add), ft.Divider()] + cards,
            spacing=8, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ── Section: Pricing ──────────────────────────────────────────────────
    def _build_pricing():
        def open_add():
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Add Pricing Rate"),
                content=ft.Column([
                    ft.TextField(label="Service Name"),
                    ft.TextField(label="Rate ($/hr)", keyboard_type=ft.KeyboardType.NUMBER),
                ], tight=True, spacing=12),
                actions=[
                    ft.TextButton("Cancel",  on_click=lambda: ft.context.page.pop_dialog()),
                    ft.ElevatedButton("Add", on_click=lambda: ft.context.page.pop_dialog()),  # TODO: persist
                ],
            )
            _open_dialog(dlg)

        def open_edit(pr):
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit Pricing Rate"),
                content=ft.Column([
                    ft.TextField(label="Service Name", value=pr["name"]),
                    ft.TextField(label="Rate ($/hr)",  value=f"{pr['cost']:.2f}",
                                 keyboard_type=ft.KeyboardType.NUMBER),
                ], tight=True, spacing=12),
                actions=[
                    ft.TextButton("Cancel",   on_click=lambda: ft.context.page.pop_dialog()),
                    ft.ElevatedButton("Save", on_click=lambda: ft.context.page.pop_dialog()),  # TODO: persist
                ],
            )
            _open_dialog(dlg)

        cards = [
            _list_card(ft.Row([
                ft.Text(p["name"], weight=ft.FontWeight.W_500, expand=True),
                ft.Text(f"${p['cost']:.2f}/hr", weight=ft.FontWeight.W_500,
                        color=ft.Colors.PRIMARY),
                ft.IconButton(ft.Icons.EDIT,   tooltip="Edit",   on_click=lambda pr=p: open_edit(pr)),
                ft.IconButton(ft.Icons.DELETE, tooltip="Remove", icon_color=ft.Colors.ERROR),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER))
            for p in pricing
        ]
        return ft.Column(
            [_section_header("Pricing", "Add Rate", open_add), ft.Divider()] + cards,
            spacing=8, scroll=ft.ScrollMode.AUTO, expand=True,
        )

    # ── Navigation rail ───────────────────────────────────────────────────
    sections = [
        ("Overview",    ft.Icons.DASHBOARD,      _build_overview),
        ("Instructors", ft.Icons.PERSON,         _build_instructors),
        ("Aircraft",    ft.Icons.FLIGHT,         _build_aircraft),
        ("Equipment",   ft.Icons.INVENTORY,      _build_equipment),
        ("Pricing",     ft.Icons.ATTACH_MONEY,   _build_pricing),
    ]

    current_content = sections[selected_index][2]()

    return ft.SafeArea(
        ft.Row([
            ft.NavigationRail(
                destinations=[
                    ft.NavigationRailDestination(icon=icon, label=label)
                    for label, icon, _ in sections
                ],
                selected_index=selected_index,
                on_change=lambda e: set_selected_index(int(e.data)),
                label_type=ft.NavigationRailLabelType.ALL,
            ),
            ft.VerticalDivider(width=1),
            ft.Container(current_content, expand=True, padding=20),
        ], expand=True),
        minimum_padding=0,
        expand=True,
    )