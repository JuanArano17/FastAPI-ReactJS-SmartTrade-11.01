import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Select, MenuItem, InputLabel, FormControl } from '@mui/material';
import { createSellerProduct } from '../../../api/services/products/ProductsService';
import {getProfileInfo }from '../../../api/services/user/profile/ProfileService';
const AddProductForm = ({ onSave }) => {
  const [product, setProduct] = useState({
    type: '',
    name: '',
    description: '',
    specSheet: '',
    quantity: '',
    price: '',
    image: null,
    // Additional fields for various product types
    author: '',
    pages: '',
    materials: '',
    brand: '',
    powerSource: '',
    capacity: '',
    ingredients: '',
    publisher: '',
    platform: '',
    size: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProduct({ ...product, [name]: value });
  };

  const handleImageChange = (e) => {
    setProduct({ ...product, image: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    Object.keys(product).forEach(key => {
      if (key !== 'image' || product[key] !== null) {
        formData.append(key, product[key]);
      }
    });
    try {
      console.log(formData.data);
      const userInfo = await getProfileInfo();
      console.log("info",userInfo.id);
      await createSellerProduct(formData,userInfo.id);
      onSave();
    } catch (error) {
      console.error('Error creating product:', error);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
      <Typography variant="h6">Add New Product</Typography>
      <FormControl fullWidth margin="normal">
        <InputLabel>Type</InputLabel>
        <Select
          label="Type"
          name="type"
          value={product.type}
          onChange={handleChange}
        >
          <MenuItem value="Book">Book</MenuItem>
          <MenuItem value="Clothes">Clothes</MenuItem>
          <MenuItem value="Electrodomestics">Electrodomestics</MenuItem>
          <MenuItem value="Electronics">Electronics</MenuItem>
          <MenuItem value="Food">Food</MenuItem>
          <MenuItem value="Game">Game</MenuItem>
          <MenuItem value="HouseUtilities">House Utilities</MenuItem>
        </Select>
      </FormControl>
      
      {/* Common fields */}
      <TextField fullWidth label="Name" name="name" value={product.name} onChange={handleChange} margin="normal" />
      <TextField fullWidth label="Description" name="description" value={product.description} onChange={handleChange} margin="normal" />
      <TextField fullWidth label="Spec Sheet" name="specSheet" value={product.specSheet} onChange={handleChange} margin="normal" />
      <TextField fullWidth type="number" label="Quantity" name="quantity" value={product.quantity} onChange={handleChange} margin="normal" />
      <TextField fullWidth label="Price" name="price" value={product.price} onChange={handleChange} margin="normal" />
      
      {/* Dynamic fields based on product type */}
      {product.type === 'Book' && (
        <>
          <TextField fullWidth label="Author" name="author" value={product.author} onChange={handleChange} margin="normal" />
          <TextField fullWidth type="number" label="Pages" name="pages" value={product.pages} onChange={handleChange} margin="normal" />
        </>
      )}
      {product.type === 'Clothes' && (
        <>
          <TextField fullWidth label="Materials" name="materials" value={product.materials} onChange={handleChange} margin="normal" />
          <TextField fullWidth label="Type" name="type" value={product.type} onChange={handleChange} margin="normal" />
        </>
      )}
      {product.type === 'Electrodomestics' && (
        <>
          <TextField fullWidth label="Brand" name="brand" value={product.brand} onChange={handleChange} margin="normal" />
          <TextField fullWidth label="Power Source" name="powerSource" value={product.powerSource} onChange={handleChange} margin="normal" />
        </>
      )}
      {product.type === 'Electronics' && (
        <>
          <TextField fullWidth label="Capacity" name="capacity" value={product.capacity} onChange={handleChange} pattern="^(\d+(\.\d+)?)(\s*[GgMmKk][Bb])?$" margin="normal" />
        </>
      )}
      {product.type === 'Food' && (
        <>
          <TextField fullWidth label="Ingredients" name="ingredients" value={product.ingredients} onChange={handleChange} margin="normal" />
        </>
      )}
      {product.type === 'Game' && (
        <>
          <TextField fullWidth label="Publisher" name="publisher" value={product.publisher} onChange={handleChange} margin="normal" />
          <TextField fullWidth label="Platform" name="platform" value={product.platform} onChange={handleChange} margin="normal" />
          <TextField fullWidth label="Size" name="size" value={product.size} onChange={handleChange} margin="normal" />
        </>
      )}
      {product.type === 'HouseUtilities' && (
        <>
          <TextField fullWidth label="Brand" name="brand" value={product.brand} onChange={handleChange} margin="normal" />
        </>
      )}

      <Button variant="contained" component="label" fullWidth sx={{ mt: 2 }}>
        Upload Image
        <input type="file" hidden onChange={handleImageChange} />
      </Button>
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 2, mb: 2 }}>
        Add Product
      </Button>
    </Box>
  );
};

export default AddProductForm;
