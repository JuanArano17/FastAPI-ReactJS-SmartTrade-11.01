import React, { useState, useEffect } from 'react';
import { Box, Grid, TextField, Typography, Button } from '@mui/material';
import styles from "../../../styles/styles";
import { validateCardNumber, validateCardExpirationV2, validateCVV } from '../../../utils/CardFormValidations'; // Adjust the path as necessary

const CardInformationForm = ({ cardData, handleChange }) => {
    const [formValidity, setFormValidity] = useState({
        CardNumber: false,
        ExpiryDate: false,
        Cvv: false
    });

    const [touched, setTouched] = useState({
        CardNumber: false,
        ExpiryDate: false,
        Cvv: false
    });

    const handleFieldValidation = (fieldId, value) => {
        switch (fieldId) {
            case "CardNumber":
                return validateCardNumber(value); 
            case "ExpiryDate":
                return validateCardExpirationV2(value);
            case "Cvv":
                return validateCVV(value);
            default:
                return false;
        }
    };

    useEffect(() => {
        // We won't automatically validate on mount to avoid initial error display
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        handleChange(e);
        setFormValidity((prevValidity) => ({
            ...prevValidity,
            [name]: handleFieldValidation(name, value)
        }));
        setTouched((prevTouched) => ({
            ...prevTouched,
            [name]: true
        }));
    };

    const isFormValid = Object.values(formValidity).every(valid => valid);
    
    const getHelperText = (field) => {
        if (!touched[field]) return '';
        switch (field) {
            case "CardNumber":
                return formValidity.CardNumber ? '' : 'Card number must be 16 digits';
            case "ExpiryDate":
                return formValidity.ExpiryDate ? '' : 'Insert a valid date';
            case "Cvv":
                return formValidity.Cvv ? '' : 'CVV must be 3 digits';
            default:
                return '';
        }
    };
    
    return (
        <Box component="form" sx={styles.formContainer}>
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                        Card Name
                    </Typography>
                    <TextField
                        id="CardName"
                        name="CardName"
                        placeholder="Nombre en la tarjeta"
                        required
                        fullWidth
                        value={cardData.CardName}
                        onChange={handleInputChange}
                        sx={{ ...styles.textfields, backgroundColor: "white" }}
                    />
                </Grid>
                <Grid item xs={12}>
                    <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                        Card Number
                    </Typography>
                    <TextField
                        id="CardNumber"
                        name="CardNumber"
                        placeholder="1234-1234-1234-1234*"
                        required
                        fullWidth
                        value={cardData.CardNumber}
                        onChange={handleInputChange}
                        inputProps={{ maxLength: 16 }}
                        sx={{ ...styles.textfields, backgroundColor: "white" }}
                        error={touched.CardNumber && !formValidity.CardNumber}
                        helperText={getHelperText("CardNumber")}
                    />
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                        Date of expiry
                    </Typography>
                    <TextField
                        id="ExpiryDate"
                        name="ExpiryDate"
                        placeholder="09/2026*"
                        required
                        fullWidth
                        value={cardData.ExpiryDate}
                        onChange={handleInputChange}
                        inputProps={{ maxLength: 7 }}
                        sx={{ ...styles.textfields, backgroundColor: "white" }}
                        error={touched.ExpiryDate && !formValidity.ExpiryDate}
                        helperText={getHelperText("ExpiryDate")}
                    />
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                        CVV
                    </Typography>
                    <TextField
                        id="Cvv"
                        name="Cvv"
                        placeholder="123*"
                        required
                        fullWidth
                        value={cardData.Cvv}
                        onChange={handleInputChange}
                        inputProps={{ maxLength: 3 }}
                        sx={{ ...styles.textfields, backgroundColor: "white" }}
                        error={touched.Cvv && !formValidity.Cvv}
                        helperText={getHelperText("Cvv")}
                    />
                </Grid>
            </Grid>
            <Button
                fullWidth
                sx={{ ...styles.registerButton, pointerEvents: isFormValid ? "auto" : "none", opacity: isFormValid ? 1 : 0.5 }}
                disabled={!isFormValid}
                onClick={() => console.log("Listo para guardar después del registro del usuario")}
            >
                Save
            </Button>
        </Box>
    );
};

export default CardInformationForm;