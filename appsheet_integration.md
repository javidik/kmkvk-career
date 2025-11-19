# Интеграция с AppSheet для личного кабинета КМКВК

## Обзор
Для реализации полноценной системы личного кабинета с хранением данных пользователей, прогресса и результатов тестов, мы будем использовать Google AppSheet - бесплатный сервис для создания приложений без кода.

## Архитектура системы

### 1. Google Таблицы (Google Sheets) как база данных
- **Таблица Users**: Хранение данных пользователей
- **Таблица Progress**: Отслеживание прогресса пользователей
- **Таблица TestResults**: Результаты пройденных тестов
- **Таблица Materials**: Доступные учебные материалы
- **Таблица Achievements**: Достижения пользователей

### 2. Структура таблиц

#### Таблица Users:
```
- ID (автоматически)
- Email
- Name
- Password (зашифрованный)
- StudentClass
- RegistrationDate
- LastLogin
- IsActive
- Role (student, cadet, admin)
```

#### Таблица Progress:
```
- ID (автоматически)
- UserID
- MaterialID
- CompletionDate
- Score
- TimeSpent
```

#### Таблица TestResults:
```
- ID (автоматически)
- UserID
- TestID
- TestDate
- Score
- Answers
- Category
```

## Настройка AppSheet

### Шаг 1: Подготовка Google Таблицы
1. Создайте новую Google Таблицу
2. Создайте листы с названиями: Users, Progress, TestResults, Materials, Achievements
3. Заполните заголовки столбцов как описано выше
4. Поделитесь таблицей, разрешив редактирование для AppSheet

### Шаг 2: Создание приложения в AppSheet
1. Перейдите на [https://www.appsheet.com](https://www.appsheet.com)
2. Войдите с вашим Google аккаунтом
3. Нажмите "Create new app"
4. Выберите "Start with a spreadsheet"
5. Выберите вашу Google Таблицу
6. AppSheet автоматически определит структуру таблиц

### Шаг 3: Настройка безопасности
1. Перейдите в "Security" в настройках приложения
2. Настройте аутентификацию пользователей
3. Определите права доступа для разных типов пользователей
4. Настройте правила доступа к данным

### Шаг 4: Настройка веб-интерфейса
1. Перейдите в "UX" (User Experience)
2. Настройте отображение данных
3. Создайте формы для регистрации и входа
4. Настройте виджеты для отображения прогресса

## Интеграция с веб-сайтом

### API-интеграция
Для интеграции с нашим веб-сайтом используем AppSheet API:

```javascript
// Пример интеграции с AppSheet API
const APPSHEET_APP_ID = 'ваш-id-приложения';
const APPSHEET_API_KEY = 'ваш-api-ключ';

// Функция для получения данных пользователя
async function getUserData(userId) {
  const response = await fetch(`https://api.appsheet.com/rest/v2/apps/${APPSHEET_APP_ID}/tables/Users/Action`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'ApplicationAccessKey': APPSHEET_API_KEY
    },
    body: JSON.stringify({
      Action: 'Find',
      TableName: 'Users',
      Filters: [
        `[_ID_] = '${userId}'`
      ]
    })
  });
  
  return response.json();
}

// Функция для обновления прогресса пользователя
async function updateProgress(userId, materialId, score) {
  const response = await fetch(`https://api.appsheet.com/rest/v2/apps/${APPSHEET_APP_ID}/tables/Progress/Action`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'ApplicationAccessKey': APPSHEET_API_KEY
    },
    body: JSON.stringify({
      Action: 'Add',
      TableName: 'Progress',
      Rows: [{
        UserID: userId,
        MaterialID: materialId,
        Score: score,
        CompletionDate: new Date().toISOString()
      }]
    })
  });
  
  return response.json();
}
```

### Альтернативные решения

Если AppSheet не подходит, можно использовать другие бесплатные сервисы:

#### 1. Google Apps Script
- Создание собственного API поверх Google Таблиц
- Полный контроль над логикой
- Бесплатный, но с ограничениями по использованию

#### 2. Firebase
- Бесплатный тариф с хорошими возможностями
- Аутентификация, база данных, хостинг
- Требует больше навыков программирования

#### 3. Airtable
- Похож на AppSheet, но с более гибкими возможностями
- Бесплатный тариф с ограничениями
- Хорошая документация и API

## Использование Google Apps Script (альтернатива)

### Шаг 1: Создание Script в Google Apps Script
1. Перейдите на [https://script.google.com](https://script.google.com)
2. Создайте новый проект
3. Добавьте код для API:

```javascript
var sheetId = 'ваш-sheet-id';
var usersSheet = 'Users';
var progressSheet = 'Progress';

function doGet(e) {
  var action = e.parameter.action;
  
  if (action === 'login') {
    return login(e.parameter.email, e.parameter.password);
  } else if (action === 'register') {
    return register(e.parameter);
  } else if (action === 'getUserData') {
    return getUserData(e.parameter.userId);
  }
  
  return ContentService.createTextOutput('Invalid action');
}

function doPost(e) {
  var action = e.parameter.action;
  
  if (action === 'updateProgress') {
    return updateProgress(e.parameter);
  }
  
  return ContentService.createTextOutput('Invalid action');
}

function login(email, password) {
  var sheet = SpreadsheetApp.openById(sheetId).getSheetByName(usersSheet);
  var data = sheet.getDataRange().getValues();
  
  for (var i = 1; i < data.length; i++) {
    if (data[i][1] === email) { // предполагаем, что email в колонке 1
      if (data[i][2] === password) { // предполагаем, что пароль в колонке 2
        var user = {
          id: data[i][0],
          email: data[i][1],
          name: data[i][3]
        };
        return ContentService.createTextOutput(JSON.stringify({success: true, user: user}))
          .setMimeType(ContentService.MimeType.JSON);
      }
    }
  }
  
  return ContentService.createTextOutput(JSON.stringify({success: false, error: 'Invalid credentials'}))
    .setMimeType(ContentService.MimeType.JSON);
}

function register(params) {
  var sheet = SpreadsheetApp.openById(sheetId).getSheetByName(usersSheet);
  var newRow = [
    new Date().getTime().toString(), // ID
    params.email,
    params.password,
    params.name,
    params.studentClass || '',
    new Date()
  ];
  
  sheet.appendRow(newRow);
  
  return ContentService.createTextOutput(JSON.stringify({success: true, id: newRow[0]}))
    .setMimeType(ContentService.MimeType.JSON);
}
```

### Шаг 2: Публикация Web App
1. В меню выберите "Publish" → "Deploy from manifest..."
2. Создайте новое развертывание
3. Установите доступ для "Anyone" (или настройте как нужно)
4. Скопируйте URL развертывания

## Заключение

Система личного кабинета для КМКВК может быть успешно реализована с использованием бесплатных сервисов:

- **AppSheet**: Для быстрой реализации с визуальным интерфейсом
- **Google Apps Script**: Для большего контроля над логикой
- **Firebase**: Для более сложных сценариев

Все эти решения позволяют создать полноценный личный кабинет с аутентификацией, отслеживанием прогресса и персонализированным контентом без необходимости в собственном сервере.