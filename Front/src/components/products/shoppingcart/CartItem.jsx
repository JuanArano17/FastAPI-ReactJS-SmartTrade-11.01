import React from 'react';
import { Box, Typography, IconButton, TextField, Grid, Paper } from '@mui/material';
import RemoveIcon from '@mui/icons-material/Remove';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import styles from "../../../styles/styles";
import imagePlaceholder from "../../../images/img_mundo.png";
import { updateCartItemQuantity, deleteCartItem } from '../../../api/services/products/ShoppingCartService';

const CartItem = ({ item, size, setCartItems, quantity }) => {
    const updateQuantity = async (newQuantity) => {
        if (newQuantity > 0 && newQuantity <= item.seller_product.stock) {
            try {
                console.log('itemx asd', item);
                await updateCartItemQuantity(item.id, newQuantity);
                setCartItems();
            } catch (error) {
                console.error('Error al actualizar la cantidad del producto:', error);
            }
        }
    };

    const removeItem = async () => {
        try {
            await deleteCartItem(item.id);
            setCartItems();
        } catch (error) {
            console.error('Error al eliminar el item:', error);
        }
    };

    const imageUrl = item.seller_product.images && item.seller_product.images.length > 0 ? item.seller_product.images[0] : imagePlaceholder;

    return (
        <Grid item xs={12} sx={styles.cartItem}>
            <Paper elevation={3} sx={{ ...styles.cartItemPaper, position: 'relative' }}>
                <IconButton onClick={removeItem} sx={{ position: 'absolute', top: 8, right: 8 }}>
                    <DeleteIcon />
                </IconButton>
                <Box sx={{ minWidth: '160px', maxWidth: '160px', minHeight: '160px', maxHeight: '160px', overflow: 'hidden', marginRight: '16px', borderRadius: '40px' }}>
                    <img src={imageUrl} alt={item.seller_product.name} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '40px' }} />
                </Box>
                <Box sx={{ display: 'flex', flexDirection: 'column', flex: '1 1 auto', justifyContent: 'space-between', textAlign: 'left' }}>
                    <Typography variant="subtitle1" noWrap>{item.seller_product.name}</Typography>
                    <Typography variant="body2" color="textSecondary" noWrap>{item.seller_product.description}</Typography>
                    {item.seller_product.category === 'Clothes' && size && (
                        <Typography variant="body2" sx={{ color: 'textSecondary', mt: 1 }}>
                            Size: {size.size}
                        </Typography>
                    )}
                    <Box sx={{ display: 'flex', alignItems: 'center', marginTop: 'auto' }}>
                        <IconButton onClick={() => updateQuantity(quantity - 1)} disabled={quantity <= 1}>
                            <RemoveIcon />
                        </IconButton>
                        <TextField
                            value={quantity}
                            onChange={(e) => updateQuantity(parseInt(e.target.value, 10))}
                            inputProps={{ min: 1, max: item.seller_product.stock }}
                            sx={{ mx: 1, maxWidth: "55px" }}
                        />
                        <IconButton onClick={() => updateQuantity(quantity + 1)} disabled={quantity >= item.seller_product.stock}>
                            <AddIcon />
                        </IconButton>
                        <Typography variant="body2" sx={{ ml: 2 }}>Subtotal: ${(item.seller_product.price * quantity).toFixed(2)}</Typography>
                    </Box>
                </Box>
            </Paper>
        </Grid>
    );
};

export default CartItem;
