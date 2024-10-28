function addMessage(content, isBot = false) {
    const now = new Date();
    const time = now.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
    
    const messageGroup = document.createElement('div');
    messageGroup.className = 'message-group';

    const botAvatar = "/static/images/bot-avatar.webp";  
    const userAvatar = "/static/images/user-avatar.webp"; 
    
    messageGroup.innerHTML = `
        <img src="${isBot ? botAvatar : userAvatar}" alt="${isBot ? 'Bot' : 'User'} Avatar" class="user-avatar">
        <div class="message-content">
            <div class="message-header">
                <span class="username ${isBot ? 'bot-name' : ''}">${isBot ? 'Ben Quadinaros' : 'You'}</span>
                <span class="timestamp">Today at ${time}</span>
            </div>
            <div class="message-text">${content}</div>
        </div>
    `;
    
    document.getElementById('chatMessages').appendChild(messageGroup);
    messageGroup.scrollIntoView({ behavior: 'smooth' });
}

// Handle form submission
document.getElementById('chatForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (message) {
        addMessage(message, false);  // Add user message immediately
        input.value = '';  // Clear input
        
        // Send to Flask backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Add bot response when it comes back
            addMessage(data.response, true);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your message.', true);
        });
    }
});