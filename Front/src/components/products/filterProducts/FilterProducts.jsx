import React, { useState, useEffect } from 'react';
import { Typography, Slider, Select, MenuItem, FormControl, InputLabel, Button, Grid } from '@mui/material';
import { myInfoService } from '../../../api/services/user/AuthService';

const FilterProducts = ({ products, setSearchFilteredProducts, searchTerm }) => {
    const [selectedCategory, setSelectedCategory] = useState('');
    const [priceRange, setPriceRange] = useState([0, 10000000]);
    const [userAge, setUserAge] = useState(null);
    const [categories, setCategories] = useState([]);
    const [maxPrice, setMaxPrice] = useState(0);

    const fetchUserInfo = async () => {
        try {
            const userInfo = await myInfoService();
            const birthDate = new Date(userInfo.birth_date);
            const age = calculateAge(birthDate);
            setUserAge(age);
        } catch (error) {
            console.error('Error al obtener la información del usuario:', error);
        }
    };

    useEffect(() => {
        if (products) {
            fetchUserInfo();
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
            const isAgeAppropriate = userAge >= 18 || !product.age_restricted;
            return matchesSearchTerm && matchesCategory && matchesPrice && isAgeAppropriate;
        });
        setSearchFilteredProducts(result);
    }, [selectedCategory, priceRange, products, searchTerm, userAge]);

    const calculateAge = (birthDate) => {
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const m = today.getMonth() - birthDate.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        return age;
    };

    const handlePriceChange = (event, newValue) => {
        setPriceRange(newValue);
    };

    const clearFilters = () => {
        setSelectedCategory('');
        setPriceRange([0, maxPrice]);
    };

    return (
        <Grid container spacing={2} alignItems="center" justifyContent="center">
            <Grid item xs={3}>
            <FormControl variant="outlined" fullWidth sx={{
                    mb: 2, height: '56px', // Set the height of the FormControl to match the button
                    '.MuiOutlinedInput-root': {
                        borderRadius: '15px', bgcolor: '#81cc5c', color: '#fff', '&:hover': { bgcolor: '#629c44' },
                        '.MuiOutlinedInput-notchedOutline': { borderColor: 'transparent' },
                        fontFamily: '"Arial Rounded MT Bold", "Helvetica Rounded", Arial, sans-serif' // Font family
                    }
                }}>
                    <InputLabel htmlFor="category-select" sx={{
                        color: '#fff',
                        fontFamily: '"Arial Rounded MT Bold", "Helvetica Rounded", Arial, sans-serif', // Font family
                        textTransform: 'capitalize' // First letter capitalized
                    }}>Category</InputLabel>
                    <Select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        label="Category"
                        inputProps={{ id: 'category-select' }}
                        sx={{
                            bgcolor: '#81cc5c', color: '#fff', '&:hover': { bgcolor: '#629c44' },
                            '.MuiOutlinedInput-notchedOutline': { borderColor: 'transparent' },
                            fontFamily: '"Arial Rounded MT Bold", "Helvetica Rounded", Arial, sans-serif' // Font family
                        }}
                    >
                        <MenuItem value="">All</MenuItem>
                        {categories.map((category) => (
                            <MenuItem key={category} value={category} sx={{ textTransform: 'capitalize' }}>{category}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Grid>
            <Grid item xs={6}>
                <Typography gutterBottom sx={{
                    fontFamily: '"Arial Rounded MT Bold", "Helvetica Rounded", Arial, sans-serif', // Font family
                    textTransform: 'capitalize' // First letter capitalized
                }}>Price Range</Typography>
                <Slider
                    value={priceRange}
                    onChange={handlePriceChange}
                    valueLabelDisplay="on"
                    aria-labelledby="range-slider"
                    min={0}
                    max={maxPrice}
                    sx={{
                        color: '#629c44', // Changes the color of the track
                        '& .MuiSlider-thumb': {
                            bgcolor: 'white', // Changes thumb color to white for better contrast
                            '&:hover': {
                                bgcolor: '#81cc5c', // Color when thumb is hovered
                            },
                            fontFamily: '"Arial Rounded MT Bold", "Helvetica Rounded", Arial, sans-serif' // Font family
                        },
                        '& .MuiSlider-valueLabel': {
                            bgcolor: 'transparent', // Makes the value label background transparent
                            color: '#629c44', // Color of the text in the value label
                            fontFamily: '"Arial Rounded MT Bold", "Helvetica Rounded", Arial, sans-serif' // Font family
                        }
                    }}
                />
            </Grid>
            <Grid item xs={3}>
                <Button variant="contained" onClick={clearFilters} fullWidth sx={{
                    minWidth: '120px',
                    borderRadius: '15px',
                    backgroundColor: '#81cc5c',
                    color: '#fff',
                    '&:hover': { backgroundColor: '#629c44', borderColor: '#f5f5f5' },
                    fontFamily: '"Arial Rounded MT Bold", "Helvetica Rounded", Arial, sans-serif', // Font family
                    textTransform: 'capitalize', // First letter capitalized
                    height: '56px' // Set the height to match the FormControl
                }}>Clear Filters</Button>
            </Grid>
        </Grid>

    );
};

export default FilterProducts;
