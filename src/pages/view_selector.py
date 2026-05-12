''' Determines what user is logged in and returns the appropriate view. '''

import flet as ft


@ft.component
def ViewSelector():

    

    # if user id is admin, return admin view. 
    # Elif user id is instructor, return instructor view. 
    # Else return student view

    #return ft.context.page.navigate("/admin_view")
    #return ft.context.page.navigate("/instructor_view")

    return ft.context.page.navigate("/student_view")
