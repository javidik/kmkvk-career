/* ============================================
   MAIN.JS - Функциональность сайта
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
  initializeBurgerMenu();
  initializeAccordion();
  initializeActiveNavLink();
});

/* ============================================
   БУРГЕР МЕНЮ ДЛЯ МОБИЛЬНЫХ
   ============================================ */

function initializeBurgerMenu() {
  const burgerMenu = document.querySelector('.burger-menu');
  const nav = document.querySelector('nav');

  if (burgerMenu) {
    burgerMenu.addEventListener('click', function(e) {
      e.preventDefault();
      nav.classList.toggle('open');
    });

    // Закрыть меню при клике на ссылку
    const navLinks = nav.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        nav.classList.remove('open');
      });
    });

    // Закрыть меню при клике вне его
    document.addEventListener('click', function(e) {
      if (!e.target.closest('nav') && !e.target.closest('.burger-menu')) {
        nav.classList.remove('open');
      }
    });
  }
}

/* ============================================
   АКТИВНАЯ ССЫЛКА В МЕНЮ
   ============================================ */

function initializeActiveNavLink() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('.nav-link');

  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

/* ============================================
   АККОРДЕОН
   ============================================ */

function initializeAccordion() {
  const accordionHeaders = document.querySelectorAll('.accordion-header');

  accordionHeaders.forEach(header => {
    header.addEventListener('click', function() {
      const accordionItem = this.closest('.accordion-item');
      const isActive = accordionItem.classList.contains('active');

      // Закрыть все аккордеоны в этом контейнере
      const accordion = this.closest('.accordion');
      if (accordion) {
        accordion.querySelectorAll('.accordion-item').forEach(item => {
          item.classList.remove('active');
        });
      }

      // Открыть текущий, если он был закрыт
      if (!isActive) {
        accordionItem.classList.add('active');
      }
    });
  });
}

/* ============================================
   ПОДБОР ВУЗОВ ПО ФИЛЬТРАМ
   ============================================ */

function filterVuzyByType(type) {
  const cards = document.querySelectorAll('.vuzy-card');
  const filterButtons = document.querySelectorAll('[data-filter]');

  // Обновить активную кнопку
  filterButtons.forEach(btn => {
    btn.classList.remove('active');
  });
  event.target.classList.add('active');

  // Фильтровать карточки
  cards.forEach(card => {
    if (type === 'all' || card.getAttribute('data-type') === type) {
      card.style.display = 'block';
      setTimeout(() => card.style.opacity = '1', 10);
    } else {
      card.style.opacity = '0';
      setTimeout(() => card.style.display = 'none', 300);
    }
  });
}

/* ============================================
   МОДАЛЬНЫЕ ОКНА
   ============================================ */

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
  }
}

document.addEventListener('click', function(e) {
  // Закрыть модаль при клике на backdrop
  if (e.target.classList.contains('modal')) {
    e.target.classList.remove('active');
    document.body.style.overflow = 'auto';
  }

  // Закрыть модаль при клике на кнопку закрытия
  if (e.target.classList.contains('modal-close')) {
    e.target.closest('.modal').classList.remove('active');
    document.body.style.overflow = 'auto';
  }
});

/* ============================================
   КАЛЬКУЛЯТОР БАЛЛОВ
   ============================================ */

function calculateScore() {
  const russianScore = parseFloat(document.getElementById('russian').value) || 0;
  const mathScore = parseFloat(document.getElementById('math').value) || 0;
  const thirdScore = parseFloat(document.getElementById('third').value) || 0;
  const physScore = parseFloat(document.getElementById('phys').value) || 0;

  const totalEGE = russianScore + mathScore + thirdScore;
  const totalScore = totalEGE + physScore;

  const resultDiv = document.getElementById('calcResult');
  if (resultDiv) {
    resultDiv.innerHTML = `
      <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin-top: 20px;">
        <h3 style="margin-top: 0; color: #1a3a52;">Результат расчета</h3>
        <p><strong>Сумма баллов ЕГЭ:</strong> ${totalEGE}</p>
        <p><strong>Баллы физподготовки:</strong> ${physScore}</p>
        <p style="font-size: 18px; color: #d4af37; font-weight: bold;">
          <strong>ИТОГО:</strong> ${totalScore}
        </p>
        <div class="progress-bar" style="margin-top: 15px;">
          <div class="progress-fill" style="width: ${Math.min(totalScore / 3, 100)}%"></div>
        </div>
        <p style="font-size: 12px; color: #666;">
          ${totalScore >= 200 ? '✓ Хороший результат для большинства ВУЗов' : 
            totalScore >= 150 ? '✓ Средний результат - подходит для ряда ВУЗов' : 
            '⚠ Рекомендуется повысить баллы'}
        </p>
      </div>
    `;
  }
}

/* ============================================
   ПРОФЕССИОНАЛЬНЫЙ ТЕСТ
   ============================================ */

