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
    CardNumber: "",
    ExpiryDate: "",
    CVV: "",
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
                    <TextField
                      {...field}
                      required
                      fullWidth
                      value={formData[field.name]}
                      onChange={handleChange}
                      sx={styles.textfields}
                    />
                  </Grid>
                ))}
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={styles.registerButton}
                  mt={4}
                >
                  Register
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
                        required
                        fullWidth
                        value={formData.CardNumber}
                        onChange={handleChange}
                        sx={{...styles.textfields, backgroundColor: "white"}}
                      />
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                        Date-of-expiry
                      </Typography>
                      <TextField
                        id="ExpiryDate"
                        name="ExpiryDate"
                        required
                        fullWidth
                        type = "month"
                        value={formData.ExpiryDate}
                        onChange={handleChange}
                        sx={{...styles.textfields, backgroundColor: "white"}}
                      />
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="232323" sx={{ textAlign: 'left' }}>
                        CVV
                      </Typography>
                      <TextField
                        id="CVV"
                        name="CVV"
                        required
                        fullWidth
                        value={formData.CVV}
                        onChange={handleChange}
                        inputProps={{ maxLength: 3 }}
                        sx={{...styles.textfields, backgroundColor: "white"}}
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
