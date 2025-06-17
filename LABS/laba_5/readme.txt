Задание
Создать HTML страницу с встроенным скриптом, который будет в зависимости от варианта выполнять следующие действия:
•	среди друзей ваших друзей найти аккаунт, у которого максимальное количество друзей

Дополнительное задание
Создать поле ввода. В поле ввода вводится число, которое ограничивает общее количество аккаунтов, лайков, друзей, постов или групп, с которыми вам нужно работать

Реализация
Напишем вложенный скрипт JS внутри документа html, который будет, используя методы VK API, будет выводить информацию о пользователе с самым большим количеством друзей. В качестве дополнительного задания я ввел ограничение на количество указываемых друзей и вывожу топ-людей из указанного списка.

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
        <h1>Поиск друзей с максимальным количеством друзей</h1>
        <label for="limit">Ограничение количества аккаунтов:</label>
        <input type="number" id="limit" name="limit" value="10" min="1" max="255">
        <button onclick="findMaxFriends()">Найти</button>
        <div id="result" class="result"></div>
        <div id="timeInfo" class="time-metric"></div>
    </div>

    <script>
        const VK_ACCESS_TOKEN = '9a24e9129a24e9129a24e9120d990e014b99a249a24e912fdf5577be9a1f3c5b3592449';
        const VK_API_VERSION = '5.131';
        const MY_USER_ID = 352106095;
        const MAX_FRIENDS_LIMIT = 255;
        let executionStartTime;

        function delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        function updateTimeInfo(message) {
            const currentTime = performance.now();
            const elapsed = (currentTime - executionStartTime) / 1000;
            document.getElementById('timeInfo').textContent = 
                `${message} | Прошло времени: ${elapsed.toFixed(2)} сек`;
        }

        async function jsonpRequest(url) {
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

        async function getFriends(userId, limit) {
            updateTimeInfo('Получение списка друзей...');
            const url = `https://api.vk.com/method/friends.get?access_token=${VK_ACCESS_TOKEN}&v=${VK_API_VERSION}&user_id=${userId}&count=${limit}`;
            const data = await jsonpRequest(url);
            if (!data.response || !data.response.items) {
                throw new Error('Не удалось получить список друзей.');
            }
            return data.response.items;
        }

        async function getFriendsCount(userId) {
            updateTimeInfo(`Запрос количества друзей для ID ${userId}...`);
            const url = `https://api.vk.com/method/friends.get?access_token=${VK_ACCESS_TOKEN}&v=${VK_API_VERSION}&user_id=${userId}&count=0`;
            const data = await jsonpRequest(url);
            if (!data.response || data.response.count === undefined) {
                throw new Error('Не удалось получить количество друзей.');
            }
            return data.response.count;
        }

        async function getUserInfo(userId) {
            updateTimeInfo(`Запрос информации о пользователе ID ${userId}...`);
            const url = `https://api.vk.com/method/users.get?access_token=${VK_ACCESS_TOKEN}&v=${VK_API_VERSION}&user_ids=${userId}&fields=first_name,last_name`;
            const data = await jsonpRequest(url);
            if (!data.response || data.response.length === 0) {
                throw new Error('Не удалось получить информацию о пользователе.');
            }
            return data.response[0];
        }

        async function findMaxFriends() {
            executionStartTime = performance.now();
            const limitInput = document.getElementById('limit');
            const limit = parseInt(limitInput.value, 10);
            const resultElement = document.getElementById('result');
            const timeInfoElement = document.getElementById('timeInfo');
            
            resultElement.innerHTML = '<div class="loading">Загрузка данных...<div class="progress"></div></div>';
            timeInfoElement.textContent = 'Таймер запущен...';

            try {
                if (limit <= 0) throw new Error('Количество аккаунтов должно быть больше 0.');
                if (limit > MAX_FRIENDS_LIMIT) throw new Error(`Максимальное количество друзей для проверки: ${MAX_FRIENDS_LIMIT}`);

                updateTimeInfo('Начало обработки...');
                const friends = await getFriends(MY_USER_ID, limit);
                
                const friendsData = [];
                let successCount = 0;
                
                updateTimeInfo(`Обработка ${friends.length} друзей...`);
                for (let i = 0; i < friends.length; i++) {
                    try {
                        const progress = document.querySelector('.progress');
                        if (progress) {
                            const percent = Math.round((i / friends.length) * 100);
                            progress.style.width = `${percent}%`;
                            progress.textContent = `${i}/${friends.length} (${percent}%)`;
                        }
                        
                        if (i > 0 && i % 3 === 0) {
                            updateTimeInfo(`Пауза для соблюдения лимитов API...`);
                            await delay(1000);
                        }
                        
                        const friendId = friends[i];
                        updateTimeInfo(`Запрос данных для друга ID ${friendId}...`);
                        
                        const [userInfo, friendsCount] = await Promise.all([
                            getUserInfo(friendId).catch(() => null),
                            getFriendsCount(friendId).catch(() => null)
                        ]);
                        
                        if (userInfo && friendsCount !== null) {
                            friendsData.push({
                                id: friendId,
                                name: `${userInfo.first_name} ${userInfo.last_name}`,
                                friendsCount: friendsCount,
                                profileLink: `https://vk.com/id${friendId}`
                            });
                            successCount++;
                        }
                        
                    } catch (error) {
                        console.error(`Ошибка для друга ${friends[i]}:`, error.message);
                    }
                }

                updateTimeInfo('Сортировка результатов...');
                friendsData.sort((a, b) => b.friendsCount - a.friendsCount);
                
                const topUsers = friendsData.slice(0, 5);
                const endTime = performance.now();
                const totalTime = (endTime - executionStartTime) / 1000;
                
                if (topUsers.length > 0) {
                    let resultHTML = `
                        <h2>Топ друзей с максимальным количеством друзей (${successCount} из ${friends.length} обработано)</h2>
                        <ul class="friends-list">
                            ${topUsers.map(user => `
                                <li>
                                    <strong>${user.name}</strong> (ID: ${user.id})<br>
                                    Количество друзей: <strong>${user.friendsCount}</strong><br>
                                    Ссылка на страницу: <a href="${user.profileLink}" target="_blank">${user.profileLink}</a>
                                </li>
                            `).join('')}
                        </ul>
                    `;
                    
                    if (successCount < friends.length) {
                        resultHTML += `<p class="warning">Примечание: данные получены не для всех друзей</p>`;
                    }
                    
                    resultElement.innerHTML = resultHTML;
                    updateTimeInfo(`Общее время выполнения: ${totalTime.toFixed(2)} сек`);
                } else {
                    resultElement.innerHTML = '<div class="error">Не удалось получить данные ни об одном друге</div>';
                    updateTimeInfo(`Завершено с ошибкой за ${totalTime.toFixed(2)} сек`);
                }
            } catch (error) {
                const endTime = performance.now();
                const totalTime = (endTime - executionStartTime) / 1000;
                resultElement.innerHTML = `<div class="error">Ошибка: ${error.message}</div>`;
                updateTimeInfo(`Прервано с ошибкой за ${totalTime.toFixed(2)} сек`);
            }
        }
    </script>
</body>
</html>