function submitTest() {
  const form = document.getElementById('testForm');
  if (!form) return;

  const formData = new FormData(form);
  const answers = {};

  formData.forEach((value, key) => {
    answers[key] = value;
  });

  const resultDiv = document.getElementById('testResult');
  if (resultDiv) {
    // Простая логика подсчета
    let points = 0;
    for (let key in answers) {
      if (answers[key] === 'yes') {
        points += 1;
      }
    }

    const percentage = Math.round((points / Object.keys(answers).length) * 100);
    const category = percentage >= 80 ? 'I категория' : 
                    percentage >= 60 ? 'II категория' : 
                    'III категория';

    resultDiv.innerHTML = `
      <div style="background: #eaf1f6; padding: 20px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #d4af37;">
        <h3 style="margin-top: 0; color: #1a3a52;">Результаты теста</h3>
        <p><strong>Ваша категория:</strong> <span style="color: #d4af37; font-weight: bold; font-size: 16px;">${category}</span></p>
        <p><strong>Совпадение:</strong> ${percentage}%</p>
        <p style="color: #666; font-size: 14px;">
          ${percentage >= 80 ? 'Вы хорошо подходите для военной карьеры! Рекомендуется выбирать ВУЗы с высокими требованиями.' : 
            percentage >= 60 ? 'Вы имеете хороший потенциал. Рекомендуется развивать военно-профессиональные навыки.' : 
            'Рекомендуется пройти консультацию с психологом для определения оптимального пути развития.'}
        </p>
      </div>
    `;
  }
}

/* ============================================
   ФОРМА ОБРАТНОЙ СВЯЗИ
   ============================================ */

function submitFeedback(e) {
  if (e) {
    e.preventDefault();
  }

  const form = document.getElementById('feedbackForm');
  if (!form) return;

  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const message = document.getElementById('message').value;

  if (!name || !email || !message) {
    alert('Заполните все поля формы');
    return;
  }

  // Валидация email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert('Введите корректный email');
    return;
  }

  // Здесь можно отправить данные на сервер
  // Для демонстрации просто показываем сообщение об успехе
  alert('Спасибо за обращение! Мы свяжемся с вами в ближайшее время.');
  form.reset();
}

/* ============================================
   ПОИСК ВУЗОВ ПО НАЗВАНИЮ
   ============================================ */

function searchVuzy(searchTerm) {
  const cards = document.querySelectorAll('.vuzy-card');
  const term = searchTerm.toLowerCase();

  cards.forEach(card => {
    const title = card.querySelector('h3').textContent.toLowerCase();
    const text = card.textContent.toLowerCase();

    if (title.includes(term) || text.includes(term)) {
      card.style.display = 'block';
      card.style.opacity = '1';
    } else {
      card.style.opacity = '0';
      setTimeout(() => card.style.display = 'none', 300);
    }
  });
}

/* ============================================
   СОРТИРОВКА ТАБЛИЦ
   ============================================ */

function sortTable(n) {
  const table = document.querySelector('table');
  let rows = Array.from(table.getElementsByTagName('tbody')[0].getElementsByTagName('tr'));
  let ascending = true;

  // Проверить текущее направление сортировки
  const header = table.querySelectorAll('th')[n];
  if (header.classList.contains('sorted-asc')) {
    ascending = false;
    header.classList.remove('sorted-asc');
    header.classList.add('sorted-desc');
  } else {
    header.classList.add('sorted-asc');
  }

  rows.sort((a, b) => {
    const aVal = a.getElementsByTagName('td')[n].textContent;
    const bVal = b.getElementsByTagName('td')[n].textContent;

    if (!isNaN(aVal) && !isNaN(bVal)) {
      return ascending ? parseFloat(aVal) - parseFloat(bVal) : parseFloat(bVal) - parseFloat(aVal);
    } else {
      return ascending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    }
  });

  const tbody = table.querySelector('tbody');
  rows.forEach(row => tbody.appendChild(row));
}

/* ============================================
   ПРОКРУТКА К ЯКОРЮ (SMOOTH SCROLL)
   ============================================ */

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const href = this.getAttribute('href');
    if (href !== '#') {
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    }
  });
});

/* ============================================
   ТАБЛИЦА НОРМАТИВОВ ПО ФИЗПОДГОТОВКЕ
   ============================================ */

function displayNormativy(type) {
  const normativy = {
    'pull-ups': {
      min: '12 раз',
      good: '18 раз',
      excellent: '25 раз'
    },
    'run100': {
      min: '15,5 сек',
      good: '13,5 сек',
      excellent: '12,5 сек'
    },
    'run3km': {
      min: '14:00',
      good: '12:00',
      excellent: '10:30'
    },
    'swimming': {
      min: '2:40',
      good: '2:05',
      excellent: '1:35'
    }
  };

  const table = normativy[type];
  if (table) {
    return `
      <table style="width: 100%; margin-top: 10px;">
        <tr style="background: #f5f5f5;">
          <th style="padding: 10px; border: 1px solid #ddd;">Удовлетворительно</th>
          <th style="padding: 10px; border: 1px solid #ddd;">Хорошо</th>
          <th style="padding: 10px; border: 1px solid #ddd;">Отлично</th>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #ddd;">${table.min}</td>
          <td style="padding: 10px; border: 1px solid #ddd;">${table.good}</td>
          <td style="padding: 10px; border: 1px solid #ddd;">${table.excellent}</td>
        </tr>
      </table>
    `;
  }
  return '';
}

