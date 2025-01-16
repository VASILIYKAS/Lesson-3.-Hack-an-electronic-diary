def find_student(student_name):
    """Поиск ученика"""
    student = Schoolkid.objects.filter(full_name__contains=student_name)
    if student.count() == 0:
        print(f'Ученик с именем "{student_name}" не найден.')
    elif student.count() == 1:
        full_name = student.get()
        print(f'Найден ученик с именем {student_name.full_name}')
        return full_name
    else:
        print(f'''Найдено несколько учеников с именем "{student_name}". 
            Пожалуйста, уточните запрос.''')



def fix_marks(student_name):
    """Исправление оценок"""
    student = find_student(student_name)
    if student is None:
        print(f'Ученик с именем "{student_name}" не найден. Исправление оценок невозможно.')
        return
    bad_points = Mark.objects.filter(schoolkid=student, points__lt=4)
    for bad_point in bad_points:
        bad_point.points = 5
        bad_point.save()
    print(f'Оценки ученика {student.full_name} исправлены')


def remove_chastisements(schoolkid):
    """Удаление замечаний учителей"""
    comments = Chastisement.objects.filter(schoolkid=schoolkid)
    comments.delete()
    print(f'Замечания ученика {schoolkid} удалены')


def create_commendation(schoolkid, date, year_of_study, group_letter):
    """Добавление похвалы от учителей"""
    lessons = Lesson.objects.filter(
        year_of_study=year_of_study, group_letter=group_letter, date=date)
    random_lesson = lessons.order_by('?').first()
    lesson_title = random_lesson.subject.title
    teachers = Lesson.objects.filter(
        subject__title=lesson_title, year_of_study=year_of_study)
    teacher = teachers.first().teacher
    subject = Subject.objects.filter(title=lesson_title).first()
    commendation = ['Молодец!', 'Отлично!', 'Хорошо!',
                    'Великолепно!', 'Прекрасно!', 'Потрясающе!']
    random_commendation = random.choice(commendation)
    Commendation.objects.create(
        text=random_commendation,
        created=date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=teacher,
    )
    print(f'''Похвала ({random_commendation}) для ученика {schoolkid} по предмету 
          {lesson_title} добавлена. Учитель {teacher}. Дата {date}.''')