import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, IconButton, Grid, TextField, Button, Checkbox, FormControlLabel, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { validateField } from '../../../utils/ShippingAddressValidation';
import getCountries from '../../../api/services/country/CountriesService'; 

const ShippingAddressItem = ({ id, street, floor, door, postal_code, city, country, adit_info, isDefault, onDelete, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedAddress, setEditedAddress] = useState({
    street, floor, door, city, postal_code, country, adit_info, isDefault
  });
  const [errors, setErrors] = useState({});
  const [countries, setCountries] = useState([]);

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const fetchedCountries = await getCountries(); 
        setCountries(fetchedCountries);
      } catch (error) {
        console.error('Failed to fetch countries:', error);
      }
    };

    fetchCountries();
  }, []);

  const handleEditChange = (event) => {
    const { name, value, checked, type } = event.target;
    const newValue = type === 'checkbox' ? checked : value;
    const error = validateField(name, newValue);
    setEditedAddress(prev => ({
      ...prev,
      [name]: newValue
    }));
    setErrors(prev => ({
      ...prev,
      [name]: error
    }));
  };

  const handleUpdate = async () => {
    const isValid = Object.values(errors).every(error => !error);
    if (isValid) {
      await onUpdate(id, editedAddress);
      setIsEditing(false);
    }
  };

  if (isEditing) {
    return (
      <Card sx={{ mb: 2, p: 2 }}>
        <Grid container spacing={2}>
          {Object.entries(editedAddress).map(([key, value]) => {
            if (key === 'isDefault') {
              return (
                <Grid item xs={12} key={key}>
                  <FormControlLabel
                    control={<Checkbox checked={!!value} onChange={handleEditChange} name={key} />}
                    label="Default Address"
                  />
                </Grid>
              );
            } else if (key === 'country') {
              return (
                <Grid item xs={6} key={key}>
                  <FormControl fullWidth>
                    <InputLabel>Country</InputLabel>
                    <Select
                      value={value}
                      onChange={handleEditChange}
                      name={key}
                      label="Country"
                    >
                      {countries.map((countryName, index) => (
                        <MenuItem key={index} value={countryName}>{countryName}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
              );
            } else {
              return (
                <Grid item xs={6} key={key}>
                  <TextField
                    fullWidth
                    label={key.replace('_', ' ').replace('adit_info', 'Additional Info')}
                    name={key}
                    value={value || ''}
                    onChange={handleEditChange}
                    error={!!errors[key]}
                    helperText={errors[key] || ' '}
                  />
                </Grid>
              );
            }
          })}
          <Grid item xs={12}>
            <Button onClick={handleUpdate} color="primary" variant="contained">
              Save
            </Button>
            <Button onClick={() => setIsEditing(false)} color="secondary">
              Cancel
            </Button>
          </Grid>
        </Grid>
      </Card>
    );
  }

  return (
    <Card sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
      <CardContent>
        <Grid container>
          {Object.entries({ street, floor, door, city, postal_code, country, adit_info, isDefault }).map(([key, value]) => (
            <Grid item xs={6} key={key}>
              <Typography variant="subtitle1"><strong>{key.replace('_', ' ').replace('adit_info', 'Additional Info')}</strong></Typography>
              <Typography variant="body2">{value ? value.toString() : 'N/A'}</Typography>
            </Grid>
          ))}
        </Grid>
      </CardContent>
      <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
        <IconButton aria-label="edit" onClick={() => setIsEditing(true)}>
          <EditIcon />
        </IconButton>
        <IconButton aria-label="delete" onClick={() => onDelete(id)}>
          <DeleteIcon />
        </IconButton>
      </CardContent>
    </Card>
  );
};

export default ShippingAddressItem;
