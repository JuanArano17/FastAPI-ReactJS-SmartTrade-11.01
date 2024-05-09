import React, { useState, useEffect } from 'react';
import { Box, TextField, Button, Typography, Snackbar, Alert } from '@mui/material';
import styles from '../../../styles/styles';
import { validateCardNumber, validateCardExpiration, validateCVV } from '../../../utils/CardFormValidations';

const AddCard = ({ onSave }) => {
  const [card, setCard] = useState({
    card_number: '',
    card_name: '',
    card_security_num: '',
    card_exp_date: '',
  });

  const [formValidity, setFormValidity] = useState({
    card_number: false,
    card_exp_date: false,
    card_security_num: false
  });

  const [apiError, setApiError] = useState('');

  useEffect(() => {
    setFormValidity({
      card_number: validateCardNumber(card.card_number),
      card_exp_date: validateCardExpiration(card.card_exp_date),
      card_security_num: validateCVV(card.card_security_num)
    });
  }, [card]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCard(prevCard => ({
      ...prevCard,
      [name]: value
    }));
  };

  const isFormValid = Object.values(formValidity).every(Boolean);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isFormValid) {
      try {
        await onSave(card);
        setApiError(''); 
      } catch (error) {
        console.error("API Error on save:", error);
        setApiError('Failed to save card. Please try again.');
      }
    } else {
      console.error("Invalid form submission");
      setApiError('Please fill in all fields correctly.');
    }
  };

  const handleCloseSnackbar = () => {
    setApiError('');
  };

  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
      <Typography variant="h6" gutterBottom>
        Add New Card
      </Typography>
      <TextField
        required
        fullWidth
        label="Card Number"
        name="card_number"
        margin="normal"
        value={card.card_number}
        onChange={handleChange}
        error={!formValidity.card_number}
        helperText={!formValidity.card_number ? "Card number must be 16 digits" : ""}
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
        inputProps={{ maxLength: 3 }}
        value={card.card_security_num}
        onChange={handleChange}
        error={!formValidity.card_security_num}
        helperText={!formValidity.card_security_num ? "CVV must be 3 digits" : ""}
      />
      <TextField
        required
        fullWidth
        label="Expiration Date"
        name="card_exp_date"
        margin="normal"
        type="date"
        InputLabelProps={{ shrink: true }}
        value={card.card_exp_date}
        onChange={handleChange}
        error={!formValidity.card_exp_date}
        helperText={!formValidity.card_exp_date ? "Expiration date must be later than today." : ""}
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        sx={{ ...styles.greenRoundedButton, mt: 3 }}
        disabled={!isFormValid}
      >
        Add Card
      </Button>
      <Snackbar open={!!apiError} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
          {apiError}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default AddCard;