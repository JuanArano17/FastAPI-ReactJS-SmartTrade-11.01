import React from 'react';
import { Box, Typography, IconButton, TextField, Grid, Paper } from '@mui/material';
import RemoveIcon from '@mui/icons-material/Remove';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import styles from "../../../styles/styles";
import imagePlaceholder from "../../../images/img_mundo.png";
import { updateCartItemQuantity, deleteCartItem } from '../../../api/services/products/ShoppingCartService';

const CartItem = ({ item, setCartItems }) => {
    const updateQuantity = async (newQuantity) => {
        if (newQuantity > 0 && newQuantity <= item.stock) {
            try {
                await updateCartItemQuantity(item.id_seller_product, newQuantity);
                setCartItems((prevItems) => prevItems.map((cartItem) =>
                    cartItem.id_seller_product === item.id_seller_product
                        ? { ...cartItem, quantity: newQuantity }
                        : cartItem
                ));
            } catch (error) {
                console.error('Error al actualizar la cantidad del producto:', error);
            }
        }
    };

    const removeItem = async () => {
        try {
            await deleteCartItem(item.id_seller_product);
            setCartItems((prevItems) => prevItems.filter((cartItem) => cartItem.id_seller_product !== item.id_seller_product));
        } catch (error) {
            console.error('Error al eliminar el item:', error);
        }
    };

    return (
        <Grid item xs={12} sx={styles.cartItem}>
            <Paper elevation={3} sx={{ ...styles.cartItemPaper, position: 'relative', display: 'flex' }}>
                <IconButton onClick={removeItem} sx={{ ...styles.deleteButton, position: 'absolute', top: 8, right: 8 }}>
                    <DeleteIcon />
                </IconButton>
                <Box sx={{ minWidth: '160px', maxWidth: '160px', minHeight: '160px', maxHeight: '160px', overflow: 'hidden', marginRight: '16px' }}>
                    <img src={item.image || imagePlaceholder} alt={item.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </Box>
                <Box sx={{ display: 'flex', flexDirection: 'column', flex: '1 1 auto', justifyContent: 'space-between', textAlign: 'left' }}>
                    <Typography variant="subtitle1" noWrap>{item.name}</Typography>
                    <Typography variant="body2" color="textSecondary" noWrap>{item.description}</Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', marginTop: 'auto' }}>
                        <IconButton onClick={() => updateQuantity(item.quantity - 1)} disabled={item.quantity <= 1}>
                            <RemoveIcon />
                        </IconButton>
                        <TextField
                            value={item.quantity}
                            onChange={(e) => updateQuantity(parseInt(e.target.value, 10))}
                            type="number"
                            inputProps={{ min: 1, max: item.stock }}
                            sx={{ mx: 1 }}
                        />
                        <IconButton onClick={() => updateQuantity(item.quantity + 1)} disabled={item.quantity >= item.stock}>
                            <AddIcon />
                        </IconButton>
                        <Typography variant="body2" sx={{ ml: 2 }}>Subtotal: ${(item.price * item.quantity).toFixed(2)}</Typography>
                    </Box>
                </Box>
            </Paper>
        </Grid>
    );
};

export default CartItem;