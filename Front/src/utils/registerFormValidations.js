export const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
};
export const validatePassword = (password) => {
    const re = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
    return re.test(password);
};
export const validateAge = (BirthDate) => {
    const today = new Date();
    const birthDate = new Date(BirthDate);
    let age = today.getFullYear() - birthDate.getFullYear(); 
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age >= 0 && age <= 100;
};
export const validateDNI = (dni) => {
    const re = /^\d{8}[a-zA-Z]$/;
    return re.test(dni);
};
export const validateCIF = (cif) => {
    const re = /^[ABCDEFGHJKLMNPQRSUVW]\d{7}[0-9A-J]$/;
    return re.test(cif);
}
export const validateBankData = (bankData) => {
    return bankData.length >= 10;
}