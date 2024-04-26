import React, { useState, useEffect } from 'react';
import { Typography, Slider, Select, MenuItem, FormControl, InputLabel, Button, Grid } from '@mui/material';

const FilterProducts = ({ products, setSearchFilteredProducts, searchTerm }) => {
    const [selectedCategory, setSelectedCategory] = useState('');
    const [priceRange, setPriceRange] = useState([0, 10000000]);

    const [categories, setCategories] = useState([]);
    const [maxPrice, setMaxPrice] = useState(0);

    useEffect(() => {
        if (products) {
            const uniqueCategories = Array.from(new Set(products.map(product => product.category)));
            setCategories(uniqueCategories);
            const highestPrice = Math.max(...products.map(product => product.price));
            setMaxPrice(highestPrice);
            setPriceRange([0, highestPrice]);
        }
    }, [products]);

    useEffect(() => {
        const result = products.filter(product => {
            const matchesSearchTerm = searchTerm === "" || product.name.toLowerCase().includes(searchTerm.toLowerCase()) || product.description.toLowerCase().includes(searchTerm.toLowerCase());
            const matchesCategory = selectedCategory === "" || product.category === selectedCategory;
            const matchesPrice = product.price >= priceRange[0] && product.price <= priceRange[1];
            return matchesSearchTerm && matchesCategory && matchesPrice;
        });
        setSearchFilteredProducts(result);
    }, [selectedCategory, priceRange, products, searchTerm]);

    const handlePriceChange = (event, newValue) => {
        setPriceRange(newValue);
    };

    const clearFilters = () => {
        setSelectedCategory('');
        setPriceRange([0, maxPrice]);
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
                    >
                        <MenuItem value="">Todas</MenuItem>
                        {categories.map((category) => (
                            <MenuItem key={category} value={category}>{category}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Grid>
            <Grid item md={6}>
                <Typography gutterBottom>Rango de Precios</Typography>
                <Slider
                    value={priceRange}
                    onChange={handlePriceChange}
                    valueLabelDisplay="auto"
                    aria-labelledby="range-slider"
                    min={0}
                    max={maxPrice}
                />
            </Grid>
            <Grid item>
                <Button variant="outlined" onClick={clearFilters}>Limpiar Filtros</Button>
            </Grid>
        </Grid>
    );
};

export default FilterProducts;