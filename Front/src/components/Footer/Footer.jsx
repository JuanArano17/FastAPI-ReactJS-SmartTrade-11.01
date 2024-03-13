import React from "react";
import { Box, Container, Typography, Link, Grid } from "@mui/material";

const Footer = ({style}) => {
    const currentYear = new Date().getFullYear();
    return (
        <Box component="footer" sx={{ bgcolor: "#cbe8ba", py: 6}}>
            <Container maxWidth="lg">
                <Grid container spacing={4} justifyContent="center">
                    <Typography color="#444444" gutterBottom sx={{ fontSize: '16px', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center' }}>
                        <Link href="#" color="inherit" sx={{ mr: 3 }}>Features</Link>
                        |
                        <Link href="#" color="inherit" sx={{ mx: 3 }}>About</Link>
                        |
                        <Link href="#" color="inherit" sx={{ mx: 3 }}>Testimonials</Link>
                        |
                        <Link href="#" color="inherit" sx={{ mx: 3 }}>Contact</Link>
                        |
                        <Link href="#" color="inherit" sx={{ ml: 3 }}>Download</Link>
                    </Typography>
                </Grid>
                <Typography variant="body2" color="textSecondary" align="center" sx={{ color: "#444444", mt: 2 }}>
                    Cami de Vera, Algiros, CA 46022, Valencia - ESP
                </Typography>
                <Typography variant="body2" color="textSecondary" align="center" sx={{ color: "#444444", mt: 1 }}>
                    {"© "}
                    {`Smart Trade ${currentYear}.`}
                </Typography>
            </Container>
        </Box>
    );
};

export default Footer;
