import React, { useState } from 'react';
import { Card, CardContent, Typography, IconButton, Grid, TextField, Button } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

const ShippingAddressItem = ({ id, street, floor, door, postal_code, city, country, adit_info, isDefault, onDelete, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedAddress, setEditedAddress] = useState({
    street, floor, door, city, postal_code, country, adit_info, isDefault
  });

  const handleEditChange = (event) => {
    const { name, value, checked } = event.target;
    setEditedAddress(prev => ({
      ...prev,
      [name]: name === 'isDefault' ? checked : value
    }));
  };

  const handleUpdate = async () => {
    await onUpdate(id, editedAddress);
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <Card sx={{ mb: 2, p: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Street"
              name="street"
              value={editedAddress.street}
              onChange={handleEditChange}
            />
            <TextField
              fullWidth
              label="Floor"
              name="floor"
              value={editedAddress.floor}
              onChange={handleEditChange}
            />
            <TextField
              fullWidth
              label="Door"
              name="door"
              value={editedAddress.door}
              onChange={handleEditChange}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="City"
              name="city"
              value={editedAddress.city}
              onChange={handleEditChange}
            />
            <TextField
              fullWidth
              label="Postal Code"
              name="postal_code"
              value={editedAddress.postal_code}
              onChange={handleEditChange}
            />
            <TextField
              fullWidth
              label="Country"
              name="country"
              value={editedAddress.country}
              onChange={handleEditChange}
            />
          </Grid>
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
          <Grid item xs={6}>
            <Typography variant="subtitle1"><strong>Street</strong></Typography>
            <Typography variant="body2">{street}</Typography>
            <Typography variant="subtitle1"><strong>Floor</strong></Typography>
            <Typography variant="body2">{floor}</Typography>
            <Typography variant="subtitle1"><strong>Door</strong></Typography>
            <Typography variant="body2">{door}</Typography>
            <Typography variant="subtitle1"><strong>City</strong></Typography>
            <Typography variant="body2">{city}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1"><strong>Postal Code</strong></Typography>
            <Typography variant="body2">{postal_code}</Typography>
            <Typography variant="subtitle1"><strong>Country</strong></Typography>
            <Typography variant="body2">{country}</Typography>
            <Typography variant="subtitle1"><strong>Additional Information</strong></Typography>
            <Typography variant="body2">{adit_info}</Typography>
            <Typography variant="subtitle1"><strong>Default</strong></Typography>
            <Typography variant="body2">{isDefault ? 'Yes' : 'No'}</Typography>
          </Grid>
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
