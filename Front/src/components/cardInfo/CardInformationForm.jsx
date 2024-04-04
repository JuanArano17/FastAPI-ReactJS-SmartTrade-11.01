import React from 'react';
import { Box, Grid, TextField, Typography, Button } from '@mui/material';
import styles from "../../styles/styles";

const CardInformationForm = ({ cardData, handleChange }) => {
    return (
        <Box component="form" sx={styles.formContainer}>
            <Grid container spacing={3}>
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
                        onChange={handleChange}
                        inputProps={{ maxLength: 16 }}
                        sx={{ ...styles.textfields, backgroundColor: "white" }}
                    />
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                        Date of expiry
                    </Typography>
                    <TextField
                        id="ExpiryDate"
                        name="ExpiryDate"
                        placeholder="09/26*"
                        required
                        fullWidth
                        value={cardData.ExpiryDate}
                        onChange={handleChange}
                        inputProps={{ maxLength: 5 }}
                        sx={{ ...styles.textfields, backgroundColor: "white" }}
                    />
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                        CVV
                    </Typography>
                    <TextField
                        id="CVV"
                        name="CVV"
                        placeholder="123*"
                        required
                        fullWidth
                        value={cardData.CVV}
                        onChange={handleChange}
                        inputProps={{ maxLength: 3 }}
                        sx={{ ...styles.textfields, backgroundColor: "white" }}
                    />
                </Grid>
            </Grid>
            <Button
                fullWidth
                sx={styles.registerButton}
                onClick={() => console.log("Listo para guardar después del registro del usuario")}
            >
                Save
            </Button>
        </Box>
    );
};

export default CardInformationForm;
