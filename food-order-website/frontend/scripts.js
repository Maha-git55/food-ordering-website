// API Configuration
const API_BASE = "http://127.0.0.1:8000/api";

// Dark Mode Toggle
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
}

// Restaurant Loading Function (NEW IMPROVED VERSION)
async function loadRestaurants() {
    const container = document.getElementById("restaurants");
    if (!container) return;

    // Loading State
    container.innerHTML = `
        <div class="text-center py-12">
            <i class="fas fa-spinner fa-spin text-4xl text-blue-500"></i>
            <p class="mt-4 text-lg dark:text-white">Loading delicious options...</p>
        </div>
    `;

    try {
        const response = await authApiCall('/restaurants/');
        
        // Check if response is OK
        if (!response.ok) {
            throw new Error(`Server returned ${response.status} status`);
        }
        
        const data = await response.json();
        
        // Clear container
        container.innerHTML = '';
        
        // Add restaurant cards
        data.forEach(restaurant => {
            container.innerHTML += `
                <div class="bg-white dark:bg-gray-700 rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                    <img src="${restaurant.image}" alt="${restaurant.name}" 
                        class="w-full h-48 object-cover hover:opacity-90 transition duration-300">
                    <div class="p-4">
                        <h3 class="text-xl font-bold dark:text-white">${restaurant.name}</h3>
                        <p class="text-gray-600 dark:text-gray-300 mt-2 text-sm">${restaurant.description}</p>
                        <button onclick="viewMenu(${restaurant.id})" 
                            class="mt-4 w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg transition duration-200">
                            <i class="fas fa-utensils mr-2"></i> View Menu
                        </button>
                    </div>
                </div>
            `;
        });
    } catch (error) {
        console.error("Restaurant loading error:", error);
        container.innerHTML = `
            <div class="text-center py-12">
                <i class="fas fa-exclamation-triangle text-4xl text-red-500 mb-4"></i>
                <p class="text-xl dark:text-white">Restaurants load nahi ho paye</p>
                <p class="text-gray-500 text-sm mt-2">${error.message}</p>
                <button onclick="loadRestaurants()" 
                    class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition">
                    <i class="fas fa-sync-alt mr-2"></i> Try Again
                </button>
            </div>
        `;
    }
}

// Cart Functions
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function updateCartCount() {
    const cartCountElements = document.querySelectorAll('#cart-count, #cart-count-mobile');
    cartCountElements.forEach(el => {
        el.textContent = cart.length;
    });
}

function addToCart(item) {
    cart.push(item);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    showNotification(`${item.name} added to cart!`, 'green');
}

function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    showNotification('Item removed from cart!', 'red');
}

function showNotification(message, color) {
    const notification = document.createElement('div');
    notification.className = `fixed bottom-4 right-4 bg-${color}-500 text-white px-4 py-2 rounded-lg shadow-lg animate-bounce`;
    notification.innerHTML = `<i class="fas fa-${color === 'green' ? 'check' : 'times'}-circle mr-2"></i> ${message}`;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('restaurants')) {
        loadRestaurants();
    }
    updateCartCount();
});



// YE CODE ADD KAR DO 👇
// JWT Token Functions
function saveToken(token) {
    localStorage.setItem('access_token', token);
}

function getToken() {
    return localStorage.getItem('access_token');
}

function removeToken() {
    localStorage.removeItem('access_token');
}

// Check if user is logged in
function checkLogin() {
    return !!getToken();
}

// Auth API Call
async function authApiCall(url, options = {}) {
    const token = getToken();
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(`${API_BASE}${url}`, finalOptions);
        if (response.status === 401) {
            // Token expired or invalid
            removeToken();
            window.location.href = "login.html";
            return null;
        }
        return response;
    } catch (error) {
        console.error('API call failed:', error);
        return null;
    }
}

function getCategoryIcon(category) {
    const icons = {
        'healthy': 'leaf',
        'fastfood': 'hamburger',
        'desi': 'utensils',
        'desserts': 'ice-cream'
    };
    return icons[category] || 'tag';
}