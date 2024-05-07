import React, { useState, useEffect } from 'react';
import { Box, Tab, Tabs, AppBar, Typography, Container, Paper } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import PersonalInfo from '../components/profile/personal-info/PersonalInfo';
import ShippingAddresses from '../components/profile/shipping-addresses/ShippingAddresses';
import Cards from '../components/profile/cards/Cards';
import styles from '../styles/styles';

const ProfilePage = () => {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  

  return (
    <Box sx={styles.mainBox}>
      <TopBar showLogoutButton={true} />
      <Container component="main" maxWidth="md" sx={styles.mainContainer}>
        <Paper elevation={3} sx={styles.paperContainer}>
          <Typography color="#629c44" variant="h4" gutterBottom>
            Profile Page
          </Typography>
          <AppBar position="static" color="default">
            <Tabs value={tabValue} onChange={handleTabChange} variant="fullWidth"aria-label="profile tabs">
              <Tab label="Personal Info" />
              <Tab label="Shipping Addresses" />
              <Tab label="Cards" />
            </Tabs>
          </AppBar>
          {tabValue === 0 && <PersonalInfo />}
          {tabValue === 1 && <ShippingAddresses />}
          {tabValue === 2 && <Cards />}
        </Paper>
      </Container>
      <Footer />
    </Box>
  );
};

export default ProfilePage;

