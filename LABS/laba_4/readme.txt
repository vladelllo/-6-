Задание
Создать HTML страницу с встроенным скриптом, который будет в зависимости от варианта выполнять следующие действия:
● Изменять статус страницы

Реализация
Напишем вложенный скрипт JS внутри документа html, который будет, используя методы VK API, менять статус в социальной сети ВК.

Код HTML файла
<!DOCTYPE html>
<html>
<head>
    <title>ЛР №4</title>
     <link rel="stylesheet" href="styles.css">
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
</head>

<body>
    <script>
        get_token = 'https://oauth.vk.com/authorize?client_id=53143641&redirect_url=https://oauth.vk.com/blank.html&response_type=token&scope=status'
        
        $(document).ready(function() {
            $("#load").click(function() {
                let text = encodeURIComponent($("#set-status").val());
                let token = 'vk1.a.gwkaMXOEfF-bUxhSdx26kRcWVJoQIjNa5rg3YGPA_0-sMXMkgbMEyeJNiLMVAjo-nIoGd_zlzARP9uGil6EnFeXgm9iMFV8ak27jup_hfov29mmBozG611CgjIST-y7D9d1fVeUxM7CsvRP6DbKyHRxAIxxfqBlcqZbmNt-nolGSq1Myy470wW27FWsa_BSV';
                
                $.ajax({
                    url: `https://api.vk.com/method/status.set?text=${text}&access_token=${token}&v=5.131`,
                    dataType: 'jsonp',
                    success: function(response) {
                        if (response.response) {
                            alert("Статус успешно изменен!");
                        } else if (response.error) {
                            alert("Ошибка: " + response.error.error_msg);
                        }
                    },
                    error: function(xhr, status, error) {
                        alert("Произошла ошибка при запросе: " + status);
                    }
                });
            });
        });
    </script>
    <div>
        <input type="text" id="set-status">
        <button id="load">Load</button>
    </div>
</body>
</html>

Код CSS файла
/* Глобальные стили с анимацией фона */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #533d7b);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #ffffff;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Контейнер с эффектом стекла и подсветкой */
.container {
    width: 100%;
    max-width: 600px;
    padding: 2.5rem;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), 
                0 0 0 1px rgba(255, 255, 255, 0.05) inset,
                0 0 30px rgba(79, 195, 247, 0.1) inset;
    text-align: center;
    position: relative;
    overflow: hidden;
    transform: translateY(0);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    z-index: 1;
}

.container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        to bottom right,
        rgba(255, 255, 255, 0) 0%,
        rgba(255, 255, 255, 0.05) 50%,
        rgba(255, 255, 255, 0) 100%
    );
    transform: rotate(30deg);
    animation: shine 6s infinite;
    z-index: -1;
}

@keyframes shine {
    0% { transform: rotate(30deg) translate(-30%, -30%); }
    100% { transform: rotate(30deg) translate(30%, 30%); }
}

.container:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 
                0 0 0 1px rgba(255, 255, 255, 0.1) inset,
                0 0 40px rgba(79, 195, 247, 0.2) inset;
}

/* Анимированный заголовок */
.title {
    margin-bottom: 2rem;
    font-size: 2.2rem;
    background: linear-gradient(90deg, #4fc3f7, #a6c1ee);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 2px 10px rgba(79, 195, 247, 0.3);
    position: relative;
    display: inline-block;
}

.title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #4fc3f7, transparent);
    border-radius: 3px;
    animation: titleUnderline 3s infinite;
}

@keyframes titleUnderline {
    0% { width: 0; left: 0; }
    50% { width: 100%; left: 0; }
    100% { width: 0; left: 100%; }
}

/* Группа ввода с плавной анимацией */
.input-group {
    display: flex;
    gap: 12px;
    margin-bottom: 2rem;
    transition: all 0.4s ease;
}

/* Поле ввода с эффектом свечения */
#set-status {
    flex: 1;
    padding: 14px 22px;
    font-size: 1.05rem;
    border: 2px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    background-color: rgba(0, 0, 0, 0.2);
    color: white;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

#set-status:focus {
    outline: none;
    border-color: rgba(79, 195, 247, 0.6);
    background-color: rgba(0, 0, 0, 0.3);
    box-shadow: 0 0 0 3px rgba(79, 195, 247, 0.2),
                0 0 20px rgba(79, 195, 247, 0.3);
    transform: translateY(-2px);
}

#set-status::placeholder {
    color: rgba(255, 255, 255, 0.4);
    transition: all 0.3s ease;
}

#set-status:focus::placeholder {
    opacity: 0.6;
    transform: translateX(5px);
}

/* Кнопка с эффектом пульсации */
#load {
    padding: 14px 28px;
    font-size: 1.05rem;
    font-weight: 600;
    background: linear-gradient(135deg, #4fc3f7 0%, #2196f3 100%);
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset;
    position: relative;
    overflow: hidden;
}

#load:hover {
    background: linear-gradient(135deg, #2196f3 0%, #4fc3f7 100%);
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(33, 150, 243, 0.5),
                0 0 0 1px rgba(255, 255, 255, 0.15) inset;
}

#load:active {
    transform: translateY(1px);
    box-shadow: 0 2px 10px rgba(33, 150, 243, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset;
}

#load::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
                rgba(255, 255, 255, 0) 0%, 
                rgba(255, 255, 255, 0.2) 50%, 
                rgba(255, 255, 255, 0) 100%);
    transform: translateX(-100%);
    transition: transform 0.6s ease;
}

#load:hover::after {
    transform: translateX(100%);
}

/* Информационный текст с мерцанием */
.info {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.7);
    margin-top: 1.5rem;
    position: relative;
    animation: subtleGlow 4s infinite alternate;
}

@keyframes subtleGlow {
    0% { opacity: 0.7; text-shadow: 0 0 5px rgba(255, 255, 255, 0); }
    100% { opacity: 1; text-shadow: 0 0 10px rgba(255, 255, 255, 0.2); }
}

/* Уведомления с улучшенной анимацией */
.notification {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%) translateY(100px) scale(0.9);
    padding: 16px 32px;
    border-radius: 12px;
    font-weight: 500;
    opacity: 0;
    transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    z-index: 1000;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.notification.show {
    transform: translateX(-50%) translateY(0) scale(1);
    opacity: 1;
}

.notification.success {
    background: rgba(76, 175, 80, 0.85);
    box-shadow: 0 10px 25px rgba(76, 175, 80, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset;
}

.notification.error {
    background: rgba(244, 67, 54, 0.85);
    box-shadow: 0 10px 25px rgba(244, 67, 54, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset;
}

@media (max-width: 768px) {
    .container {
        width: 92%;
        padding: 2rem 1.5rem;
        border-radius: 16px;
    }
    
    .input-group {
        flex-direction: column;
        gap: 15px;
    }
    
    #load {
        width: 100%;
        padding: 14px;
    }

    .title {
        font-size: 1.8rem;
        margin-bottom: 1.8rem;
    }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%, 60% { transform: translateX(-5px); }
    40%, 80% { transform: translateX(5px); }
}

.shake {
    animation: shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
    border-color: #f44336 !important;
}
