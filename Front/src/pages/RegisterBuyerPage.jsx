import React, { useState } from "react";
import { Box, Typography, TextField, Button, Container, Grid, Paper,IconButton, InputAdornment, } from "@mui/material";
import TopBar from "../components/TopBar/TopBar";
import Footer from "../components/Footer/Footer";
import styles from "../styles/styles";
import img_mundo from "../images/img_mundo.png";
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';

const formFields = [
  { id: "firstName", placeholder: "Patricio", name: "Name *", autoComplete: "fname", autoFocus: true },
  { id: "lastName", placeholder: "Letelier", name: "Surname *", autoComplete: "lname" },
  { id: "email", placeholder: "letelier@upv.edu.es", name: "Email *", autoComplete: "email" },
  { id: "dni", name: "DNI *", placeholder: "12345678A" },
  { id: "password", placeholder: "PSW_curso_2023_2024", name: "Password *", autoComplete: "new-password", type: "password" },
  { id: "age", name: "Date Of Birth *", type: "date"}
];

const RegisterPage = () => {
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

  const [isValidPassword, setIsValidPassword] = useState(false);
  const [isAllFieldsFilled, setIsAllFieldsFilled] = useState(false);
  const [dniError, setDniError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const validatePassword = (value) => {
    // Use regex to validate password requirements
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(value);
  };

  const validateDNI = (value) => {
    // Use regex to validate DNI format
    const dniRegex = /^\d{8}[A-Z]$/;
    return dniRegex.test(value);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "Name" || name === "Surname") {
      setFormData((prevData) => ({
        ...prevData,
        [name]: value.replace(/[^A-Za-z]/g, ""),
      }));
    } else if (name === "CVV" || name === "CardNumber") {
      setFormData((prevData) => ({
        ...prevData,
        [name]: value.replace(/\D/g, ""),
      }));
    } else if (name === "DNI") {
      const formattedDNI = value.replace(/[^A-Za-z0-9]/g, "");
      setFormData((prevData) => ({
        ...prevData,
        [name]: formattedDNI.slice(0, -1) + formattedDNI.slice(-1),
      }));
      if (!validateDNI(formattedDNI)) {
        setDniError("Invalid DNI format");
      } else {
        setDniError("");
      }
    } else if (name === "ExpiryDate") {
      let formattedDate = value
        .slice(0, 5)
        .replace(/(\d{2})(\d{2})/, "$1/$2");
      if (value.length === 2 && !value.includes("/")) {
        formattedDate += "/";
      }
      setFormData((prevData) => ({
        ...prevData,
        [name]: formattedDate,
      }));
    } else if (name === "Password") {
      setFormData((prevData) => ({
        ...prevData,
        [name]: value,
      }));
      setIsValidPassword(validatePassword(value));
    } else {
      setFormData((prevData) => ({ ...prevData, [name]: value }));
    }

    const requiredFields = ["firstName", "lastName", "email", "dni", "password", "age"];
    const isFilled = requiredFields.every((field) => formData[field]);
    setIsAllFieldsFilled(isFilled);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Logic for communicating with backend
  };

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  return (
    <Box sx={styles.mainBox}>
      <TopBar />
      <img src={img_mundo} style={styles.rounded_img} />
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
                        error={field.name === 'DNI' && dniError !== ""}
                        helperText={field.name === 'DNI' && dniError}
                        type={showPassword ? 'text' : 'password'} // Mostrar contraseña si showPassword es true
                        InputProps={{ // Agregar icono de ojo para mostrar/ocultar contraseña
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
                        error={field.name === 'DNI' && dniError !== ""}
                        helperText={field.name === 'DNI' && dniError}
                      />
                    )}
                  </Grid>
                ))}
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={styles.registerButton}
                  mt={4}
                  //tengo que arreglarlo disabled={!isAllFieldsFilled || !isValidPassword}
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
                        Card Number*
                      </Typography>
                      <TextField
                        id="CardNumber"
                        name="CardNumber *"
                        placeholder="1234-1234-1234-1234"
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
                        Date of expiry *
                      </Typography>
                      <TextField
                        id="ExpiryDate"
                        name="ExpiryDate"
                        placeholder="09/26"
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
                        CVV*
                      </Typography>
                      <TextField
                        id="CVV"
                        name="CVV *"
                        placeholder="123"
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
                    mt={4}
                  >
                    Save
                  </Button>
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </Paper>
      </Container>
      <Footer />
    </Box>
  );
};

export default RegisterPage;

