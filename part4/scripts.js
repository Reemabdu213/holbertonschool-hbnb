// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// ==================== Cookie Helper Functions ====================
// Check for the JWT token in cookies and redirect unauthenticated users.
function checkAuthentication() {
      const token = getCookie('token');
      if (!token) {
          window.location.href = 'index.html';
      }
      return token;
  }

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

function deleteCookie(name) {
    document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`;
}

// ==================== Authentication ====================

function checkAuth() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    /*if (loginLink) {
        if (token) {
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.addEventListener('click', (e) => {
                e.preventDefault();
                logout();
            });
        } else {
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';
        }
    }*/
    if (!loginLink) return;

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
    }
}

async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            const error = await response.json();
            const errorMessage = document.getElementById('error-message');
            if (errorMessage) {
                errorMessage.textContent = error.error || 'Login failed: ' + response.statusText;
            } else {
                alert('Login failed: ' + response.statusText);
            }
        }
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = document.getElementById('error-message');
        if (errorMessage) {
            errorMessage.textContent = 'An error occurred during login';
        } else {
            alert('An error occurred during login');
        }
    }
}

function logout() {
    deleteCookie('token');
    window.location.href = 'login.html';
}

// ==================== Places ====================
let allPlaces = [];

async function fetchPlaces(country = '') {
    try {
        const token = getCookie('token');
        let url = `${API_BASE_URL}/places/`;

        if (country) {
            url += `?country=${encodeURIComponent(country)}`;
        }

        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(url, { headers });

        if (response.ok) {
            const places = await response.json();
            allPlaces = places;
            displayPlaces(places);
        } else if (response.status === 401) {
            logout();
        } else {
            throw new Error('Failed to fetch places');
        }
    } catch (error) {
        console.error('Error:', error);
        const placesList = document.getElementById('places-list');
        if (placesList) {
            placesList.innerHTML = '<p>Failed to load places. Please try again later.</p>';
        }
    }
}

// Image mapping for places
const placeImages = {
    'cozy apartment': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=600&h=400&fit=crop',
    'luxury beach villa': 'https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=600&h=400&fit=crop',
    'mountain cabin retreat': 'https://images.unsplash.com/photo-1449158743715-0a90ebb6d2d8?w=600&h=400&fit=crop'
};

function getPlaceImage(title) {
    const key = title.toLowerCase();
    return placeImages[key] || 'images/placeholder.jpg';
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    if (!container) return;
    container.innerHTML = '';

    if (places.length === 0) {
        container.innerHTML = '<p>No places found.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.setAttribute('data-price', place.price_per_night || place.price);
        const imageUrl = getPlaceImage(place.title);
        card.innerHTML = `
            <img src="${imageUrl}" alt="${place.title}" onerror="this.src='images/placeholder.jpg'">
            <h3>${place.title}</h3>
            <p class="price">$${place.price_per_night || place.price} per night</p>
            <p class="location">${place.city || ''}, ${place.country || ''}</p>
            <a href="places.html?id=${place.id}" class="details-button">View Details</a>
        `;
        container.appendChild(card);
    });
}

function filterByPrice() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    const selectedPrice = priceFilter.value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price'));
        
        if (selectedPrice === 'all') {
            card.style.display = 'block';
        } else {
            const maxPrice = parseFloat(selectedPrice);
            if (price <= maxPrice) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}
// ==================== Place Details ====================

async function fetchPlaceDetails(placeId) {
    try {
        const token = getCookie('token');
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, { headers });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else if (response.status === 401) {
            logout();
        } else {
            throw new Error('Failed to fetch place details');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load place details');
    }
}

function displayPlaceDetails(place) {
    const titleEl = document.getElementById('place-title');
    const imageEl = document.getElementById('place-image');
    const descEl = document.getElementById('place-description');
    const priceEl = document.getElementById('place-price');
    const locationEl = document.getElementById('place-location');

    // بعض الـ APIs تستخدم name بدل title
    const placeTitle = place.title || place.name || 'Place';

    if (titleEl) titleEl.textContent = placeTitle;
    if (imageEl) {
        imageEl.src = getPlaceImage(placeTitle);
        imageEl.alt = placeTitle;
        imageEl.onerror = function() { this.src = 'images/placeholder.jpg'; };
    }
    if (descEl) descEl.textContent = place.description || 'No description available';
    if (priceEl) priceEl.textContent = `$${place.price_per_night || place.price} per night`;
    if (locationEl) {
        const city = place.city || '';
        const country = place.country || '';
        locationEl.textContent = `${city}${city && country ? ', ' : ''}${country}`;
    }

    const amenitiesList = document.getElementById('amenities-list');
    if (amenitiesList) {
        amenitiesList.innerHTML = '';
        if (place.amenities && place.amenities.length > 0) {
            place.amenities.forEach(amenity => {
                const li = document.createElement('li');
                // amenity ممكن يكون string أو object
                li.textContent = (typeof amenity === 'string') ? amenity : (amenity.name || 'Amenity');
                amenitiesList.appendChild(li);
            });
        } else {
            amenitiesList.innerHTML = '<li>No amenities listed</li>';
        }
    }

    displayReviews(place.reviews || []);
}

// ==================== Reviews ====================

function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    if (!reviewsList) return;
    reviewsList.innerHTML = '';

    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet</p>';
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        reviewCard.innerHTML = `
            <h4>${review.user_name || 'Anonymous'}</h4>
            <p class="rating">Rating: ${review.rating}/5</p>
            <p>${review.comment}</p>
        `;
        reviewsList.appendChild(reviewCard);
    });
}

async function addReview(event) {
    event.preventDefault();

    const token = checkAuthentication();
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    const rating = document.getElementById('rating').value;
    const comment = document.getElementById('comment').value;

    if (!placeId) {
        alert('No place selected');
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ rating: parseInt(rating), comment })
        });

        if (response.ok) {
            alert('Review added successfully!');
           // window.location.href = `place.html?id=${placeId}`;
            document.getElementById('review-form').reset();
        } else if (response.status === 401) {
            logout();
        } else {
            const error = await response.json();
            alert(error.error || 'Failed to add review');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while adding review');
    }
}

// ==================== Filters ====================

function filterByCountry() {
    const country = document.getElementById('country-filter').value;
    fetchPlaces(country);
}

// ==================== Page Initialization ====================

document.addEventListener('DOMContentLoaded', () => {
    checkAuth();

    const currentPage = window.location.pathname;

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    if (currentPage.includes('index.html') || currentPage.endsWith('/')) {
        fetchPlaces();
    }

  if (currentPage.includes('places.html')) {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    // Show Add Review button only if authenticated
    const token = getCookie('token');
    const addReviewBtn = document.getElementById('add-review-btn');
    if (addReviewBtn) {
        if (token && placeId) {
            addReviewBtn.style.display = 'inline-block';
            addReviewBtn.href = `add_review.html?id=${placeId}`;
        } else {
            addReviewBtn.style.display = 'none';
        }
    }

    if (placeId) {
        fetchPlaceDetails(placeId);
    } else {
        document.getElementById('place-title').textContent = 'Place not found';
    }
}

    const countryFilter = document.getElementById('country-filter');
    if (countryFilter) {
        countryFilter.addEventListener('change', filterByCountry);
    }

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterByPrice);
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', addReview);
    }
});