/* ============================================
   ЭКСПОРТ ДАННЫХ (CSV)
   ============================================ */

function exportTableToCSV(filename) {
  const table = document.querySelector('table');
  let csv = [];

  // Добавить заголовки
  const headers = [];
  table.querySelectorAll('th').forEach(th => {
    headers.push(th.textContent);
  });
  csv.push(headers.join(','));

  // Добавить строки
  table.querySelectorAll('tbody tr').forEach(tr => {
    const row = [];
    tr.querySelectorAll('td').forEach(td => {
      row.push('"' + td.textContent.replace(/"/g, '""') + '"');
    });
    csv.push(row.join(','));
  });

  // Скачать файл
  const csvContent = 'data:text/csv;charset=utf-8,' + csv.join('\n');
  const link = document.createElement('a');
  link.setAttribute('href', encodeURI(csvContent));
  link.setAttribute('download', filename || 'export.csv');
  link.click();
}

/* ============================================
   ПЕЧАТЬ СТРАНИЦЫ
   ============================================ */

function printPage() {
  window.print();
}

/* ============================================
   ВАЛИДАЦИЯ ФОРМ
   ============================================ */

function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function validatePhone(phone) {
  const regex = /^[0-9+\-\s()]+$/;
  return regex.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

/* ============================================
   ПЕЧАТЬ СТРАНИЦЫ
   ============================================ */

function printPage() {
  window.print();
}

/* ============================================
   ВАЛИДАЦИЯ ФОРМ
   ============================================ */

function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function validatePhone(phone) {
  const regex = /^[0-9+\-\s()]+$/;
  return regex.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

/* ============================================
   УПРАВЛЕНИЕ АККАУНТОМ
   ============================================ */

// Состояние аутентификации
let isAuthenticated = false;
let currentUser = null;

// Инициализация состояния аутентификации
function initializeAuth() {
  const userData = localStorage.getItem('kmkvk_user');
  if (userData) {
    currentUser = JSON.parse(userData);
    isAuthenticated = true;
    updateAccountUI();
  }
}

// Обновление UI в зависимости от состояния аутентификации
function updateAccountUI() {
  const accountLink = document.querySelector('.account-link');
  const loginLink = document.querySelector('.login-link');
  
  if (accountLink) {
    if (isAuthenticated) {
      accountLink.style.display = 'inline-block';
      accountLink.innerHTML = `<i class="fas fa-user"></i> ${currentUser.name}`;
      if (loginLink) loginLink.style.display = 'none';
    } else {
      accountLink.style.display = 'none';
      if (loginLink) loginLink.style.display = 'inline-block';
    }
  }
}

// Регистрация пользователя
function registerUser(userData) {
  // В реальном приложении здесь будет отправка на сервер
  // Для демонстрации сохраним в localStorage
  const user = {
    id: Date.now().toString(),
    name: userData.name,
    email: userData.email,
    role: 'student',
    registrationDate: new Date().toISOString(),
    progress: 0,
    achievements: []
  };
  
  localStorage.setItem('kmkvk_user', JSON.stringify(user));
  currentUser = user;
  isAuthenticated = true;
  
  // Перенаправление на профиль
  window.location.href = 'profile.html';
  return true;
}

// Вход пользователя
function loginUser(credentials) {
  // В реальном приложении здесь будет запрос к серверу
  // Для демонстрации проверим в localStorage
  const storedUser = localStorage.getItem('kmkvk_user');
  if (storedUser) {
    const user = JSON.parse(storedUser);
    if (user.email === credentials.email) { // В демонстрации используем только email
      currentUser = user;
      isAuthenticated = true;
      updateAccountUI();
      return true;
    }
  }
  return false;
}

// Выход из аккаунта
function logoutUser() {
  isAuthenticated = false;
  currentUser = null;
  localStorage.removeItem('kmkvk_user');
  updateAccountUI();
  
  // Перенаправление на главную
  window.location.href = 'index.html';
}

// Обновление профиля пользователя
function updateUserProfile(profileData) {
  if (!isAuthenticated || !currentUser) return false;
  
  // Обновляем данные пользователя
  Object.assign(currentUser, profileData);
  currentUser.updatedAt = new Date().toISOString();
  
  // Сохраняем обновленные данные
  localStorage.setItem('kmkvk_user', JSON.stringify(currentUser));
  
  // Обновляем UI профиля если находимся на странице профиля
  updateProfilePage();
  
  return true;
}

// Обновление страницы профиля
function updateProfilePage() {
  if (!isAuthenticated || !currentUser) return;
  
  const nameElement = document.querySelector('.profile-name');
  const emailElement = document.querySelector('.profile-email');
  const avatarElement = document.querySelector('.profile-avatar');
  
  if (nameElement) nameElement.textContent = currentUser.name;
  if (emailElement) emailElement.textContent = currentUser.email;
  if (avatarElement) avatarElement.alt = currentUser.name;
}

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', function() {
  initializeBurgerMenu();
  initializeAccordion();
  initializeActiveNavLink();
  initializeAuth();
});