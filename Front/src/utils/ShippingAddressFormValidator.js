export const validateStreet = (street) => {
    return street.trim().length > 0; 
};

export const validateFloor = (floor) => {
    return Number.isInteger(floor) && floor > 0; 
};

export const validateDoor = (door) => {
    return door.trim().length > 0; 
};

export const validateCity = (city) => {
    return city.trim().length > 0;
};

export const validatePostalCode = (postalCode) => {
    return /^\d{5}$/.test(postalCode);  
};

export const validateCountry = (country) => {
    return country.trim().length > 0; 
};

export const validateAdditionalInfo = (info) => {
    return true; 
};

export const validateDefault = (isDefault) => {
    return typeof isDefault === 'boolean';  
};
