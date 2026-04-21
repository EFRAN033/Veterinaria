const adminUI = {
    renderDashboard: () => {
        document.getElementById('admin-login').classList.add('hidden');
        document.getElementById('admin-dashboard').classList.remove('hidden');
        adminUI.renderAdminCalendar();
        adminUI.renderPatientCards();
        lucide.createIcons();
    },

    openAdmin: () => {
        document.getElementById('admin-root').classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    },

    closeAdmin: () => {
        document.getElementById('admin-root').classList.add('hidden');
        document.body.style.overflow = 'auto';
    },

    switchTab: (tab) => {
        const isAgenda = tab === 'agenda';
        document.getElementById('view-agenda').classList.toggle('hidden', !isAgenda);
        document.getElementById('view-casos').classList.toggle('hidden', isAgenda);
        
        // Estilo de botones
        document.getElementById('tab-agenda').className = isAgenda ? 'px-4 py-2 rounded-lg bg-primary text-white font-medium' : 'px-4 py-2 rounded-lg text-slate-500 hover:bg-slate-100 font-medium';
        document.getElementById('tab-casos').className = !isAgenda ? 'px-4 py-2 rounded-lg bg-primary text-white font-medium' : 'px-4 py-2 rounded-lg text-slate-500 hover:bg-slate-100 font-medium';
    },

    renderAdminCalendar: () => {
        const grid = document.getElementById('admin-calendar');
        grid.innerHTML = '<b>L</b><b>M</b><b>M</b><b>J</b><b>V</b><b>S</b><b>D</b>';
        
        // Simulación de días con citas (colores por tipo)
        const appointments = {
            24: 'bg-primary',   // Cita Médica
            25: 'bg-secondary', // Estética
            28: 'bg-orange-400' // Vacunación
        };

        for (let i = 1; i <= 31; i++) {
            const day = document.createElement('div');
            day.className = `h-10 flex flex-col items-center justify-center rounded-lg cursor-pointer hover:bg-slate-100 border border-slate-50`;
            day.innerHTML = `<span>${i}</span>`;
            if(appointments[i]) {
                day.innerHTML += `<div class="w-1.5 h-1.5 rounded-full ${appointments[i]}"></div>`;
            }
            day.onclick = () => adminUI.showDayDetails(i);
            grid.appendChild(day);
        }
    },

    showDayDetails: (day) => {
        const container = document.getElementById('day-agenda-list');
        const header = document.querySelector('#day-details-header h3');
        header.innerText = `Agenda: ${day} de Marzo, 2026`;
        
        // Datos Mock de ejemplo
        const mockData = [
            { time: "09:00 AM", pet: "Toby", type: "Vacunación Sextuple", owner: "Juan P.", status: "Confirmado" },
            { time: "11:30 AM", pet: "Luna", type: "Corte y Baño", owner: "Maria G.", status: "Pendiente" }
        ];

        container.innerHTML = mockData.map(app => `
            <div class="flex items-center gap-4 p-4 bg-slate-50 rounded-2xl border-l-4 border-primary">
                <div class="text-sm font-bold text-primary w-20">${app.time}</div>
                <div class="flex-1">
                    <div class="font-bold text-slate-800">${app.pet} <span class="font-normal text-slate-500">(${app.type})</span></div>
                    <div class="text-xs text-slate-400">Propietario: ${app.owner}</div>
                </div>
                <div class="text-xs bg-white px-3 py-1 rounded-full border shadow-sm">${app.status}</div>
            </div>
        `).join('');
    },

    renderPatientCards: () => {
        const container = document.getElementById('patients-list');
        const patients = [
            { name: "Max", breed: "Golden Retriever", lastVisit: "12 Feb", issue: "Dermatitis" },
            { name: "Mimi", breed: "Siames", lastVisit: "05 Mar", issue: "Control Post-Operatorio" }
        ];

        container.innerHTML = patients.map(p => `
            <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
                <div class="flex justify-between items-start mb-2">
                    <h4 class="font-bold text-slate-800">${p.name}</h4>
                    <span class="text-[10px] bg-slate-100 px-2 py-0.5 rounded text-slate-500 uppercase">${p.breed}</span>
                </div>
                <p class="text-xs text-slate-500 mb-2">Último caso: ${p.issue}</p>
                <div class="text-[10px] text-primary font-bold">Ver historial completo →</div>
            </div>
        `).join('');
    },

    updateAISummary: (data) => {
        const panel = document.getElementById('ai-summary');
        const content = document.getElementById('ai-summary-content');
        panel.classList.remove('hidden');
        content.innerHTML = `
            <p><strong>Diagnóstico:</strong> ${data.diagnostico}</p>
            <p><strong>Tratamiento:</strong> ${data.tratamiento}</p>
            <p><strong>Síntomas:</strong> ${data.sintomas}</p>
        `;
    }
};