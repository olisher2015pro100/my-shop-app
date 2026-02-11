let tg = window.Telegram.WebApp;
tg.expand(); // Раскрываем окно на максимум

// Функция, которая отправляет данные боту
function sendOrder(name, price) {
    let data = {
        item: name,
        price: price
    };
    
    // Передаем данные в Telegram
    tg.sendData(JSON.stringify(data)); 
}
