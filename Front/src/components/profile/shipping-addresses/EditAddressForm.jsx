import React, { useState } from 'react';
import { Box, TextField, Button, FormControlLabel, Checkbox } from '@mui/material';

const EditAddressForm = ({ addressData, onSave, onCancel }) => {
  const [editedAddress, setEditedAddress] = useState({ ...addressData });

  const handleChange = (e) => {
    const { name, value, checked } = e.target;
    setEditedAddress(prevAddress => ({
      ...prevAddress,
      [name]: name === 'default' ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(editedAddress);
  };

  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
      <TextField
        required
        fullWidth
        label="Calle"
        name="street"
        margin="normal"
        value={editedAddress.street}
        onChange={handleChange}
      />
      <TextField
        fullWidth
        label="Piso"
        name="floor"
        margin="normal"
        value={editedAddress.floor}
        onChange={handleChange}
      />
      <TextField
        fullWidth
        label="Puerta"
        name="door"
        margin="normal"
        value={editedAddress.door}
        onChange={handleChange}
      />
      <TextField
        required
        fullWidth
        label="Ciudad"
        name="city"
        margin="normal"
        value={editedAddress.city}
        onChange={handleChange}
      />
      <TextField
        required
        fullWidth
        label="Código Postal"
        name="postalCode"
        margin="normal"
        value={editedAddress.postalCode}
        onChange={handleChange}
      />
      <TextField
        required
        fullWidth
        label="País"
        name="country"
        margin="normal"
        value={editedAddress.country}
        onChange={handleChange}
      />
      <TextField
        fullWidth
        label="Información Adicional"
        name="additionalInfo"
        margin="normal"
        value={editedAddress.additionalInfo}
        onChange={handleChange}
      />
      <FormControlLabel
        control={
          <Checkbox
            checked={editedAddress.default}
            onChange={handleChange}
            name="default"
            color="primary"
          />
        }
        label="Establecer como dirección predeterminada"
      />
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
        <Button variant="contained" color="primary" type="submit">
          Guardar Cambios
        </Button>
        <Button variant="outlined" color="secondary" onClick={onCancel} sx={{ ml: 2 }}>
          Cancelar
        </Button>
      </Box>
    </Box>
  );
};

export default EditAddressForm;
