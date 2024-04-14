import React, { useState } from "react";
import { Box, Typography, TextField, Button, Container, Paper } from "@mui/material";
import TopBar from "../components/topbar/TopBar";
import Footer from "../components/footer/Footer";
import styles from "../styles/styles";
import { validateEmail } from "../utils/registerFormValidations"; 
import img_mundo from "../images/img_mundo.png";

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState(""); 

  const handleChange = (e) => {
    const { value } = e.target;
    setEmail(value);
    if (!validateEmail(value)) {
      setError("El email no es válido.");
    } else {
      setError(""); 
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateEmail(email)) {
      // Lógica para enviar el correo electrónico de recuperación de contraseña
      console.log("Email enviado para recuperar contraseña.");
    } else {
      setError("Por favor ingrese un email válido para continuar.");
    }
  };

  return (
    <Box sx={styles.mainBox}>
      <TopBar />
      <img
        src={img_mundo}
        alt="Forgot Password"
        style={{
          width: "200px",
          height: "auto",
          marginTop: "40px",
          marginBottom: "20px",
          margin: "0 auto",
          borderRadius: "50%",
          boxShadow: "0px 4px 20px rgba(0, 0, 0, 0.2)"
        }}
      />
      <Container component="main" maxWidth="xs" sx={styles.mainContainer}>
        <Paper elevation={3} sx={styles.paperContainer}>
          <Typography component="h1" variant="h5" sx={styles.headerText}>
            Forgot Password?
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={styles.formContainer}>
            <TextField
              id="email"
              label="Email"
              type="email"
              fullWidth
              autoComplete="email"
              value={email}
              onChange={handleChange}
              error={!!error}
              helperText={error}
              required
              sx={{ marginBottom: '20px' }}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={!email || !!error}
              sx={styles.registerButton}
            >
              Send Email
            </Button>
          </Box>
        </Paper>
      </Container>
      <Footer />
    </Box>
  );
};

export default ForgotPasswordPage;
