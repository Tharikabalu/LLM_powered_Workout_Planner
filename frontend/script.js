// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Global state
let currentSection = 'dashboard';
let allWorkouts = [];

// DOM Elements
const sections = document.querySelectorAll('.section');
const navButtons = document.querySelectorAll('.nav-btn');
const loadingOverlay = document.getElementById('loading-overlay');
const toastContainer = document.getElementById('toast-container');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadDashboard();
});

// Initialize the application
function initializeApp() {
    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
    
    // Check API connection
    checkApiConnection();
}

// Setup event listeners
function setupEventListeners() {
    // Navigation
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const section = btn.dataset.section;
            showSection(section);
        });
    });
    
    // Workout form
    document.getElementById('workout-form').addEventListener('submit', handleWorkoutSubmit);
    
    // Load all workouts button
    document.getElementById('load-all-workouts').addEventListener('click', loadAllWorkouts);
    
    // Get suggestion button
    document.getElementById('get-suggestion').addEventListener('click', getWorkoutSuggestion);
}

// Navigation functions
function showSection(sectionName) {
    // Update active nav button
    navButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.section === sectionName);
    });
    
    // Update active section
    sections.forEach(section => {
        section.classList.toggle('active', section.id === sectionName);
    });
    
    currentSection = sectionName;
    
    // Load section-specific data
    switch(sectionName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'history':
            loadWorkoutHistory();
            break;
        case 'suggestions':
            // Clear previous suggestions
            document.getElementById('suggestion-result').innerHTML = '';
            break;
    }
}

// API connection check
async function checkApiConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            showToast('API connected successfully', 'success');
        } else {
            showToast('API connection failed', 'error');
        }
    } catch (error) {
        showToast('Cannot connect to API. Make sure the server is running.', 'error');
    }
}

// Loading overlay functions
function showLoading() {
    loadingOverlay.classList.add('active');
}

function hideLoading() {
    loadingOverlay.classList.remove('active');
}

// Toast notification functions
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
    toast.innerHTML = `
        <i class="${icon}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Dashboard functions
async function loadDashboard() {
    showLoading();
    try {
        // Load stats and recent workouts in parallel
        const [statsResponse, recentResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/workouts/stats`),
            fetch(`${API_BASE_URL}/workouts/recent?limit=5`)
        ]);
        
        if (statsResponse.ok) {
            const stats = await statsResponse.json();
            updateDashboardStats(stats);
        }
        
        if (recentResponse.ok) {
            const recentWorkouts = await recentResponse.json();
            displayRecentWorkouts(recentWorkouts);
        }
    } catch (error) {
        showToast('Failed to load dashboard data', 'error');
        console.error('Dashboard loading error:', error);
    } finally {
        hideLoading();
    }
}

function updateDashboardStats(stats) {
    document.getElementById('total-workouts').textContent = stats.total_workouts || 0;
    document.getElementById('unique-exercises').textContent = stats.unique_exercises || 0;
    document.getElementById('total-duration').textContent = stats.total_duration_minutes || 0;
    document.getElementById('last-workout').textContent = stats.most_recent_workout || '-';
}

function displayRecentWorkouts(workouts) {
    const container = document.getElementById('recent-workouts-list');
    
    if (workouts.length === 0) {
        container.innerHTML = '<p class="no-data">No recent workouts found. Start logging your workouts!</p>';
        return;
    }
    
    container.innerHTML = workouts.map(workout => createWorkoutItemHTML(workout)).join('');
}

// Workout form handling
async function handleWorkoutSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const workoutData = {
        exercise_name: formData.get('exercise_name'),
        sets: formData.get('sets') ? parseInt(formData.get('sets')) : null,
        reps: formData.get('reps') ? parseInt(formData.get('reps')) : null,
        weight: formData.get('weight') ? parseFloat(formData.get('weight')) : null,
        duration: formData.get('duration') ? parseInt(formData.get('duration')) : null,
        date: formData.get('date') || new Date().toISOString().split('T')[0]
    };
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/log_workout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(workoutData)
        });
        
        if (response.ok) {
            const result = await response.json();
            showToast(`Workout logged successfully: ${result.exercise}`, 'success');
            event.target.reset();
            document.getElementById('date').value = new Date().toISOString().split('T')[0];
            
            // Refresh dashboard if we're on it
            if (currentSection === 'dashboard') {
                loadDashboard();
            }
        } else {
            const error = await response.json();
            showToast(`Failed to log workout: ${error.detail}`, 'error');
        }
    } catch (error) {
        showToast('Failed to log workout', 'error');
        console.error('Workout logging error:', error);
    } finally {
        hideLoading();
    }
}

