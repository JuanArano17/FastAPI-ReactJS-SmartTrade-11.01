import React, { useState, useEffect } from 'react';
import { Box, Container, Grid, Paper, Typography, Slider, Select, MenuItem, FormControl, InputLabel, Button, IconButton, Rating, Pagination } from '@mui/material';
import { useHistory } from 'react-router-dom'; 
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import SummarizedProduct from '../components/products/summarizedProduct/SummarizedProduct';
import styles from '../styles/styles';
import { getAllProducts } from '../api/services/products/ProductsService';

const CatalogPage = () => {
    const history = useHistory();
    const [selectedCategory, setSelectedCategory] = useState('');
    const [priceRange, setPriceRange] = useState([20, 40]);
    const [rating, setRating] = useState(0);
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const productsPerPage = 12;
    const categories = ['Category 1', 'Category 2', 'Category 3'];

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const response = await getAllProducts();
                console.log("PRODUCTOS: ", response);
                setProducts(response);
                setLoading(false);
                setError(null); // resetear errores anteriores
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };
        fetchProducts();
    }, []);
    const totalPages = Math.ceil(products.length / productsPerPage);
    const indexOfLastProduct = currentPage * productsPerPage;
    const indexOfFirstProduct = indexOfLastProduct - productsPerPage;
    const currentProducts = products.slice(indexOfFirstProduct, indexOfLastProduct);
    const handleChangePage = (event, value) => {
        setCurrentPage(value);
    };
    const handleCategoryChange = (event) => {
        setSelectedCategory(event.target.value);
    };

    const handlePriceChange = (event, newValue) => {
        setPriceRange(newValue);
    };

    const clearFilters = () => {
        setSelectedCategory('');
        setPriceRange([20, 40]);
        setRating(0);
    };
    const handleProductClick = (productId) => {
        history.push(`/catalog/product/${productId}`); // Función para manejar el click
    };
    if (loading) return <Typography>Cargando...</Typography>;
    if (error) return <Typography>Error: {error}</Typography>;

    return (
        <Box sx={styles.mainBox}>
            <TopBar showSearchBar={true} showLogoutButton={true} />
            <Container sx={styles.mainContainer}>
                <Box sx={{ padding: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <FormControl variant="outlined" sx={{ m: 1, minWidth: 120 }}>
                        <InputLabel>Categoría</InputLabel>
                        <Select
                            value={selectedCategory}
                            onChange={handleCategoryChange}
                            label="Categoría"
                        >
                            {categories.map((category) => (
                                <MenuItem key={category} value={category}>
                                    {category}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <Typography id="range-slider" gutterBottom>
                        Rango de Precios
                    </Typography>
                    <Slider
                        value={priceRange}
                        onChange={handlePriceChange}
                        valueLabelDisplay="auto"
                        aria-labelledby="range-slider"
                        sx={{ width: 300 }}
                    />
                    <Rating
                        name="simple-controlled"
                        value={rating}
                        onChange={(event, newValue) => {
                            setRating(newValue);
                        }}
                    />
                    <Button
                        variant="outlined"
                        sx={styles.clearFiltersButtonStyle}
                        onClick={clearFilters}
                    >
                        Limpiar Filtros
                    </Button>
                </Box>
                <Paper elevation={3} sx={styles.paperContainer}>
                    <Grid container spacing={3}>
                        {currentProducts && currentProducts.map((product) => (
                            <Grid item xs={12} sm={4} md={4} lg={4} key={product.id}>
                                <Button
                                    onClick={() => handleProductClick(product.id)}
                                    sx={{ width: '100%', height: '100%', padding: 0 }}
                                >
                                    <SummarizedProduct product={product} />
                                </Button>
                            </Grid>
                        ))}
                    </Grid>
                </Paper>
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
                    <Pagination count={totalPages} page={currentPage} onChange={handleChangePage} />
                </Box>
            </Container>
            <Footer />
        </Box>
    );
};
export default CatalogPage;