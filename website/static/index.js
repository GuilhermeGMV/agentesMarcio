document.addEventListener("DOMContentLoaded", function() {
        const chatBox = document.getElementById("chat-box");
        chatBox.scrollTop = chatBox.scrollHeight;
});

document.getElementById("note").addEventListener("keypress", function(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();  // Evita que a quebra de linha ocorra
            this.form.submit();  // Submete o formulário
        }
});