def find_student(schoolkids):
    """Поиск ученика"""
    try:
        schoolkids = Schoolkid.objects.filter(full_name__contains=schoolkids)
        if schoolkids.count() == 0:
            print(f'Ученик с именем "{schoolkids}" не найден.')
        elif schoolkids.count() == 1:
            schoolkid = schoolkids.get()
            print(f'Найден ученик с именем {schoolkid.full_name}')
            return schoolkid
        else:
            print(f'''Найдено несколько учеников с именем "{schoolkids}". 
                Пожалуйста, уточните запрос.''')
    except ObjectDoesNotExist:
        print(f'Ученик с именем "{schoolkids}" не найден.')



def fix_marks(schoolkid):
    """Исправление оценок"""
    bad_points = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for bad_point in bad_points:
        bad_point.points = 5
        bad_point.save()
    print(f'Оценки ученика {schoolkid.full_name} исправлены')


def remove_chastisements(schoolkid):
    """Удаление замечаний учителей"""
    comments = Chastisement.objects.filter(schoolkid=schoolkid)
    comments.delete()
    print(f'Замечания ученика {schoolkid} удалены')


def create_commendation(schoolkid, date):
    """Добавление похвалы от учителей"""
    lessons = Lesson.objects.filter(
        year_of_study=6, group_letter='А', date=date)
    random_lesson = lessons.order_by('?').first()
    lesson_title = random_lesson.subject.title
    teachers = Lesson.objects.filter(
        subject__title=lesson_title, year_of_study=6)
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