from modules.window import Window
from modules.course import Course, global_timetable

def main():
    window = Window()
    all_courses: list[Course] = [Course(i, j, window.frame.interior) for i, j in global_timetable.get()]

    for course in all_courses:
        course.frame.show()
    window.show()

if __name__ == "__main__":
    main()