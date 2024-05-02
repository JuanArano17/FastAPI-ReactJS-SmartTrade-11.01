import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Container, Typography, Grid, Button, Paper, Divider, CircularProgress, Rating, ButtonBase } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import styles from '../styles/styles';
import { getProductSellerById } from '../api/services/products/ProductsService';
import { addCartItem } from '../api/services/products/ShoppingCartService';
import FavoriteButton from '../components/favorite-button/FavoriteButton';

const ProductDetailPage = () => {
    const { id } = useParams();
    const [productData, setProductData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [imageIndex, setImageIndex] = useState(0);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const response = await getProductSellerById(id);
                console.log(response.data)
                if (response) {
                    setProductData(response);
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

    const handleAddToCart = async () => {
        const quantity = 1;
        try {
            await addCartItem(productData.id, quantity);
            console.log('Producto añadido al carrito');
        } catch (error) {
            console.error('Error al añadir producto al carrito', error);
        }
    };
    const renderAdditionalAttributes = (productData) => {
        const commonAttributes = ['name', 'description', 'eco_points', 'id_product', 'id_seller', 'spec_sheet', 'stock', 'id', 'images', 'seller_products'];
        return Object.keys(productData)
            .filter(key => !commonAttributes.includes(key))
            .map(key => (
                <Paper key={key} elevation={1} sx={{ margin: '10px 0', padding: '10px' }}>
                    <Typography variant="body2" color="text.secondary" component="span">
                        {`${key.charAt(0).toUpperCase() + key.slice(1)}: `}
                    </Typography>
                    <Typography variant="body2" component="span" sx={{ fontWeight: 'bold' }}>
                        {productData[key]}
                    </Typography>
                </Paper>
            ));
    };

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return <Typography color="error">{error}</Typography>;
    }
    const handleImageChange = (newIndex) => {
        setImageIndex(newIndex);
    };
    return (
        <Box sx={styles.mainBox}>
            <TopBar showSearchBar={true} showLogoutButton={true} />
            <Container sx={styles.mainContainer}>
                {productData && (
                    <Paper elevation={3} sx={{ ...styles.paperContainer, position: 'relative' }}>
                        <FavoriteButton productId={productData.id} ></FavoriteButton>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={5} sx={{ display: 'flex', justifyContent: 'center' }}>
                                <Box sx={{ width: '100%', height: 300, display: 'flex', justifyContent: 'center', alignItems: 'center', overflow: 'hidden' }}>
                                    <ButtonBase onClick={() => handleImageChange((imageIndex + 1) % productData.images.length)} disabled={productData.images.length <= 1}>
                                        <img
                                            src={productData.images[imageIndex]}
                                            alt={`Image ${imageIndex + 1} of ${productData.name}`}
                                            style={{ maxWidth: '100%', maxHeight: '100%', width: 'auto', height: 'auto' }}
                                        />
                                    </ButtonBase>
                                </Box>
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
                                    Precio: ${productData.price}
                                </Typography>
                                <Button variant="contained" sx={{ mb: 2 }} onClick={handleAddToCart}>
                                    Add to Cart
                                </Button>
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
