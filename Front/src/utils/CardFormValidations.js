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