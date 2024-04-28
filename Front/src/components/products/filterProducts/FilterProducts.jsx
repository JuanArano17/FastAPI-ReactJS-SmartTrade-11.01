import React, { useState, useEffect } from 'react';
import { Typography, Slider, Select, MenuItem, FormControl, InputLabel, Button, Grid, Switch, FormControlLabel } from '@mui/material';
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
        console.log(result);
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
            <Grid item md={2}>
                <FormControl variant="outlined" fullWidth>
                    <InputLabel htmlFor="category-select">Category</InputLabel>
                    <Select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        label="Categoría"
                        inputProps={{ id: 'category-select' }}
                    >
                        <MenuItem value="">All</MenuItem>
                        {categories.map((category) => (
                            <MenuItem key={category} value={category}>{category}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Grid>
            <Grid item md={6}>
                <Typography gutterBottom>Price range</Typography>
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
                <Button variant="outlined" onClick={clearFilters}>Clean Filters</Button>
            </Grid>
        </Grid>
    );
};

export default FilterProducts;