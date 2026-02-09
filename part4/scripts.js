// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// Check if user is logged in
function checkAuth() {
    const token = localStorage.getItem('token');
    const currentPage = window.location.pathname;
    
    if (!token && !currentPage.includes('login.html') && !currentPage.includes('index.html')) {
        window.location.href = 'login.html';
    } else if (token && (currentPage.includes('login.html') || currentPage.includes('index.html'))) {
        window.location.href = 'places.html';
    }
}

// Login function
async function login(event) {
    event.preventDefault();
    console.log('Login function called!');
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    console.log('Email:', email);
    console.log('Password:', password);
    
    try {
        console.log('Sending request to:', `${API_BASE_URL}/auth/login`);
        
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        console.log('Response status:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log('Login successful!', data);
            localStorage.setItem('token', data.access_token);
            window.location.href = 'places.html';
        } else {
            const error = await response.json();
            console.error('Login failed:', error);
            alert(error.error || 'Login failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login');
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

// Fetch all places
async function fetchPlaces(country = '') {
    try {
        const token = localStorage.getItem('token');
        let url = `${API_BASE_URL}/places/`;
        
        if (country) {
            url += `?country=${encodeURIComponent(country)}`;
        }
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else if (response.status === 401) {
            logout();
        } else {
            throw new Error('Failed to fetch places');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('places-list').innerHTML = 
            '<p>Failed to load places. Please try again later.</p>';
    }
}

// Display places as cards
function displayPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = '';

    if (places.length === 0) {
        container.innerHTML = '<p>No places found.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
            <img src="images/placeholder.jpg" alt="${place.title}" onerror="this.src='images/placeholder.jpg'">
            <h3>${place.title}</h3>
            <p class="price">$${place.price_per_night} per night</p>
            <p class="location">${place.city}, ${place.country}</p>
            <button onclick="viewPlaceDetails('${place.id}')">View Details</button>
        `;
        container.appendChild(card);
    });
}

// View place details
async function viewPlaceDetails(placeId) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const place = await response.json();
            localStorage.setItem('currentPlace', JSON.stringify(place));
            window.location.href = 'place.html';
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

// Display single place details
function displayPlaceDetails() {
    const place = JSON.parse(localStorage.getItem('currentPlace'));
    
    if (!place) {
        window.location.href = 'places.html';
        return;
    }
    
    document.getElementById('place-title').textContent = place.title;
    document.getElementById('place-image').src = 'images/placeholder.jpg';
    document.getElementById('place-image').alt = place.title;
    document.getElementById('place-description').textContent = place.description || 'No description available';
    document.getElementById('place-price').textContent = `$${place.price_per_night} per night`;
    document.getElementById('place-location').textContent = `${place.city}, ${place.country}`;
    
    const amenitiesList = document.getElementById('amenities-list');
    amenitiesList.innerHTML = '';
    
    if (place.amenities && place.amenities.length > 0) {
        place.amenities.forEach(amenity => {
            const li = document.createElement('li');
            li.textContent = amenity;
            amenitiesList.appendChild(li);
        });
    } else {
        amenitiesList.innerHTML = '<li>No amenities listed</li>';
    }
    
    displayReviews(place.reviews || []);
}

// Display reviews
function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
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

// Add review
async function addReview(event) {
    event.preventDefault();
    
    const place = JSON.parse(localStorage.getItem('currentPlace'));
    const rating = document.getElementById('rating').value;
    const comment = document.getElementById('comment').value;
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/places/${place.id}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ rating: parseInt(rating), comment })
        });
        
        if (response.ok) {
            alert('Review added successfully!');
            viewPlaceDetails(place.id);
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

// Filter places by country
function filterByCountry() {
    const country = document.getElementById('country-filter').value;
    fetchPlaces(country);
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    
    const currentPage = window.location.pathname;
    
    if (currentPage.includes('places.html')) {
        fetchPlaces();
    } else if (currentPage.includes('place.html')) {
        displayPlaceDetails();
    }
});