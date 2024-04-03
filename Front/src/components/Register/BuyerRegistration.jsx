import React, { useState } from "react";
import { Box, Typography, TextField, Button, Container, Grid, Paper, IconButton, InputAdornment, } from "@mui/material";
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import styles from "../../styles/styles";
const formFields = [
    { id: "firstName", placeholder: "Patricio*", name: "Name", autoComplete: "fname", autoFocus: true },
    { id: "lastName", placeholder: "Letelier*", name: "Surname", autoComplete: "lname" },
    { id: "email", placeholder: "letelier@upv.edu.es*", name: "Email", autoComplete: "email" },
    { id: "dni", name: "DNI", placeholder: "12345678A*" },
    { id: "password", placeholder: "PSW_curso_2023_2024*", name: "Password", autoComplete: "new-password", type: "password" },
    { id: "age", name: "Date Of Birth", type: "date" }
];
const BuyerRegistration = () => {
    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        email: "",
        dni: "",
        password: "",
        dateOfBirth: "",
        CardNumber: "",
        ExpiryDate: "",
        CVV: "",
    });
    const [showPassword, setShowPassword] = useState(false);
    const handleChange = (e) => {
    }
    const handleSubmit = (e) => {
        e.preventDefault();
        // Logic for communicating with backend
    };
    const togglePasswordVisibility = () => {
        setShowPassword((prev) => !prev);
    };
    return (
        <Container component="main" maxWidth="lg">
            <Paper elevation={3} sx={styles.paperContainer}>
                <Grid container spacing={3}>
                    <Grid item xs={12} sm={6}>
                        <Typography component="h1" variant="h5" color="#629c44" mb={2}>
                            Register
                        </Typography>
                        <Box component="form" onSubmit={handleSubmit} sx={styles.formContainer}>
                            {formFields.map((field) => (
                                <Grid item xs={12} key={field.id}>
                                    <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                                        {field.name}
                                    </Typography>
                                    {field.type === 'password' ? (
                                        <TextField
                                            {...field}
                                            required
                                            fullWidth
                                            value={formData[field.name]}
                                            onChange={handleChange}
                                            sx={styles.textfields}
                                            inputProps={field.name === 'DNI' ? { maxLength: 9 } : {}}
                                            type={showPassword ? 'text' : 'password'}
                                            InputProps={{
                                                endAdornment: (
                                                    <InputAdornment position="end">
                                                        <IconButton
                                                            onClick={togglePasswordVisibility}
                                                            edge="end"
                                                            aria-label="toggle password visibility"
                                                        >
                                                            {showPassword ? <VisibilityIcon /> : <VisibilityOffIcon />}
                                                        </IconButton>
                                                    </InputAdornment>
                                                ),
                                            }}
                                        />
                                    ) : (
                                        <TextField
                                            {...field}
                                            required
                                            fullWidth
                                            value={formData[field.name]}
                                            onChange={handleChange}
                                            sx={styles.textfields}
                                            inputProps={field.name === 'DNI' ? { maxLength: 9 } : {}}
                                        />
                                    )}
                                </Grid>
                            ))}
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={styles.registerButton}
                            >
                                Register BUYER
                            </Button>
                        </Box>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Paper elevation={3} sx={{ ...styles.paperContainer, backgroundColor: "#f2f2f7" }}>
                            <Typography component="h2" variant="h6" color="#629c44" mb={2}>
                                Enter your card information (OPTIONAL)
                            </Typography>
                            <Box component="form" onSubmit={handleSubmit} sx={styles.formContainer}>
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
                                            value={formData.CardNumber}
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
                                            value={formData.ExpiryDate}
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
                                            value={formData.CVV}
                                            onChange={handleChange}
                                            inputProps={{ maxLength: 3 }}
                                            sx={{ ...styles.textfields, backgroundColor: "white" }}
                                        />
                                    </Grid>
                                </Grid>
                                <Button
                                    type="submit"
                                    fullWidth
                                    sx={styles.registerButton}
                                >
                                    Save
                                </Button>
                            </Box>
                        </Paper>
                    </Grid>
                </Grid>
            </Paper>
        </Container>
    );
};
export default BuyerRegistration;