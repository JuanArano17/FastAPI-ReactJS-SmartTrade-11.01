import React, { useEffect } from 'react';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Footer from '../components/footer/Footer';
import TopBar from '../components/topbar/TopBar';
import styles from '../styles/styles';
import { useHistory } from 'react-router-dom';
import { Button, IconButton } from '@mui/material';
import StarBorder from '@mui/icons-material/StarBorder';

const HomePage = () => {
    const history = useHistory();

    return (
        <Box sx={{ ...styles.mainBox, backgroundColor: '#f0f0f0' }}>
            <TopBar />
            <Container component="main" sx={{ padding: 4, maxWidth: '100%' }}>
                <Grid container spacing={3} alignItems="center" justifyContent="center" style={{ minHeight: '80vh' }}>
                    <Grid item xs={12} md={6} lg={4} >
                        <Typography variant="h3" align="center" gutterBottom sx={{ color: '#629C44' }}>
                            Welcome to Smart Trade
                        </Typography>
                        <Typography variant="h6" align="center" color="textSecondary" paragraph>
                            Líder en ventas ecológicas mundial.
                        </Typography>
                    </Grid>
                    <Grid item xs={12} md={6} lg={4}>
                        <Box
                            borderRadius={25}
                            component="img"
                            sx={{
                                height: 'auto',
                                width: '100%',
                                maxWidth: { xs: 350, md: 500 },
                                boxShadow: 10
                            }}
                            alt="Eco friendly"
                            src={`${process.env.PUBLIC_URL}/images/EcoWorld.png`}
                        />
                    </Grid>
                </Grid>
            </Container>
            <Footer />
        </Box>
    );
};

export default HomePage;
