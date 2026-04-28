// Simple job storage
let jobs = [
    { id: 1, name: "John Doe", email: "john@example.com", location: "Classroom 101", problem: "Projector not working", status: "incomplete" }
];

// Password visibility toggle
const showPasswordBtn = document.getElementById('showPassword');
if (showPasswordBtn) {
    showPasswordBtn.addEventListener('click', function() {
    const pwd = document.getElementById('password');
        if (pwd) {
    if (pwd.type === 'password') {
        pwd.type = 'text';
        this.textContent = 'Hide';
    } else {
        pwd.type = 'password';
        this.textContent = 'Show';
            }
    }
});
}

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
    const errorElement = document.getElementById('userError');
    
        if (usernameInput && passwordInput && errorElement) {
            const username = usernameInput.value;
            const password = passwordInput.value;
            
    errorElement.textContent = '';
    
    if (username === 'staffmember' && password === 'letmein!123') {
                const loginPage = document.getElementById('loginPage');
                const staffPage = document.getElementById('staffPage');
                if (loginPage && staffPage) {
                    loginPage.style.display = 'none';
                    staffPage.style.display = 'block';
                }
    } 
    else if (username === 'admin' && password === 'heretohelp!456') {
                const loginPage = document.getElementById('loginPage');
                const techPage = document.getElementById('techPage');
                if (loginPage && techPage) {
                    loginPage.style.display = 'none';
                    techPage.style.display = 'block';
        showJobs('incomplete');
                }
    }
    else {
        errorElement.textContent = 'Wrong username or password!';
            }
    }
});
}

// Staff form submission
const staffForm = document.getElementById('staffForm');
if (staffForm) {
    staffForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
        const nameInput = document.getElementById('name');
        const emailInput = document.getElementById('email');
        const locationInput = document.getElementById('location');
        const descriptionInput = document.getElementById('description');
        
        if (nameInput && emailInput && locationInput && descriptionInput) {
            const name = nameInput.value;
            const email = emailInput.value;
            const location = locationInput.value;
            const description = descriptionInput.value;
            
    if (name && email.includes('@') && location && description.length > 5) {
        jobs.push({
            id: jobs.length + 1,
            name: name,
            email: email,
            location: location,
            problem: description,
            status: 'incomplete'
        });
        alert('Request submitted!');
        this.reset();
    } else {
        alert('Please fill all fields correctly');
            }
    }
});
}

// Job display function
function showJobs(status) {
    const container = document.getElementById('jobList');
    if (container) {
    container.innerHTML = '';
    
    jobs.forEach(job => {
        if (job.status === status) {
            const jobDiv = document.createElement('div');
            jobDiv.innerHTML = `
                <h3>${job.name}</h3>
                <p><strong>Location:</strong> ${job.location}</p>
                <p><strong>Problem:</strong> ${job.problem}</p>
                ${status === 'incomplete' ? 
                    `<button onclick="completeJob(${job.id})">Mark Complete</button>` : 
                    ''
                }
            `;
            container.appendChild(jobDiv);
        }
    });
    }
}

// Job completion
function completeJob(id) {
    const job = jobs.find(j => j.id === id);
    if (job) {
        job.status = 'completed';
        showJobs('incomplete');
    }
}

// Event listeners for job filtering
const showIncompleteBtn = document.getElementById('showIncomplete');
if (showIncompleteBtn) {
    showIncompleteBtn.addEventListener('click', () => showJobs('incomplete'));
}

const showCompletedBtn = document.getElementById('showCompleted');
if (showCompletedBtn) {
    showCompletedBtn.addEventListener('click', () => showJobs('completed'));
}

// Logout functionality
const staffLogoutBtn = document.getElementById('staffLogout');
if (staffLogoutBtn) {
    staffLogoutBtn.addEventListener('click', function() {
        const staffPage = document.getElementById('staffPage');
        const loginPage = document.getElementById('loginPage');
        if (staffPage && loginPage) {
            staffPage.style.display = 'none';
            loginPage.style.display = 'block';
        }
});
}

const techLogoutBtn = document.getElementById('techLogout');
if (techLogoutBtn) {
    techLogoutBtn.addEventListener('click', function() {
        const techPage = document.getElementById('techPage');
        const loginPage = document.getElementById('loginPage');
        if (techPage && loginPage) {
            techPage.style.display = 'none';
            loginPage.style.display = 'block';
        }
});
}