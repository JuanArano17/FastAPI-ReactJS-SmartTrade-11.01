import React, { useState, useEffect } from 'react';
import { Typography, Slider, Select, MenuItem, FormControl, InputLabel, Button, Grid } from '@mui/material';

const FilterProducts = ({ products, setSearchFilteredProducts, searchTerm }) => {
    const [selectedCategory, setSelectedCategory] = useState('');
    const [priceRange, setPriceRange] = useState([0, 10000000]);
    const [ecoPointsRange, setEcoPointsRange] = useState([0, 100]);
    const [categories, setCategories] = useState([]);
    const [maxPrice, setMaxPrice] = useState(0);
    const [maxEcoPoints, setMaxEcoPoints] = useState(100); 

    useEffect(() => {
        if (products) {
            const uniqueCategories = Array.from(new Set(products.map(product => product.category)));
            setCategories(uniqueCategories);
            const highestPrice = Math.max(...products.map(product => product.price));
            const highestEcoPoints = Math.max(...products.map(product => product.ecoPoints)); 
            setMaxPrice(highestPrice);
            setMaxEcoPoints(highestEcoPoints);
            setPriceRange([0, highestPrice]);
            setEcoPointsRange([0, highestEcoPoints]); 
        }
    }, [products]);

    useEffect(() => {
        const result = products.filter(product => {
            const matchesSearchTerm = searchTerm === "" || product.name.toLowerCase().includes(searchTerm.toLowerCase()) || product.description.toLowerCase().includes(searchTerm.toLowerCase());
            const matchesCategory = selectedCategory === "" || product.category === selectedCategory;
            const matchesPrice = product.price >= priceRange[0] && product.price <= priceRange[1];
            const matchesEcoPoints = product.ecoPoints >= ecoPointsRange[0] && product.ecoPoints <= ecoPointsRange[1]; 
            return matchesSearchTerm && matchesCategory && matchesPrice && matchesEcoPoints;
        });
        setSearchFilteredProducts(result);
    }, [selectedCategory, priceRange, ecoPointsRange, products, searchTerm]);

    const handlePriceChange = (event, newValue) => {
        setPriceRange(newValue);
    };

    const handleEcoPointsChange = (event, newValue) => {
        setEcoPointsRange(newValue);
    };

    const clearFilters = () => {
        setSelectedCategory('');
        setPriceRange([0, maxPrice]);
        setEcoPointsRange([0, maxEcoPoints]);
    };

    return (
        <Grid container spacing={2} alignItems="center" justifyContent="center">
            <Grid item md={2}>
                <FormControl fullWidth>
                    <InputLabel>Category</InputLabel>
                    <Select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        label="Category"
                    >
                        <MenuItem value="">All</MenuItem>
                        {categories.map((category) => (
                            <MenuItem key={category} value={category}>{category}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Grid>
            <Grid item md={3}sx={{ margin: '0 10px' }}>
                <Typography gutterBottom>Price Range</Typography>
                <Slider
                    value={priceRange}
                    onChange={handlePriceChange}
                    valueLabelDisplay="auto"
                    max={maxPrice}
                    
                />
            </Grid>
            <Grid item md={3}sx={{ margin: '0 10px' }}>
                <Typography gutterBottom>Eco Points Range</Typography>
                <Slider
                    value={ecoPointsRange}
                    onChange={handleEcoPointsChange}
                    valueLabelDisplay="auto"
                    max={maxEcoPoints}
                />
            </Grid>
            <Grid item md={2}>
                <Button variant="outlined" onClick={clearFilters}>Clear Filters</Button>
            </Grid>
        </Grid>
    );
};

export default FilterProducts;
