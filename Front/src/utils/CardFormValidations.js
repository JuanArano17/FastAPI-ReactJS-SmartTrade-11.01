export const validateCardNumber = (value) => {
    return /^\d{16}$/.test(value.replace(/\s+/g, ''));
};

export const validateCardExpiration = (value) => {
    const currentDate = new Date();
    const inputDate = new Date(value);
    return inputDate > currentDate;
};

export const validateCVV = (value) => {
    return /^\d{3}$/.test(value);
};

export const validateCardExpirationV2 = (value) => {
    const matches = value.match(/^(0[1-9]|1[0-2])\/(\d{4})$/);
    if (matches) {
        const year = parseInt(matches[2], 10);
        const month = parseInt(matches[1], 10);
        const currentYear = new Date().getFullYear();
        if (year >= currentYear && year <= currentYear + 50) {
            return true;
        }
    }
    return false;
}
