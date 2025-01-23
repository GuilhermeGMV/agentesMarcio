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
const body = document.querySelector("body"),
    sidebar = body.querySelector(".sidebar"),
    toggle = body.querySelector(".toggle");

    toggle.addEventListener("click", () =>{
        sidebar.classList.toggle("close");
    })

document.querySelectorAll('.delet').forEach(button => {
        button.addEventListener('click', function() {
            const conversaId = this.closest('.conversation-item').querySelector('a').href.split('=')[1];
            document.getElementById('conversa-id-input').value = conversaId;
        });
    });