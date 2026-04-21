// Lógica de negocio y validaciones
const logic = {
    validateStep1: () => {
        const fields = ['pet-name', 'pet-species', 'pet-years', 'pet-months', 'pet-gender', 'symptom-desc', 'symptom-time', 'owner-name', 'owner-phone'];
        const allFilled = fields.every(id => document.getElementById(id).value.trim() !== "");
        document.getElementById('btn-next-1').classList.toggle('btn-disabled', !allFilled);
    },
    renderCalendar: () => {
        const grid = document.getElementById('calendar-grid');
        grid.innerHTML = '<b>L</b><b>M</b><b>M</b><b>J</b><b>V</b><b>S</b><b>D</b>';
        for (let i = 1; i <= 31; i++) {
            const btn = document.createElement('button');
            btn.innerText = i;
            btn.className = `p-2 rounded-lg transition-all ${i < state.today ? 'day-disabled' : 'hover:bg-secondary'}`;
            if (i >= state.today) {
                btn.onclick = () => {
                    document.querySelectorAll('#calendar-grid button').forEach(b => b.classList.remove('bg-primary', 'text-white'));
                    btn.classList.add('bg-primary', 'text-white');
                    state.selectedDate = i;
                    logic.validateStep2();
                };
            }
            grid.appendChild(btn);
        }
    },
    filterHours: (turno) => {
        const container = document.getElementById('hours-container');
        const isMorning = turno === 'M';
        container.innerHTML = '';

        document.getElementById('btn-morning').className = isMorning ?
            'px-4 py-1 bg-secondary/20 text-primary font-bold rounded-full text-xs' : 'px-4 py-1 bg-slate-100 text-neutral font-bold rounded-full text-xs';
        document.getElementById('btn-afternoon').className = !isMorning ?
            'px-4 py-1 bg-secondary/20 text-primary font-bold rounded-full text-xs' : 'px-4 py-1 bg-slate-100 text-neutral font-bold rounded-full text-xs';

        const hours = isMorning ? ['09:00', '10:00', '11:00'] : ['14:00', '15:00', '17:00'];
        hours.forEach(h => {
            const b = document.createElement('button');
            b.innerText = h;
            b.className = "border p-2 rounded-lg hover:bg-primary hover:text-white";

            b.onclick = () => {
                document.querySelectorAll('#hours-container button').forEach(btn => btn.classList.remove('bg-primary', 'text-white'));
                b.classList.add('bg-primary', 'text-white');
                state.selectedHour = h;
                logic.validateStep2();
            };
            container.appendChild(b);
        });
    },
    validateStep2: () => {
        const isValid = state.selectedDate && state.selectedHour;
        document.getElementById('btn-next-2').classList.toggle('btn-disabled', !isValid);
    },
    validateStep3: () => {
        const val = document.getElementById('yape-code').value.trim();
        document.getElementById('btn-finish').classList.toggle('btn-disabled', val.length < 5);
    },
    nextStep: (step) => {
        document.querySelectorAll('[id^="step-"]').forEach(s => s.classList.add('step-hidden'));
        document.getElementById(`step-${step}`).classList.remove('step-hidden');

        for (let i = 1; i <= 3; i++) {
            const circle = document.getElementById(`circle-${i}`);
            circle.className = `step-circle ${i <= step ? 'step-active' : 'step-inactive'}`;
        }
        if (step === 2) {
            logic.renderCalendar();
            logic.filterHours('M');
        }
    },
    validateGroomingStep1: () => {
        const fields = ['g-pet-name', 'g-pet-species', 'g-pet-gender', 'g-pet-breed', 'g-service-type', 'g-owner-phone'];
        const allFilled = fields.every(id => document.getElementById(id).value.trim() !== "" && document.getElementById(id).value !== "Especie");
        document.getElementById('g-btn-next-1').classList.toggle('btn-disabled', !allFilled);
    },
    renderGroomingCalendar: () => {
        const grid = document.getElementById('g-calendar-grid');
        grid.innerHTML = '<b>L</b><b>M</b><b>M</b><b>J</b><b>V</b><b>S</b><b>D</b>';
        for (let i = 1; i <= 31; i++) {
            const btn = document.createElement('button');
            btn.innerText = i;
            btn.className = `p-2 rounded-lg ${i < state.today ? 'day-disabled' : 'hover:bg-secondary'}`;
            if (i >= state.today) {
                btn.onclick = () => {
                    grid.querySelectorAll('button').forEach(b => b.classList.remove('bg-primary', 'text-white'));
                    btn.classList.add('bg-primary', 'text-white');
                    state.grooming.date = i;
                    logic.validateGroomingStep2();
                };
            }
            grid.appendChild(btn);
        }
    },
    renderGroomingHours: () => {
        const container = document.getElementById('g-hours-container');
        container.innerHTML = '';
        ['09:00', '11:00', '14:00', '16:00'].forEach(h => {
            const b = document.createElement('button');
            b.innerText = h;
            b.className = "border p-2 rounded-lg text-xs hover:bg-primary hover:text-white";
            
            b.onclick = () => {
                container.querySelectorAll('button').forEach(btn => btn.classList.remove('bg-primary', 'text-white'));
                b.classList.add('bg-primary', 'text-white');
                state.grooming.hour = h;
                logic.validateGroomingStep2();
            };
            container.appendChild(b);
        });
    },
    validateGroomingStep2: () => {
        const isValid = state.grooming.date && state.grooming.hour;
        document.getElementById('g-btn-next-2').classList.toggle('btn-disabled', !isValid);
    },
    validateGroomingStep3: () => {
        const val = document.getElementById('g-yape-code').value.trim();
        document.getElementById('g-btn-finish').classList.toggle('btn-disabled', val.length < 5);
    },
    nextStepGrooming: (step) => {
        document.querySelectorAll('[id^="g-step-"]').forEach(s => s.classList.add('step-hidden'));
        document.getElementById(`g-step-${step}`).classList.remove('step-hidden');
        for (let i = 1; i <= 3; i++) {
            document.getElementById(`g-circle-${i}`).className = `step-circle ${i <= step ? 'step-active' : 'step-inactive'}`;
        }
        if (step === 2) { 
            logic.renderGroomingCalendar();
            logic.renderGroomingHours();
        }
    }
};