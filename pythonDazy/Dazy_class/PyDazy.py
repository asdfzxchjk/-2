from datetime import datetime
from fileinput import filename
import random
# 重写了 __init__ 方法，用于初始化异常对象时接受一个消息参数。传入的消息保存在 self.message 属性中，并调用父类 Exception 的 __init__ 方法，将消息传递给父类以进行异常的初始化。
class InputError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# 创建学生类
class Student:
    def __init__(self, student_id, name, gender, birthday, grade, hobby, major):
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.grade = grade
        self.hobby = hobby
        self.major = major

    # 用于定义对象的字符串表示形式。调用该对象的__str__方法来获取其字符串表示形式。
    def __str__(self):
        return f"学号: {self.student_id}, 姓名: {self.name}, 性别: {self.gender}, 生日: {self.birthday}, 年级: {self.grade}, 爱好: {self.hobby}, 专业: {self.major}"

# 从键盘输入学生信息
#加密函数
def Jiami(text, offset):
    Jiami_text = ""
    for char in text:
        if char.isupper():
            Jiami_text += chr((ord(char) - 65 + offset) % 26 + 65)
        elif char.islower():
            Jiami_text += chr((ord(char) - 97 + offset) % 26 + 97)
        elif char.isdigit():
            Jiami_text += chr((ord(char) - 48 + offset) % 10 + 48)
        else:
            Jiami_text += char
    return Jiami_text
#解密函数
def jiemi(jiemi_text, offset):
    jiemi_text = ""
    for char in jiemi_text:
        if char.isupper():
            jiemi_text += chr((ord(char) - 65 - offset) % 26 + 65)
        elif char.islower():
            jiemi_text += chr((ord(char) - 97 - offset) % 26 + 97)
        elif char.isdigit():
            jiemi_text += chr((ord(char) - 48 - offset) % 10 + 48)
        else:
            jiemi_text += char
    return jiemi_text
def input_student():
    student_id = input("请输入学号（8位整数）: ")
    if not student_id.isdigit() or len(student_id) != 8:  # isdigit() 是 Python 字符串对象的一个方法，用于检查字符串是否由数字组成。
        raise InputError("学号必须是8位整数。")

    name = input("请输入姓名: ")

    gender = input("请输入性别（male/female）: ")
    if gender.lower() not in ['male', 'female']:
        raise InputError("性别只能为male或female。")

    birthday = input("请输入生日（YYYY-MM-DD）: ")
    try:
        datetime.strptime(birthday, '%Y-%m-%d')  # 检查日期格式是否正确
    except ValueError:
        raise InputError("日期格式不正确。")

    grade = input("请输入年级: ")

    hobby = input("请输入爱好: ")

    major = input("请输入专业: ")
#加密
    # 使用演示人真实学号的四位尾号作为随机种子
    random.seed('0510')  # 0510 是演示人真实学号的四位尾号
    offset = random.randint(1, 63)  # 生成随机偏移量（1到63之间的整数）

    # 对学号、性别和爱好进行凯撒密码加密
    Jm_student_id = Jiami(student_id, offset)
    Jm_gender =Jiami(gender, offset)
    Jm_hobby = Jiami(hobby, offset)
    return Student(Jm_student_id, name, Jm_gender, birthday, grade, Jm_hobby, major)


# 将学生信息保存到文件
def save_student(filename, student):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{student.student_id}\t{student.name}\t{student.gender}\t{student.birthday}\t{student.grade}\t{student.hobby}\t{student.major}\n")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 查询

