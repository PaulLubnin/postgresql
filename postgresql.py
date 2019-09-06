import psycopg2


class WorkWithDataBase:
    def __init__(self, dbname, user, password, host):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.connection, self.cursor = self.get_connection()

    # создает подключение
    def get_connection(self):
        connection = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        connection.autocommit = True
        cursor = connection.cursor()
        return connection, cursor

    # создает таблицы
    def create_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Course (
                            id serial PRIMARY KEY NOT NULL, 
                            name VARCHAR(100) NOT NULL);                        
                        
                            CREATE TABLE IF NOT EXISTS Student (
                            id serial PRIMARY KEY NOT NULL, 
                            name VARCHAR(100) NOT NULL, 
                            gpa NUMERIC(10, 2), 
                            birth TIMESTAMP WITH TIME ZONE);
                            
                            CREATE TABLE IF NOT EXISTS Student_course (
                            id serial PRIMARY KEY NOT NULL,
                            student_id INTEGER REFERENCES Student(id) NOT NULL,
                            course_id INTEGER REFERENCES Course(id) NOT NULL);
                            """)
        print('Таблицы созданы')
        return

    # создание курса
    def create_course(self, name_course):
        self.cursor.execute("""INSERT INTO Course 
                            (name) values (%s);""", (name_course,))
        print('\tкурс добавлен в таблицу')
        return

    # возвращает студентов выбранного курса
    def get_students(self, course_id):
        self.cursor.execute("""SELECT * FROM Student_course WHERE
                            course_id = (%s);""", (course_id,))
        print(self.cursor.fetchall())
        return

    # записывает студентов на курс
    def add_students(self, course_id, student_id):
        self.cursor.execute("""INSERT INTO Student_course 
                            (course_id, student_id) values (%s, %s)""", (course_id, student_id))
        print('\tстудент записан')
        return

    # просто создает студента в таблице из словаря
    def add_student(self, student):
        self.cursor.execute("""INSERT INTO Student 
                            (name, gpa, birth) values (%(name)s, %(gpa)s, %(birth)s);""", student)
        return

    # посмотреть студента
    def get_student(self, student_id):
        self.cursor.execute("""SELECT * FROM Student WHERE 
                            id = (%s);""", student_id)
        print(self.cursor.fetchall())
        return

    # посмотреть курсы
    def get_course(self):
        print('\tдоступные курсы')
        self.cursor.execute("""SELECT * FROM Course""")
        print(self.cursor.fetchall())
        return

def create_student_dict():
    student_dict = {}
    while True:
        print('создание студента(ов): "n" - новый студент, "e" - выход')
        input_command = input('\tвведите комманду ')
        if input_command == 'n':
            name_student = input('\tимя ')
            gpa_student = input('\tсредняя оценка ')
            birth_student = input('\tдата рождения ')
            student = {'name': name_student,
                       'gpa': gpa_student,
                       'birth': birth_student}
            student_dict.update(student)
        if input_command == 'e':
            break
    return student_dict


if __name__ == '__main__':
    print('\nСкрипт для работы с базой PostgreSQL\n'
          'Для дальнейшей работы необходимо ввести данные:')
    base_name = input('\tназвание базы ')
    user = input('\tлогин ')
    password = input('\tпароль ')
    host = input('\tадрес сервера ')
    postgres_db = WorkWithDataBase(base_name, user, password, host)
    print('Подключение к базе данных прошло уcпешно')
    while True:
        print('\nДоступные команды:\n'
              '\t"с" - создать таблицу\n'
              '\t"cc" - создание курса\n'
              '\t"lc" - посмотреть курсы\n'
              '\t"g" - показать студентов курса\n'
              '\t"a" - записать студента на курс\n'          
              '\t"s" - создание студента\n'          
              '\t"l" - посмотреть студента\n'
              '\t"q" - выход')
        input_command = input('Ввведите команду: ')
        if input_command == 'c':
            postgres_db.create_db()
        if input_command == 'cc':
            postgres_db.create_course(input('\tнаберите название курса '))
        if input_command == 'lc':
            postgres_db.get_course()
        if input_command == 'g':
            postgres_db.get_students(input('\tнаберите id курса '))
        if input_command == 'a':
            postgres_db.add_students(input('\tнаберите id курса '), input('\tнаберите id студента '))
        if input_command == 's':
            postgres_db.add_student(create_student_dict())
        if input_command == 'l':
            postgres_db.get_student(input('\tнаберите id студента '))
        if input_command == 'q':
            print('\tвыход')
            break
