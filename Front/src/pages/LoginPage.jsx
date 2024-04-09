import React, { useState } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Container,
  Grid,
  Paper,
  Link, 
} from "@mui/material";
import { useHistory } from "react-router-dom";
import TopBar from "../components/TopBar/TopBar";
import Footer from "../components/Footer/Footer";
import styles from "../styles/styles";
import img_mundo from "../images/img_mundo.png";

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    rememberMe: false,
  });

  const history = useHistory();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === "checkbox") {
      setFormData((prevData) => ({ ...prevData, [name]: checked }));
    } else {
      setFormData((prevData) => ({ ...prevData, [name]: value }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Lógica de envío aquí
  };

  const handleForgotPasswordClick = () => {
    history.push("/forgotPassword"); 
  };

  return (
    <Box sx={styles.mainBox}>
      <TopBar />
      <img
        src={img_mundo}
        alt="Login"
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
            Login
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
                  value={formData.email}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" style={{ color: "#232323", textAlign: "left" }}>
                  Password
                </Typography>
                <TextField
                  id="password"
                  name="password"
                  required
                  fullWidth
                  type="password"
                  autoComplete="current-password"
                  value={formData.password}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sx={{ display: "flex", justifyContent: "space-between" }}>
                <Link href="/forgotPassword" variant="body2" sx={{ color: "blue" }} onClick={handleForgotPasswordClick}>
                  Forgot Password
                </Link>
                <label style={{ display: "flex", alignItems: "center" }}>
                  <input
                    type="checkbox"
                    name="rememberMe"
                    checked={formData.rememberMe}
                    onChange={handleChange}
                  />
                  <Typography variant="body2" style={{ color: "#232323", textAlign: "left", marginLeft: "5px" }}>
                    Remember me
                  </Typography>
                </label>
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={styles.registerButton}
            >
              Login
            </Button>
          </Box>
        </Paper>
      </Container>
      <Footer />
    </Box>
  );
};

export default LoginPage;