import React, { useState, useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import { Box, Container, Typography, Grid, Button, Paper, Divider, CircularProgress, Rating, IconButton, Snackbar } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import styles from '../styles/styles';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { getProductSellerById, getAllProductsSeller } from '../api/services/products/ProductsService';
import { addCartItem } from '../api/services/products/ShoppingCartService';
import FavoriteButton from '../components/favorite-button/FavoriteButton';
import ImageSelector from '../components/products/ImageSelector/ImageSelector';
import SimilarProduct from '../components/products/similarProduct/SimilarProduct';
import ProductReviews from '../components/reviews/ProductReviews'; 
import Slider from 'react-slick';
import "slick-carousel/slick/slick.css"; 
import "slick-carousel/slick/slick-theme.css";

const ProductDetailPage = () => {
    const { id } = useParams();
    const [snackbar, setSnackbar] = useState({ open: false, message: '', backgroundColor:'' });
    const [productData, setProductData] = useState(null);
    const [similarProducts, setSimilarProducts] = useState([]);
    const [selectedSize, setSelectedSize] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const history = useHistory();

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const response = await getProductSellerById(id);
                if (response) {
                    setProductData(response);
                    if (response.sizes && response.sizes.length > 0) {
                        setSelectedSize(response.sizes[0].size); 
                    }
                    const allProducts = await getAllProductsSeller();
                    const similar = allProducts.filter(product => 
                        product.id !== response.id &&
                        product.category === response.category &&
                        Math.abs(product.price - response.price) <= 25 &&
                        Math.abs(product.ecoPoints - response.eco_points) <= 25
                    );
                    setSimilarProducts(similar);
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
        history.push('/catalog'); 
    };

    const handleAddToCart = async () => {
        try {
            const quantity = 1;
            if (productData.category === 'Clothes') {
                await addCartItem(productData.id, quantity, selectedSize);
            } else {
                await addCartItem(productData.id, quantity);
            }
            setSnackbar({ open: true, message: "Producto añadido al carrito!", backgroundColor: "green" });
        } catch (error) {
            console.error('Error al añadir producto al carrito', error);
            setSnackbar({ open: true, message: "El producto no ha podido ser añadido.", backgroundColor: "red" });
        }
    };

    const handleCloseSnackbar = () => {
        setSnackbar({ open: false, message: '', backgroundColor: '' });
    };

    const handleSizeChange = (sizeId) => {
        setSelectedSize(sizeId);
    };

    const renderSizeButtons = (sizes) => {
        return sizes.map(size => (
            <Button
                key={size.id}
                variant={selectedSize === size.id ? "contained" : "outlined"}
                onClick={() => handleSizeChange(size.id)}
                sx={{
                    m: 1,
                    color: selectedSize === size.id ? 'white' : 'green',
                    borderColor: 'green',
                    backgroundColor: selectedSize === size.id ? 'green' : 'white',
                    '&:hover': {
                        backgroundColor: selectedSize === size.id ? 'darkgreen' : '#f4f4f4',
                    }
                }}
            >
                {size.size}
            </Button>
        ));
    };

    const renderAdditionalAttributes = (productData) => {
        const commonAttributes = ['id_product', 'id_seller', 'spec_sheet', 'stock', 'id', 'images', 'seller_products', 'justification', 'age_restricted', 'sizes', 'state'];
        return (
            <Grid container spacing={2} sx={{ fontSize: '1.1rem', mt: 2 }}>
                {Object.keys(productData)
                    .filter(key => !commonAttributes.includes(key))
                    .map(key => (
                        <React.Fragment key={key}>
                            <Grid item xs={6}>
                                <Typography variant="h5" color="text.secondary" component="span">
                                    {`${key.charAt(0).toUpperCase() + key.slice(1)}:`}
                                </Typography>
                            </Grid>
                            <Grid item xs={6}>
                                <Typography variant="h5" component="span" sx={{ fontWeight: 'bold' }}>
                                    {productData[key]}
                                </Typography>
                            </Grid>
                        </React.Fragment>
                    ))}
            </Grid>
        );
    };

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return <Typography color="error">{error}</Typography>;
    }

    const sliderSettings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 3,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
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
                            <Grid item xs={12} md={5} mt={2}>
                                <ImageSelector images={productData.images} />  {/* Utilizamos el nuevo componente */}
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
                            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                                Product characteristics
                            </Typography>
                            {renderAdditionalAttributes(productData)}
                        </Box>
                        <Divider sx={styles.ThickDivider}></Divider>
                        <Box sx={{ textAlign: 'left' }}>
                            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                                Similar Products
                            </Typography>
                            <Slider {...sliderSettings}>
                                {similarProducts.map((product) => (
                                    <SimilarProduct key={product.id} product={product} />
                                ))}
                            </Slider>
                        </Box>
                        <Divider sx={styles.ThickDivider}></Divider>
                        <ProductReviews productId={id} />  
                    </Paper>
                )}
            </Container>
            <Snackbar
                open={snackbar.open}
                autoHideDuration={6000}
                onClose={handleCloseSnackbar}
                message={snackbar.message}
                ContentProps={{
                    sx: { align: 'auto', backgroundColor: snackbar.backgroundColor }
                }}
                action={
                    <Button color="inherit" size="small" onClick={handleCloseSnackbar}>
                        OK
                    </Button>
                }
            />
            <Footer />
        </Box>
    );
};

export default ProductDetailPage;
