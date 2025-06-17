Задание
Создать HTML страницу с встроенным скриптом, который будет обрабатывать выданный вам XML файл. Вам необходимо вывести на экран все элементы третьего, последнего уровня вложенности одного из элементов второго уровня.
Дополнительное задание: в HTML файле создать поле ввода, в которое вводится номер элемента второго уровня, для которого выведутся элементы третьего уровня.

Реализация
Вдобавок с существующему XML файлу из первой лабораторной работы (см. предыдущий отчет) создаем HTML страницу с встроенным скриптом, который будет обрабатывать выданный вам XML файл, выводя на экран все элементы третьего, последнего уровня вложенности одного из элементов второго уровня, номер которого введен в специальное поле ввода

Код HTML файла
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Парсинг XML: Университет</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Парсинг XML: Университет</h1>
        <div class="search-box">
            <label for="facultyName">Поиск по факультетам:</label>
            <input type="text" id="facultyName" placeholder="Например, Факультет информатики">
            <button onclick="parseXML()">Показать информацию</button>
        </div>
        <div id="output"></div>
    </div>

    <script>
        function normalizeString(str) {
            return str.slice(0, -2).toLowerCase();
        }

        function parseXML() {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', 'data.xml', false);
            xhr.send();

            if (xhr.status != 200) {
                alert('Ошибка: ' + xhr.status + ': ' + xhr.statusText);
                return;
            }

            var xmlDoc = xhr.responseXML;
            var faculties = xmlDoc.getElementsByTagName('faculty');

            var facultyName = document.getElementById('facultyName').value.trim();
            if (!facultyName) {
                alert('Введите название факультета');
                return;
            }

            var output = document.getElementById('output');
            output.innerHTML = '';

            var facultyFound = false;

            var normalizedFacultyName = normalizeString(facultyName);

            for (var i = 0; i < faculties.length; i++) {
                var faculty = faculties[i];
                var currentFacultyName = faculty.getElementsByTagName('name')[0].textContent;

                var normalizedCurrentFacultyName = normalizeString(currentFacultyName);

                if (normalizedCurrentFacultyName.includes(normalizedFacultyName)) {
                    facultyFound = true;

                    var departments = faculty.getElementsByTagName('department');

                    output.innerHTML += `<div class="faculty"><h2>${currentFacultyName}</h2>`;

                    for (var j = 0; j < departments.length; j++) {
                        var department = departments[j];
                        var departmentName = department.getElementsByTagName('name')[0].textContent;
                        var departmentHead = department.getElementsByTagName('head')[0].textContent;
                        var courses = department.getElementsByTagName('course');

                        output.innerHTML += `
                            <div class="department">
                                <h3>${departmentName}</h3>
                                <p><strong>Заведующий:</strong> ${departmentHead}</p>
                        `;

                        for (var k = 0; k < courses.length; k++) {
                            var course = courses[k];
                            var title = course.getElementsByTagName('title')[0].textContent;
                            var credits = course.getElementsByTagName('credits')[0].textContent;
                            var lecturer = course.getElementsByTagName('lecturer')[0].textContent;

                            output.innerHTML += `
                                <div class="course">
                                    <p><strong>Название курса:</strong> ${title}</p>
                                    <p><strong>Курс:</strong> ${credits}</p>
                                    <p><strong>Преподаватель:</strong> ${lecturer}</p>
                                </div>
                            `;
                        }

                        output.innerHTML += `</div>`;
                    }

                    output.innerHTML += `</div>`;
                }
            }

            if (!facultyFound) {
                output.innerHTML = `<p class="error">Факультет с названием "${facultyName}" не найден.</p>`;
            }
        }
    </script>
</body>
</html>

Код CSS файла
Создаем файл с расширением .css, в котором находится набор CSS-стилей элементов.
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #e8f0fe;
    color: #34495e;
}

.container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #2c3e50;
}

.search-box {
    margin-bottom: 20px;
    text-align: center;
}

.search-box label {
    font-size: 16px;
    margin-right: 10px;
    color: #546e7a;
}

.search-box input {
    padding: 8px;
    font-size: 14px;
    border: 1px solid #a7c4eb;
    border-radius: 4px;
    width: 300px;
}

.search-box button {
    padding: 8px 16px;
    font-size: 14px;
    background-color: #4a69bd;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.search-box button:hover {
    background-color: #384f8a;
}

#output {
    margin-top: 20px;
}

.faculty {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #c5cae9;
    border-radius: 8px;
    background-color: #f2f3f7;
}

.faculty h2 {
    color: #34495e;
    margin-bottom: 18px;
}

.department {
    margin-bottom: 15px;
    padding: 10px;
    border: 1px solid #d7dbe8;
    border-radius: 6px;
    background-color: #edf2f7;
}

.department h3 {
    color: #2c3e50;
    margin-bottom: 10px;
}

.course {
    margin-bottom: 10px;
    padding: 10px;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    background-color: #fff;
}

.course p {
    margin: 5px 0;
}

.error {
    color: #c62828;
    text-align: center;
    font-size: 16px;
}
