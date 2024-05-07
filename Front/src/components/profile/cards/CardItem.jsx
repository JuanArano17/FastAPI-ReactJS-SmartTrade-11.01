import React, { useState } from 'react';
import { Card, CardContent, Typography, IconButton, Grid, TextField, Button } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

const CardItem = ({ id, card_number, card_name, card_exp_date, card_security_num, onDelete, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedCard, setEditedCard] = useState({
    card_number, card_name, card_exp_date, card_security_num
  });

  const handleEditChange = (event) => {
    const { name, value } = event.target;
    setEditedCard(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleUpdate = async () => {
    await onUpdate(id, editedCard);
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <Card sx={{ mb: 2 }}>
        <Grid container spacing={2} padding={2}>
          <Grid item xs={6}>
            <TextField
              label="Card Number"
              name="card_number"
              value={editedCard.card_number}
              onChange={handleEditChange}
              fullWidth
            />
            <TextField
              label="Card Name"
              name="card_name"
              value={editedCard.card_name}
              onChange={handleEditChange}
              fullWidth
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              label="Expiration Date"
              name="card_exp_date"
              type="date"
              value={editedCard.card_exp_date}
              onChange={handleEditChange}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
            <TextField
              label="CVV"
              name="card_security_num"
              value={editedCard.card_security_num}
              onChange={handleEditChange}
              fullWidth
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
            <Typography variant="subtitle1"><strong>Card Number</strong></Typography>
            <Typography variant="body2">{card_number}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1"><strong>Card Name</strong></Typography>
            <Typography variant="body2">{card_name}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1"><strong>Expiration Date</strong></Typography>
            <Typography variant="body2">{card_exp_date}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1"><strong>CVV</strong></Typography>
            <Typography variant="body2">{card_security_num}</Typography>
          </Grid>
        </Grid>
      </CardContent>
      <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
        <IconButton aria-label="edit" onClick={() => setIsEditing(true)} size="large">
          <EditIcon />
        </IconButton>
        <IconButton aria-label="delete" onClick={onDelete} size="large">
          <DeleteIcon />
        </IconButton>
      </CardContent>
    </Card>
  );
};

export default CardItem;
