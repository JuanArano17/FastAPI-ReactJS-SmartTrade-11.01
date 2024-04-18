import React from 'react';
import { Box, Typography, IconButton, TextField, Grid, Paper } from '@mui/material';
import RemoveIcon from '@mui/icons-material/Remove';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import styles from "../../../styles/styles";
import imagePlaceholder from "../../../images/img_mundo.png";
import { updateProductQuantity, deleteItemService } from '../../../api/services/user/ShoppingCartService';

const CartItem = ({ item, setCartItems }) => {
    const updateQuantity = async (newQuantity) => {
        if (newQuantity >= 0) { // Asegúrate de que la cantidad no sea negativa
            try {
                // Actualizar la cantidad del producto en el backend
                const updatedItem = await updateProductQuantity(item.id_seller_product, newQuantity);
                
                // Actualizar el estado local del carrito
                setCartItems((prevItems) => prevItems.map((cartItem) =>
                    cartItem.id_seller_product === item.id_seller_product
                        ? { ...cartItem, quantity: newQuantity } // Asegúrate de que actualizas el campo correcto
                        : cartItem
                ));
            } catch (error) {
                console.error('Error al actualizar la cantidad del producto:', error);
            }
        }
    };

    const removeItem = async () => {
        try {
            await deleteItemService(item.id_seller_product);
            setCartItems((prevItems) => prevItems.filter((cartItem) => cartItem.id_seller_product !== item.id_seller_product));
        } catch (error) {
            console.error('Error al eliminar el item:', error);
        }
    };

    return (
        <Grid item xs={12} sx={styles.cartItem}>
            <Paper elevation={3} sx={{ ...styles.cartItemPaper, position: 'relative' }}>
                <IconButton onClick={removeItem} sx={{ ...styles.deleteButton, position: 'absolute', top: 8, right: 8 }}>
                    <DeleteIcon />
                </IconButton>
                <Box sx={{ display: 'flex', alignItems: 'center', padding: 2 }}>
                    <img src={item.imageUrl || imagePlaceholder} alt={item.name} style={styles.imageStyle} />
                    <Box sx={{ flex: '1 1 auto', padding: '0 16px' }}>
                        <Typography variant="subtitle1" noWrap>{item.name}</Typography>
                        <Typography variant="body2" color="textSecondary" noWrap>{item.description || "Seller info"}</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <IconButton onClick={() => updateQuantity(item.quantity - 1)} disabled={item.quantity <= 1}>
                            <RemoveIcon />
                        </IconButton>
                        <TextField
                            value={item.quantity}
                            onChange={(e) => updateQuantity(parseInt(e.target.value, 10))}
                            type="number"
                            inputProps={{ min: 1 }}
                            sx={{ width: '4em', mx: 1 }}
                        />
                        <IconButton onClick={() => updateQuantity(item.quantity + 1)}>
                            <AddIcon />
                        </IconButton>
                        <Typography variant="body2" sx={{ ml: 2 }}>Subtotal: {item.price * item.quantity}</Typography>
                    </Box>
                </Box>
            </Paper>
        </Grid>
    );
};

export default CartItem;
