import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Container, Typography, Grid, Button, Paper, Divider, IconButton, CircularProgress, Stack, Rating } from '@mui/material';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarIcon from '@mui/icons-material/Star';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import styles from '../styles/styles';
import { getProduct  } from '../api/services/products/ProductsService';


const ProductDetailPage = () => {
    const { id } = useParams();
    const [productData, setProductData] = useState(null);
    const [isFavorite, setIsFavorite] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const response = await getProduct(id);
    
                if (response) {
                    setProductData(response.product);

                    setLoading(false);
                    setError(null);
    
                }
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };
        fetchProducts();
    }, [id]);
    



    const handleFavoriteClick = () => {
        setIsFavorite(!isFavorite);
    };

    const renderAdditionalAttributes = (productData) => {
        const commonAttributes = ['name', 'description', 'eco_points', 'spec_sheet', 'stock', 'id', 'images', 'seller_products'];
        return Object.keys(productData)
            .filter(key => !commonAttributes.includes(key))
            .map(key => (
                <Typography variant="body2" key={key}>
                    {key.charAt(0).toUpperCase() + key.slice(1)}: {productData[key]}
                </Typography>
            ));
    };

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return <Typography color="error">{error}</Typography>;
    }
    return (
        <Box sx={styles.mainBox}>
            <TopBar showSearchBar={true} showLogoutButton={true} />
            <Container sx={styles.mainContainer}>
                {productData && (
                    <Paper elevation={3} sx={{ ...styles.paperContainer, position: 'relative' }}>
                        <IconButton
                            onClick={handleFavoriteClick}
                            sx={{ position: 'absolute', top: 8, right: 8, backgroundColor: 'background.paper', borderRadius: '50%' }}
                        >
                            {isFavorite ? <StarIcon sx={{ color: "#ffcc00" }} /> : <StarBorderIcon />}
                        </IconButton>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={5} sx={{ display: 'flex', justifyContent: 'center' }}>
                                <img
                                    src={productData.images.length > 0 ? productData.images[0].url : '/path/to/default.jpg'}
                                    alt={productData.name}
                                    style={styles.imageStyle}
                                />
                            </Grid>
                            <Grid item xs={12} md={7}>
                                <Typography variant="h6" color="text.secondary">
                                    {productData.brand}
                                </Typography>
                                <Typography variant="h4" sx={{ mb: 2, fontWeight: 'bold' }}>
                                    {productData.name}
                                </Typography>
                                <Rating name="read-only" value={4} readOnly />
                                <Typography sx={{ mt: 2 }}>{productData.description}</Typography>
                                <Typography variant="h5" sx={{ my: 2 }}>
                                    Precio: ${productData.seller_products.length > 0 ? productData.seller_products[0].price : "Consultar"}
                                </Typography>
                                <Button variant="contained" sx={{ mb: 2 }}>
                                    Add to Cart
                                </Button>
                                <IconButton
                                    onClick={handleFavoriteClick}
                                    sx={{ position: 'absolute', top: 8, right: 8 }}
                                >
                                    {isFavorite ? <StarIcon sx={{ color: "#ffcc00" }} /> : <StarBorderIcon />}
                                </IconButton>
                            </Grid>
                        </Grid>
                        <Divider sx={styles.ThickDivider}></Divider>
                        <Box sx={{ textAlign: 'left' }}>
                            <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                Product characteristics
                            </Typography>
                            {renderAdditionalAttributes(productData)}
                        </Box>
                        <Divider sx={styles.ThickDivider}></Divider>
                        <Box sx={{ textAlign: 'left' }}>
                            <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                Similar Products
                            </Typography>
                        </Box>
                    </Paper>
                )}
            </Container>
            <Footer />
        </Box>
    );
};

export default ProductDetailPage;
