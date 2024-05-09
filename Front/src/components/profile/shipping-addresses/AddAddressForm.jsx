import React, { useEffect, useState } from 'react';
import { Box, TextField, Button, FormControlLabel, Checkbox, Typography, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import styles from '../../../styles/styles';
import getCountries from '../../../api/services/country/CountriesService';
import { createAddress } from '../../../api/services/user/profile/ProfileService';
import { validateField } from '../../../utils/ShippingAddressValidation';

const AddAddressForm = ({ onAddressCreated }) => {
  const [address, setAddress] = useState({
    street: '',
    floor: '',
    door: '',
    city: '',
    postalCode: '',
    country: '',
    additionalInfo: '',
    isDefault: false,
  });
  const [errors, setErrors] = useState({});
  const [countries, setCountries] = useState([]);

  useEffect(() => {
    const loadCountries = async () => {
      try {
        const countryData = await getCountries();
        setCountries(countryData);
      } catch (error) {
        console.error('Error loading countries:', error);
      }
    };

    loadCountries();
  }, []);

  const handleChange = (e) => {
    const { name, value, checked, type } = e.target;
    const newValue = type === 'number' ? parseInt(value, 10) : value;
    setAddress(prev => ({
      ...prev,
      [name]: name === 'isDefault' ? checked : newValue,
    }));
    const error = validateField(name, name === 'isDefault' ? checked : newValue);
    setErrors(prev => ({ ...prev, [name]: error }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};
    Object.keys(address).forEach(key => {
      newErrors[key] = validateField(key, address[key]);
    });
    setErrors(newErrors);
    const formIsValid = Object.values(newErrors).every(error => !error);
    if (formIsValid) {
      try {
        const newAddress = await createAddress(address);
        onAddressCreated(newAddress);
      } catch (error) {
        console.error('Error saving new address:', error);
        setErrors(prev => ({ ...prev, form: 'Failed to save new address' }));
      }
    } else {
      console.log('Validation errors', newErrors);
    }
  };

  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
      {Object.values(errors).map((error, index) => error && (
        <Typography key={index} color="error">{error}</Typography>
      ))}
      <TextField
        required
        fullWidth
        label="Street"
        name="street"
        margin="normal"
        value={address.street}
        onChange={handleChange}
        error={!!errors.street}
        helperText={errors.street || ' '}
      />
      <TextField
        fullWidth
        label="Floor"
        name="floor"
        type="number"
        margin="normal"
        value={address.floor}
        onChange={handleChange}
        error={!!errors.floor}
        helperText={errors.floor || ' '}
      />
      <TextField
        fullWidth
        label="Door"
        name="door"
        margin="normal"
        value={address.door}
        onChange={handleChange}
        error={!!errors.door}
        helperText={errors.door || ' '}
      />
      <TextField
        required
        fullWidth
        label="City"
        name="city"
        margin="normal"
        value={address.city}
        onChange={handleChange}
        error={!!errors.city}
        helperText={errors.city || ' '}
      />
      <TextField
        required
        fullWidth
        label="Postal Code"
        name="postalCode"
        margin="normal"
        value={address.postalCode}
        onChange={handleChange}
        error={!!errors.postalCode}
        helperText={errors.postalCode || ' '}
      />
      <FormControl fullWidth margin="normal">
        <InputLabel id="country-select-label">Country</InputLabel>
        <Select
          labelId="country-select-label"
          id="country-select"
          value={address.country}
          label="Country"
          name="country"
          onChange={handleChange}
          error={!!errors.country}
        >
          {countries.map((country, index) => (
            <MenuItem key={index} value={country}>{country}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <TextField
        fullWidth
        label="Additional Information"
        name="additionalInfo"
        margin="normal"
        value={address.additionalInfo}
        onChange={handleChange}
      />
      <FormControlLabel
        control={
          <Checkbox
            checked={address.isDefault}
            onChange={handleChange}
            name="isDefault"
            color="primary"
          />
        }
        label="Default Address"
      />
      <Button sx={{ ...styles.greenRoundedButton, mt: 2 }} type="submit" fullWidth variant="contained" color="primary">
        Add Address
      </Button>
    </Box>
  );
};

export default AddAddressForm;
