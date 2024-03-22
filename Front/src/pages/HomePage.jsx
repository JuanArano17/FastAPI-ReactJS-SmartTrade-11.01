import React from "react";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Footer from "../components/Footer/Footer";
import TopBar from "../components/TopBar/TopBar";
import styles from "../styles/styles";

const HomePage = () => {
    return (
        <Box sx={styles.mainBox}>
            <TopBar />
            <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
                <Grid container spacing={3} alignItems="center" justifyContent="center">
                    <Grid item xs={12} md={8}>
                        <Typography variant="h3" align="center" gutterBottom color="#629c44">
                            Welcome to Smart Trade
                        </Typography>
                        <Typography
                            variant="h6"
                            align="center"
                            color="textSecondary"
                            paragraph
                        >
                            Líder en ventas ecológicas mundial.
                        </Typography>
                    </Grid>
                    <Box
                        borderRadius={25}
                        component="img"
                        sx={{
                            height: 233,
                            width: 350,
                            maxHeight: { xs: 233, md: 167 },
                            maxWidth: { xs: 350, md: 250 },
                        }}
                        alt="Eco friendly"
                        src={`${process.env.PUBLIC_URL}/images/EcoWorld.png`}
                    />
                </Grid>
            </Container>
            <Footer />
        </Box>
    );
};

export default HomePage;
