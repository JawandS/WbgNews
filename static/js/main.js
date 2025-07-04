/**
 * Main JavaScript file for Williamsburg News App
 * Handles common functionality across all pages
 */

// Global configuration
const CONFIG = {
    API_BASE_URL: '',
    REFRESH_INTERVAL: 300000, // 5 minutes
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000 // 1 second
};

// Utility functions
const Utils = {
    /**
     * Format date string to human readable format
     */
    formatDate: function(dateString, options = {}) {
        const defaultOptions = {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };
        const formatOptions = Object.assign(defaultOptions, options);
        
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', formatOptions);
        } catch (error) {
            console.error('Error formatting date:', error);
            return dateString;
        }
    },

    /**
     * Format time string
     */
    formatTime: function(timeString) {
        try {
            const [hours, minutes] = timeString.split(':');
            const hour = parseInt(hours);
            const ampm = hour >= 12 ? 'PM' : 'AM';
            const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
            return `${displayHour}:${minutes} ${ampm}`;
        } catch (error) {
            console.error('Error formatting time:', error);
            return timeString;
        }
    },

    /**
     * Show loading spinner
     */
    showLoading: function(elementId, message = 'Loading...') {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="text-center py-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-3 text-muted">${message}</p>
                </div>
            `;
            element.classList.remove('d-none');
        }
    },

    /**
     * Show error message
     */
    showError: function(elementId, message = 'An error occurred') {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="text-center py-5">
                    <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                    <h5 class="text-muted">Error</h5>
                    <p class="text-muted">${message}</p>
                    <button class="btn btn-primary" onclick="location.reload()">
                        <i class="fas fa-sync-alt me-1"></i>Try Again
                    </button>
                </div>
            `;
            element.classList.remove('d-none');
        }
    },

    /**
     * Debounce function calls
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Make API request with retry logic
     */
    apiRequest: async function(url, options = {}, retries = CONFIG.MAX_RETRIES) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            if (retries > 0) {
                console.warn(`API request failed, retrying... (${retries} attempts left)`);
                await new Promise(resolve => setTimeout(resolve, CONFIG.RETRY_DELAY));
                return this.apiRequest(url, options, retries - 1);
            }
            throw error;
        }
    }
};

// Meeting service
const MeetingService = {
    /**
     * Fetch all meetings
     */
    fetchMeetings: async function() {
        try {
            return await Utils.apiRequest('/api/meetings');
        } catch (error) {
            console.error('Error fetching meetings:', error);
            throw error;
        }
    },

    /**
     * Fetch meeting details
     */
    fetchMeetingDetails: async function(council, meetingId) {
        try {
            return await Utils.apiRequest(`/api/meeting/${council}/${meetingId}`);
        } catch (error) {
            console.error('Error fetching meeting details:', error);
            throw error;
        }
    }
};

