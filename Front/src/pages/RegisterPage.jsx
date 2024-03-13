import React, { useState } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Container,
  Grid,
  Paper,
} from "@mui/material";
import TopBar from "../components/TopBar/TopBar";
import Footer from "../components/Footer/Footer";
import styles from "../styles/styles";
import img_mundo from "../images/img_mundo.png";

const formFields = [
  { id: "firstName", label: "Patricio", name: "Name", autoComplete: "fname", autoFocus: true },
  { id: "lastName", label: "Letelier", name: "Surname", autoComplete: "lname" },
  { id: "email", label: "letelier@upv.edu.es", name: "Email", autoComplete: "email" },
  { id: "password", label: "PSW_curso_2023_2024", name: "Password", autoComplete: "new-password", type: "password" },
  { id: "age", name: "Date Of Birth", type: "date" },
];

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    dateOfBirth: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Lógica comunicación con backend
  };

  return (
    <Box sx={styles.mainContainer}>
      <TopBar toggleSearchBar="False" />
      <img
        src={img_mundo}
        alt="Example"
        style={{
          width: "200px",
          height: "auto",
          marginTop:"20px",
          marginBottom: "20px",
          margin: "0 auto",
          borderRadius: "50%",
          boxShadow: "0px 4px 20px rgba(0, 0, 0, 0.2)",
        }}
      />
      <Container component="main" maxWidth="xs">
        <Paper elevation={3} sx={styles.paperContainer}>
          <Typography component="h1" variant="h5" color="#629c44">
            Register
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={styles.formContainer}>
            <Grid container spacing={2}>
              {formFields.map((field) => (
                <Grid item xs={12} key={field.id}>
                  <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                    {field.name}
                  </Typography>
                  <TextField
                    {...field}
                    required
                    fullWidth
                    value={formData[field.name]}
                    onChange={handleChange}
                  />
                </Grid>
              ))}
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={styles.registerButton}
            >
              Register
            </Button>
          </Box>
        </Paper>
      </Container>
      <Footer />
    </Box>
  );
};

export default RegisterPage;
