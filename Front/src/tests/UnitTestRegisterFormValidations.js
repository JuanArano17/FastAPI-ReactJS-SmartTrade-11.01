import {
    validateEmail,
    validatePassword,
    validateAge,
    validateDNI,
    validateCIF,
    validateBankData
} from '../utils/registerFormValidations';

describe('Validation Functions', () => {
    test('validateEmail returns true for valid emails', () => {
        expect(validateEmail('test@example.com')).toBe(true);
        expect(validateEmail('user.name+tag+sorting@example.com')).toBe(true);
    });

    test('validateEmail returns false for invalid emails', () => {
        expect(validateEmail('plainaddress')).toBe(false);
        expect(validateEmail('@missingusername.com')).toBe(false);
    });

    test('validatePassword returns true for valid passwords', () => {
        expect(validatePassword('Password123!')).toBe(true);
    });

    test('validatePassword returns false for invalid passwords', () => {
        expect(validatePassword('password')).toBe(false);
        expect(validatePassword('Password')).toBe(false);
    });

    test('validateAge returns true for valid ages', () => {
        const validBirthDate = new Date();
        validBirthDate.setFullYear(validBirthDate.getFullYear() - 25);
        expect(validateAge(validBirthDate.toISOString().split('T')[0])).toBe(true);
    });

    test('validateAge returns false for invalid ages', () => {
        const futureBirthDate = new Date();
        futureBirthDate.setFullYear(futureBirthDate.getFullYear() + 1);
        expect(validateAge(futureBirthDate.toISOString().split('T')[0])).toBe(false);
    });

    test('validateDNI returns true for valid DNIs', () => {
        expect(validateDNI('12345678Z')).toBe(true);
    });

    test('validateDNI returns false for invalid DNIs', () => {
        expect(validateDNI('12345678')).toBe(false);
        expect(validateDNI('Z12345678')).toBe(false);
    });

    test('validateCIF returns true for valid CIFs', () => {
        expect(validateCIF('A12345678')).toBe(true);
    });

    test('validateCIF returns false for invalid CIFs', () => {
        expect(validateCIF('12345678A')).toBe(false);
    });

    test('validateBankData returns true for valid bank data', () => {
        expect(validateBankData('1234567890')).toBe(true);
    });

    test('validateBankData returns false for invalid bank data', () => {
        expect(validateBankData('12345')).toBe(false);
    });
});
