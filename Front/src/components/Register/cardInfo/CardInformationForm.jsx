import React, { useState, useEffect } from 'react';
import { Box, Grid, TextField, Typography, Alert } from '@mui/material';
import styles from "../../../styles/styles";

const CardInformationForm = ({ cardData, handleChange, setCardFormValidity }) => {
    const [formValidity, setFormValidity] = useState({
        CardName: false,
        CardNumber: false,
        ExpiryDate: false,
        Cvv: false
    });

    const handleFieldValidation = (fieldId, value) => {
        if (typeof value !== 'string') {
            console.error(`Invalid value for ${fieldId}. Expected a string but got ${typeof value}`);
            return false;
        }
    
        switch (fieldId) {
            case "CardName":
                return value.trim().length > 0;
            case "CardNumber":
                return /^\d{16}$/.test(value.replace(/\s+/g, ''));
            case "ExpiryDate":
                const matches = value.match(/^(0[1-9]|1[0-2])\/(\d{4})$/);
                if (matches) {
                    const year = parseInt(matches[2], 10);
                    const month = parseInt(matches[1], 10);
                    const currentYear = new Date().getFullYear();
                    if (year >= currentYear && year <= currentYear + 50) {
                        return true;
                    }
                }
                return false;
            case "Cvv":
                return /^\d{3}$/.test(value);
            default:
                return false;
        }
    };
    

    useEffect(() => {
        const validity = {
            CardName: handleFieldValidation("CardName",cardData.CardName),
            CardNumber: handleFieldValidation("CardNumber", cardData.CardNumber),
            ExpiryDate: handleFieldValidation("ExpiryDate", cardData.ExpiryDate),
            Cvv: handleFieldValidation("Cvv", cardData.Cvv)
        };
        setFormValidity(validity);
        setCardFormValidity(Object.values(validity).every(valid => valid));
    }, [cardData, setCardFormValidity]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        handleChange(e);
        setFormValidity((prevValidity) => ({
            ...prevValidity,
            [name]: handleFieldValidation(name, value)
        }));
    };

    const getHelperText = (field) => {
        switch (field) {
            case "CardNumber":
                return formValidity.CardNumber ? '' : 'Card number must be 16 digits';
            case "ExpiryDate":
                return formValidity.ExpiryDate ? '' : 'Insert a valid Date';
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
                        error={!formValidity.CardNumber}
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
                        error={!formValidity.ExpiryDate}
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
                        helperText={getHelperText("Cvv")}
                        error={!formValidity.Cvv}
                    />
                </Grid>
            </Grid>
            {Object.values(formValidity).every(valid => valid) ? (
                <Alert severity="success" sx={{ mt: 2 }}>
                    The card information is correct.
                </Alert>
            ) : (
                <Alert severity="error" sx={{ mt: 2 }}>
                    Please fill in the card information correctly.
                </Alert>
            )}
        </Box>
    );
};

export default CardInformationForm;
