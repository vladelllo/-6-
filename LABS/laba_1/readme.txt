Задание
Создать xml файл валидной разметки с вложенностью не менее трёх уровней. Количество различных элементов второго уровня должно быть не менее двух. Количество различных элементов третьего уровня должно быть не менее четырёх. Тематика xml файла произвольная. Для каждого элемента первого уровня предусмотреть не менее 3 экземпляров, для каждого элемента последующих уровней – не менее двух экземпляров.
Код XML файла

Создаем xml файл валидной разметки с вложенностью не менее трёх уровней.

<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/css" href="styles.css"?>

<university>
    <faculty>
        <name>Факультет информатики</name>
        <department>
            <name>Кафедра программирования</name>
            <head>Иван Иванов</head>
            <courses>
                <course>
                    <title>Введение в программирование</title>
                    <credits>1 курс</credits>
                    <lecturer>Алексей Петров</lecturer>
                </course>
                <course>
                    <title>Алгоритмы и структуры данных</title>
                    <credits>1 курс</credits>
                    <lecturer>Мария Сидорова</lecturer>
                </course>
            </courses>
        </department>
        <department>
            <name>Кафедра искусственного интеллекта</name>
            <head>Ольга Кузнецова</head>
            <courses>
                <course>
                    <title>Машинное обучение</title>
                    <credits>2 курс</credits>
                    <lecturer>Дмитрий Смирнов</lecturer>
                </course>
                <course>
                    <title>Нейронные сети</title>
                    <credits>3 курс</credits>
                    <lecturer>Елена Иванова</lecturer>
                </course>
            </courses>
        </department>
    </faculty>
    <faculty>
        <name>Факультет математики</name>
        <department>
            <name>Кафедра алгебры</name>
            <head>Сергей Васильев</head>
            <courses>
                <course>
                    <title>Линейная алгебра</title>
                    <credits>1 курс</credits>
                    <lecturer>Анна Михайлова</lecturer>
                </course>
                <course>
                    <title>Теория чисел</title>
                    <credits>5 курс</credits>
                    <lecturer>Павел Николаев</lecturer>
                </course>
            </courses>
        </department>
        <department>
            <name>Кафедра геометрии</name>
            <head>Александр Белов</head>
            <courses>
                <course>
                    <title>Дифференциальная геометрия</title>
                    <credits>2 курс</credits>
                    <lecturer>Татьяна Федорова</lecturer>
                </course>
                <course>
                    <title>Топология</title>
                    <credits>4 курс</credits>
                    <lecturer>Виктор Соколов</lecturer>
                </course>
            </courses>
        </department>
    </faculty>
    <faculty>
        <name>Факультет физики</name>
        <department>
            <name>Кафедра теоретической физики</name>
            <head>Николай Павлов</head>
            <courses>
                <course>
                    <title>Квантовая механика</title>
                    <credits>3 курс</credits>
                    <lecturer>Екатерина Волкова</lecturer>
                </course>
                <course>
                    <title>Теория относительности</title>
                    <credits>3 курс</credits>
                    <lecturer>Андрей Морозов</lecturer>
                </course>
            </courses>
        </department>
        <department>
            <name>Кафедра экспериментальной физики</name>
            <head>Дмитрий Козлов</head>
            <courses>
                <course>
                    <title>Физика твердого тела</title>
                    <credits>2 курс</credits>
                    <lecturer>Ольга Семенова</lecturer>
                </course>
                <course>
                    <title>Ядерная физика</title>
                    <credits>4 курс</credits>
                    <lecturer>Игорь Петров</lecturer>
                </course>
            </courses>
        </department>
    </faculty>
</university>

Код CSS файла
Создаем файл с расширением .css, в котором находится набор CSS-стилей элементов.
body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
}

university {
    display: block;
    width: fit-content;
    max-width: 1200px;
    margin: 20px auto;
    background: #e3e6e6;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    border-radius: 12px;
    padding: 30px;
    animation: fadeIn 1s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

faculty {
    display: block;
    width: fit-content;
    margin-bottom: 30px;
    border-radius: 12px;
    padding: 20px;
    background:#82898f;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

faculty:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
}

faculty > departments {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

faculty > name {
    display: block;
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 10px;
    color: #fafbfb;
    padding-bottom: 5px;
    position: relative;
}

faculty > name::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: -2px;
    width: 0;
    height: 2px;
    transition: width 0.3s ease-in-out;
}

faculty:hover > name::after {
    width: 100%;
}

department {
    display: inline-block;
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #555;
    border-radius: 8px;
    background: linear-gradient(145deg, #1a242e, #1a2632);
    transition: background-color 0.3s ease-in-out;
    flex: 1 1 block;
    min-width: 400px;
    text-align: left;
}

department:hover {
    background: linear-gradient(145deg, #1a2632, #1a242e);
}

department > name {
    display: block;
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 5px;
    color: #aacee5;
    transition: color 0.3s ease-in-out;
}

department:hover > name {
    color: #979898;
}

department > head {
    display: block;
    font-style: italic;
    margin-bottom: 10px;
    color: #979898;
}

courses {
    display: block;
}

course {
    display: block;
    margin-bottom: 10px;
    padding: 10px;
    border: 1px solid #555;
    border-radius: 8px;
    background:#2c3e50;
    transition: transform 0.2s ease-in-out;
}

course:hover {
    transform: scale(1.03);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

course > title {
    display: block;
    font-weight: bold;
    color: #c8caca;
    transition: color 0.2s ease-in-out;
}

course:hover > title {
    color: #979898;
}

course > credits {
    display: block;
    font-size: 0.9em;
    color: #95a5a6;
}

course > lecturer {
    display: block;
    font-size: 0.9em;
    color: #95a5a6;
}