class StudentDatabase:
    def __init__(self, file_path):
        self.file_path = file_path
        self.students = []
        self.load_data()
        self.operations = []

    def load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data = line.strip().split('\t')
                student = Student(*data)
                self.students.append(student)

    def query_statistics(self):
        from datetime import datetime

        total_students = len(self.students)
        total_age = 0
        male_count = 0
        female_count = 0

        current_year = datetime.now().year
        for student in self.students:
            birth_year = int(student.birthday.split('-')[0])
            age = current_year - birth_year
            total_age += age

            if student.gender.lower() == 'male':
                male_count += 1
            elif student.gender.lower() == 'female':
                female_count += 1
        male_count   =    male_count/total_students
        female_count = female_count / total_students
        avg_age = total_age / total_students if total_students > 0 else 0
        gender_ratio = {'male': f"{male_count*100}%", 'female': f"{female_count*100}%"}#构建性别比例字典

        self.log_operation("查询学生总人数，学生平均年龄，性别比例")

        return total_students, avg_age, gender_ratio

    def query_by_student_id(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                self.log_operation(f"查询学号为{student_id}的学生信息")
                return vars(student)#如果找到了匹配的学生，将该学生的属性转换为字典并返回。
        return None

    def query_by_year_and_grade(self):
        from collections import defaultdict

        year_dict = defaultdict(int)#创建了一个默认字典 year_dict，默认值为 int 类型的 0。
        grade_dict = defaultdict(int)

        for student in self.students:
            year = student.birthday.split('-')[0]
            grade = student.grade
            year_dict[year] += 1
            grade_dict[grade] += 1

        self.log_operation("查询各年份的学生人数，各年级的学生人数")

        return dict(year_dict), dict(grade_dict)

    def log_operation(self, operation):
        self.operations.append(operation)
        if len(self.operations) > 10:
            self.operations.pop(0)#删除

    def get_recent_operations(self):
        self.log_operation("查询最近十次操作")
        return list(reversed(self.operations))

def query_function(db):
    while True:
        print("请选择查询选项：")
        print("1: 查询学生总人数，学生平均年龄，性别比例")
        print("2: 根据学号查询个人信息")
        print("3: 查询各年份的学生人数，各年级的学生人数")
        print("4: 查询最近十次操作")
        print("0: 返回上一级菜单")

        choice = input("输入选项: ")

        if choice == '1':
            total_students, avg_age, gender_ratio = db.query_statistics()
            print(f"总人数: {total_students}, 平均年龄: {avg_age}, 性别比例: {gender_ratio}")

        elif choice == '2':
            student_id = input("输入学生学号: ")
            student_info = db.query_by_student_id(student_id)
            if student_info:
                print(f"学生信息: {student_info}")
            else:
                print("未找到该学生信息")

        elif choice == '3':
            year_dict, grade_dict = db.query_by_year_and_grade()
            print(f"各年份学生人数: {year_dict}")
            print(f"各年级学生人数: {grade_dict}")

        elif choice == '4':
            recent_operations = db.get_recent_operations()
            print(f"最近十次操作: {recent_operations}")

        elif choice == '0':
            print("返回上一级菜单")
            break

        else:
            print("无效选项，请重新选择")


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# 修改
def xg_student(filename, student_id, db):
    updated = False  # 用于标记是否已更新学生信息
    # 读取文件，查找匹
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # 逐行读取文件内容
        for i, line in enumerate(lines):
            # 解析每行数据
            parts = line.strip().split('\t')
            if parts[0] == student_id:  # 找到匹配学号的学生
                print("找到匹配的学生信息：")
                print("学号:", parts[0])
                print("姓名:", parts[1])
                print("性别:", parts[2])
                print("生日:", parts[3])
                print("年级:", parts[4])
                print("爱好:", parts[5])
                print("专业:", parts[6])
                print("请输入要修改的信息：")
                name = input("姓名：")
                gender = input("性别（male/female）：")
                birthday = input("生日（YYYY-MM-DD）：")
                grade = input("年级：")
                hobby = input("爱好：")
                major = input("专业：")
                # 更新学生信息
                updated_info = '\t'.join([student_id, name, gender, birthday, grade, hobby, major])
                lines[i] = updated_info + '\n'  # 更新文件内容
                updated = True
                print("学生信息已更新。")
                break  # 找到匹配学生后立即跳出循环
    # 如果未找到匹配的学生，抛出自定义的异常
    if not updated:
        raise InputError("未找到匹配的学生信息。")
    # 将更新后的内容写回文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# 删除
def sc_student(filename, student_id, db):
    deleted = False  # 用于标记是否已删除学生信息
    # 读取文件，查找匹配学号的学生并删除信息
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # 逐行读取文件内容
    with open(filename, 'w', encoding='utf-8') as file:
        for line in lines:
            # 解析每行数据
            parts = line.strip().split('\t')
            if parts[0] == student_id:  # 找到匹配学号的学生
                print("找到匹配的学生信息：")
                print("学号:", parts[0])
                print("姓名:", parts[1])
                print("性别:", parts[2])
                print("生日:", parts[3])
                print("年级:", parts[4])
                print("爱好:", parts[5])
                print("专业:", parts[6])
                choice = input("是否要删除该学生信息？（yes/no）: ")
                if choice.lower() == 'yes':
                    deleted = True
                    print("学生信息已删除。")
                    continue  # 删除该学生信息后跳过写入文件
            file.write(line)  # 将未删除的学生信息写回文件
    # 如果未找到匹配的学生，抛出自定义的异常
    if not deleted:
        raise InputError("未找到匹配的学生信息。")

def main():
    # 读取学生数据
    filename = "E:/PyCh/Dazy/pythonDazy/Dazy_class/students.txt"
    db = StudentDatabase(filename)
    while True:
        print("1. 输入内容")
        print("2. 查询内容")
        print("3. 修改内容")
        print("4. 删除内容")
        print("5. 退出程序")

        c = input("请选择操作：")

        if c == "1":
            while True:
                try:
                    new_student = input_student()
                    save_student(filename, new_student)
                    print("学生信息已成功保存到文件。")
                except InputError as e:
                    print(e)

                choice = input("是否继续输入学生信息？（yes/no）: ")
                if choice.lower() != 'yes':
                    break
        elif c == "2":
            query_function(db)

        elif c == "3":
            student_id = input("请输入要修改信息的学生学号：")
            try:
                xg_student(filename, student_id, db)
            except InputError as e:
                print(e)
        elif c == "4":
            student_id = input("请输入要删除信息的学生学号：")
            try:
                sc_student(filename, student_id, db)
            except InputError as e:
                print(e)
        elif c == "5":
            print("程序已退出。")
            break
        else:
            print("请输入正确的选项。")

if __name__ == "__main__":
    main()