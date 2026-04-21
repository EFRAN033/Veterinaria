// Orquestador de la interfaz
const ui = {
    openModal: (id) => {
        document.getElementById(id).classList.add('modal-active');
        state.activeModal = id;
        logic.nextStep(1);
    },
    closeModal: (id) => {
        document.getElementById(id).classList.remove('modal-active');
        state.activeModal = null;
    },
    toggleAdmin: () => {
        document.getElementById('admin-root').classList.toggle('hidden');
    },
    confirmFinal: (modalId = 'modal-consulta') => {
        alert('¡Cita registrada correctamente! En revisión administrativa.');
        ui.closeModal(modalId);
    }
};