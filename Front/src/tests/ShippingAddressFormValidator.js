import {
    validateStreet,
    validateFloor,
    validateDoor,
    validateCity,
    validatePostalCode,
    validateCountry,
    validateAdditionalInfo,
    validateDefault,
} from '../utils/ShippingAddressFormValidator';

describe('Validation Functions', () => {
    test('validateStreet returns true for non-empty streets', () => {
        expect(validateStreet('123 Main St')).toBe(true);
        expect(validateStreet('   ')).toBe(false);
    });

    test('validateFloor returns true for valid floors', () => {
        expect(validateFloor(1)).toBe(true);
        expect(validateFloor(0)).toBe(false);
        expect(validateFloor(-1)).toBe(false);
        expect(validateFloor('1')).toBe(false);
    });

    test('validateDoor returns true for non-empty doors', () => {
        expect(validateDoor('A')).toBe(true);
        expect(validateDoor('   ')).toBe(false);
    });

    test('validateCity returns true for non-empty cities', () => {
        expect(validateCity('New York')).toBe(true);
        expect(validateCity('   ')).toBe(false);
    });

    test('validatePostalCode returns true for valid postal codes', () => {
        expect(validatePostalCode('12345')).toBe(true);
        expect(validatePostalCode('1234')).toBe(false);
        expect(validatePostalCode('123456')).toBe(false);
        expect(validatePostalCode('12a45')).toBe(false);
    });

    test('validateCountry returns true for non-empty countries', () => {
        expect(validateCountry('USA')).toBe(true);
        expect(validateCountry('   ')).toBe(false);
    });

    test('validateAdditionalInfo always returns true', () => {
        expect(validateAdditionalInfo('Any info')).toBe(true);
        expect(validateAdditionalInfo('')).toBe(true);
    });

    test('validateDefault returns true for boolean values', () => {
        expect(validateDefault(true)).toBe(true);
        expect(validateDefault(false)).toBe(true);
        expect(validateDefault('true')).toBe(false);
        expect(validateDefault(0)).toBe(false);
    });
});
