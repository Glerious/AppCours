from tkinter import StringVar, Button

def switch_update_text(text_: StringVar, button_: Button):
    if text_.get() == "À jour":
        text_.set("Non à jour")
        button_.configure(foreground="red")
    else :
        text_.set("À jour")
        button_.configure(foreground="green")