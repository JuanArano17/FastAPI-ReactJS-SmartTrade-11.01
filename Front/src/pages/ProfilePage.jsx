import React, { useState, useEffect } from 'react';
import { Box, Tab, Tabs, AppBar, Typography, Container, Paper } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import PersonalInfo from '../components/profile/personal-info/PersonalInfo';
import ShippingAddresses from '../components/profile/shipping-addresses/ShippingAddresses';
import Cards from '../components/profile/cards/Cards';
import styles from '../styles/styles';
import { myInfoService } from '../api/services/user/AuthService';

const ProfilePage = () => {
  const [tabValue, setTabValue] = useState(0);
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    myInfoService()
      .then(data => {
        setUserInfo(data);
      })
      .catch(error => {
        console.error('Error fetching user info', error);
      });
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const renderTabs = () => {
    const tabs = [<Tab key="personal-info" label="Personal Info" />];
    if (userInfo && userInfo.type === 'Buyer') {
      tabs.push(<Tab key="shipping-addresses" label="Shipping Addresses" />);
      tabs.push(<Tab key="cards" label="Cards" />);
    }
    return tabs;
  };

  return (
    <Box sx={styles.mainBox}>
      <TopBar showLogoutButton={true} />
      <Container component="main" maxWidth="md" sx={styles.mainContainer}>
        <Paper elevation={3} sx={styles.profilePagePaperContainer}>
          <Typography color="#629c44" variant="h4" gutterBottom>
            Profile Page
          </Typography>
          <AppBar position="static" color="default" sx={{ borderRadius:'40px', backgroundColor: 'white', color: 'black' }}>
            <Tabs value={tabValue} onChange={handleTabChange} variant="fullWidth" aria-label="profile tabs" 
                  sx={{ 
                    '.MuiTabs-indicator': { backgroundColor: '#4d9e20' },  
                    '.Mui-selected': { color: '#000' } 
                  }}>
              {renderTabs()}
            </Tabs>
          </AppBar>
          {tabValue === 0 && <PersonalInfo />}
          {userInfo && userInfo.type === 'Buyer' && (
            <>
              {tabValue === 1 && <ShippingAddresses />}
              {tabValue === 2 && <Cards />}
            </>
          )}
        </Paper>
      </Container>
      <Footer />
    </Box>
  );
};

export default ProfilePage;
