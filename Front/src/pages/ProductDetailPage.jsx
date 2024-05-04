import React, { useState, useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import { Box, Container, Typography, Grid, Button, Paper, Divider, CircularProgress, Rating, ButtonBase, IconButton } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import styles from '../styles/styles';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { getProductSellerById } from '../api/services/products/ProductsService';
import { addCartItem } from '../api/services/products/ShoppingCartService';
import FavoriteButton from '../components/favorite-button/FavoriteButton';

const ProductDetailPage = () => {
    const { id } = useParams();
    const [productData, setProductData] = useState(null);
    const [selectedSize, setSelectedSize] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [imageIndex, setImageIndex] = useState(0);
    const history = useHistory();

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const response = await getProductSellerById(id);
                console.log("Product by id: ", response);
                if (response) {
                    setProductData(response);
                    if (response.sizes && response.sizes.length > 0) {
                        setSelectedSize(response.sizes[0].size); // Default to first size
                    }
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

    const handleBackToCatalog = () => {
        history.push('/catalog'); // Asegúrate de usar la ruta correcta para el catálogo
    };

    const handleAddToCart = async () => {
        const quantity = 1;
        try {
            await addCartItem(productData.id, quantity, selectedSize);
            console.log('Producto añadido al carrito con tamaño: ', selectedSize);
        } catch (error) {
            console.error('Error al añadir producto al carrito', error);
        }
    };

    const handleSizeChange = (size) => {
        setSelectedSize(size);
    };

    const renderSizeButtons = (sizes) => {
        return sizes.map(size => (
            <Button
                key={size.id}
                variant={selectedSize === size.size ? "contained" : "outlined"}
                onClick={() => handleSizeChange(size.size)}
                sx={{
                    m: 1,
                    color: selectedSize === size.size ? 'white' : 'green',
                    borderColor: 'green',
                    backgroundColor: selectedSize === size.size ? 'green' : 'white',
                    '&:hover': {
                        backgroundColor: selectedSize === size.size ? 'darkgreen' : '#f4f4f4',
                    }
                }}
            >
                {size.size}
            </Button>
        ));
    };

    const renderAdditionalAttributes = (productData) => {
        const commonAttributes = ['id_product', 'id_seller', 'spec_sheet', 'stock', 'id', 'images', 'seller_products', 'justification', 'age_restricted', 'sizes', 'state'];
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
                        <IconButton onClick={handleBackToCatalog} sx={{ position: 'absolute', left: '10px', top: '10px' }}>
                            <ArrowBackIcon />
                        </IconButton>
                        <FavoriteButton productId={productData.id} />
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={5} sx={{ display: 'flex', justifyContent: 'center' }}>
                                <Box sx={{
                                    width: 600,
                                    height: 600,
                                    display: 'flex',
                                    justifyContent: 'center',
                                    alignItems: 'center',
                                    overflow: 'hidden',
                                    borderRadius: '40px',
                                }}>
                                    <ButtonBase onClick={() => handleImageChange((imageIndex + 1) % productData.images.length)} disabled={productData.images.length <= 1}>
                                        <img
                                            src={productData.images[imageIndex]}
                                            alt={`Image ${imageIndex + 1} of ${productData.name}`}
                                            style={{
                                                height: '100%',
                                                width: '100%',
                                                objectFit: 'cover',  // Cubre el contenedor sin distorsionar
                                                objectPosition: 'center center',  // Centra la imagen en el contenedor
                                                borderRadius: '40px',  // borderRadius a la imagen
                                                boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.7)'  // Sombra a la imagen
                                            }}
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
                                <Box sx={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap' }}>
                                    {productData.sizes && renderSizeButtons(productData.sizes)}
                                </Box>
                                <Button
                                    variant="contained"
                                    color="primary"
                                    sx={{ mt: 2, display: 'block', marginLeft: 'auto', marginRight: 'auto', borderRadius: '40px', background: 'darkgreen' }}
                                    onClick={handleAddToCart}
                                >
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
