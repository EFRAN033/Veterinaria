import { ref, computed } from 'vue';

/**
 * Composable para validación de formularios
 * @returns {Object} Métodos y estado de validación
 */
export const useFormValidation = () => {
    const errors = ref({});

    /**
     * Valida un email
     * @param {string} email - Email a validar
     * @returns {string} Mensaje de error o string vacío
     */
    const validateEmail = (email) => {
        if (!email) return 'El email es requerido';
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email) ? '' : 'Email inválido';
    };

    /**
     * Valida una contraseña
     * @param {string} password - Contraseña a validar
     * @returns {string} Mensaje de error o string vacío
     */
    const validatePassword = (password) => {
        if (!password) return 'La contraseña es requerida';
        if (password.length < 6) return 'Mínimo 6 caracteres';
        if (!/[A-Z]/.test(password)) return 'Debe contener una mayúscula';
        if (!/[0-9]/.test(password)) return 'Debe contener un número';
        return '';
    };

    /**
     * Valida que un campo no esté vacío
     * @param {string} value - Valor a validar
     * @param {string} fieldName - Nombre del campo para el mensaje
     * @returns {string} Mensaje de error o string vacío
     */
    const validateRequired = (value, fieldName = 'Este campo') => {
        return value && value.trim() ? '' : `${fieldName} es requerido`;
    };

    /**
     * Valida que dos valores coincidan
     * @param {string} value1 - Primer valor
     * @param {string} value2 - Segundo valor
     * @param {string} fieldName - Nombre del campo
     * @returns {string} Mensaje de error o string vacío
     */
    const validateMatch = (value1, value2, fieldName = 'Los campos') => {
        return value1 === value2 ? '' : `${fieldName} no coinciden`;
    };

    /**
     * Valida la longitud mínima
     * @param {string} value - Valor a validar
     * @param {number} min - Longitud mínima
     * @returns {string} Mensaje de error o string vacío
     */
    const validateMinLength = (value, min) => {
        return value && value.length >= min ? '' : `Mínimo ${min} caracteres`;
    };

    /**
     * Valida la longitud máxima
     * @param {string} value - Valor a validar
     * @param {number} max - Longitud máxima
     * @returns {string} Mensaje de error o string vacío
     */
    const validateMaxLength = (value, max) => {
        return value && value.length <= max ? '' : `Máximo ${max} caracteres`;
    };

    /**
     * Establece un error para un campo
     * @param {string} field - Nombre del campo
     * @param {string} message - Mensaje de error
     */
    const setError = (field, message) => {
        errors.value[field] = message;
    };

    /**
     * Limpia el error de un campo
     * @param {string} field - Nombre del campo
     */
    const clearError = (field) => {
        delete errors.value[field];
    };

    /**
     * Limpia todos los errores
     */
    const clearAllErrors = () => {
        errors.value = {};
    };

    /**
     * Verifica si hay errores
     */
    const hasErrors = computed(() => {
        return Object.keys(errors.value).length > 0;
    });

    /**
     * Valida un formulario completo
     * @param {Object} formData - Datos del formulario
     * @param {Object} rules - Reglas de validación
     * @returns {boolean} True si es válido
     */
    const validateForm = (formData, rules) => {
        clearAllErrors();

        Object.keys(rules).forEach(field => {
            const rule = rules[field];
            const value = formData[field];

            if (rule.required) {
                const error = validateRequired(value, rule.label || field);
                if (error) {
                    setError(field, error);
                    return;
                }
            }

            if (rule.email) {
                const error = validateEmail(value);
                if (error) setError(field, error);
            }

            if (rule.password) {
                const error = validatePassword(value);
                if (error) setError(field, error);
            }

            if (rule.minLength) {
                const error = validateMinLength(value, rule.minLength);
                if (error) setError(field, error);
            }

            if (rule.maxLength) {
                const error = validateMaxLength(value, rule.maxLength);
                if (error) setError(field, error);
            }

            if (rule.match) {
                const error = validateMatch(value, formData[rule.match], rule.label);
                if (error) setError(field, error);
            }
        });

        return !hasErrors.value;
    };

    return {
        errors,
        hasErrors,
        validateEmail,
        validatePassword,
        validateRequired,
        validateMatch,
        validateMinLength,
        validateMaxLength,
        validateForm,
        setError,
        clearError,
        clearAllErrors,
    };
};
