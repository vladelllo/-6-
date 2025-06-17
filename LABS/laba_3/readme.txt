Задание
Создать HTML страницу с вложенным javascript, который бы выдавал список ID ваших друзей вконтакте. Для каждого друга необходимо вывести дополнительную информацию, согласно варианту.

Дополнительное задание:
Оформить возвращенный JSON в виде таблицы HTML. 

Реализация
Напишем вложенный скрипт JS внутри документа html, который будет, используя методы VK API, выдавать список моих друзей в социальной сети ВК с датами рождения и прочей информацией, оформленный в виде таблицы HTML. Дополнительно можно указать сортировку друзей по фамилиям (в обычном и обратном порядке) и также дополнительно я вывел количество прожитых дней у своих друзей.

Код HTML файла
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Список друзей ВКонтакте</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>Список друзей ВКонтакте</h1>
        <button id="loadFriends">Загрузить список друзей</button>
        <div id="output"></div>
    </div>

    <script>
        const accessToken = 'b2d30e1db2d30e1db2d30e1da1b1f9e644bb2d3b2d30e1dd5138b9f2e98368f66c6e7c9';
        const apiVersion = '5.131';
        const userID = '340553765';

        let friendsData = [];

        function loadFriends() {
            $.getJSON({
                url: `https://api.vk.com/method/friends.get?access_token=${accessToken}&v=${apiVersion}&fields=first_name,last_name,city,bdate&user_id=${userID}`,
                jsonp: "callback",
                dataType: "jsonp"
            }).done(function(response) {
                if (response.response) {
                    friendsData = response.response.items;
                    displayFriends(friendsData);
                } else {
                    $('#output').html('<p class="error">Ошибка при загрузке данных.</p>');
                }
            }).fail(function() {
                $('#output').html('<p class="error">Ошибка при выполнении запроса.</p>');
            });
        }

        function displayFriends(friends) {
            let html = '<table>';
            html += `
                <tr>
                    <th>ID</th>
                    <th>Имя</th>
                    <th>
                        <div class="sort-buttons">
                            <button class="sort-button" id="sortLastNameAsc"><i class="fas fa-sort-up"></i></button>
                            <button class="sort-button" id="sortLastNameDesc"><i class="fas fa-sort-down"></i></button>
                        </div>
                        Фамилия
                    </th>
                    <th>Город</th>
                    <th>Дата рождения</th>
                    <th>Возраст (дни)</th>
                </tr>
            `;
            friends.forEach(friend => {
                const city = friend.city ? friend.city.title : 'Не указан';
                const bdate = friend.bdate ? friend.bdate : 'Не указана';
                const ageInDays = calculateAgeInDays(friend.bdate);
                html += `
                    <tr>
                        <td>${friend.id}</td>
                        <td>${friend.first_name}</td>
                        <td>${friend.last_name}</td>
                        <td>${city}</td>
                        <td>${bdate}</td>
                        <td>${ageInDays}</td>
                    </tr>
                `;
            });
            html += '</table>';
            $('#output').html(html);

            $('#sortLastNameAsc').click(() => sortFriends('asc'));
            $('#sortLastNameDesc').click(() => sortFriends('desc'));
        }

        function sortFriends(order) {
            const sortedFriends = friendsData.slice().sort((a, b) => {
                if (order === 'asc') {
                    return a.last_name.localeCompare(b.last_name);
                } else {
                    return b.last_name.localeCompare(a.last_name);
                }
            });
            displayFriends(sortedFriends);
        }

        function calculateAgeInDays(bdate) {
            if (!bdate || bdate.split('.').length < 3) return 'Неизвестно';

            const [day, month, year] = bdate.split('.').map(Number);
            const birthDate = new Date(year, month - 1, day);
            const today = new Date();
            const diffTime = today - birthDate;
            const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

            return diffDays;
        }

        $(document).ready(function() {
            $('#loadFriends').click(loadFriends);
        });
    </script>
</body>
</html>

Код CSS файла
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #e6f0ff;
    color: #2c3e50;
}

.container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #1a2a4f;
}

button {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #1a2a4f;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: block;
    margin: 0 auto 20px;
}

button:hover {
    background-color: #0d1a33;
}

#output {
    margin-top: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

table, th, td {
    border: 1px solid #a8c6ff;
}

th, td {
    padding: 10px;
    text-align: left;
}

th {
    background-color: #1a2a4f;
    color: #ffffff;
    position: relative;
    padding-left: 50px;
}

th .sort-buttons {
    position: absolute;
    left: 10px;
    top: 65%;
    transform: translateY(-50%);
    display: flexbox;
    flex-direction: column;
    gap: 5px;
}

th .sort-button {
    background: none;
    border: none;
    color: #ffffff;
    cursor: pointer;
    padding: 0px;
    font-size: 14px;
    transition: color 0.3s ease;
}

th .sort-button:hover {
    color: #a8c6ff;
}

.error {
    color: #e74c3c;
    text-align: center;
    font-size: 16px;
}

th:nth-child(4), td:nth-child(4), 
th:nth-child(5), td:nth-child(5),
th:nth-child(6), td:nth-child(6) { 
    padding-left: 5px; 
    padding-right: 5px; 
    text-align: center;
}
