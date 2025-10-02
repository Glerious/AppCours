from modules.configurable import Configurable, global_config
from modules.eventhandler import switch_update_text

from tkinter import Frame, Button, Label, Misc, StringVar
from tkinter import X, W, E, EW
from json import loads, dump
from functools import reduce

class Timetable:
    """
    Cette Classe permet d'obtenir l'emploi du temps.
    """
    def __init__(self):
        self.__path: str = "../../resources/timetable.json"
        self.__timetable: dict = self.__save_default_timetable()

    def get(self):
        return self.__timetable.items()

    def __save_default_timetable(self) -> dict:
        json_file = open(self.__path, 'r+', encoding='utf-8')
        data = json_file.read()
        return loads(data)
    
    def update_default_timetable(self, button_: Button, selection_: str, value_: str | int | bool):
        print(value_)
        self.deep_set(button_.winfo_name() + "_" + selection_, value_)
        json_file = open(self.__path, 'r+', encoding='utf-8')
        json_file.seek(0)
        dump(self.__timetable, json_file, indent=4, ensure_ascii=False)
        json_file.truncate()

    def deep_get(self, keys_: str, default_=None, target_type_=None):
        _value = reduce(
            lambda d, key: d.get(key, default_) if isinstance(d, dict) else default_,
            keys_.split("."),
            self.__timetable
        )
        return _value if not target_type_ else target_type_(_value)
    
    def deep_set(self, path_: str, value):
        _saved_timetable: dict = self.__timetable
        _keys = path_.split('_')
        _latest = _keys.pop()
        for k in _keys:
            _saved_timetable = _saved_timetable.setdefault(k, {})
        _saved_timetable[_latest] = value
    
class Course:
    def __init__(self, name_: str, information_: dict, master_: Misc):
        self.info = CourseInformation(information_)
        self.frame: CourseFrame = CourseFrame(name_, self.info, master_)
        self.statut: int = 3

class CourseInformation:
    def __init__(self, information_):
        self.name: str = information_["name"]
        self.id: str = information_["id"]
        self.lecture: dict = information_["lecture"]
        self.tutorial: dict = information_["tutorial"]
        self.practical: dict = information_["practical"]
    
class CourseFrame(Configurable):
    def __init__(self, name_: str, information_: CourseInformation, master_: Misc):
        super().__init__(global_config.course, "frame")
        self.background = self.config["background"]
        self.box: Frame = Frame(master_,
                         name=name_,
                         background=self.background,
                         relief="groove",
                         borderwidth=2)
        self.box.columnconfigure(0, weight=1)
        self.box.columnconfigure(1, weight=1)
        self.box.columnconfigure(2, weight=1)
        self.name: Label = Label(self.box, 
                          text=information_.name,
                          background=self.background,
                          font=("Helvetica", 14)).grid(column=0, row=0, columnspan=2, sticky=W)
        self.id: Label = Label(self.box,
                        text=information_.id,
                        background=self.background).grid(column=0, row=1, columnspan=2, sticky=W)
        self.statut_text: StringVar = StringVar(self.box, "À jour")
        self.statut: Button = Button(self.box,
                             textvariable=self.statut_text,
                             background=self.background,
                             foreground="green",
                             font=("Helvetica", 12),
                             command=lambda: switch_update_text(self.statut_text, self.statut))
        self.statut.grid(column=2, row=0, rowspan=2, padx=(0, 30), sticky=E)
        self.lecture: Frame = self.button_courses(
            name_ + "_lecture", information_.lecture, "greenyellow").grid(column=0, row=2, sticky=EW, padx=5, pady= 5)
        self.tutorial: Frame = self.button_courses(
            name_ + "_tutorial", information_.tutorial, "MediumTurquoise").grid(column=1, row=2, sticky=EW, padx=5, pady= 5)
        self.practical: Frame = self.button_courses(
            name_ + "_practical", information_.practical, "Coral").grid(column=2, row=2, sticky=EW, padx=5, pady= 5)
        
    def button_courses(self, name_: str, courses_: dict, color_: str) -> Frame:
        _box = Frame(self.box, background=self.background)
        for i in range(len(courses_)):
            _background = "gray" if courses_.get(str(i))["done"] else color_
            _button = Button(_box, width=2, text=i + 1, background=_background, name=name_+f"_{i}")
            _button["command"] = lambda b_=_button, v_=str(i): self.button_color_update(
                b_, not courses_.get(v_)["done"], color_)
            _button.grid(column=i, row=0, padx=5, pady=5)
        return _box
    
    def button_color_update(self, button_: Button, value_: bool, color_: str):
        global_timetable.update_default_timetable(
                button_, "done", value_)
        _background = "gray" if value_ else color_
        button_.configure(background=_background)
        
    def show(self):
        self.box.pack(fill=X, side= "top", padx=5, pady=5)
        
global_timetable: Timetable = Timetable()