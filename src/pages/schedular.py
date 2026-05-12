# Main view for the schedular app
import flet as ft

@ft.component
def SchedularPage():
    return ft.SafeArea(
        ft.Text("Schedular Page"),
        expand=True
    )