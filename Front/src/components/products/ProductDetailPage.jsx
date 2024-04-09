// ProductDetailPage.jsx
import React, { useState } from 'react';
import { Box, Container, Typography, Grid, Button, Paper, Divider, IconButton } from '@mui/material';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarIcon from '@mui/icons-material/Star';
import TopBar from '../TopBar/TopBar';
import Footer from '../Footer/Footer';
import styles from '../../styles/styles';

const ProductDetailPage = () => {
    const [isFavorite, setIsFavorite] = useState(false);

    const handleFavoriteClick = () => {
        setIsFavorite(!isFavorite);
    };

    // Asumiremos que estos datos vendrán de la API o de un componente padre
    const productData = {
        brand: {
            name: "Product Brand",
            logo: "/path/to/logo.jpg", // Asumiendo que tienes una imagen para el logo
        },
        name: "Product Name",
        description: "Product description",
        price: "PRICE $$$",
        characteristics: [
            { label: "Height", value: "10cm" },
            { label: "Width", value: "5cm" },
            // Más características...
        ],
        similarProducts: [/* array of similar products data */],
    };

    return (
        <Box sx={styles.mainBox}>
            <TopBar showSearchBar={true} showLogoutButton={true} />


            <Container component="main" sx={styles.mainContainer}>
                <Paper elevation={3} sx={styles.paperContainer}>
                    <Box sx={{ position: 'relative', padding: 2 }}>
                        <IconButton onClick={handleFavoriteClick} sx={{ position: 'absolute', top: 0, right: 0 }}>
                            {isFavorite ? <StarIcon sx={{ color: "#ffcc00" }} /> : <StarBorderIcon />}
                        </IconButton>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <img src={productData.brand.logo} alt={`${productData.brand.name} Logo`} style={{ width: '50px', height: '50px' }} />
                            <Typography variant="h6" sx={styles.headerText}>{productData.brand.name}</Typography>
                        </Box>
                        <Divider sx={styles.ThickDivider} />
                        <Grid container spacing={3}>
                            {/* Imagen y descripción general del Producto */}
                            <Grid item xs={12} md={6}>
                                {/* Componente para la galería de imágenes */}
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <Typography variant="h5" sx={styles.headerText}>
                                    {productData.name}
                                </Typography>
                                <Typography paragraph>
                                    {productData.description}
                                </Typography>
                                <Typography variant="h4" sx={{ mb: 2 }}>
                                    {productData.price}
                                </Typography>
                                <Button variant="contained" sx={styles.registerButton}>
                                    Add to Cart
                                </Button>
                            </Grid>
                        </Grid>
                        <Divider sx={styles.ThickDivider} />
                        <Typography variant="h6" sx={styles.headerText}>Product Characteristics</Typography>
                        {/* Características del Producto */}
                        <Divider sx={styles.ThickDivider} />
                        <Typography variant="h6" sx={styles.headerText}>Similar Products</Typography>
                        {/* Productos Similares */}
                    </Box>
                </Paper>
            </Container>
            <Footer />
        </Box>
    );
};

export default ProductDetailPage;
