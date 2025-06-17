Задание
Задание на эту лабораторную работу такое же, как и для предыдущей, однако реализовать её нужно с помощью async/await. Необходимо создать HTML страницу с встроенным скриптом, который будет в зависимости от варианта выполнять следующие действия:
● среди друзей ваших друзей найти аккаунт, у которого максимальное количество друзей 

Дополнительное задание
Создать поле ввода. В поле ввода вводится число, которое ограничивает общее количество аккаунтов, лайков, друзей, постов или групп, с которыми вам нужно работать

Реализация
Напишем вложенный скрипт JS внутри документа html, который будет, используя методы VK API, будет выводить информацию о пользователе с самым большим количеством друзей. В качестве дополнительного задания я ввел ограничение на количество указываемых друзей и вывожу топ-людей из указанного списка.
Код будет реализован по принципам асинхронного программирования при помощи async/await, а также будет указано время выполнения

Код HTML файла
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VK API Friends</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Поиск друзей с максимальным количеством друзей (Promise версия)</h1>
        <label for="limit">Ограничение количества аккаунтов:</label>
        <input type="number" id="limit" name="limit" value="10" min="1" max="255">
        <button onclick="findMaxFriends()">Найти</button>
        <div id="result" class="result"></div>
        <div id="timeInfo" class="time-info"></div>
    </div>

    <script>
        const VK_ACCESS_TOKEN = '9a24e9129a24e9129a24e9120d990e014b99a249a24e912fdf5577be9a1f3c5b3592449';
        const VK_API_VERSION = '5.131';
        const MY_USER_ID = 352106095;
        const MAX_FRIENDS_LIMIT = 255;
        let startTime;

        function jsonpRequest(url) {
            return new Promise((resolve, reject) => {
                const callbackName = `jsonp_callback_${Math.round(100000 * Math.random())}`;
                window[callbackName] = (data) => {
                    delete window[callbackName];
                    document.body.removeChild(script);
                    if (data.error) {
                        reject(new Error(data.error.error_msg));
                    } else {
                        resolve(data);
                    }
                };

                const script = document.createElement('script');
                script.src = `${url}&callback=${callbackName}`;
                script.onerror = () => {
                    reject(new Error('Ошибка при загрузке данных.'));
                };
                document.body.appendChild(script);
            });
        }

        function getFriends(userId, limit) {
            const url = `https://api.vk.com/method/friends.get?access_token=${VK_ACCESS_TOKEN}&v=${VK_API_VERSION}&user_id=${userId}&count=${limit}`;
            return jsonpRequest(url)
                .then(data => {
                    if (!data.response || !data.response.items) {
                        throw new Error('Не удалось получить список друзей.');
                    }
                    return data.response.items;
                });
        }

        function getFriendsCount(userId) {
            const url = `https://api.vk.com/method/friends.get?access_token=${VK_ACCESS_TOKEN}&v=${VK_API_VERSION}&user_id=${userId}&count=0`;
            return jsonpRequest(url)
                .then(data => {
                    if (!data.response || data.response.count === undefined) {
                        throw new Error('Не удалось получить количество друзей.');
                    }
                    return data.response.count;
                });
        }

        function getUserInfo(userId) {
            const url = `https://api.vk.com/method/users.get?access_token=${VK_ACCESS_TOKEN}&v=${VK_API_VERSION}&user_ids=${userId}&fields=first_name,last_name`;
            return jsonpRequest(url)
                .then(data => {
                    if (!data.response || data.response.length === 0) {
                        throw new Error('Не удалось получить информацию о пользователе.');
                    }
                    return data.response[0];
                });
        }

        function delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        function findMaxFriends() {
            startTime = performance.now();
            const limitInput = document.getElementById('limit');
            const limit = parseInt(limitInput.value, 10);
            const resultElement = document.getElementById('result');
            const timeInfoElement = document.getElementById('timeInfo');
            
            resultElement.textContent = 'Загрузка...';
            timeInfoElement.textContent = '';

            if (limit <= 0) {
                resultElement.textContent = 'Количество аккаунтов должно быть больше 0.';
                return;
            }
            if (limit > MAX_FRIENDS_LIMIT) {
                resultElement.textContent = `Максимальное количество друзей для проверки: ${MAX_FRIENDS_LIMIT}`;
                return;
            }

            getFriends(MY_USER_ID, limit)
                .then(friends => {
                    const friendsDataPromises = [];
                    let processed = 0;

                    friends.forEach((friendId, index) => {
                        // Добавляем задержку между запросами
                        const promise = delay(index * 300)
                            .then(() => Promise.all([
                                getUserInfo(friendId).catch(() => null),
                                getFriendsCount(friendId).catch(() => null)
                            ]))
                            .then(([userInfo, friendsCount]) => {
                                processed++;
                                resultElement.textContent = `Обработано ${processed} из ${friends.length} друзей...`;
                                
                                if (userInfo && friendsCount !== null) {
                                    return {
                                        id: friendId,
                                        name: `${userInfo.first_name} ${userInfo.last_name}`,
                                        friendsCount: friendsCount,
                                        profileLink: `https://vk.com/id${friendId}`
                                    };
                                }
                                return null;
                            });

                        friendsDataPromises.push(promise);
                    });

                    return Promise.all(friendsDataPromises);
                })
                .then(friendsData => {
                    // Фильтруем null значения (ошибки запросов)
                    const validFriendsData = friendsData.filter(f => f !== null);
                    
                    // Сортируем по количеству друзей
                    validFriendsData.sort((a, b) => b.friendsCount - a.friendsCount);
                    
                    // Берем топ-5
                    const topUsers = validFriendsData.slice(0, 5);
                    
                    const endTime = performance.now();
                    const executionTime = (endTime - startTime) / 1000;
                    
                    if (topUsers.length > 0) {
                        resultElement.innerHTML = `
                            <h2>Топ друзей с максимальным количеством друзей:</h2>
                            <ul>
                                ${topUsers.map(user => `
                                    <li>
                                        <strong>${user.name}</strong> (ID: ${user.id})<br>
                                        Количество друзей: <strong>${user.friendsCount}</strong><br>
                                        Ссылка на страницу: <a href="${user.profileLink}" target="_blank">${user.profileLink}</a>
                                    </li>
                                `).join('')}
                            </ul>
                        `;
                    } else {
                        resultElement.textContent = 'Не удалось получить информацию о друзьях.';
                    }
                    
                    timeInfoElement.textContent = `Время выполнения: ${executionTime.toFixed(2)} секунд`;
                })
                .catch(error => {
                    resultElement.textContent = 'Произошла ошибка: ' + error.message;
                    const endTime = performance.now();
                    timeInfoElement.textContent = `Время выполнения: ${((endTime - startTime)/1000).toFixed(2)} секунд (с ошибкой)`;
                });
        }
    </script>
</body>
</html>
