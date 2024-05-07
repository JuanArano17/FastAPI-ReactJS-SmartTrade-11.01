import React, { useState } from 'react';
import { Box, TextField, Button } from '@mui/material';
import styles from '../../../styles/styles';

const AddCardForm = ({ onSave }) => {
  const [card, setCard] = useState({
    card_number: '',
    card_name: '',
    card_security_num: '',
    card_exp_date: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCard(prevCard => ({
      ...prevCard,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    onSave({
      card_number: card.card_number,
      card_name: card.card_name,
      card_security_num: card.card_security_num,
      card_exp_date: card.card_exp_date,
    });
  };

  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
      <TextField
        required
        fullWidth
        label="Card Number"
        name="card_number"
        margin="normal"
        value={card.card_number}
        onChange={handleChange}
      />
      <TextField
        required
        fullWidth
        label="Card Name"
        name="card_name"
        margin="normal"
        value={card.card_name}
        onChange={handleChange}
      />
      <TextField
        required
        fullWidth
        label="CVV"
        name="card_security_num"
        margin="normal"
        value={card.card_security_num}
        onChange={handleChange}
      />
      <TextField
        required
        fullWidth
        label="Expiration Date"
        name="card_exp_date"
        margin="normal"
        type="date"
        InputLabelProps={{
          shrink: true,
        }}
        value={card.expirationDate}
        onChange={handleChange}
      />
      <Button type="submit" fullWidth variant="contained" color="primary" sx={{...styles.greenRoundedButton,mt:3}} 
        
      >
        Add Card
      </Button>
    </Box>
  );
};

export default AddCardForm;
