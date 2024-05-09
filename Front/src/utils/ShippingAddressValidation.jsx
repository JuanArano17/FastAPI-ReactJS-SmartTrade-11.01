export const validateStreet = (street) => {
    return street.trim().length >= 5 && street.trim().length <= 35;
};

export const validateFloor = (floor) => {
    return floor === '' || (Number.isInteger(floor) && floor >= 1 && floor <= 200);
};

export const validateDoor = (door) => {
    return door.trim().length >= 1 && door.trim().length <= 6;
};

export const validateAdditionalInfo = (info) => {
    return !info || info.trim().length <= 70;
};

export const validateCity = (city) => {
    return city.trim().length >= 1 && city.trim().length <= 28;
};

export const validatePostalCode = (postalCode) => {
    return postalCode.trim().length >= 5 && postalCode.trim().length <= 8;
};

export const validateCountry = (country) => {
    return country.trim().length >= 1;
};

export const validateDefault = (isDefault) => {
    return typeof isDefault === 'boolean';
};

export const validateField = (name, value) => {
    switch (name) {
        case 'street':
            return validateStreet(value) ? '' : 'Invalid street';
        case 'floor':
            return validateFloor(value) ? '' : 'Invalid floor';
        case 'door':
            return validateDoor(value) ? '' : 'Invalid door';
        case 'additionalInfo':
            return validateAdditionalInfo(value) ? '' : 'Invalid additional information';
        case 'city':
            return validateCity(value) ? '' : 'Invalid city';
        case 'postalCode':
            return validatePostalCode(value) ? '' : 'Invalid postal code';
        case 'country':
            return validateCountry(value) ? '' : 'Invalid country';
        case 'isDefault':
            return validateDefault(value) ? '' : 'Invalid default flag';
        default:
            return '';
    }
};
