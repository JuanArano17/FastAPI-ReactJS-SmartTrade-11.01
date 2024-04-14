import React, { useState } from 'react';
import { Box, Grid, TextField, Typography, Button } from '@mui/material';
import styles from "../../styles/styles";

const CardInformationForm = ({ cardData, handleChange }) => {
    const [formValidity, setFormValidity] = useState({
        CardNumber: false,
        ExpiryDate: false,
        CVV: false
    });

    const handleFieldValidation = (fieldId, value) => {
        switch (fieldId) {
            case "CardNumber":
                return value.length === 16;
            case "ExpiryDate":
                return /^\d{2}\/\d{2}$/.test(value);
            case "CVV":
                return /^\d{3}$/.test(value);
            default:
                return false;
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        handleChange(e);
        setFormValidity((prevValidity) => ({
            ...prevValidity,
            [name]: handleFieldValidation(name, value)
        }));
    };

    const isFormValid = Object.values(formValidity).every(valid => valid);

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
                        onChange={handleChange}
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
                        onChange={handleChange}
                        inputProps={{ maxLength: 7 }}
                        sx={{ ...styles.textfields, backgroundColor: "white" }}
                        error={!formValidity.ExpiryDate}
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
                        value={cardData.CVV}
                        onChange={handleInputChange}
                        inputProps={{ maxLength: 3 }}
                        sx={{ ...styles.textfields, backgroundColor: "white" }}
                        error={!formValidity.CVV}
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
