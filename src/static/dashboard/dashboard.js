document.addEventListener('DOMContentLoaded', function() {
    // Fetch user data
    fetch('/api/profile')
        .then(response => {
            if (!response.ok) {
                // If not authenticated, redirect to login
                if (response.status === 401) {
                    window.location.href = '/';
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update user name
            const userName = document.getElementById('user-name');
            if (userName && data.user && data.user.full_name) {
                userName.textContent = data.user.full_name;
            } else if (userName && data.user && data.user.username) {
                userName.textContent = data.user.username;
            }
        })
        .catch(error => {
            console.error('Error fetching user data:', error);
        });
    
    // Logout functionality
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                window.location.href = '/';
            })
            .catch(error => {
                console.error('Error logging out:', error);
            });
        });
    }
    
    // Sidebar navigation
    const navItems = document.querySelectorAll('.sidebar-nav ul li');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
