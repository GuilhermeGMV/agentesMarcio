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

function toggleTextarea() {
    const agenteSelect = document.getElementById("agente");
    const messageForm = document.getElementById("message-form-container");

    const conversaAtiva = document.querySelector(".conversation-item.active");

    if (conversaAtiva || (agenteSelect && agenteSelect.value)) {
        messageForm.style.display = "block";
    } else {
        messageForm.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    toggleTextarea();
});
