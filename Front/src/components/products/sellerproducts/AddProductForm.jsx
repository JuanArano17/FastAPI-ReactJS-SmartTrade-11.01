import React, { useState } from 'react';
import { Box, TextField, Button, Typography } from '@mui/material';
import { createSellerProduct } from '../../../api/services/products/ProductsService'; // Asegúrate de tener esta función definida y exportada correctamente

const AddProductForm = ({ onSave }) => {
  const [product, setProduct] = useState({
    name: '',
    description: '',
    specSheet: '',
    quantity: '',
    price: '',
    author: '',
    pages: '',
    image: null,
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
      await createSellerProduct(formData); // Assumiendo que esta función maneja la creación del producto
      onSave();
    } catch (error) {
      console.error('Error creating product:', error);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
      <Typography variant="h6">Add New Product</Typography>
      <TextField fullWidth label="Name" name="name" value={product.name} onChange={handleChange} margin="normal" />
      <TextField fullWidth label="Description" name="description" value={product.description} onChange={handleChange} margin="normal" />
      <TextField fullWidth label="Spec Sheet" name="specSheet" value={product.specSheet} onChange={handleChange} margin="normal" />
      <TextField fullWidth type="number" label="Quantity" name="quantity" value={product.quantity} onChange={handleChange} margin="normal" />
      <TextField fullWidth label="Price" name="price" value={product.price} onChange={handleChange} margin="normal" />
      <TextField fullWidth label="Author" name="author" value={product.author} onChange={handleChange} margin="normal" />
      <TextField fullWidth label="Pages" name="pages" value={product.pages} onChange={handleChange} margin="normal" />
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
