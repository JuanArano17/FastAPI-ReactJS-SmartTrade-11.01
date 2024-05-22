import React from 'react';
import { Box, Container, Typography, Grid } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import styles from '../styles/styles';
import tutorialData from '../utils/tutorialData';
import TutorialSection from '../components/tutorials/TutorialSection';

const TutorialPage = () => {
    return (
        <Box sx={styles.mainBox}>
            <TopBar showSearchBar={false} showLogoutButton={true} />
            <Container sx={styles.mainContainer}>
                <Typography variant="h3" align="center" gutterBottom sx={{ color: '#629C44' }}>
                    Tutorial de la Aplicación
                </Typography>
                <Grid container spacing={4}>
                    {tutorialData.map((section, index) => (
                        <Grid item xs={12} key={index}>
                            <TutorialSection section={section} />
                        </Grid>
                    ))}
                </Grid>
            </Container>
            <Footer />
        </Box>
    );
};

export default TutorialPage;
