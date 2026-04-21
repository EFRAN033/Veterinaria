const adminLogic = {
    login: () => {
        const user = document.getElementById('admin-user').value.trim();
        const pass = document.getElementById('admin-pass').value;
        const demo = window.SISTEMA_DEMO_LOGIN || { usuario: 'demo', password: 'demo' };

        // Simulación de Auth (QA: En producción usar JWT/Bcrypt)
        if (user === demo.usuario && pass === demo.password) {
            state.isAdminLoggedIn = true;
            adminUI.renderDashboard();
        } else {
            alert("Credenciales incorrectas");
        }
    },

    logout: () => {
        state.isAdminLoggedIn = false;
        document.getElementById('admin-dashboard').classList.add('hidden');
        document.getElementById('admin-login').classList.remove('hidden');
        location.reload(); // Hard reset para seguridad
    },

    askAI: async () => {
        const input = document.getElementById('ai-input');
        const chatBox = document.getElementById('chat-box');
        const prompt = input.value.trim();
        
        if(!prompt) return;

        // UI Feedback
        chatBox.innerHTML += `<div class="bg-slate-700 p-3 rounded-xl ml-auto max-w-[80%] text-white">${prompt}</div>`;
        input.value = "";

        // Integración Mock de API ChatGPT (Requiere KEY en entorno real)
        chatBox.innerHTML += `<div id="ai-loading" class="italic text-slate-500">Analizando historial y base científica...</div>`;
        
        try {
            /* const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: { 'Authorization': 'Bearer YOUR_KEY', 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: "gpt-4", messages: [{role: "user", content: prompt}] })
            });
            */
            
            // Simulación de respuesta inteligente
            setTimeout(() => {
                document.getElementById('ai-loading').remove();
                const fakeResponse = "Basado en los síntomas de Toby (canino, 5 años), la falta de apetito y letargo tras la vacunación puede ser una reacción leve. Se recomienda monitoreo de temperatura y dieta blanda.";
                chatBox.innerHTML += `<div class="bg-primary/20 p-3 rounded-xl mr-auto max-w-[80%] border border-primary/30">${fakeResponse}</div>`;
                
                // Actualizar Resumen Lateral
                adminUI.updateAISummary({
                    diagnostico: "Reacción post-vacunal leve",
                    tratamiento: "Hidratación y reposo",
                    sintomas: "Letargo, Inapetencia"
                });
            }, 1500);
            
        } catch (error) {
            console.error("AI Error:", error);
        }
    }
};