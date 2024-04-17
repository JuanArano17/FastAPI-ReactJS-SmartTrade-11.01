// FilterProducts.jsx
import React, { useState, useEffect } from 'react';
import { Box, Typography, Slider, Select, MenuItem, FormControl, InputLabel, Button, Rating, Grid } from '@mui/material';

const FilterProducts = ({ products, setSearchFilteredProducts, searchTerm }) => {
    const [selectedCategory, setSelectedCategory] = useState('');
    const [priceRange, setPriceRange] = useState([20, 40]);
    const [rating, setRating] = useState(0);
    const categories = ['Category 1', 'Category 2', 'Category 3'];

    useEffect(() => {
        const result = products.filter(product =>
            (searchTerm === "" || product.name.toLowerCase().includes(searchTerm.toLowerCase()) || product.description.toLowerCase().includes(searchTerm.toLowerCase())) &&
            (selectedCategory ? product.category === selectedCategory : true) /*&&
            product.price >= priceRange[0] && product.price <= priceRange[1] &&
            product.rating >= rating*/
        );
        setSearchFilteredProducts(result);
    }, [selectedCategory, priceRange, rating, products, searchTerm, setSearchFilteredProducts]);

    const clearFilters = () => {
        setSelectedCategory('');
        setPriceRange([20, 40]);
        setRating(0);
    };

    return (
        <Grid container spacing={2} alignItems="center" justifyContent="center">
            <Grid item md={2}>
                <FormControl variant="outlined" fullWidth>
                    <InputLabel htmlFor="category-select">Categoría</InputLabel>
                    <Select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        label="Categoría"
                        inputProps={{ id: 'category-select' }}
                        sx={{ width: 'auto' }}  // Asegúrate de que el ancho sea suficiente para mostrar el texto completo
                    >
                        {categories.map((category, index) => (
                            <MenuItem key={index} value={category}>{category}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Grid>
            <Grid item md={6}>
                <Typography gutterBottom>Rango de Precios</Typography>
                <Slider
                    value={priceRange}
                    onChange={(e, newValue) => setPriceRange(newValue)}
                    valueLabelDisplay="auto"
                    aria-labelledby="range-slider"
                    min={0}
                    max={100}
                />
            </Grid>
            <Grid item>
                <Rating
                    name="simple-controlled"
                    value={rating}
                    onChange={(e, newValue) => setRating(newValue)}
                />
            </Grid>
            <Grid item>
                <Button variant="outlined" onClick={clearFilters}>Limpiar Filtros</Button>
            </Grid>
        </Grid>
    );
};

export default FilterProducts;