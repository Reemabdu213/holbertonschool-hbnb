// ========== Configuration ==========
const API_URL = 'http://localhost:5000/api/v1';

// ========== Helper Functions ==========

// Get cookie by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Check if user is authenticated
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (token && loginLink) {
        loginLink.textContent = 'Logout';
        loginLink.onclick = (e) => {
            e.preventDefault();
            document.cookie = 'token=; path=/; max-age=0';
            window.location.href = 'login.html';
        };
        return token;
    }
    return null;
}

// ========== Login Page (login.html) ==========
if (document.getElementById('login-form')) {
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorMessage = document.getElementById('error-message');
        
        try {
            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            if (!response.ok) {
                throw new Error('Invalid credentials');
            }
            
            const data = await response.json();
            
            // Save token in cookie
            document.cookie = `token=${data.access_token}; path=/; max-age=3600`;
            
            // Redirect to index page
            window.location.href = 'index.html';
            
        } catch (error) {
            errorMessage.textContent = 'Invalid email or password. Please try again.';
        }
    });
}

// ========== Index Page (index.html) ==========
if (document.getElementById('places-list')) {
    checkAuthentication();
    
    // Fetch and display places
   /* async function fetchPlaces(country = '') { 
        try {
            const response = await fetch(`${API_URL}/places/`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch places');
            }
            
            let places = await response.json();
            
            // Filter by country if selected
            if (country) {
                places = places.filter(place => place.country === country);
            }
            
            displayPlaces(places);
            populateCountryFilter(places);
            
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('places-list').innerHTML = 
                '<p>Failed to load places. Please try again later.</p>';
        }
    } */
    let allPlaces = []; 
    async function fetchPlaces(token) {
        try {
            const response = await fetch(`${API_URL}/places/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                });

            if (!response.ok) {
                throw new Error('Failed to fetch places');
            }

            const places = await response.json();
            allPlaces = await response.json();
            displayPlaces(places);
            populateCountryFilter(places);
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
            // images/placeholder.jpg not exist yet
            card.innerHTML = `
                <img src="images/placeholder.jpg" alt="${place.title}" onerror="this.src='images/icon.png'">
                <h3>${place.title}</h3>
                <p class="price">$${place.price} / night</p>
                <p>${place.city || ''}, ${place.country || ''}</p>
                <button class="details-button" onclick="viewPlace('${place.id}')">View Details</button>
            `;
            container.appendChild(card);
        });
    }
    
    // Populate country filter dropdown
    function populateCountryFilter(places) {
        const countries = [...new Set(places.map(p => p.country).filter(Boolean))];
        const select = document.getElementById('country-filter');
        
        // Clear existing options (except "All Countries")
        select.innerHTML = '<option value="">All Countries</option>';
        
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            select.appendChild(option);
        });
    }
    
    // Country filter change event
    document.getElementById('country-filter').addEventListener('change', (e) => {
        fetchPlaces(e.target.value);
    });
    
    // Navigate to place details
    window.viewPlace = function(placeId) {
        window.location.href = `place.html?id=${placeId}`;
    };
    // Implement Price Filter
    document.getElementById('price-filter').addEventListener('change', (event) => {
    const selectedPrice = event.target.value;

    let filteredPlaces = allPlaces;
    if (selectedPrice !== 'all') {
        const maxPrice = parseInt(selectedPrice);
        filteredPlaces = allPlaces.filter(place => place.price <= maxPrice);
    }

    displayPlaces(filteredPlaces);
});

    // Load places on page load
    fetchPlaces();
}

// ========== Place Details Page (place.html) ==========
if (document.getElementById('place-details')) {
    const token = checkAuthentication();
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
        window.location.href = 'index.html';
    } else {
        fetchPlaceDetails(placeId, token);
    }
    
    async function fetchPlaceDetails(placeId, token) {
        try {
            const headers = {};
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            
            const response = await fetch(`${API_URL}/places/${placeId}`, { headers });
            
            if (!response.ok) {
                throw new Error('Failed to fetch place details');
            }
            
            const place = await response.json();
            displayPlaceDetails(place);
            fetchReviews(placeId);
            
            // Show add review button if user is logged in
            if (token) {
                const addReviewBtn = document.getElementById('add-review-btn');
                addReviewBtn.style.display = 'block';
                addReviewBtn.onclick = () => {
                    window.location.href = `add_review.html?place_id=${placeId}`;
                };
            }
            
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('place-details').innerHTML = 
                '<p>Failed to load place details.</p>';
        }
    }
    
    function displayPlaceDetails(place) {
        const container = document.getElementById('place-details');
        container.innerHTML = `
            <div class="place-info">
                <h1>${place.title}</h1>
                <img src="images/placeholder.jpg" alt="${place.title}" onerror="this.src='images/icon.png'">
                <p class="price">$${place.price} / night</p>
                <p><strong>Host:</strong> ${place.owner?.first_name || 'Unknown'} ${place.owner?.last_name || ''}</p>
                <p><strong>Location:</strong> ${place.city || ''}, ${place.country || ''}</p>
                <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
                
                ${place.amenities && place.amenities.length > 0 ? `
                    <div class="amenities">
                        <h3>Amenities:</h3>
                        <ul>
                            ${place.amenities.map(a => `<li>${a.name}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    async function fetchReviews(placeId) {
        try {
            const response = await fetch(`${API_URL}/places/${placeId}/reviews`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch reviews');
            }
            
            const reviews = await response.json();
            displayReviews(reviews);
            
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    function displayReviews(reviews) {
        const container = document.getElementById('reviews-list');
        
        if (!reviews || reviews.length === 0) {
            container.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
            return;
        }
        
        container.innerHTML = reviews.map(review => `
            <div class="review-card">
                <div class="rating">${'⭐'.repeat(review.rating)}</div>
                <p>${review.text}</p>
                <small>by ${review.user?.first_name || 'Anonymous'}</small>
            </div>
        `).join('');
    }
}

// ========== Add Review Page (add_review.html) ==========
if (document.getElementById('review-form')) {
    const token = checkAuthentication();
    
    // Redirect to index if not authenticated
    if (!token) {
        alert('Please login to add a review');
        window.location.href = 'login.html';
    }
    
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('place_id');
    
    if (!placeId) {
        alert('Invalid place ID');
        window.location.href = 'index.html';
    }
    
    document.getElementById('review-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const rating = document.getElementById('rating').value;
        const text = document.getElementById('comment').value;
        const errorMessage = document.getElementById('error-message');
        
        try {
            const response = await fetch(`${API_URL}/reviews/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    place_id: placeId,
                    rating: parseInt(rating),
                    text: text
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to submit review');
            }
            
            alert('Review submitted successfully!');
            window.location.href = `place.html?id=${placeId}`;
            
        } catch (error) {
            errorMessage.textContent = 'Failed to submit review. Please try again.';
        }
    });
}