// UI Components
const UIComponents = {
    /**
     * Create meeting card element
     */
    createMeetingCard: function(meeting, variant = 'compact') {
        const div = document.createElement('div');
        
        if (variant === 'compact') {
            div.className = 'meeting-card mb-3 p-3 border rounded fade-in';
            div.innerHTML = this.getCompactMeetingHTML(meeting);
        } else {
            div.className = 'meeting-item mb-4 p-4 border rounded shadow-sm fade-in';
            div.innerHTML = this.getDetailedMeetingHTML(meeting);
        }
        
        return div;
    },

    /**
     * Generate compact meeting card HTML
     */
    getCompactMeetingHTML: function(meeting) {
        const statusBadge = meeting.status === 'completed' ? 
            '<span class="badge bg-success">Completed</span>' : 
            '<span class="badge bg-primary">Upcoming</span>';
        
        const councilIcon = meeting.council === 'williamsburg' ? 
            '<i class="fas fa-building text-primary me-2"></i>' : 
            '<i class="fas fa-landmark text-success me-2"></i>';
        
        const agendaLink = meeting.agenda_url ? 
            `<a href="${meeting.agenda_url}" target="_blank" class="btn btn-sm btn-outline-primary me-2">
                <i class="fas fa-file-alt me-1"></i>Agenda
            </a>` : '';
        
        const minutesLink = meeting.minutes_url ? 
            `<a href="${meeting.minutes_url}" target="_blank" class="btn btn-sm btn-outline-success me-2">
                <i class="fas fa-file-text me-1"></i>Minutes
            </a>` : '';
        
        return `
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h6 class="mb-1">
                        ${councilIcon}
                        ${meeting.title}
                        ${statusBadge}
                    </h6>
                    <p class="text-muted mb-1">
                        <i class="fas fa-building me-1"></i>${meeting.council_name}
                    </p>
                    <p class="text-muted mb-0">
                        <i class="fas fa-calendar me-1"></i>${Utils.formatDate(meeting.date)}
                        <i class="fas fa-clock ms-3 me-1"></i>${Utils.formatTime(meeting.time)}
                    </p>
                </div>
                <div class="col-md-4 text-end">
                    ${agendaLink}
                    ${minutesLink}
                    <a href="/meeting/${meeting.council}/${meeting.id}" class="btn btn-sm btn-primary">
                        <i class="fas fa-eye me-1"></i>Details
                    </a>
                </div>
            </div>
        `;
    },

    /**
     * Generate detailed meeting card HTML
     */
    getDetailedMeetingHTML: function(meeting) {
        const statusBadge = meeting.status === 'completed' ? 
            '<span class="badge bg-success fs-6">Completed</span>' : 
            '<span class="badge bg-primary fs-6">Upcoming</span>';
        
        const buttonColor = meeting.council === 'williamsburg' ? 'primary' : 'success';
        
        const agendaButton = meeting.agenda_url ? 
            `<a href="${meeting.agenda_url}" target="_blank" class="btn btn-outline-${buttonColor} me-2">
                <i class="fas fa-file-alt me-1"></i>View Agenda
            </a>` : 
            '<button class="btn btn-outline-secondary me-2" disabled>No Agenda Available</button>';
        
        const minutesButton = meeting.minutes_url ? 
            `<a href="${meeting.minutes_url}" target="_blank" class="btn btn-outline-info me-2">
                <i class="fas fa-file-text me-1"></i>View Minutes
            </a>` : 
            '<button class="btn btn-outline-secondary me-2" disabled>No Minutes Available</button>';
        
        return `
            <div class="row">
                <div class="col-md-8">
                    <h5 class="mb-2">
                        ${meeting.title}
                        ${statusBadge}
                    </h5>
                    <p class="text-muted mb-2">
                        <i class="fas fa-tag me-2"></i>${meeting.type}
                    </p>
                    <p class="text-muted mb-3">
                        <i class="fas fa-calendar me-2"></i>${Utils.formatDate(meeting.date, { weekday: 'long' })}
                        <span class="ms-4">
                            <i class="fas fa-clock me-2"></i>${Utils.formatTime(meeting.time)}
                        </span>
                    </p>
                </div>
                <div class="col-md-4 text-end">
                    <div class="d-flex flex-column gap-2">
                        ${agendaButton}
                        ${minutesButton}
                        <a href="/meeting/${meeting.council}/${meeting.id}" class="btn btn-${buttonColor}">
                            <i class="fas fa-eye me-1"></i>View Details
                        </a>
                    </div>
                </div>
            </div>
        `;
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add click animation to buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn')) {
            e.target.style.transform = 'scale(0.95)';
            setTimeout(() => {
                e.target.style.transform = '';
            }, 150);
        }
    });

    // Add tooltips to buttons (if Bootstrap tooltips are available)
    if (window.bootstrap && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Auto-refresh functionality (disabled by default)
    // Uncomment to enable auto-refresh of meetings data
    /*
    if (window.location.pathname === '/') {
        setInterval(() => {
            console.log('Auto-refreshing meetings data...');
            if (typeof loadMeetings === 'function') {
                loadMeetings();
            }
        }, CONFIG.REFRESH_INTERVAL);
    }
    */
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    // Could send error reports to a logging service here
});

// Service worker registration (if available)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment to register a service worker for offline functionality
        /*
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
        */
    });
}

// Export utilities for use in other scripts
window.WilliamsburgNews = {
    Utils,
    MeetingService,
    UIComponents,
    CONFIG
};
