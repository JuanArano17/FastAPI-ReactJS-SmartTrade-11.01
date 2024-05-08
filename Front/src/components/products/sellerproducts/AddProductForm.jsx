import React, { useState, useEffect } from 'react';
import { TextField, Button, Container, Paper, Typography, FormControl, InputLabel, Select, MenuItem, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import Autocomplete from '@mui/material/Autocomplete';
import { getAllProductsForAutocomplete, createSellerProduct } from '../../../api/services/products/ProductsService';
import { getLoggedInfo } from '../../../api/services/user/profile/ProfileService';

const categoryAttributes = {
  Book: [{ name: 'author', label: 'Author', type: 'text' }, { name: 'pages', label: 'Pages', type: 'number' }],
  Clothes: [{ name: 'materials', label: 'Materials', type: 'text' }, { name: 'type', label: 'Type', type: 'text' }],
  Electrodomestics: [{ name: 'brand', label: 'Brand', type: 'text' }, { name: 'powerSource', label: 'Power Source', type: 'text' }],
  Electronics: [{ name: 'capacity', label: 'Capacity', type: 'text' }],
  Food: [{ name: 'ingredients', label: 'Ingredients', type: 'text' }],
  Game: [{ name: 'publisher', label: 'Publisher', type: 'text' }, { name: 'platform', label: 'Platform', type: 'text' }, { name: 'size', label: 'Size', type: 'text' }],
  HouseUtilities: [{ name: 'brand', label: 'Brand', type: 'text' }]
};

function AddProductForm() {
  const [isNewProduct, setIsNewProduct] = useState(true);
  const [product, setProduct] = useState({
    productId: '',
    quantity: 0,
    price: 0,
    shippingCosts: 0,
    category: '',
    name: '',
    description: '',
    specSheet: '',
    images: '',
    stock: '',
    attributes: {}
  });
  const [products, setProducts] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  useEffect(() => {
    const fetchProducts = async () => {
      const fetchedProducts = await getAllProductsForAutocomplete();
      setProducts(fetchedProducts);
    };
    fetchProducts();
  }, []);

  const handleSwitch = (event) => {
    setIsNewProduct(event.target.value === 'new');
    setProduct({ ...product, category: '', attributes: {} }); // Reset category and attributes on switch
  };
  const handleCloseDialog = () => {
    setDialogOpen(false);
  };


  const handleChange = (event) => {
    const { name, value } = event.target;
    setProduct({
      ...product,
      [name]: name === 'quantity' || name === 'price' || name === 'shippingCosts' ? parseInt(value, 10) : value
    });
  };

  const handleAutocompleteChange = (event, newValue) => {
    if (newValue) {
      const selectedProductData = {
        productId: newValue.id,
        name: newValue.name,
        price: parseInt(newValue.price, 10),
        quantity: parseInt(newValue.quantity || 0, 10),
        shippingCosts: parseInt(newValue.shippingCosts || 0, 10)
      };
      setProduct({
        ...product,
        ...selectedProductData
      });
    } else {
      setProduct({
        ...product,
        productId: '',
        name: '',
        price: 0,
        quantity: 0,
        shippingCosts: 0
      });
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const sellerData = await getLoggedInfo();
      const response = await createSellerProduct(product, sellerData.id);
      console.log('Producto creado:', response);
    } catch (error) {
      if (error.response && error.response.status === 409) {
        setDialogOpen(true);
      } else {
        console.error('Error al crear el producto:', error);
      }
    }
  };
  return (
    <Container component="main" maxWidth="sm">
      <Paper elevation={6} style={{ padding: '20px', marginTop: '20px' }}>
        <Typography component="h1" variant="h5">
          {isNewProduct ? 'Add New Product' : 'Add Existing Product'}
        </Typography>
        <FormControl fullWidth margin="normal">
          <InputLabel>Type</InputLabel>
          <Select
            name="type"
            value={isNewProduct ? 'new' : 'existing'}
            label="Type"
            onChange={handleSwitch}
          >
            <MenuItem value="new">New Product</MenuItem>
            <MenuItem value="existing">Existing Product</MenuItem>
          </Select>
        </FormControl>
        {!isNewProduct ? (
          <>
            <Autocomplete
              options={products}
              getOptionLabel={(option) => option.name}
              style={{ width: '100%' }}
              onChange={handleAutocompleteChange}
              renderInput={(params) => <TextField {...params} label="Search Product" variant="outlined" />}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Quantity"
              name="quantity"
              value={product.quantity}
              onChange={handleChange}
              type="number"
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Price"
              name="price"
              value={product.price}
              onChange={handleChange}
              type="number"
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Shipping Costs"
              name="shippingCosts"
              value={product.shippingCosts}
              onChange={handleChange}
              type="number"
            />
          </>
        ) : (
          <>
            <FormControl fullWidth margin="normal">
              <InputLabel>Category</InputLabel>
              <Select
                name="category"
                value={product.category}
                label="Category"
                onChange={handleChange}
              >
                {Object.keys(categoryAttributes).map(category => (
                  <MenuItem key={category} value={category}>{category}</MenuItem>
                ))}
              </Select>
            </FormControl>
            {product.category && categoryAttributes[product.category].map(attr => (
              <TextField
                key={attr.name}
                margin="normal"
                required
                fullWidth
                label={attr.label}
                name={attr.name}
                value={product.attributes[attr.name] || ''}
                onChange={handleChange}
                type={attr.type}
              />
            ))}
            <TextField
              margin="normal"
              required
              fullWidth
              label="Product Name"
              name="name"
              value={product.name}
              onChange={handleChange}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Description"
              name="description"
              value={product.description}
              onChange={handleChange}
              multiline
              rows={4}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Price"
              name="price"
              value={product.price}
              onChange={handleChange}
              type="number"
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Spec Sheet"
              name="specSheet"
              value={product.specSheet}
              onChange={handleChange}
              type="text"
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Images URL"
              name="images"
              value={product.images}
              onChange={handleChange}
              type="text"
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Stock"
              name="stock"
              value={product.stock}
              onChange={handleChange}
              type="number"
            />
          </>
        )}
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          style={{ margin: '24px 0px 8px' }}
        >
          Submit
        </Button>
        <Dialog
          open={dialogOpen}
          onClose={handleCloseDialog}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">{"Error de Duplicación"}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              Este producto ya está en su lista de productos. Por favor, verifique o agregue un producto diferente.
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog} color="primary" autoFocus>
              Cerrar
            </Button>
          </DialogActions>
        </Dialog>
      </Paper>
    </Container>
  );
}

export default AddProductForm;
