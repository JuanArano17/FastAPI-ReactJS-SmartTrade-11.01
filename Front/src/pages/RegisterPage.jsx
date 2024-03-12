import React, { useState } from "react";
import TopBar from "../components/TopBar/TopBar";
import {
  Box,
  Typography,
  TextField,
  Button,
  Container,
  Grid,
} from "@mui/material";
import Footer from "../components/Footer/Footer";

const RegistrationForm = () => {
  const [formData, setFormData] = useState({
    firstName: "", lastName: "", email: "", password: "",  age: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    // lógica backend
  };

  return (
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      ><TopBar toggleSearchBar='False'/>
        <Container component="main" maxWidth="xs">
       <Typography component="h1" variant="h5" color="#629c44">
          Register
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="body2" color="232323">
                First Name
              </Typography>
              <TextField
                autoComplete="fname"
                name="firstName"
                required
                fullWidth
                id="firstName"
                label="Patricio"
                autoFocus
                value={formData.firstName}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="body2" color="232323">
                Last Name
              </Typography>
              <TextField
                required
                fullWidth
                id="lastName"
                label="Letelier"
                name="lastName"
                autoComplete="lname"
                value={formData.lastName}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="body2" color="232323">
                Email Address
              </Typography>
              <TextField
                required
                fullWidth
                id="email"
                label="letelier@upv.edu.es"
                name="email"
                autoComplete="email"
                value={formData.email}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="body2" color="232323">
                Password
              </Typography>
              <TextField
                required
                fullWidth
                name="password"
                label="PSW_curso_2023_2024"
                type="password"
                id="password"
                autoComplete="new-password"
                value={formData.password}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="body2" color="232323">
                Age
              </Typography>
              <TextField
                required
                fullWidth
                name="age"
                label="59"
                type="number"
                id="age"
                value={formData.age}
                onChange={handleChange}
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2, bgcolor: "#dfedd6", color: "#232323",
            boxShadow: "0px 4px 20px rgba(0, 0, 0, 0.2)",
            borderRadius: "10px",
            bordercolor:"232323"}}
          >
            Register
          </Button>
        </Box>
        </Container>
        <Footer style = {{ width: "100%" }}/>
      </Box>
    
  );
};

export default RegistrationForm;
