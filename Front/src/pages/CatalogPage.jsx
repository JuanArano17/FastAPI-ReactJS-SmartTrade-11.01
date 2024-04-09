import React, { useState } from 'react';
import { Box, Container, Grid, Paper, Typography, Slider, Select, MenuItem, FormControl, InputLabel, Button, IconButton, Rating } from '@mui/material';
import TopBar from '../components/TopBar/TopBar';
import Footer from '../components/Footer/Footer';
import ProductDetail from '../components/products/ProductDetailPage'; 
import styles from '../styles/styles';

const CatalogPage = () => {
    const [selectedCategory, setSelectedCategory] = useState('');
    const [priceRange, setPriceRange] = useState([20, 40]);
    const [rating, setRating] = useState(0);

    // Asumiremos que estos datos vendrán de un estado o una API
    const categories = ['Category 1', 'Category 2', 'Category 3'];
    const products = [/* array de productos aquí */];

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


    return (
        <Box sx={styles.mainBox}>
            <TopBar showSearchBar={true} showLogoutButton={true} />
            <Container sx={styles.mainContainer}>
                {/* Filtros de búsqueda */}
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
                        Precio Mínimo
                    </Typography>
                    <Slider
                        value={priceRange}
                        onChange={handlePriceChange}
                        valueLabelDisplay="auto"
                        aria-labelledby="range-slider"
                        sx={{ width: 300 }}
                    />
                    <Typography id="range-slider" gutterBottom>
                        Precio Máximo
                    </Typography>
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
                        Clear Filters
                    </Button>
                </Box>
                {/* Lista de productos */}
                <Paper elevation={3} sx={styles.paperContainer}>
                    <Grid container spacing={3}>
                        {products.map((product, index) => (
                            <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
                                <ProductDetail product={product} />
                            </Grid>
                        ))}
                    </Grid>
                </Paper>
            </Container>
            <Footer />
        </Box>
    );
};

export default CatalogPage;
