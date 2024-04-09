import React, { useState } from "react";
import { Box, Typography, TextField, Button, Container, Grid, Paper } from "@mui/material";
import TopBar from "../components/topbar/TopBar";
import Footer from "../components/footer/Footer";
import styles from "../styles/styles";
import img_mundo from "../images/img_mundo.png";

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState("");
  
  const handleChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Lógica para enviar el correo electrónico de recuperación de contraseña
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
          boxShadow: "0px 4px 20px rgba(0, 0, 0, 0.2)",
        }}
      />
      <Container component="main" maxWidth="xs" sx={styles.mainContainer}>
        <Paper elevation={3} sx={styles.paperContainer}>
          <Typography component="h1" variant="h5" sx={styles.headerText}>
            Forgot Password?
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={styles.formContainer}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Typography variant="body2" style={{ color: "#232323", textAlign: "left" }}>
                  Email
                </Typography>
                <TextField
                  id="email"
                  name="email"
                  required
                  fullWidth
                  autoComplete="email"
                  value={email}
                  onChange={handleChange}
                />
              </Grid>
            </Grid>
            <Button
              type="submit" fullWidth variant="contained" sx={styles.registerButton}
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
