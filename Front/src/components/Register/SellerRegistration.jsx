import React, { useState } from "react";
import { useHistory } from 'react-router-dom';
import { Box, Typography, TextField, Button, Container, Grid, Paper, IconButton, InputAdornment, Snackbar } from "@mui/material";
import { getDefaultRegisterSellerModel } from "../../models/RegisterSellerModel";
import { validateEmail, validatePassword, validateAge, validateCIF, validateBankData } from "../../utils/registerFormValidations";
import { registerUserSellerService } from "../../api/services/user/AuthService";
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import styles from "../../styles/styles";

const formFields = [
    { id: "firstName", name: "Name", label: "Patricio", autoComplete: "fname", autoFocus: true },
    { id: "lastName", name: "Surname", label: "Letelier", autoComplete: "lname" },
    { id: "email", name: "Email", label: "letelier@upv.edu.es", autoComplete: "email" },
    { id: "password", name: "Password", label: "PSW_curso_2023_2024", autoComplete: "new-password", type: "password" },
    { id: "birth_date", name: "Birth date", type: "date" },
];

const formBankFields = [
    { id: "cif", name: "CIF", label: "CIF", autoComplete: "cif" },
    { id: "bankData", name: "Bank data", label: "Your bank data", autoComplete: "bankData" }
];

const SellerRegistration = () => {
    const history = useHistory();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [formData, setFormData] = useState(getDefaultRegisterSellerModel());
    const [formErrors, setFormErrors] = useState({});
    const [showPassword, setShowPassword] = useState(false);

    const togglePasswordVisibility = () => {
        setShowPassword((prev) => !prev);
    };

    const isFormValid = () => {
        const isAnyFieldEmpty = [...formFields, ...formBankFields].some(field => !formData[field.id]);
        const isAnyFieldError = [...formFields, ...formBankFields].some(field => formErrors[field.id]);
        return !isAnyFieldEmpty && !isAnyFieldError;
    };

    const handleChange = (e) => {
        const { id, value } = e.target;
        let errors = { ...formErrors };
        if (id === 'email') {
            errors.email = validateEmail(value) ? '' : 'Please enter a valid email address. Example: "jhondoe214@gmail.com".';
        }
        if (id === 'password') {
            errors.password = validatePassword(value) ? '' : 'Password must be at least 8 characters long and include at least one letter, one number, and one special character.';
        }
        if (id === 'birth_date') {
            errors.birth_date = validateAge(value) ? '' : 'Please enter a valid birth date. Age must be between 0 and 100 years.';
        }
        if (id === 'cif') {
            const upperCaseValue = value.toUpperCase();
            errors.cif = validateCIF(upperCaseValue) ? '' : 'CIF must start with a letter (A-H, J, L, M, N, P, Q, R, S, U, V, W) followed by exactly 8 digits.';
            setFormData((prevData) => ({ ...prevData, [id]: upperCaseValue }));
        } else {
            setFormData((prevData) => ({ ...prevData, [id]: value }));
        }
        if (id === 'bankData') { 
            errors.bankData = validateBankData(value) ? '' : 'Bank data must be at least 10 characters long.';
        }
        setFormErrors(errors);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (isFormValid()) {
            try {
                console.log('Se esta intentando registrar un usuario Seller: ', formData)
                const userResponse = await registerUserSellerService(formData);
                console.log('Se a registrado un usuario Seller', userResponse)
                setOpenSnackbar(true);
                history.push("/");
            } catch (error) {
                console.error('Hubo un error al registrar al usuario:', error);
            }
        } else {
            console.log('El formulario no es válido.');
        }
    };

    return (
        <Container component="main" maxWidth="lg">
            <Paper elevation={3} sx={styles.paperContainer}>
                <Typography component="h1" variant="h5" color="#629c44" mb={2} textAlign="center">
                    Register
                </Typography>
                <Box component="form" onSubmit={handleSubmit} sx={styles.formContainer}>
                    <Grid container spacing={3}>
                        <Grid item xs={12} md={6}>
                            {formFields.map((field) => (
                                <Box key={field.id} mb={2}>
                                    <Typography variant="body2" sx={{ textAlign: 'left' }}>{field.name}</Typography>
                                    {field.id === 'password' ? (
                                        <TextField
                                            fullWidth
                                            required
                                            {...field}
                                            error={!!formErrors[field.id]}
                                            helperText={formErrors[field.id]}
                                            value={formData[field.id]}
                                            onChange={handleChange}
                                            type={showPassword ? 'text' : 'password'}
                                            InputProps={{
                                                endAdornment: (
                                                    <InputAdornment position="end">
                                                        <IconButton
                                                            aria-label="toggle password visibility"
                                                            onClick={togglePasswordVisibility}
                                                        >
                                                            {showPassword ? <VisibilityIcon /> : <VisibilityOffIcon />}
                                                        </IconButton>
                                                    </InputAdornment>
                                                ),
                                            }}
                                            sx={styles.textField}
                                        />
                                    ) : (
                                        <TextField
                                            fullWidth
                                            required
                                            {...field}
                                            error={!!formErrors[field.id]}
                                            helperText={formErrors[field.id]}
                                            value={formData[field.id]}
                                            onChange={handleChange}
                                            sx={styles.textField}
                                        />
                                    )}
                                </Box>
                            ))}
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <Paper elevation={3} sx={{ ...styles.paperContainer, backgroundColor: "#f2f2f7", padding: '16px' }}>
                                <Typography component="h2" variant="h6" mb={2}>
                                    Enter your bank information
                                </Typography>
                                {formBankFields.map((field) => (
                                    <Box key={field.id} mb={2}>
                                        <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                                            {field.name}
                                        </Typography>
                                        <TextField
                                            {...field}
                                            required
                                            fullWidth
                                            value={formData[field.id]}
                                            onChange={handleChange}
                                            error={!!formErrors[field.id]}
                                            helperText={formErrors[field.id]}
                                            sx={styles.textField}
                                            InputProps={{
                                                sx: styles.textfields
                                            }}
                                        />
                                    </Box>
                                ))}
                            </Paper>
                        </Grid>
                    </Grid>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ ...styles.registerButton, pointerEvents: isFormValid() ? "auto" : "none", opacity: isFormValid() ? 1 : 0.5 }}
                        disabled={!isFormValid()}
                    >
                        Register Seller
                    </Button>
                </Box>
            </Paper>
            <Snackbar
                open={openSnackbar}
                autoHideDuration={6000}
                onClose={() => setOpenSnackbar(false)}
                message="You have successfully registered."
            />
        </Container>
    );
};

export default SellerRegistration;
