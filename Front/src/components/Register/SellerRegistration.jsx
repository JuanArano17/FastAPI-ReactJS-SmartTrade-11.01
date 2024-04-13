import React, { useState } from "react";
import { useHistory } from 'react-router-dom';
import { Box, Typography, TextField, Button, Container, Grid, Paper, IconButton, InputAdornment, Snackbar} from "@mui/material";
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
    { id: "age", name: "Birth date", type: "date" },
];
const formBankFields = [
    { id: "cif", name: "CIF", label: "CIF", autoComplete: "cif" },
    { id: "bankData", name: "Bank data", label: "your bank data", autoComplete: "cif" }
]
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
        const isAnyFieldEmpty = formFields.some(field => !formData[field.id]);
        const isAnyFieldError = formFields.some(field => formErrors[field.id]);
        return !isAnyFieldEmpty && !isAnyFieldError;
    };
    const handleChange = (e) => {
        const { id, value } = e.target;
        let errors = { ...formErrors };
        if (id === 'email') {
            errors.email = validateEmail(value) ? '' : 'Email is not valid!';
        }
        if (id === 'password') {
            errors.password = validatePassword(value) ? '' : 'Password does not meet criteria!';
        }
        if (id === 'age') {
            errors.age = validateAge(value) ? '' : 'Age is not valid!';
        }
        if (id === 'cif') {
            errors.cif = validateCIF(value) ? '' : 'CIF is not valid!';
        }
        if (id === 'bankData') {
            errors.bankData = validateBankData(value) ? '' : 'Bank data must be at least 10 caracrers long!';
        }
        setFormErrors(errors);
        setFormData((prevData) => ({ ...prevData, [id]: value }));
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (isFormValid()) {
            try {
                console.log('Se esta intentando registrar un usuario Seller: ', formData)
                const userResponse = await registerUserSellerService(formData);
                console.log('Se a registrado un usuario Seller', userResponse)
                setOpenSnackbar(true);
                setTimeout(() => {
                    history.push("/");
                }, 2000);
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
                                            value={formData[field.name]}
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
                                            value={formData[field.name]}
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
                                            value={formData[field.name]}
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
                        sx={styles.registerButton}
                    >
                        Register Seller
                    </Button>
                </Box>
            </Paper>
            <Snackbar
                open={openSnackbar}
                autoHideDuration={6000}
                onClose={() => setOpenSnackbar(false)}
                message="Te has registrado con éxito."
            />
        </Container>
    );
};
export default SellerRegistration;