import React, { useState } from "react";
import { useHistory } from 'react-router-dom';
import { Box, Typography, TextField, Button, Container, Grid, Paper, IconButton, InputAdornment, Snackbar } from "@mui/material";
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import { getDefaultRegisterBuyerModel } from "../../models/RegisterBuyerModel";
import { getDefaultCardInformationModel } from "../../models/CardInformationModel";
import { validateEmail, validatePassword, validateAge, validateDNI } from "../../utils/registerFormValidations";
import styles from "../../styles/styles";
import { registerUserBuyerService } from "../../api/services/user/AuthService";
import registerCardService from "../../api/services/user/BuyerService";
import CardInformationForm from "./cardInfo/CardInformationForm";

const formFields = [
    { id: "name", name: "Name", placeholder: "Patricio*", autoComplete: "fname", autoFocus: true },
    { id: "surname", name: "Surname", placeholder: "Letelier*", autoComplete: "lname" },
    { id: "email", name: "Email", placeholder: "letelier@upv.edu.es*", autoComplete: "email" },
    { id: "dni", name: "DNI", placeholder: "12345678A*" },
    { id: "password", name: "Password", placeholder: "PSW_curso_2023_2024*", autoComplete: "new-password", type: "password" },
    { id: "billing_address", name: "Billing Address", placeholder: "Calle nueva 123", autoComplete:""},
    { id: "birth_date", name: "Birth date", type: "date" }
];

const BuyerRegistration = () => {
    const history = useHistory();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [formData, setFormData] = useState(getDefaultRegisterBuyerModel());
    const [cardData, setCardData] = useState(getDefaultCardInformationModel());
    const [showPassword, setShowPassword] = useState(false);
    const [formErrors, setFormErrors] = useState({});
    const [isCardFormValid, setCardFormValidity] = useState(false);
    const [showCardForm, setShowCardForm] = useState(false);

    const togglePasswordVisibility = () => {
        setShowPassword((prev) => !prev);
    };

    const handleCardChange = (e) => {
        const { name, value } = e.target;
        setCardData(prevCardData => ({ ...prevCardData, [name]: value }));
    };

    const isFormValid = () => {
        const isAnyFieldEmpty = formFields.some(field => !formData[field.id]);
        const isAnyFieldError = formFields.some(field => formErrors[field.id]);
        const isBirthDateValid = validateAge(formData.birth_date);
        const isRegisterFormValid = !isAnyFieldEmpty && !isAnyFieldError && isBirthDateValid;
        return isRegisterFormValid && (!showCardForm || isCardFormValid);
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
        if (id === 'dni') {
            errors.dni = validateDNI(value) ? '' : 'DNI must contain exactly 8 numbers followed by a letter. Example: "12345678A".';
        }
        setFormErrors(errors);
        setFormData({ ...formData, [id]: value });
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (isFormValid()) {
            try {
                console.log('Se esta intentando registrar un usuario Buyer: ', formData);
                const userResponse = await registerUserBuyerService(formData);
                console.log('Se ha registrado un usuario Buyer', userResponse);
                setOpenSnackbar(true);
                const userId = userResponse.id;
                console.log('UserIDBeforeRegisterService: ', userId);
                if (userId && showCardForm && Object.values(cardData).some(value => value !== "")) {
                    try {
                        await registerCardService({...cardData}, userId);
                    } catch (cardError) {
                        console.error('Hubo un error al registrar la tarjeta:', cardError);
                    }
                }
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
                                            fullWidth
                                            variant="outlined"
                                            error={!!formErrors[field.id]}
                                            helperText={formErrors[field.id]}
                                            onChange={handleChange}
                                            sx={styles.textfields}
                                            value={formData[field.id]}
                                            type={showPassword ? 'text' : 'password'}
                                            InputProps={{
                                                endAdornment: (
                                                    <InputAdornment position="end">
                                                        <IconButton
                                                            aria-label="toggle password visibility"
                                                            onClick={togglePasswordVisibility}
                                                            edge="end"
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
                                            fullWidth
                                            variant="outlined"
                                            error={!!formErrors[field.id]}
                                            helperText={formErrors[field.id]}
                                            onChange={handleChange}
                                            sx={styles.textfields}
                                            value={formData[field.id]}
                                        />
                                    )}
                                </Grid>
                            ))}
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={styles.registerButton}
                                disabled={!isFormValid()}
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
                            <Button
                                variant="outlined"
                                onClick={() => setShowCardForm(!showCardForm)}
                                sx={styles.greenRoundedButton}
                            >
                                {showCardForm ? "Hide Card Information" : "Add Card Information"}
                            </Button>
                            {showCardForm && (
                                <CardInformationForm cardData={cardData} handleChange={handleCardChange} setCardFormValidity={setCardFormValidity} />
                            )}
                        </Paper>
                    </Grid>
                </Grid>
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

export default BuyerRegistration;
