// Punto de entrada e inicialización
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    const demo = window.SISTEMA_DEMO_LOGIN;
    const adminUser = document.getElementById('admin-user');
    const adminPass = document.getElementById('admin-pass');
    if (demo && adminUser && adminPass) {
        adminUser.placeholder = demo.usuario;
        adminPass.placeholder = demo.password;
        adminUser.value = demo.usuario;
        adminPass.value = demo.password;
    }
});