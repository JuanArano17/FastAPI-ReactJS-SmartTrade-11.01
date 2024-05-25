import React, { useState } from "react";
import { Box, Typography, TextField, Button, Container, Grid, Paper, Link, IconButton, InputAdornment } from "@mui/material";
import { useHistory } from "react-router-dom";
import { loginUserService } from "../api/services/user/AuthService";
import TopBar from "../components/topbar/TopBar";
import Footer from "../components/footer/Footer";
import styles from "../styles/styles";
import img_mundo from "../images/img_mundo.png";
import { validateEmail, validatePassword } from "../utils/registerFormValidations";
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';

const LoginPage = () => {
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    rememberMe: false,
  });
  const [showPassword, setShowPassword] = useState(false);
  const history = useHistory();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === "checkbox") {
      setFormData((prevData) => ({ ...prevData, [name]: checked }));
    } else {
      setFormData((prevData) => ({ ...prevData, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      console.log('Se esta intentando loguear un usuario: ', formData);
      const userResponse = await loginUserService(formData);
      console.log('Se ha logueado un usuario', userResponse);
      history.push("/catalog");
    } catch (error) {
      console.error('Hubo un error al intentar loguear al usuario:', error);
      const errorMessage = error.response && error.response.data && error.response.data.detail
        ? error.response.data.detail
        : 'An unexpected error occurred';
      setError(errorMessage);
    }
  };

  const handleForgotPasswordClick = () => {
    history.push("/forgotPassword");
  };

  const isEmailValid = validateEmail(formData.email);
  const isPasswordValid = validatePassword(formData.password);
  const isFormValid = formData.email !== "" && formData.password !== "" && isEmailValid && isPasswordValid;

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
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
                {error && (
                  <Typography color="error" style={{ textAlign: "center" }}>
                    {error}
                  </Typography>
                )}
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
                  error={!isEmailValid}
                  helperText={!isEmailValid ? 'Please enter a valid email address. Example: "jhondoe214@gmail.com".' : ''}
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
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  value={formData.password}
                  onChange={handleChange}
                  error={!isPasswordValid}
                  helperText={!isPasswordValid ? 'Password must be at least 8 characters long and include at least one letter, one number, and one special character.' : ''}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={togglePasswordVisibility}
                          edge="end"
                        >
                          {showPassword ? <VisibilityIcon /> : <VisibilityOffIcon />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
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
              sx={{ ...styles.registerButton, pointerEvents: isFormValid ? "auto" : "none", opacity: isFormValid ? 1 : 0.5 }}
              disabled={!isFormValid}
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