import React, { useState } from 'react';
import { Box, TextField, Button, FormControlLabel, Checkbox } from '@mui/material';
import styles from '../../../styles/styles';
const AddAddressForm = ({ onSave, buyerId }) => {
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

  const handleChange = (e) => {
    const { name, value, checked } = e.target;
    setAddress(prev => ({
      ...prev,
      [name]: name === 'isDefault' ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(address);
  };
  

  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <TextField
                required
                fullWidth
                label="Street"
                name="street"
                margin="normal"
                value={address.street}
                onChange={handleChange}
            />
            <TextField
                fullWidth
                label="Floor"
                name="floor"
                margin="normal"
                value={address.floor}
                onChange={handleChange}
            />
            <TextField
                fullWidth
                label="Door"
                name="door"
                margin="normal"
                value={address.door}
                onChange={handleChange}
            />
            <TextField
                required
                fullWidth
                label="City"
                name="city"
                margin="normal"
                value={address.city}
                onChange={handleChange}
            />
            <TextField
                required
                fullWidth
                label="Postal Code"
                name="postalCode"
                margin="normal"
                value={address.postalCode}
                onChange={handleChange}
            />
            <TextField
                required
                fullWidth
                label="Country"
                name="country"
                margin="normal"
                value={address.country}
                onChange={handleChange}
            />
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
            <Button sx={{...styles.greenRoundedButton, mt:2}} type="submit" fullWidth variant="contained" color="primary" >
        Add Address
      </Button>
    </Box>
  );
};

export default AddAddressForm;