// Workout history functions
async function loadWorkoutHistory() {
    showLoading();
    try {
        const response = await fetch(`${API_BASE_URL}/workouts/recent?limit=20`);
        if (response.ok) {
            const workouts = await response.json();
            displayWorkoutHistory(workouts);
        } else {
            showToast('Failed to load workout history', 'error');
        }
    } catch (error) {
        showToast('Failed to load workout history', 'error');
        console.error('History loading error:', error);
    } finally {
        hideLoading();
    }
}

async function loadAllWorkouts() {
    showLoading();
    try {
        const response = await fetch(`${API_BASE_URL}/workouts/all`);
        if (response.ok) {
            const workouts = await response.json();
            allWorkouts = workouts;
            displayWorkoutHistory(workouts);
            showToast(`Loaded ${workouts.length} workouts`, 'success');
        } else {
            showToast('Failed to load all workouts', 'error');
        }
    } catch (error) {
        showToast('Failed to load all workouts', 'error');
        console.error('All workouts loading error:', error);
    } finally {
        hideLoading();
    }
}

function displayWorkoutHistory(workouts) {
    const container = document.getElementById('workout-history');
    
    if (workouts.length === 0) {
        container.innerHTML = '<p class="no-data">No workouts found. Start logging your workouts!</p>';
        return;
    }
    
    // Group workouts by date
    const groupedWorkouts = groupWorkoutsByDate(workouts);
    
    container.innerHTML = Object.entries(groupedWorkouts)
        .map(([date, dateWorkouts]) => `
            <div class="workout-date-group">
                <h4 class="date-header">${formatDate(date)}</h4>
                ${dateWorkouts.map(workout => createWorkoutItemHTML(workout)).join('')}
            </div>
        `).join('');
}

function groupWorkoutsByDate(workouts) {
    return workouts.reduce((groups, workout) => {
        const date = workout.date;
        if (!groups[date]) {
            groups[date] = [];
        }
        groups[date].push(workout);
        return groups;
    }, {});
}

// AI Suggestions functions
async function getWorkoutSuggestion() {
    const fitnessGoal = document.getElementById('fitness-goal').value;
    
    if (!fitnessGoal) {
        showToast('Please select a fitness goal', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/get_suggestions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                fitness_goal: fitnessGoal,
                user_id: 'default'
            })
        });
        
        if (response.ok) {
            const suggestion = await response.json();
            displayWorkoutSuggestion(suggestion);
        } else {
            const error = await response.json();
            showToast(`Failed to get suggestion: ${error.detail}`, 'error');
        }
    } catch (error) {
        showToast('Failed to get workout suggestion', 'error');
        console.error('Suggestion error:', error);
    } finally {
        hideLoading();
    }
}

function displayWorkoutSuggestion(suggestion) {
    const container = document.getElementById('suggestion-result');
    
    container.innerHTML = `
        <div class="suggestion-header">
            <div class="suggestion-goal">
                <i class="fas fa-robot"></i>
                ${suggestion.fitness_goal}
            </div>
            <div class="suggestion-meta">
                Based on ${suggestion.workout_history_count} recent workouts
            </div>
        </div>
        <div class="suggestion-content">
            ${suggestion.suggestion}
        </div>
        <div class="suggestion-footer">
            <small>Generated on ${formatDateTime(suggestion.generated_at)}</small>
        </div>
    `;
}

// Utility functions
function createWorkoutItemHTML(workout) {
    const details = [];
    
    if (workout.sets) details.push(`<div class="workout-detail"><div class="workout-detail-label">Sets</div><div class="workout-detail-value">${workout.sets}</div></div>`);
    if (workout.reps) details.push(`<div class="workout-detail"><div class="workout-detail-label">Reps</div><div class="workout-detail-value">${workout.reps}</div></div>`);
    if (workout.weight) details.push(`<div class="workout-detail"><div class="workout-detail-label">Weight</div><div class="workout-detail-value">${workout.weight} kg</div></div>`);
    if (workout.duration) details.push(`<div class="workout-detail"><div class="workout-detail-label">Duration</div><div class="workout-detail-value">${workout.duration} min</div></div>`);
    
    return `
        <div class="workout-item">
            <div class="workout-header">
                <div class="workout-name">${workout.exercise_name}</div>
                <div class="workout-date">${formatDate(workout.date)}</div>
            </div>
            ${details.length > 0 ? `<div class="workout-details">${details.join('')}</div>` : ''}
        </div>
    `;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Add some CSS for missing elements
const additionalStyles = `
    .no-data {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        font-style: italic;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 2px dashed rgba(255, 255, 255, 0.3);
    }
    
    .workout-date-group {
        margin-bottom: 2rem;
    }
    
    .date-header {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .suggestion-footer {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e1e5e9;
        text-align: right;
        color: #666;
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);
